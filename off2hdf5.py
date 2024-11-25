import os
from cProfile import label
import numpy as np
import glob
from tensorflow.python.ops.numpy_ops.np_dtypes import int16
from utils.data_prep_util import save_h5
from numpy.ma.core import count, shape

# P = vertex_arrays[0].shape[0]  # Number of vertices in the first file
P = 409600

def read_off(file_path):
    with open(file_path, 'r') as f:
        header = f.readline().strip()
        if header != 'OFF':
            raise ValueError(f"{file_path} is not a valid OFF file")
        # Read the number of vertices, faces, and edges
        lines = f.readlines()[3:]

        counter_line = lines[0:1]
        vertices_num = int(counter_line[0].split()[0])

        vertices = []
        for line in lines[1:vertices_num]:
            line = line.strip()
            # Ignore comments and empty lines
            if line and not line.startswith('#'):
                vertex = list(map(float, line.split()[:3]))  # Only get x, y, z
                vertices.append(vertex)

    return np.array(vertices)

def off_files_to_numpy_array(root_directory):
    off_files = []
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath,filename)
            off_files.append(file_path)

    #off_files = glob.glob(f"{root_directory}/*.off")
    N = len(off_files)

    vertex_arrays = []
    label_arrays = []

    for file_path in off_files:
        vertices= read_off(file_path)
        vertex_arrays.append(vertices)
        if len(os.path.basename(os.path.dirname(file_path))) <= 7:
            unit_type = os.path.basename(os.path.dirname(file_path))[0]
        else:
            unit_type = os.path.basename(os.path.dirname(file_path))[0:2]
        label_arrays.append(unit_type)

    # Check if all files have the same number of vertices


    # Create a 3D NumPy array
    numpy_array_data = np.zeros((len(off_files), P, 3), dtype=float)
    #numpy_array_label = np.zeros((len(off_files), 1), dtype=uint8)
    numpy_array_label = np.array(label_arrays).astype(int).reshape(-1, 1)
    numpy_array_label -= 1
    for i, vertices in enumerate(vertex_arrays):
        numpy_array_data[i, :vertices.shape[0], :] = vertices  # Fill in the vertices
        #print(vertices)
    return numpy_array_data,numpy_array_label

def create_new_hdf5():
    directory_path = './data/off/training/'  # Replace with your directory path
    numpy_array_data,numpy_array_label  = off_files_to_numpy_array(directory_path)
    save_h5('./data/off/hdf5/hdf5_training.hdf5',numpy_array_data,numpy_array_label)
    print(numpy_array_data.shape)  # Should print (N, P, 3)
    print(numpy_array_label.shape)  # Print the resulting NumPy array
    directory_path = './data/off/testing/'  # Replace with your directory path
    numpy_array_data,numpy_array_label  = off_files_to_numpy_array(directory_path)
    save_h5('./data/off/hdf5/hdf5_testing.hdf5',numpy_array_data,numpy_array_label)
    print(numpy_array_data.shape)  # Should print (N, P, 3)
    print(numpy_array_label.shape)  # Print the resulting NumPy array

def create_new_hdf5_2048():
    directory_path = './data/off/training_2048/'
    numpy_array_data,numpy_array_label  = off_files_to_numpy_array(directory_path)
    save_h5('./data/off/hdf5_2048/hdf5_training.hdf5',numpy_array_data,numpy_array_label)
    print(numpy_array_data.shape)  # Should print (N, P, 3)
    print(numpy_array_label.shape)  # Print the resulting NumPy array
    directory_path = './data/off/testing_2048/'
    numpy_array_data,numpy_array_label  = off_files_to_numpy_array(directory_path)
    save_h5('./data/off/hdf5_2048/hdf5_testing.hdf5',numpy_array_data,numpy_array_label)
    print(numpy_array_data.shape)  # Should print (N, P, 3)
    print(numpy_array_label.shape)  # Print the resulting NumPy array

if __name__ == "__main__":
    create_new_hdf5()
