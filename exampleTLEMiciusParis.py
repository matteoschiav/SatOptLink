import model as ns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

# Creating a datetime list for the orbit propagator
start = pd.Timestamp(datetime.now())
start = pd.Timestamp(datetime(2024, 1, 23, 23))
end = pd.Timestamp(datetime.now()+timedelta(hours= 12))
end = pd.Timestamp(datetime(2024, 1, 24, 1))
t = np.linspace(start.value, end.value, 100000)
datetime_list = pd.to_datetime(t)

# Using TLE from 27/07/2021 QSS-Micius
tle_line_1 = "1 41731U 16051A   21117.42314584  .00000696  00000-0  30260-4 0  9998"
tle_line_2 = "2 41731  97.3499  30.8507 0012844 347.0485 124.2616 15.25507799261429"
tle = (tle_line_1, tle_line_2)

parisparams = [48.8566, 2.3522, 80, "Paris"]

micius = ns.Satellite(tle, simType= "tle")

paris = ns.GroundStation(*parisparams)

# Creating the channel
TESTCHANNEL_paris = ns.SimpleDownlinkChannel(micius, paris)

# Calculating the channel parameters for the datetime list
results_paris = TESTCHANNEL_paris.calculateChannelParameters(datetime_list)

nice = ns.GroundStation(*niceparams)

# Creating the channel
TESTCHANNEL_nice = ns.SimpleDownlinkChannel(micius, nice)

# Calculating the channel parameters for the datetime list
results_nice = TESTCHANNEL_nice.calculateChannelParameters(datetime_list)

#             - length [m]
#             - elevation [degrees]
#             - timeList (datetime)


filtered_timelist_paris = (results_paris[2])[index]
filtered_elevation_paris = (results_paris[1])[index]
filtered_elevation_nice = (results_nice[1])[index]

plt.figure(dpi=600)
plt.title("Elevation as a Function of Time")
plt.ylabel("Elevation (degrees)")
plt.xlabel("Time (GMT+1)")
plt.plot(filtered_timelist, filtered_elevation_paris)
plt.plot(filtered_timelist, filtered_elevation_nice, color="#710193")
plt.grid(color="gray")

elevations_satellite_paris = 90-filtered_elevation_paris
elevations_satellite_nice = 90-filtered_elevation_nice

data_paris_1550 = np.genfromtxt('transmission_data_Paris.csv', delimiter=',', skip_header=1)
data_nice_1550 = np.genfromtxt('transmission_data_Nice.csv', delimiter=',', skip_header=1)


zenith_angles_paris = data_paris_1550[:, 0]
transmittance_values_paris = data_paris_1550[:, 1]

zenith_angles_nice = data_nice_1550[:, 0]
transmittance_values_nice = data_nice_1550[:, 1]

transmittance_paris_interpolated = np.interp(elevations_satellite_paris, zenith_angles_paris, transmittance_values_paris)
transmittance_nice_interpolated = np.interp(elevations_satellite_nice, zenith_nice, transmittance_values, paris)

plt.figure()
plt.title("Transmittance as a Function of Time")
plt.ylabel("Transmittance")
plt.xlabel("Time (GMT+1)")
plt.plot(filtered_timelist, transmittance_paris_interpolated)
plt.plot(filtered_timelist, transmittance_nice_interpolated, color="#710193")
plt.grid(color="gray")
plt.show()