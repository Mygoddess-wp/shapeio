import numpy as np
from struct import unpack
from os import path


def load_mgh(filename):

    fobj = open(filename, "rb")
    ver = unpack('>i', fobj.read(4))[0]
    dim1 = unpack('>i', fobj.read(4))[0]
    dim2 = unpack('>i', fobj.read(4))[0]
    dim3 = unpack('>i', fobj.read(4))[0]
    frames = unpack('>i', fobj.read(4))[0]
    datatype = unpack('>i', fobj.read(4))[0]

    type_info = {0: (1, 'c'),
                 1: (4, 'i'),
                 3: (4, 'f'),
                 4: (2, 'h'),
                 }
    bytes_per_voxel, fmt_string = type_info[datatype]
    fobj.seek(284)  # Skip the header and jump past the unused bytes. See load_mgh supplied by Freesurfer (c) MGH
    nvoxels = dim1 * dim2 * dim3 * frames
    data = np.array(unpack('>' + fmt_string * nvoxels, fobj.read(nvoxels * bytes_per_voxel)), dtype='float32')
    return data


def readdata(filename):

    path_filename, ext = path.splitext(filename)
    options = {'.mgh': load_mgh}
    if ext in options:
        data = options[ext](filename)
        return data
