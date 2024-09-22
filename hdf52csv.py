import os, h5py, numpy

def convertHDF5File(file : str, basedir : str):
    print(f"Converting HDF5 file {file}")
    hdf = h5py.File(file, "r")
    for item in list(hdf.keys()):
        if type(hdf[item]) == h5py._hl.group.Group:
            group_base_dir = os.path.join(basedir, os.path.basename(hdf[item].name))
            os.mkdir(group_base_dir, 0o774)
            convertHDF5Group(hdf[item], group_base_dir)
        elif type(hdf[item]) == h5py._hl.dataset.Dataset:
            convertHDF5Dataset(hdf[item], basedir)

def convertHDF5Group(item, group_base_dir):
    print(f"Converting Group {item.name}")
    for sub_item in list(item.keys()):
        if type(item[sub_item]) == h5py._hl.group.Group:
            new_group_base_dir = os.path.join(group_base_dir, os.path.basename(item[sub_item].name))
            os.mkdir(new_group_base_dir, 0o774)
            convertHDF5Group(item[sub_item], new_group_base_dir)
        elif type(item[sub_item]) == h5py._hl.dataset.Dataset:
            convertHDF5Dataset(item[sub_item], group_base_dir)

def convertHDF5Dataset(dataset, basedir):
    print(f"Converting Dataset {dataset.name}")
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

convertHDF5File("/home/debasish/Downloads/MP101.hdf5", "/home/debasish/test")