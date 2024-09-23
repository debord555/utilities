import os, h5py, numpy
from tkinter import filedialog, messagebox

def countDatasets(hdf5_file):
    count = 0
    hdf = h5py.File(hdf5_file)
    for item in list(hdf.keys()):
        if type(hdf[item]) == h5py._hl.group.Group:
            count += countDatasetsInGroup(hdf[item])
        elif type(hdf[item]) == h5py._hl.dataset.Dataset:
            count += 1
    hdf.close()
    return count

def countDatasetsInGroup(group):
    count = 0
    for item in list(group.keys()):
        if type(group[item]) == h5py._hl.group.Group:
            count += countDatasetsInGroup(group[item])
        elif type(group[item]) == h5py._hl.dataset.Dataset:
            count += 1
    return count

def convertHDF5File(file : str, basedir : str):
    global dataset_curr
    global num_datasets
    print(f"[{dataset_curr}/{num_datasets}] Converting HDF5 file {file}")
    hdf = h5py.File(file, "r")
    for item in list(hdf.keys()):
        if type(hdf[item]) == h5py._hl.group.Group:
            group_base_dir = os.path.join(basedir, os.path.basename(hdf[item].name))
            os.mkdir(group_base_dir, 0o774)
            convertHDF5Group(hdf[item], group_base_dir)
        elif type(hdf[item]) == h5py._hl.dataset.Dataset:
            convertHDF5Dataset(hdf[item], basedir)
    hdf.close()

def convertHDF5Group(item, group_base_dir):
    global dataset_curr
    global num_datasets
    print(f"[{dataset_curr}/{num_datasets}] Converting Group {item.name}")
    for sub_item in list(item.keys()):
        if type(item[sub_item]) == h5py._hl.group.Group:
            new_group_base_dir = os.path.join(group_base_dir, os.path.basename(item[sub_item].name))
            os.mkdir(new_group_base_dir, 0o774)
            convertHDF5Group(item[sub_item], new_group_base_dir)
        elif type(item[sub_item]) == h5py._hl.dataset.Dataset:
            convertHDF5Dataset(item[sub_item], group_base_dir)

def convertHDF5Dataset(dataset, basedir):
    global dataset_curr
    global num_datasets
    print(f"[{dataset_curr}/{num_datasets}] Converting Dataset {dataset.name}")
    filename = os.path.join(basedir, os.path.basename(dataset.name)) + ".csv"
    file = open(filename, "w")
    if dataset.shape != ():
        for entry in dataset:
            if type(entry) == numpy.ndarray:
                length = len(entry)
                if length != 0:
                    file.write(str(entry[0]))
                if length > 1:
                    count = 1
                    while count < length:
                        file.write(",")
                        file.write(str(entry[count]))
                        count += 1
            else:
                file.write(str(entry))
            file.write("\n")
    else:
        file.write(str(dataset[()]))
    file.close()
    dataset_curr += 1

print("----------------------------------")
print("| HDF5 to CSV Conversion Utility |")
print("----------------------------------")
print("")
print("")
print("Asking user for .hdf5 file...")
hdf_location = filedialog.askopenfilename(filetypes=(("HDF5 File", "*.hdf5"), ("All Files", "*.*")), title="Select HDF5 file")
if hdf_location == "":
    print("User aborted selection of HDF5 file.")
    input("Press Enter to exit.")
    exit(0)
print(f"HDF5 File selected: {hdf_location}")
print("Asking user for output directory...")
output_location = filedialog.askdirectory(title="Select EMPTY folder to store CSV files in")
while len(os.listdir(output_location)) != 0:
    messagebox.showerror("Error", f"Folder '{output_location}' is not empty!")
    output_location = filedialog.askdirectory(title="Select EMPTY folder to store CSV files in")    
try:
    print(f"Counting datasets in {hdf_location}")
    num_datasets = countDatasets(hdf_location)
    print(f"{num_datasets} datasets found in {hdf_location}")
    dataset_curr = 1
    convertHDF5File(hdf_location, output_location)
    print(f"Successfully converted {num_datasets} datasets in {hdf_location}")
    input("Press ENTER to exit.")
except Exception as e:
    print(f"Exception occured: {e}")
    input("Press ENTER to exit.")
    exit(1)