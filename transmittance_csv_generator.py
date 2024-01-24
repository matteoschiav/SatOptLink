#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def main(obsalt=0.0, short=200, long=2000, step=20, model=5, target_wl=810):
    """This function generates atmospheric transmission data for a given ground station.

    Parameters:
        obsalt (float, optional): The altitude of the ground station in kilometers. Default is 0.0.
        short (int, optional): The minimum wavelength in nanometers. Default is 200.
        long (int, optional): The maximum wavelength in nanometers. Default is 2000.
        step (int, optional): The step between wavelengths in nanometers. Default is 20.
        model (int, optional): The atmospheric model to use (e.g., 5 for mid-latitude winter). Default is 5.
        target_wl (int, optional): The target wavelength in nanometers if you want to use a single wavelength.
                                  Default is 810.

    Additional Atmospheric Model Parameters:
        - itype (int): Specifies the type of atmosphere, where 3 represents a standard atmosphere.
        - iemsct (int): Specifies the scattering model, where 0 represents no scattering.
        - im (int): Specifies the aerosol model, where 0 represents a rural aerosol model.
        - ihaze (int): Specifies the haze model, where 5 represents a continental model.
        - h1 (float): Altitude of the ground station above sea level in kilometers.
        - angle (array): Array of zenith angles ranging from 30 to 90 degrees with a step of 0.1 degree.

    The function generates atmospheric transmission data based on wavelength, ground station altitude,
    atmospheric model, and zenith angles. It then saves this data to a CSV file named 'transmission_data5.csv'.
    """

    #generating zenith angles from 30 to 90 degrees with a step of 0.1 degree
    zenang = np.arange(30, 90.1, 0.1)

    #defining parameters for the atmospheric model
    context = {
        "wlshort": short,
        "wllong": long,
        "wlstep": step,
        "model": model,
        "itype": 3,
        "iemsct": 0,
        "im": 0,
        "ihaze": 5,
        "h1": obsalt,
        "angle": zenang,
    }

    #calling the lowtran.loopangle function to obtain transmission data
    TR = lowtran.loopangle(context).squeeze()

    #displaying the keys and dimensions of the dataset (optional)
    print(TR.keys())
    print(TR.dims)

    #filtering data for the target wavelength (810 nm)
    target_index = np.abs(TR['wavelength_nm'] - target_wl).argmin()
    transmission_at_target_wl = TR['transmission'][:, target_index]

    #extracting transmission values as a Python list
    transmission_values = transmission_at_target_wl.values.tolist()

    #preparing data for the CSV file with zenith angles and transmission values
    csv_data = [['Zenith Angle (degrees)', 'Transmission at 810 nm']]
    csv_data.extend(zip(zenang, transmission_values))

    #writing the data to the 'transmission_data5.csv' CSV file
    with open('transmission_data5.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print("CSV file 'transmission_data5.csv' created.")

