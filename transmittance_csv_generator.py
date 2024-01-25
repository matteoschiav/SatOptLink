#!/usr/bin/env python
# coding: utf-8


import numpy as np
import csv
import matplotlib.pyplot as plt
import lowtran

def main(obsalt=0.0, target_wl=810, model=5): 
    """
This script interacts with the LOWTRAN atmospheric model to compute and visualize the transmission data for a specific wavelength across a range of zenith angles. The focus is on providing detailed insights into ground-to-space transmission at a single wavelength, particularly useful for applications in atmospheric sciences and satellite communications.

Functions:
    main(obsalt=0.0, target_wl=810, model=5):
        Runs the LOWTRAN model for a specific wavelength (default 810 nm) across a range of zenith angles. It generates a CSV file with the calculated transmission data and plots the transmission versus zenith angles.

        Parameters:
            obsalt (float): The altitude of the observer/ground station in kilometers. Default is 0.0 km.
            target_wl (float): The target wavelength in nanometers for which the transmission data is to be calculated. Default is 810 nm.
            model (int): The LOWTRAN atmospheric model to be used for calculations. Default is model 5 (subarctic winter).

        The function computes the transmission data using LOWTRAN, focusing on the target wavelength over a range of zenith angles from 0 to 60 degrees (with a step of 0.1 degrees). It then writes this data to a CSV file named 'transmission_data.csv'. Additionally, it plots the transmission data against the zenith angles, providing a visual representation of how atmospheric transmission varies with the angle at the specified wavelength.

        The script ensures that the data for the specific wavelength is accurately extracted and correctly aligned with each zenith angle, thus providing precise and reliable results suitable for further analysis in atmospheric transmission studies.

Example Usage:
    To run the script for an observer altitude of 1 km, target wavelength of 810 nm, and using LOWTRAN model 5, simply call:
    
    main(obsalt=1.0, target_wl=810, model=5)

    This will generate the CSV file and display the plot for the specified parameters.
"""

    zenang = np.arange(0, 60.1, 0.1)  #we generate angles from 0 to 60 with a step of 0.1

    #context for specific wavelength (810 nm)
    context = {
        "wlshort": target_wl,
        "wllong": target_wl,
        "wlstep": 20,  # minimum step size
        "model": model,
        "itype": 3,
        "iemsct": 0,
        "im": 0,
        "ihaze": 5,
        "h1": obsalt,
        "angle": zenang,
    }

    TR = lowtran.loopangle(context).squeeze()

    #we extract transmission data for 810 nm at each zenith angle
    transmission_at_target_wl = TR['transmission'].values.flatten()

    #we prepare the data for CSV
    csv_data = [['Zenith Angle (degrees)', 'Transmission at 810 nm']]
    csv_data.extend(zip(zenang, transmission_at_target_wl))

    #we write the data to CSV
    with open('transmission_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print("CSV file 'transmission_data.csv' created.")
    
    print(np.size(zenang))
    print(np.size(transmission_at_target_wl))
    plt.figure()
    plt.plot(zenang, transmission_at_target_wl)
    plt.xlabel('Zenith Angle (degrees)')
    plt.ylabel('Transmission at 810 nm')
    plt.title('Ground to Space Transmission')
    plt.show()

# Test the function
main()
