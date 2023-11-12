import os

# set the path to the OUTCAR file
outcar_path = os.path.join(os.getcwd(), 'OUTCAR_files')


# print(outcar_path)
# files = os.listdir(outcar_path)
# print(files)

def get_name(filename):
    """
    Split the given filename into three components.

    Parameters:
    - filename (str): The name of the file to be split.

    Returns:
    Tuple[str, str, str]: A tuple containing three components extracted from the filename.
    """

    components = filename.split('_')
    return components[0], components[1], components[2]


def make_dirs(files):
    """
    Create a separate directory for each OUTCAR file in the OUTCAR_files directory.

    Parameters:
    - files (list): A list of filenames to process.

    Returns:
    None
    """

    for file in files:
        file_type, molecule, site = get_name(file)
        # print(file_type, molecule, site)
        if file_type == 'OUTCAR':
            poscar_dir = os.getcwd() + '/POSCAR_files/' + f'POSCAR_{molecule}_{site}'
            # print(poscar_dir)
            if not os.path.exists(poscar_dir):
                os.makedirs(poscar_dir)
                print(f'Made a directory called POSCAR_{molecule}_{site}')
            else:
                print(f'POSCAR_{molecule}_{site} already exists')
