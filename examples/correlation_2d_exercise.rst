.. vim: ft=rst

############################
Correlation per voxel, in 2D
############################

* For code template see: :download:`correlation_2d_code.py`;
* For solution see: :doc:`correlation_2d_solution`.

In this exercise, we will take each voxel time course in the brain, and
calculate a correlation between the task-on / task-off vector and the voxel
time course.  We then make a new 3D volume that contains correlation values
for each voxel.

.. nbplot::
    :include-source: false


.. nbplot::

    >>> #: Standard imports
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> import nibabel as nib

Import the ``events2neural`` function from the :download:`stimuli.py` module:

.. nbplot::

    >>> #- import events2neural from stimuli module

If you don't have it already, download the :download:`ds114_sub009_t2r1.nii`
image.  Load it with nibabel.

.. nbplot::

    >>> #- Load the ds114_sub009_t2r1.nii image

    >>> #- Get the number of volumes in ds114_sub009_t2r1.nii

The TR (time between scans) is 2.5 seconds.

.. nbplot::

    >>> #: TR
    >>> TR = 2.5

Call the ``events2neural`` function to give you a time course that is 1 for
the volumes during the task (thinking of verbs) and 0 for the volumes during
rest.

.. nbplot::

    >>> #- Call events2neural to give on-off values for each volume

Using slicing, drop the first 4 volumes, and the corresponding on-off values:

.. nbplot::

    >>> #- Drop the first 4 volumes, and the first 4 on-off values

.. nbplot::

    >>> #- Calculate the number of voxels (number of elements in one volume)

Reshape the 4D data to a 2D array shape (number of voxels, number
of volumes).

.. nbplot::

    >>> #- Reshape 4D array to 2D array n_voxels by n_volumes

.. nbplot::

    >>> #- Make a 1D array of size (n_voxels,) to hold the correlation values

If you finished the :doc:`pearson_functions` exercise, you can use your
``pearson_2d`` routine for calculating Pearson correlations across a 2D array.
Otherwise, loop over all voxels, calculate the correlation coefficient with
``time_course`` at this voxel, and fill in the corresponding entry in your 1D
array.

.. nbplot::

    >>> #- Loop over voxels filling in correlation at this voxel

.. nbplot::

    >>> #- Or (much faster) use pearson_2d function

Reshape the correlations 1D array back to a 3D array, using the original 3D
shape.

.. nbplot::

    >>> #- Reshape the correlations array back to 3D

Test that your brain-at-a-time correlation image gives the same answer when
you run the correlation on a single voxel time course.  Select an example
voxel |--| say ``data[42, 32, 19]`` |--| and check that this gives the same
answer as you found for the matching voxel in your correlations 3D array:

.. nbplot::

    >>> #- Check you get the same answer when selecting a voxel time course
    >>> #- and running the correlation on that time course.  One example voxel
    >>> #- could be the voxel at array coordinate [42, 32, 19]

Plot the middle slice (plane) of the third axis from the correlations array.
Look for any voxels with a high task correlation in the frontal lobe:

.. nbplot::

    >>> #- Plot the middle slice of the third axis from the correlations array
