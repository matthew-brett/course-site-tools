.. vim:ft=rst

#####################################
Making a predicted neural time course
#####################################

* For code template see: :download:`hrf_correlation_code.py`;
* For solution see: :doc:`hrf_correlation_solution`.

.. nbplot::
    :include-source: false

    >>> #: compatibility with Python 2
    >>> from __future__ import print_function, division

.. nbplot::


We are going to be analyzing the data for the 4D image
:download:`ds114_sub009_t2r1.nii` again.

Load the image into an image object with nibabel, and get the image data
array. Print the shape.

.. nbplot::

    >>> #- Load the image with nibabel.
    >>> #- Get the image data array, print the data shape.

Next we read in the stimulus file for this run to make an on - off
time-series.

The stimulus file is :download:`ds114_sub009_t2r1_cond.txt`.

Here's a version of the same thing we did in an earlier exercise, as a
function:

.. nbplot::

    >>> #: Read in stimulus file, return neural prediction
    >>> def events2neural(task_fname, tr, n_trs):
    ...     """ Return predicted neural time course from event file
    ...
    ...     Parameters
    ...     ----------
    ...     task_fname : str
    ...         Filename of event file
    ...     tr : float
    ...         TR in seconds
    ...     n_trs : int
    ...         Number of TRs in functional run
    ...
    ...     Returns
    ...     -------
    ...     time_course : array shape (n_trs,)
    ...         Predicted neural time course, one value per TR
    ...     """
    ...     task = np.loadtxt(task_fname)
    ...     if task.ndim != 2 or task.shape[1] != 3:
    ...         raise ValueError("Is {0} really a task file?", task_fname)
    ...     task[:, :2] = task[:, :2] / tr
    ...     time_course = np.zeros(n_trs)
    ...     for onset, duration, amplitude in task:
    ...         time_course[onset:onset + duration] = amplitude
    ...     return time_course

Use this function to read ``ds114_sub009_t2r1_cond.txt`` and return a
predicted neural time course.

The TR for this run is 2.5. You know the number of TRs from the image
data shape above.

.. nbplot::

    >>> #- Read the stimulus data file and return a predicted neural time
    >>> #- course.
    >>> #- Plot the predicted neural time course.

We had previously found that the first volume in this run was bad. Use your
slicing skills to make a new array called ``data_no_0`` that is the data array
without the first volume:

.. nbplot::

    >>> #- Make new array excluding the first volume
    >>> #- data_no_0 = ?

Our neural prediction time series currently has one value per volume,
including the first volume. To match the data, make a new neural prediction
variable that does not include the first value of the time series. Call this
new variable ``neural_prediction_no_0``.

.. nbplot::

    >>> #- Knock the first element off the neural prediction time series.
    >>> #- neural_prediction_no_0 = ?

For now, we're going to play with data for a single voxel.

In an earlier exercise, we subtracted the rest scans from the task scans,
something like this:

.. nbplot::

    >>> #: subtracting rest from task scans
    >>> task_scans = data_no_0[..., neural_prediction_no_0 == 1]
    >>> rest_scans = data_no_0[..., neural_prediction_no_0 == 0]
    >>> difference = np.mean(task_scans, axis=-1) - np.mean(rest_scans, axis=-1)

.. nbplot::

    >>> #: showing slice 14 from the difference image
    >>> plt.imshow(difference[:, :, 14], cmap='gray')
    <...>

It looks like there's a voxel that is greater for activation than rest at
about (i, j, k) == (45, 43, 14).

Get and plot the values for this voxel position, for every volume in the 4D
data (not including the first volume). You can do it with a loop, but slicing
is much nicer.

.. nbplot::

    >>> #- Get the values for (i, j, k) = (45, 43, 14) and every volume.
    >>> #- Plot the values (voxel time course).

Correlate the predicted neural time series with the voxel time course:

.. nbplot::

    >>> #- Correlation of predicted neural time course with voxel signal time
    >>> #- course

Now we will do a predicted hemodynamic time course using convolution.

Next we need to get the HRF vector to convolve with.

Remember we have defined the HRF as a function of time, not TRs.

For our convolution, we need to *sample* the HRF at times corresponding the
start of the TRs.

So, we need to sample at times (0, 2.5, ...)

Make a vector of times at which to sample the HRF. We want to sample every TR
up until (but not including) somewhere near 35 seconds (where the HRF should
have got close to zero again).

.. nbplot::

    >>> #- Make a vector of times at which to sample the HRF

Sample your HRF function at these times and plot:

.. nbplot::

    >>> #- Sample HRF at given times
    >>> #- Plot HRF samples against times

Convolve the predicted neural time course with the HRF samples:

.. nbplot::

    >>> #- Convolve predicted neural time course with HRF samples

The default output of convolve is longer than the input neural prediction
vector, by the length of the convolving vector (the HRF samples) minus 1.
Knock these last values off the result of the convolution to get a vector the
same length as the neural prediction:

.. nbplot::

    >>> #- Remove extra tail of values put there by the convolution

Plot the convolved neural prediction, and then, on the same plot, plot the
unconvolved neural prediction.

.. nbplot::

    >>> #- Plot convolved neural prediction and unconvolved neural prediction

Does the new convolved time course correlate better with the voxel time
course?

.. nbplot::

    >>> #- Correlation of the convolved time course with voxel time course

Plot the hemodynamic prediction against the actual signal (voxel values).
Remember to use a marker such as '+' to give you a scatter plot. How does it
look?

.. nbplot::

    >>> #- Scatterplot the hemodynamic prediction against the signal
