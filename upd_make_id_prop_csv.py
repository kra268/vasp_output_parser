import os
import pandas as pd
from glob import glob
from utils import get_name

def read_energy_values(file_path):
    """
    Read energy values from an OSZICAR file.

    Parameters
    ----------
    file_path : str
        The path to the OSZICAR file.

    Returns
    -------
    list of str
        A list containing energy values extracted from the OSZICAR file.
    """
    with open(file_path, "r") as f:
        contents = f.read()
        lines = contents.split("\n")
        energies = []
        for line in lines:
            if line.startswith("  "):
                parts = line.split()
                energies.append(parts[4])
        return energies


def clean_energy_values(energies):
    """
    Clean energy values by removing 'eps'.

    Parameters
    ----------
    energies : list of str
        List of energy values.

    Returns
    -------
    list of str
        Cleaned list of energy values.
    """
    return [energy for energy in energies if energy != 'eps']


def extract_number(file_name):
    """
    Extract a number from a file name.

    Parameters
    ----------
    file_name : str
        The file name.

    Returns
    -------
    int
        The extracted number.
    """

    try:
        return int(file_name.split("POSCAR")[-1].split("_")[-1])
    except ValueError:
        print('ValueError: Error in the file name')


def sort_file_names(file_names):
    """
    Sort file names based on the extracted number.

    Parameters
    ----------
    file_names : list of str
        List of file names.

    Returns
    -------
    list of str
        Sorted list of file names.
    """
    return sorted(file_names, key=extract_number)


def generate_target_value_array(pos_path):
    """
    Generate the target value array.

    Parameters
    ----------
    pos_path : str
        The path to the POSCAR files directory.

    Returns
    -------
    list of str
        The target value array.
    """
    target_value_array = []
    for di in glob(f'{pos_path}/*'):
        dir_path = di
        poscar_name = os.path.split(dir_path)[-1]
        target_value_array.append(poscar_name)
    return target_value_array


def create_target_value_dataframe(sorted_filenames, energies):
    """
    Create a target value dataframe.

    Parameters
    ----------
    sorted_filenames : list of str
        Sorted list of filenames.
    energies : list of str
        List of energy values.

    Returns
    -------
    pandas.DataFrame
        The target value dataframe.
    """
    #sorted_file_names = sort_file_names(file_names)
    target_value_dataframe = pd.DataFrame(sorted_filenames, columns=None)
    energy = pd.Series(energies)
    target_value_dataframe['energy'] = energy.values
    return target_value_dataframe


def save_dataframe_to_csv(dataframe, destination_path, csv_name):
    """
    Save the dataframe to a CSV file.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The dataframe to save.
    destination_path : str
        The path to the destination directory.
    csv_name : str
        The name of the CSV file.
    """
    dataframe.to_csv(
        os.path.join(destination_path, csv_name),
        index=False, mode='a', header=False, sep=','
    )


if __name__ == '__main__':
    pos_path = os.path.join('/'.join(os.getcwd().split('/')), 'POSCAR_files')
    osz_path = os.path.join('/'.join(os.getcwd().split('/')), 'OUTCAR_files')
    destination_path = os.getcwd()
    # Get the list of directories in POSCAR_files
    poscar_list = [p for p in glob(f'{pos_path}/*')]
    # Loop through each directory
    for l in poscar_list:
        filenames = generate_target_value_array(l)
        f_name = l.split('/')[-1]
        f, m, s = f_name.split('_')
        sorted_filenames = sort_file_names(filenames)
        # Loop through each file in OUTCAR_files directory
        for file_path in glob(f'{osz_path}/*'):
            file = file_path.split('/')[-1]
            filename, molecule, site = get_name(file)  # Splitting file name. We need only OSZICAR files
            if filename == 'OSZICAR' and molecule == m and site == s:  # Checking if the file is OSZICAR
                energies = read_energy_values(os.path.join(file_path))
                energies = clean_energy_values(energies)
                csv_name = f'{molecule}_{site}_id_prop.csv'
                target_value_dataframe = create_target_value_dataframe(sorted_filenames, energies)
                save_dataframe_to_csv(target_value_dataframe, destination_path, csv_name)

