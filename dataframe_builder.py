import os
import pandas as pd

def create_struc_df(poscar_dir):
    """
    Create a Pandas DataFrame containing structures from POSCAR files in a directory.

    Parameters
    ----------
    poscar_dir : str
        The path to the directory containing POSCAR files.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with a single column named 'structure' containing the content of each POSCAR file.
    """
    poscar_files = [f for f in os.listdir(poscar_dir) if f.startswith('POSCAR_')]
    struc_df = pd.DataFrame(columns=['structure'])

    for poscar_file in poscar_files:
        with open(os.path.join(poscar_dir, poscar_file), 'r') as f:
            structure = f.read()
        struc_df = struc_df.append({'structure': structure}, ignore_index=True)

    return struc_df

# Example usage
poscar_dir = os.path.join(os.getcwd(), 'POSCAR_files')
struc_df = create_struc_df(poscar_dir)

# Save the DataFrame to a CSV file
csv_filename = "data.csv"
struc_df.to_csv(csv_filename, index=False)
