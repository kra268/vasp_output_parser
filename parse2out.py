import os
from utils import get_name, make_dirs

def remove_space(string):
    """
    Remove spaces from a string.

    Parameters
    ----------
    string : str
        The input string.

    Returns
    -------
    str
        The string with spaces removed.
    """
    return "".join(string.split())


def get_number_of_atoms(modified):
    """
    Get the number of atoms from the modified lines.

    Parameters
    ----------
    modified : list of str
        List of modified lines.

    Returns
    -------
    int
        The number of atoms.
    """
    no_of_atoms = 0
    for line_no, line in enumerate(modified):
        if remove_space(line) == 'POSITIONTOTAL-FORCE(eV/Angst)':
            no_of_atoms = 0
            while remove_space(modified[
                                   line_no + 2]) != '-----------------------------------------------------------------------------------':
                no_of_atoms += 1
                line_no += 1
            break
    return no_of_atoms


def read_file_lines(filepath):
    """
    Read lines from a file.

    Parameters
    ----------
    filepath : str
        The path of the file.

    Returns
    -------
    list of str
        List of lines from the file.
    """
    with open(filepath, 'r') as file:
        return file.readlines()


def write_file_lines(filename, lines):
    """
    Write lines to a file.

    Parameters
    ----------
    filename : str
        The name of the file.
    lines : list of str
        List of lines to write to the file.
    """
    with open(filename, 'a+') as file:
        for line in lines:
            file.writelines(line + '\n')


def extract_geometry_from_outcar(outcar_filepath, poscar_filepath, molecule_name, site_name):
    """
    Extract geometry information from an OUTCAR file and write it to a corresponding POSCAR file.

    Parameters
    ----------
    outcar_filepath : str
        The filepath of the OUTCAR file to extract geometry from.
    poscar_filepath : str
        The directory path where the corresponding POSCAR file should be written to.
    molecule_name : str
        The name of the molecule in the file.
    site_name : str
        The name of the site in the molecule.
    """
    modified = []
    with open(os.path.join(outcar_filepath), 'r') as f:
        lines = f.readlines()
        # modify lines to remove the '\n' and store all lines in a list called 'modified'
        for line in lines:
            # print(line)
            modified.append(line.strip())
            #print(modified)

    no_of_atoms = get_number_of_atoms(modified)
    poscar_head = read_file_lines(os.path.join('/', *outcar_filepath.split('/')[:-1], f'POSCAR_{molecule_name}_{site_name}'))

    atom_no = 2
    i = 1
    for line_no in range(len(modified)):
        if remove_space(modified[line_no]) == 'POSITIONTOTAL-FORCE(eV/Angst)':
            with open(os.path.join(poscar_filepath, f'POSCAR_{molecule_name}_{site_name}_{i}'), 'a+') as poscar:
                poscar.writelines(poscar_head[:7])
                poscar.writelines('Cartesian\n')
                while atom_no <= (no_of_atoms + 1):
                    poscar.writelines(modified[line_no + atom_no] + '\n')
                    atom_no += 1
            atom_no = 2
            i += 1


if __name__ == '__main__':
    out_path = os.path.join(os.getcwd(), 'OUTCAR_files')
    pos_path = os.path.join(os.getcwd(), 'POSCAR_files')
    files = os.listdir(out_path)
    make_dirs(files)
    for file in files:
        file_name, molecule, site = get_name(file)
        if file_name == 'OUTCAR':
            outcar_file_path = os.path.join(f'{out_path}/{file_name}_{molecule}_{site}')
            poscar_file_path = os.path.join(f'{pos_path}/POSCAR_{molecule}_{site}')
            #print(outcar_file_path)
            #print(poscar_file_path)
            extract_geometry_from_outcar(outcar_file_path, poscar_file_path, molecule, site)


