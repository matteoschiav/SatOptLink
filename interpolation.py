import matplotlib.pyplot as plt
import numpy as np

#charger le fichier CSV
data = np.genfromtxt('transmission_data8.csv', delimiter=',', skip_header=1)

#on extrait les données d'angle et de transmittance
zenith_angles = data[:, 0]
transmittance_values = data[:, 1]

#on définit les élévations du satellite Micius pour la groundstation correspondante (ici Paris) :
elevations_satellite = [10.0, 20.0, 30.0, 40.0, 50.0] #exemple

#on interpole les valeurs de transmittance pour les élévations spécifiques
transmittance_interpolated = np.interp(elevations_satellite, zenith_angles, transmittance_values)

#transmittance_interpolated contient les valeurs interpolées de transmittance pour les élévations données.
plt.figure()
plt.plot(90-zenith_angles, transmittance_values)
plt.show()