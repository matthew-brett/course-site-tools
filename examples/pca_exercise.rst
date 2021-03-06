############
PCA exercise
############

* For code template see: :download:`pca_code.py`;
* For solution see: :doc:`pca_solution`.

.. nbplot::
    :include-source: false


.. nbplot::

    >>> #: import common modules
    >>> import numpy as np  # the Python array package
    >>> import matplotlib.pyplot as plt  # the Python plotting package
    >>> # Display array values to 6 digits of precision
    >>> np.set_printoptions(precision=4, suppress=True)

.. nbplot::

    >>> #: import numpy.linalg with a shorter name
    >>> import numpy.linalg as npl

Download the image :download:`ds114_sub009_t2r1.nii` if you don't already have
it. Load it with nibabel. Get the data.

.. nbplot::

    >>> #- Load the image 'ds114_sub009_t2r1.nii' with nibabel
    >>> #- Get the data array from the image

We can think of the shape of the data as two parts - the first 3 values are
the 3D shape of the individual volumes, and the last value is the number of
volumes.

Put the 3D shape into a variable ``vol_shape`` and the number of volumes into
a variable ``n_vols``:

.. nbplot::

    >>> #- Make variables:
    >>> #- 'vol_shape' for shape of volumes
    >>> #- 'n_vols' for number of volumes

We are going to take the time axis as containing the "features".  We will take
the voxels as being the "samples".  We start by taking the first two features
(time points).

Slice the data array to make a new array that contains only the first two
volumes:

.. nbplot::

    >>> #- Slice the image data array to give array with only first two
    >>> #- volumes

How many voxels are there in one volume? Put this number in a variable ``N``:

.. nbplot::

    >>> #- Set N to be the number of voxels in a volume

Reshape the new two-volume data array to have a first dimension length ``N``
and second dimension length 2.  Each of the two columns corresponds to the
voxels for a whole volume.

.. nbplot::

    >>> #- Reshape to 2D array with first dimension length N

Take the transpose of this array to get a 2 by ``N`` array, ready for the PCA:

.. nbplot::

    >>> #- Transpose to 2 by N array

Calculate the mean across columns (row means).  Put these means into a
variable ``row_means``.

.. nbplot::

    >>> #- Calculate the mean across columns

Expand the ``row_means`` vector out to a 2 by N array by using ``np.outer``
and a vector of ones:

.. nbplot::

    >>> #- Row means copied N times to become a 2 by N array

Subtract this expanded 2 by N means array from the 2 by N data matrix and put
the result into a variable ``X``. Print the means across columns (row means)
to check they are now very close to 0:

.. nbplot::

    >>> #- Subtract the means for each row, put the result into X
    >>> #- Show the means over the columns, after the subtraction

Plot the two rows against each other to get a feel for the variation.
Remember that each row in ``X`` is a volume, so you are plotting the signal
from the first volume against the corresponding signal for the second volume.

.. nbplot::

    >>> #- Plot the signal in the first row against the signal in the second

Time for the PCA.

We are going to use the *unscaled* covariance across time. This is given by
the matrix multiplication of ``X`` with its transpose. Calculate this:

.. nbplot::

    >>> #- Calculate unscaled covariance matrix for X

Use SVD to get the ``U``, ``S`` and ``VT`` matrices from the unscaled
covariance:

.. nbplot::

    >>> #- Use SVD to return U, S, VT matrices from unscaled covariance

Confirm that the column vectors in ``U`` are both unit vectors. A unit vector
has vector length (vector *norm*) 1:

.. nbplot::

    >>> #- Show that the columns in U each have vector length 1

Confirm that the first column in ``U`` is orthogonal to the second:

.. nbplot::

    >>> #- Confirm orthogonality of columns in U

Confirm that the transpose of ``U`` is also the matrix inverse of ``U``:

.. nbplot::

    >>> #- Confirm tranpose of U is inverse of U

Show the total sum of squares in ``X``. Confirm that the total sum of squares
in ``X`` is the same as the sum of the *singular values* in the ``S`` vector
from the SVD:

.. nbplot::

    >>> #- Show the total sum of squares in X
    >>> #- Is this (nearly) the same as the sum of the values in S?

Plot the first row in ``X`` against the second row in ``X`` again. This
time add a line to the plot that corresponds to the first principal component.
You'll have to scale this line (a unit vector) to make it long enough to see
on the axes of the plot. If the first principal component is flipped
(:math:`\vec{r}` defines same line as :math:`-\vec{r}`) you may need to scale
by a negative number for it to look nice on the plot:

.. nbplot::

    >>> #- Plot the signal in the first row against the signal in the second
    >>> #- Plot line corresponding to a scaled version of the first principal component
    >>> #- (Scaling may need to be negative)

Remember the projection formula :math:`c = \hat{u} \cdot \vec{v}`.

We now need to calculate the scalar projections :math:`c` for each component
:math:`\hat{u}` and each voxel (each :math:`\vec{v}`).

This will give us a new output matrix of scalar projections :math:`C` of shape
``(2, N)``, where the rows give the scalar projections for one component, and
the columns give the coefficients for one voxel.

For example, ``C[0, 0]`` will be the result of ``U[0, :].dot(X[:, 0])``, ``C[0,
1]`` will be the result of ``U[0, :].dot(X[:, 1])``, and ``C[1, 0]`` will be the
result of ``U[:, 1].dot(X[:, 0])``.

With that background, use matrix multiplication to calculate the scalar
projections ``C`` for projecting the data ``X`` onto the vectors in ``U``:

.. nbplot::

    >>> #- Calculate the scalar projections for projecting X onto the
    >>> #- vectors in U.
    >>> #- Put the result into a new array C.

Remember that ``C`` - the matrix of scalar projections |--| has one column per
voxel. We can think of each row as corresponding to a volume where the volumes
are contained in: ``C[0]`` (first row of ``C``) |--| scalar projections for
first principal component; ``C[1]`` (second row of C) |--| scalar projections
for second principal component.

Take the transpose of ``C`` and reshape the resulting first dimension (length
``N``) back to ``vol_shape`` - the original shape of the 3D volumes in the
data:

.. nbplot::

    >>> #- Transpose C
    >>> #- Reshape the first dimension of C to have the 3D shape of the
    >>> #- original data volumes.

Break this 4D array up into two volumes (volume for first component, volume
for second component) using slicing:

.. nbplot::

    >>> #- Break 4D array into two 3D volumes

Show the middle plane (slice over the third dimension) from the volume of
scalar projections for the first component:

.. nbplot::

    >>> #- Show middle slice (over third dimension) from scalar projections
    >>> #- for first component

Show the middle plane (slice over the third dimension) from the volume of
scalar projections for the second component:

.. nbplot::

    >>> #- Show middle slice (over third dimension) from scalar projections
    >>> #- for second component

Now we are ready to do the same thing for all the time points, instead of just
the first two.

Take the original array data matrix with ``n_vols`` volumes. Reshape to be
shape ``(N, nvols)``. Take the transpose to get an array shape ``(n_vols,
N)``:

.. nbplot::

    >>> #- Reshape first dimension of whole image data array to N, and take
    >>> #- transpose

Calculate the mean across columns (mean per volume). Expand this 1D shape
``(173,)`` vector to an array shape ``(173, N)``, using ``np.outer`` and a
vector of ones. Subtract this array from the ``(173, N)`` data array to remove
the mean across columns (mean per volume). Call this mean-corrected variable
``X``:

.. nbplot::

    >>> #- Calculate mean across columns
    >>> #- Expand to (173, N) shape using np.outer
    >>> #- Subtract from data array to remove mean over columns (row means)
    >>> #- Put result into array X

Get the unscaled covariance matrix of ``X``:

.. nbplot::

    >>> #- Calculate unscaled covariance matrix of X

Get ``U``, ``S``, ``VT`` outputs from the SVD of the unscaled covariance

.. nbplot::


Use ``plt.subplots`` to make a column of 10 axes. Iterate over these axes,
plotting one principal component vector per axis. You should then have a plot
of each of the first 10 principal component vectors:

.. nbplot::

    >>> #- Use subplots to make axes to plot first 10 principal component
    >>> #- vectors
    >>> #- Plot one component vector per sub-plot.

Use ``U`` and matrix multiplication to calculate the scalar projection
coefficients for projecting the data ``X`` onto the principal components
``U``. Put the result into ``C``:

.. nbplot::

    >>> #- Calculate scalar projections for projecting X onto U
    >>> #- Put results into array C.

Remember, each row of ``C`` is a full volume of scalar projections, one row
per principal component.

Reconstruct these rows as volumes by taking the transpose of ``C`` and
reshaping the first dimension length ``N`` to the original three dimensions of
the original data volumes.

.. nbplot::

    >>> #- Transpose C
    >>> #- Reshape the first dimension of C to have the 3D shape of the
    >>> #- original data volumes.

Take the first volume (corresponding to the first principal component) and
display the middle plane (slicing over the third dimension):

.. nbplot::

    >>> #- Show middle slice (over third dimension) of first principal
    >>> #- component volume

What does this first component show us?

Remember that the projections coefficients tell us how much of the component
vector there is in the data, at each voxel. If the voxel has a high value it
means there is a large amplitude of the component time-course at this voxel,
and if the component is dark it means there is a large negative amplitude of
the component time course.

Have a look again at the first component time course. How would a large
positive or negative amplitude of the time course come about?

As a hint while you are thinking, get the mean over time from the image data
(mean over the last axis), and show the middle plane (slicing over the third
axis):

.. nbplot::

    >>> #- Make the mean volume (mean over the last axis)
    >>> #- Show the middle plane (slicing over the third axis)

Display the middle plane (slicing over the third dimension) for the second
principal component volume.

Looking at the principal component plot - what kind of changes over time does
this principal component represent?

.. nbplot::

    >>> #- Show middle plane (slice over third dimension) of second principal
    >>> #- component volume

Do the same for the third principal component volume:

.. nbplot::

    >>> #- Show middle plane (slice over third dimension) of third principal
    >>> #- component volume
