import model as ns
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

start = pd.Timestamp(datetime.now())
start = pd.Timestamp(datetime(2024, 1, 23, 23))
end = pd.Timestamp(datetime.now()+timedelta(hours= 12))
end = pd.Timestamp(datetime(2024, 1, 24, 1))
t = np.linspace(start.value, end.value, 100000)
datetime_list = pd.to_datetime(t)

tle_line_1 = "1 41731U 16051A   24016.15735159  .00011450  00000-0  34540-3 0  9998"
tle_line_2 = "2 41731  97.3167 289.0989 0012522  59.2544 300.9930 15.34373256413200"
tle = (tle_line_1, tle_line_2)

parisparams = [48.8566, 2.3522, 35, "Paris"]

micius = ns.Satellite(tle, simType= "tle")

paris = ns.GroundStation(*parisparams)

TESTCHANNEL_paris = ns.SimpleDownlinkChannel(micius, paris)

results_paris = TESTCHANNEL_paris.calculateChannelParameters(datetime_list)

#             - length [m]
#             - elevation [degrees]
#             - timeList (datetime)

index = np.where(results_paris[1] > 30)

filtered_timelist = (results_paris[2])[index]
filtered_elevation = (results_paris[1])[index]

plt.figure(dpi=600)
plt.title("Elevation as a Function of Time")
plt.ylabel("Elevation (degrees)")
plt.xlabel("Time (GMT+1)")
plt.plot(filtered_timelist, filtered_elevation, color="#710193")
plt.grid(color="gray")
plt.xticks(rotation=45)

zenith_transmittance = 0.5

filtered_transmittance = zenith_transmittance ** (1/np.sin(np.deg2rad(filtered_elevation)))

plt.figure()
plt.plot(filtered_timelist, filtered_transmittance)
plt.show()