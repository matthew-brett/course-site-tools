""" Making a predicted neural time course
"""
#: compatibility with Python 2
from __future__ import print_function, division


#- Load the image with nibabel.
#- Get the image data array, print the data shape.

#: Read in stimulus file, return neural prediction
def events2neural(task_fname, tr, n_trs):
    """ Return predicted neural time course from event file

    Parameters
    ----------
    task_fname : str
        Filename of event file
    tr : float
        TR in seconds
    n_trs : int
        Number of TRs in functional run

    Returns
    -------
    time_course : array shape (n_trs,)
        Predicted neural time course, one value per TR
    """
    task = np.loadtxt(task_fname)
    if task.ndim != 2 or task.shape[1] != 3:
        raise ValueError("Is {0} really a task file?", task_fname)
    task[:, :2] = task[:, :2] / tr
    time_course = np.zeros(n_trs)
    for onset, duration, amplitude in task:
        time_course[onset:onset + duration] = amplitude
    return time_course

#- Read the stimulus data file and return a predicted neural time
#- course.
#- Plot the predicted neural time course.

#- Make new array excluding the first volume
#- data_no_0 = ?

#- Knock the first element off the neural prediction time series.
#- neural_prediction_no_0 = ?

#: subtracting rest from task scans
task_scans = data_no_0[..., neural_prediction_no_0 == 1]
rest_scans = data_no_0[..., neural_prediction_no_0 == 0]
difference = np.mean(task_scans, axis=-1) - np.mean(rest_scans, axis=-1)

#: showing slice 14 from the difference image
plt.imshow(difference[:, :, 14], cmap='gray')
    <...>

#- Get the values for (i, j, k) = (45, 43, 14) and every volume.
#- Plot the values (voxel time course).

#- Correlation of predicted neural time course with voxel signal time
#- course

#- Make a vector of times at which to sample the HRF

#- Sample HRF at given times
#- Plot HRF samples against times

#- Convolve predicted neural time course with HRF samples

#- Remove extra tail of values put there by the convolution

#- Plot convolved neural prediction and unconvolved neural prediction

#- Correlation of the convolved time course with voxel time course

#- Scatterplot the hemodynamic prediction against the signal
