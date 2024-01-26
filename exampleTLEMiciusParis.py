import model as ns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from model import timelistgen

# Creating a datetime list for the orbit propagator
start = (2024, 1, 23, 23)
stop = (2024, 1, 24, 1)
datetime_list = timelistgen(start, stop)

# Using TLE from 27/07/2021 QSS-Micius
tle_line_1 = "1 41731U 16051A   21117.42314584  .00000696  00000-0  30260-4 0  9998"
tle_line_2 = "2 41731  97.3499  30.8507 0012844 347.0485 124.2616 15.25507799261429"
tle = (tle_line_1, tle_line_2)

# Location coordinates, altitude and name
parisparams = [48.8566, 2.3522, 80, "Paris"]
niceparams = [43.6274, 7.2991, 1200, "Nice"]

r0=1.5

# Creating an orbitting body from the Satellite class
micius = ns.Satellite(tle, simType= "tle")

# Creating GroundStation objects for each of the locations
paris = ns.GroundStation(*parisparams)
nice = ns.GroundStation(*niceparams)

# Creating the channel between the orbitting body and each ground station
TESTCHANNEL_paris = ns.SimpleDownlinkChannel(micius, paris)
TESTCHANNEL_nice = ns.SimpleDownlinkChannel(micius, nice)

# Calculating the channel parameters for the datetime list
results_paris = TESTCHANNEL_paris.calculateChannelParameters(datetime_list)
results_nice = TESTCHANNEL_nice.calculateChannelParameters(datetime_list)

#  Returns:
#             - length [m]
#             - elevation [degrees]
#             - timeList (datetime)

# Extracting the results
filtered_timelist_paris = (results_paris[2])#[index]
filtered_elevation_paris = (results_paris[1])#[index]
filtered_elevation_nice = (results_nice[1])#[index]

filtered_distance_paris = results_paris[0]
filtered_distance_nice =results_nice[0]

# Plotting the elevation
plt.figure(dpi=600)
plt.title("Elevation as a Function of Time")
plt.ylabel("Elevation (degrees)")
plt.xlabel("Time (GMT+1)")
plt.plot(filtered_timelist_paris, filtered_elevation_paris)
plt.plot(filtered_timelist_paris, filtered_elevation_nice, color="#710193")
plt.grid(color="gray")

# Converting elevation to zenith angles for interpolation with atmospheric data
zenith_to_satellite_paris = 90 - filtered_elevation_paris
zenith_to_satellite_nice = 90 - filtered_elevation_nice

# Reading pregenerated data for each location, see lowtran branch
data_paris_1550 = np.genfromtxt('transmission_data_Paris.csv', delimiter=',', skip_header=1)
data_nice_1550 = np.genfromtxt('transmission_data_Nice.csv', delimiter=',', skip_header=1)

# Extracting data from csv
zenith_angles_paris = data_paris_1550[:, 0]
transmittance_values_paris = data_paris_1550[:, 1]

zenith_angles_nice = data_nice_1550[:, 0]
transmittance_values_nice = data_nice_1550[:, 1]

transmittance_paris_interpolated = np.interp(zenith_to_satellite_paris, zenith_angles_paris, transmittance_values_paris)
transmittance_nice_interpolated = np.interp(zenith_to_satellite_nice, zenith_angles_nice, transmittance_values_nice)

lgt_paris = 10*np.log10(transmittance_paris_interpolated)
lgt_nice = 10*np.log10(transmittance_nice_interpolated)

#paris_index =  np.where(transmittance_paris_interpolated>0.01)
#nice_index =  np.where(transmittance_nice_interpolated>0.01)
paris_index = nice_index = np.where((transmittance_paris_interpolated>0.01) * (
        transmittance_nice_interpolated>0.01))[0]
print( (paris_index))
print(paris_index.dtype)

filtered_timelist_nice = filtered_timelist_paris[nice_index]
filtered_timelist_paris = filtered_timelist_paris[paris_index]

filtered_distance_paris = filtered_distance_paris[paris_index]
filtered_distance_nice = filtered_distance_nice[nice_index]

transmittance_paris_interpolated = transmittance_paris_interpolated[paris_index]
transmittance_nice_interpolated = transmittance_nice_interpolated[nice_index]

lgt_paris = lgt_paris[paris_index]
lgt_nice = lgt_nice[nice_index]
# Plotting transmittance

plt.figure()
plt.title("Atmospheric Transmittance (QSS-Micius) as a Function of Time")
plt.ylabel("Transmittance")
plt.xlabel("Time (GMT+1)")
plt.plot(filtered_timelist_paris, transmittance_paris_interpolated, label = "Paris")
plt.plot(filtered_timelist_nice, transmittance_nice_interpolated, label = "Nice")
plt.grid(color="gray")
plt.legend()

plt.figure()
plt.title("Atmospheric Transmittance (QSS-Micius) as a Function of Time")
plt.ylabel("Transmittance (dB)")
plt.xlabel("Time (GMT+1)")
plt.plot(filtered_timelist_paris, lgt_paris, label = "Paris")
plt.plot(filtered_timelist_nice, lgt_nice, label = "Nice")
plt.grid(color="gray")
plt.legend()

T_total_paris = TESTCHANNEL_paris.end_to_end(0.3,0.8,1550e-9,transmittance_paris_interpolated, filtered_distance_paris,\
    r0)
T_total_nice = TESTCHANNEL_nice.end_to_end(0.3,0.8,1550e-9,transmittance_nice_interpolated, filtered_distance_nice, r0)

Reprate = 1e6
assert T_total_nice.shape == T_total_paris.shape , "check the time lists"
EPRpairsnomem = Reprate * T_total_nice* T_total_paris
EPRpairsQmem = Reprate *np.array([T_total_nice, T_total_paris]).min(0)

plt.figure()
plt.title("Transmittance (QSS-Micius) as a Function of Time")
plt.ylabel("Transmittance")
plt.xlabel("Time (GMT+1)")
plt.plot(filtered_timelist_paris, T_total_paris, label = "Paris")
plt.plot(filtered_timelist_nice, T_total_nice, label = "Nice")
plt.grid(color="gray")
plt.legend()

deltaT=(filtered_timelist_paris[1]-filtered_timelist_paris[0]).total_seconds()
def Totpairs(pairpersec, deltaT):
    return pairpersec.cumsum()*deltaT
plt.figure()
plt.semilogy(filtered_timelist_paris,EPRpairsnomem)
plt.semilogy(filtered_timelist_paris,EPRpairsQmem)

plt.figure()
plt.semilogy(filtered_timelist_paris,Totpairs(EPRpairsnomem, deltaT))
plt.semilogy(filtered_timelist_paris,Totpairs(EPRpairsQmem, deltaT))
plt.grid()
plt.ylim((1,1e7))

plt.show()
