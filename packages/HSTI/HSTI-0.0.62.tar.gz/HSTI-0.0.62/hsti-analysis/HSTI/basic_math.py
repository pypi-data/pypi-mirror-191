import numpy as np
from scipy.ndimage import median_filter
from IPython.display import clear_output
import concurrent.futures as cf
import os
import cv2 as cv
import pkg_resources

#Multiple of these functions takes an optional argument defining in which axis
#the function operates. If 's' is passed as an argument, the operation is performed
#along the spectral axis (across bands/variables). If the argument is 'b', the
#function operates on each band/variable individually

#Subtrats the mean from the data, either the mean of each spectrum (axis = 's')
#or the mean of each band (axis = 'b')
def mean_center(data_cube, axis = 's'):
    if axis == 's':
        return data_cube - np.nanmean(data_cube, axis = 2)[:,:,np.newaxis]
    elif axis == 'b':
        return data_cube - np.nanmean(data_cube, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Subtracts mean and scales with STD - the old standardize function. Setting
#axis = 's' is the same as doing SNV (standard normal variate)
def autoscale(data_cube, axis = 's'):
    if axis == 's':
        std_cube = np.std(data_cube, axis = 2)[:,:,np.newaxis]
        std_cube[std_cube < 1e-6] = np.nan
        return (data_cube - np.mean(data_cube, axis = 2)[:,:,np.newaxis])/std_cube
    elif axis == 'b':
        return (data_cube - np.mean(data_cube, axis = (0,1)))/np.std(data_cube, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Uses norm of given order for normalization. If axis = 's', then each spectrum is
#divided by its norm. If axis = 'b', then every band is divided by the norm of
#the entire band.
def norm_normalization(data_cube, order, axis = 's'):
    if axis == 's':
        return data_cube/np.linalg.norm(data_cube, ord = order, axis = 2)[:,:,np.newaxis]
    elif axis == 'b':
        return data_cube/np.linalg.norm(data_cube, ord = order, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Apply multiplicative scatter correction to entire datacube. If no reference
#spectrum is supplied, the mean spectrum of the cube is used instead.
def msc(data_cube, ref_spec = None):
    if ref_spec == None:
        ref_spec = np.nanmean(data_cube, axis = (0,1))
        ref_spec_mean = np.nanmean(ref_spec)
        ref_spec = ref_spec - ref_spec_mean
    else:
        ref_spec_mean = np.nanmean(ref_spec)
        ref_spec - ref_spec_mean
    ref_spec = ref_spec[:,np.newaxis]
    X = mean_center(data_cube, 's')
    X = X.reshape([X.shape[0]*X.shape[1], X.shape[2]])
    X = np.rot90(X, 3)

    b = np.linalg.inv(ref_spec.T@ref_spec)@ref_spec.T@X
    b[b<1e-8] = np.nan
    X_new = X/b + ref_spec_mean
    X_new = np.rot90(X_new)
    X_new = X_new.reshape([data_cube.shape[0], data_cube.shape[1], data_cube.shape[2]])
    return X_new

#Setting axis = 's' is the same as normalizing each spectrum (pixel) to span from 0 to 1
#axis = 'b' normalizes each band individually
def normalize(data_cube, axis = 's'):
    if axis == 's':
        cube = data_cube - np.nanmin(data_cube, axis = 2)[:,:,np.newaxis]
        max_cube = np.nanmax(cube, axis = 2)[:,:,np.newaxis]
        return cube/max_cube
    elif axis == 'b':
        cube = data_cube - np.nanmin(data_cube, axis = (0,1))
        return cube/np.nanmax(cube, axis = (0,1))
    else:
        raise Exception("Invalid input argument. Axis input argument must be either 's' or 'b'")

#Normalizes the cube to span from 0 to 1
def normalize_cube(data_cube):
    cube = data_cube - np.nanmin(data_cube)
    return cube/np.nanmax(cube)

#Subtracts selected band from all layers in the cube
def subtract_band(data_cube, band):
    return data_cube - data_cube[:,:,band][:,:,np.newaxis]

#Flattens data cube into 2D array
def flatten(data_cube):
    return np.reshape(data_cube, [data_cube.shape[0]*data_cube.shape[1], data_cube.shape[2]])

#Reshapes flattened data cube back into 3 dimensions
def inflate(array_2D, n_rows, n_cols):
    return np.reshape(array_2D, [n_rows, n_cols, array_2D.shape[1]])

#Median filters each band in data cube
def median_filter_cube(data_cube, kernel_size):
    band_lst = []
    for i in range(data_cube.shape[2]):
        band_lst.append(data_cube[:,:,i])
    kernel_size_lst = np.ones(len(band_lst), dtype = int)*kernel_size
    with cf.ThreadPoolExecutor() as executor:
        results = executor.map(median_filter, band_lst, kernel_size_lst)
    filtered_cube = np.zeros_like(data_cube)
    for i, result in enumerate(results):
        filtered_cube[:,:,i] = result
    return filtered_cube

#Median filters a 2D array and only applies it to the locations marked as True
#in the px_idx array.
def targeted_median_filter(input_array, px_idx, kernel_size):
    if input_array.shape != px_idx.shape:
        print("Arrays must be the same shape. px_idx must be a true/false numpy array")
        return
    if type(input_array[0,0]) is not np.float64:
         input_array = input_array.astype(float)
    filtered_array = median_filter(input_array, size = kernel_size)
    input_array[px_idx] = filtered_array[px_idx]
    return input_array

#Imports cube based on directory argument
def load_cube(directory):
    NoB = sum([ '.ppm' in s for s in os.listdir(f'{directory}/images/capture')])
    steps = np.arange(0,NoB*10,10) #vector with all the steps at which an image is taken
    cube = []
    for step in steps: #load bands into data structure
        cube.append(np.rot90(cv.imread(f'{directory}/images/capture/step{step}.ppm',cv.IMREAD_ANYDEPTH)))
    cube = np.array(cube, dtype = 'float64')
    cube = np.moveaxis(cube, 0, 2) #Rearranges the array to required shape
    return cube

#Calculates hottelings T^2 statistic for matrix X, where the variables are
#represented by each column and the samples by the rows
#https://learnche.org/pid/latent-variable-modelling/principal-component-analysis/hotellings-t2-statistic
def hottelings(X):
    return np.nansum((X/np.nanstd(X, axis=0))**2, axis=1)

#Calculates the upper and lower 95% confidence limits of the mean of input vector, x
def conf95lim(x):
    conf = []
    mean = np.nanmean(x)
    std = np.nanstd(x)
    conf.append(mean-2*std)
    conf.append(mean+2*std)
    return conf

#Select three layers (either as a list or numpy vector) and use these three as the
#channels of an rgb image. The first layer is the red channel, the second layer
#the green channel and the third layer is the blue channel.
def array2rgb(data_cube, three_layers):
    three_layer_cube = np.zeros([data_cube.shape[0], data_cube.shape[1], 3])
    three_layer_cube[:,:,0] = data_cube[:,:,three_layers[0]] - np.nanmin(data_cube[:,:,three_layers[0]])
    three_layer_cube[:,:,0] = three_layer_cube[:,:,0]/np.nanmax(three_layer_cube[:,:,0])
    three_layer_cube[:,:,1] = data_cube[:,:,three_layers[1]] - np.nanmin(data_cube[:,:,three_layers[1]])
    three_layer_cube[:,:,1] = three_layer_cube[:,:,1]/np.nanmax(three_layer_cube[:,:,1])
    three_layer_cube[:,:,2] = data_cube[:,:,three_layers[2]] - np.nanmin(data_cube[:,:,three_layers[2]])
    three_layer_cube[:,:,2] = three_layer_cube[:,:,2]/np.nanmax(three_layer_cube[:,:,2])
    return three_layer_cube

#This function calculates and applies a NUC to the entire datacube. The NUC is
#dependent on the sensor temperature and the GSK settings of the camera. The
#NUC is calculated from camera specific calibration files from the accompanying NUC directory
def apply_NUC_cube(cube, sensor_temp, GSK, camera_ID = '10_10_200_191'):

    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)

    M = np.array([[GSK, sensor_temp, 1]]).T

    offsets = offset_coefs@M
    slopes = slope_coefs@M

    mean_offset = np.nanmean(offsets)
    mean_slopes = np.nanmean(slopes)

    offset_correction = - mean_slopes*offsets/slopes + mean_offset
    slope_correction = (mean_slopes - slopes)/slopes

    offset_matrix = offset_correction.reshape([cube.shape[0], cube.shape[1]], order = 'C')
    slope_matrix = slope_correction.reshape([cube.shape[0], cube.shape[1]], order = 'C')

    temp_cube = np.copy(cube)
    for i in range(temp_cube.shape[2]):
        temp_cube[:,:,i] = temp_cube[:,:,i] + temp_cube[:,:,i]*slope_matrix + offset_matrix
    return temp_cube

#This function calculates and applies a NUC to a single image. The NUC is dependent
#on the sensor temperature and the GSK settings of the camera. The NUC is
#calculated from camera specific calibration files from the accompanying NUC directory.
def apply_NUC_image(image, sensor_temp, GSK, camera_ID = '10_10_200_191'):

    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"NUC/{camera_ID}/slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)


    M = np.array([[GSK, sensor_temp, 1]]).T

    offsets = offset_coefs@M
    slopes = slope_coefs@M

    mean_offset = np.nanmean(offsets)
    mean_slopes = np.nanmean(slopes)

    offset_correction = - mean_slopes*offsets/slopes + mean_offset
    slope_correction = (mean_slopes - slopes)/slopes

    offset_matrix = offset_correction.reshape([image.shape[0], image.shape[1]], order = 'C')
    slope_matrix = slope_correction.reshape([image.shape[0], image.shape[1]], order = 'C')

    return image  + image*slope_matrix + offset_matrix

def naive_temperature_image(image, sensor_temp, GSK, camera_ID = '10_10_200_191'):
    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)

    a = slope_coefs[:,0]*GSK + slope_coefs[:,1]*sensor_temp + slope_coefs[:,2]
    b = offset_coefs[:,0]*GSK + offset_coefs[:,1]*sensor_temp + offset_coefs[:,2]

    flat_img = np.reshape(image, image.size)
    flat_img = flat_img*a + b
    return np.reshape(flat_img, [image.shape[0], image.shape[1]])

def naive_temperature_cube(data_cube, sensor_temp, GSK, camera_ID = '10_10_200_191'):
    resource_package = __name__
    resource_path_offset = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_offset_coefs_1st_order.npy"))  # Do not use os.path.join()
    resource_path_slope = '/'.join(('HSTI_data_files-main', f"Temperature_conversions/{camera_ID}/temp_slope_coefs_1st_order.npy"))  # Do not use os.path.join()
    path_offset = pkg_resources.resource_stream(resource_package, resource_path_offset)
    path_slope = pkg_resources.resource_stream(resource_package, resource_path_slope)
    offset_coefs = np.load(path_offset, allow_pickle = True)
    slope_coefs = np.load(path_slope, allow_pickle = True)

    a = slope_coefs[:,0]*GSK + slope_coefs[:,1]*sensor_temp + slope_coefs[:,2]
    b = offset_coefs[:,0]*GSK + offset_coefs[:,1]*sensor_temp + offset_coefs[:,2]

    flat_cube = np.reshape(data_cube, [data_cube.shape[0]*data_cube.shape[1], data_cube.shape[2]])
    flat_cube = flat_cube*a[:,np.newaxis] + b[:,np.newaxis]
    return np.reshape(flat_cube, [data_cube.shape[0], data_cube.shape[1], data_cube.shape[2]])

def rsvd(input_matrix, rank, power_iter = 3): #https://towardsdatascience.com/intuitive-understanding-of-randomized-singular-value-decomposition-9389e27cb9de
    Omega = np.random.randn(input_matrix.shape[1], rank)
    Y = input_matrix @ Omega
    for q in range(power_iter):
        Y = input_matrix @ (input_matrix.T @ Y)
    Q, _ = np.linalg.qr(Y)
    B = Q.T @ input_matrix
    u_tilde, s, v = np.linalg.svd(B, full_matrices = False)
    u = Q @ u_tilde
    return u, s, v 