import os
import numpy as np
import sys
import pandas
import surfio
import curveio
import FSdataio

class Shape(object):

    def __init__(self):
        pass

    datatype = {'.dfs': 'surface',
                '.dfc': 'curve,',
                '.ucf': 'curve',
                '.vtp': 'surface',
                '.vtk': 'surface',
                '.mgh': 'FSdata',
                }

    @staticmethod
    def readfile(filename):
        filenamewoext, ext = os.path.splitext(filename)
        if ext not in Shape.datatype.keys():
            sys.stdout.write('Error: Unsupported data type. Supported data types are: ' + ', '.join(Shape.datatype.keys()))
            return

        if Shape.datatype[ext] == 'curve':
            shapobj = curveio.Curve.readfile(filename)
            return shapobj
        elif Shape.datatype[ext] == 'surface':
            shapobj = surfio.Surface.readfile(filename)
            return shapobj
        elif Shape.datatype[ext] == 'FSdata':
            shapeobj = surfio.Surface(coords=0, faces=0, ismultilevelUCF=False)
            shapeobj.attributes = FSdataio.load_mgh(filename)
            return shapeobj
        else:
            sys.stdout.write('Error: Unsupported data type. Supported data types are: ' + ', '.join(Shape.datatype.keys()))

    @staticmethod
    def writefile(filename, shapeobj):
        filenamewoext, ext = os.path.splitext(filename)
        if ext not in Shape.datatype.keys():
            sys.stdout.write('Error: Unsupported data type. Supported data types are: ' + ', '.join(Shape.datatype.keys()))
            return

        if isinstance(shapeobj, curveio.Curve):
            curveio.writecurve(filename, shapeobj.coords, shapeobj.attributes, shapeobj.isMultilevelUCF)
        elif isinstance(shapeobj, surfio.Surface):
            surfio.writesurface_new(filename, shapeobj.coords, shapeobj.faces, shapeobj.attributes)

    @staticmethod
    def read_aggregated_attributes_from_shapefilelist(shapefilelist):
        s1 = Shape.readfile(shapefilelist[0])
        attributes_new = s1.attributes

        num_files = len(shapefilelist)
        attrib_size = len(attributes_new)

        attribute1_array = np.empty((num_files, attrib_size), 'float')
        attribute1_array[0, :] = attributes_new

        average_coords = s1.coords

        for i in range(1, len(shapefilelist)):
            s1 = Shape.readfile(shapefilelist[i])
            average_coords += s1.coords
            if len(s1.attributes) != attrib_size:
                sys.stdout.write("Length of attributes in Files " + shapefilelist[i] + " and " + shapefilelist[0] + " do not match. Quitting.\n")
                attribute1_array = []
                return attribute1_array
            else:
                attribute1_array[i, :] = s1.attributes

        average_coords /= len(shapefilelist)
        s1_average = s1
        s1_average.coords = average_coords

        return s1, s1_average, attribute1_array

    @staticmethod
    def read_aggregated_attributes_from_surfaces(filename):
        data_list = pandas.read_table(filename, sep='\t')

        try:
            shapefile_list = data_list['File']
        except KeyError:
            fid = open(filename, 'rt')
            shapefile_list = [i.strip('\n') for i in fid.readlines()]

        return Shape.read_aggregated_attributes_from_shapefilelist(shapefile_list)

    @staticmethod
    def determine_file_extension(filename, contains_filelist=False):
        ext = ''

        if contains_filelist:
            data_list = pandas.read_table(filename, sep='\t')
            try:
                shapefile_list = data_list['File']
            except KeyError:
                fid = open(filename, 'rt')
                filename = fid.readline().strip('\n')
                root, ext = os.path.splitext(filename)
        else:
            root, ext = os.path.splitext(filename)
        return ext
