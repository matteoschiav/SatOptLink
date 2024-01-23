#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
18/01/2024

@author: schiavon, snailpi

Original description: This script implements the actual moving satellite channel to be used with the
FixedSatelliteLossModel NetSQUID class.

v00     Changes made:
    - removed lowtran dependence
    - removed all calculations other than satellite coordinates

v01     Changes made:
    - added keplerian propagation
"""

import orekit

from orekit.pyhelpers import download_orekit_data_curdir, setup_orekit_curdir, datetime_to_absolutedate

import os

import numpy as np

from math import radians

# setup orekit
vm = orekit.initVM()

if not os.path.isfile('orekit-data.zip'):
    download_orekit_data_curdir()

setup_orekit_curdir()

# Orekit imports
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.propagation.analytical import KeplerianPropagator
from org.orekit.orbits import KeplerianOrbit
from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.utils import IERSConventions, Constants

# Prepare global variables - time and space reference systems
ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                         Constants.WGS84_EARTH_FLATTENING, ITRF)
inertialFrame = FramesFactory.getEME2000()


# utc = TimeScalesFactory.getUTC()


# Define classes for the different objects
class orbitModelError(Exception):
    pass


class Satellite:
    """ Satellite orbit

    This class implements a real satellite orbit.

    The class defines the satellite using different simulation orbit techniques:
        * 'tle': use the two-line elements (TLE) of an existing satellite
        * "kepler": use the Keplerian elements:
            - a
            - e
            - i
            - omega
            - Omega
            - v
        * 'polOrbPass': use the model of polar orbit passage described in
            [Moll et al., PRA 99, 053830 (2019)]

    Paramters
    ---------
    incAngle: float
        Inclination angle of the satellite w.r.t. the ground station [deg].
    satAlt: float
        Altitude of the satellite [km].
    """

    simTypeAllowed = ('tle', 'polOrbPass', "keplerian", '')

    def __init__(self, params, simType='tle', incAngle=0, satAlt=0):
        self.simType = simType

        if simType == 'tle':
            """ Initializpaation of the satellite orbit from a TLE list """
            self.tleList = params
            self.tleObject = TLE(*self.tleList)
            self.propagator = TLEPropagator.selectExtrapolator(self.tleObject)
        elif simType == 'keplerian':
            """ Initialization of the satellite orbit from a Keplerian list """
            self.keplerList = params
            self.keplerObject = KeplerianOrbit(*self.keplerList)
            self.propagator = KeplerianPropagator(self.keplerObject)
        elif simType == 'polOrbPass':
            self.incAngle = radians(incAngle)
            self.satAlt = satAlt * 1e3
        else:
            self.simType = ''

    def setSimTLE(self, tle):
        self.simType = 'tle'
        self.tleList = tle
        self.tleObject = TLE(*self.tleList)
        self.propagator = TLEPropagator.selectExtrapolator(self.tleObject)

    def setSimKeplerian(self, kepler):
        self.simType = 'keplerian'
        self.keplerList = kepler
        self.keplerObject = KeplerianOrbit(*self.keplerList)
        self.propagator = KeplerianPropagator(self.keplerObject)

    def setSimPolOrbPass(self, incAngle, satAlt):
        self.simType = 'polOrbPass'
        self.incAngle = radians(incAngle)
        self.satAlt = satAlt * 1e3

    def isPolOrbPass(self):
        return (self.simType == 'polOrbPass')

    def isTLE(self):
        return (self.simType == "tle")

    def isKeplerian(self):
        return (self.simType == 'keplerian')


class GroundStation:
    """ Ground station

    This class implements a ground station.

    Parameters
    ----------
    latitude: float
        Latitude of the ground station [degrees]. Positive towards North.
    longitude: float
        Longitude of the ground station [degrees]. Positive towards East.
    altitude: float
        Altitude of the ground station [m].
    name: str
        Name of the station
    """

    def __init__(self, lat, long, alt, name):
        self.latitude = radians(lat)
        self.longitude = radians(long)
        self.altitude = float(alt)
        self.name = name

        # define the station Topocentric Frame
        self.geodeticPoint = GeodeticPoint(self.latitude, self.longitude, self.altitude)
        self.frame = TopocentricFrame(earth, self.geodeticPoint, self.name)


class SimpleDownlinkChannel:
    """ Downlink channel

    This class describes a simple downlink channel.

    Parameters
    ----------
    satellite: Satellite
        Instance of the Satellite class.
    groundStation: GroundStation
        Instance of the GroundStation class.
    date_range: Date range
        List containing start and end date for downlink channel
    """

    def __init__(self, sat, gs, timeList):
        self.satellite = sat
        self.groundStation = gs
        self.timeList = timeList

    def calculateChannelParameters(self, timeList):
        """ Calculate channel paramters

        This function calculates the parameters of the channels for the times
        given in timeList.

        Parameters
        ----------
        timeList : li
            List of times at which to calculate satellite parameters.

        Returns
        -------
        tuple (np.array, np.array)
            The elements of the tuple are the parameters of the channel for the
            different times in timeList filte:
            - length [m]
            - elevation [degrees]
        """
        print(f"isTlE: {self.satellite.isTLE()}")
        print(f"isKeplerian: {self.satellite.isKeplerian()}")

        if self.satellite.isPolOrbPass():
            # calculate the orbit parameters using the [Moll et al.] model.
            psi = self.groundStation.latitude

            deltaI = self.satellite.incAngle
            hs = self.satellite.satAlt

            deltaMin = np.arccos(np.cos(psi) * np.cos(deltaI) / np.sqrt(1 - (np.cos(psi) * np.sin(deltaI)) ** 2))
            tMin = timeList[int(len(timeList) / 2)]

            # Earth parameters (from Daniele's code)
            Rt = 6.37e6  # Earth radius
            M = 5.97e24  # Earth mass
            G = 6.67e-11  # Gravitational constant

            Omega = np.sqrt(G * M / (Rt + hs) ** 3)

            relTime = np.array([(timeList[i] - tMin).total_seconds() for i in range(len(timeList))])
            delta = Omega * relTime + deltaMin

            Zc = np.arccos(np.sin(psi) * np.sin(delta) + np.cos(psi) * np.cos(delta) * np.cos(deltaI))
            Z = np.arcsin((Rt + hs) * np.sin(Zc) / np.sqrt(Rt ** 2 + (Rt + hs) ** 2 - 2 * Rt * (Rt + hs) * np.cos(Zc)))
            elevation = 90 - np.rad2deg(Z)

            channelLength = -Rt * np.cos(Z) + np.sqrt((Rt * np.cos(Z)) ** 2 + 2 * Rt * hs + hs ** 2)


        elif self.satellite.isTLE() or self.satellite.isKeplerian():
            channelLength = np.zeros((len(timeList),))
            elevation = np.zeros((len(timeList),))

            # calculate the orbit parameters using the TLE
            absDateList = [datetime_to_absolutedate(i) for i in timeList]

            for i in range(len(absDateList)):
                pv = self.satellite.propagator.getPVCoordinates(absDateList[i], inertialFrame)
                pos_tmp = pv.getPosition()

                frameTrans = inertialFrame.getStaticTransformTo(self.groundStation.frame, absDateList[i])

                channelLength[i] = frameTrans.transformPosition(pos_tmp).getNorm()
                print(channelLength[i])

                elevation[i] = np.rad2deg(
                    self.groundStation.frame.getElevation(pv.getPosition(), inertialFrame, absDateList[i]))

        return (channelLength, elevation, timeList )
