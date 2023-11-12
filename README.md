# VASP OUTCAR parser

## Overview

This project consists of  Python scripts for processing data related to molecular structures and energy values from VASP OUTCAR files. 
OUTCAR files from relaxation calculations contain the structural and energy info for each step. This parser can be used to convert this information to 'semi-structured' data that can be processed further for ML algorithms like graph neural network.
The motivation here is to 'mine' more data from each relaxation calculation.

## Scripts

### 1. Geometry Extractor (`parse2out.py`)
### 2. ID-property CSV generator (`upd_make_id_prop_csv.py`)
### 3. Dataframe builder (`dataframe_builder.py`)

#### Description

The `parse2out.py` script extracts geometry information from an OUTCAR file and writes it to corresponding POSCAR files.

The `upd_make_id_prop_csv.py` script prepares csv files with POSCAR IDs and the energy extracted for each structure.

The `dataframe_builder.py` script makes dataframes if needed. More work is ongoing to add functionalities for this script.

Make sure you have two directories in the current directory namely, OUTCAR_files and POSCAR_files. OUTCAR_files will have the OUTCAR files you want to process. POSCAR_files is where the POSCAR files parsed will be written.
#### Usage

```bash
python parse2out.py
```
```bash
python upd_make_id_prop_csv.py
```

## Directory structure

project_root/
│
├── OUTCAR_files/
│   ├── OUTCAR_molecule1_site1
│   ├── OUTCAR_molecule1_site2
│   └── ...
│
├── POSCAR_files/
│   ├── POSCAR_molecule1_site1_1
│   ├── POSCAR_molecule1_site1_2
│   └── ...
│
├── utils.py
├── geometry_extractor.py
└── energy_reader.py

## Contact

For any questions or feedback, please contact [Keerthan Rao] at [keerthanr1@gmail.com].