.. vim: ft=rst

######################################
Understanding least-squares regression
######################################

****************************
Introduction and definitions
****************************

.. nbplot::

    >>> #: Import numerical and plotting libraries
    >>> import numpy as np
    >>> # Print to four digits of precision
    >>> np.set_printoptions(precision=4, suppress=True)
    >>> import numpy.linalg as npl
    >>> import matplotlib.pyplot as plt

These exercises are to practice thinking about how the regression estimation
works, and the relationship of correlation and regression.

To give us some concrete data to play with, here are some more samples of the
"psychopathy" and "clamminess" scores that we saw in the `introduction to the
general linear model`_:

.. nbplot::

    >>> #: The data, that we are trying to model.
    >>> psychopathy = np.array([ 11.914,   4.289,  10.825,  14.987,
    ...                          7.572,   5.447,   17.332,  12.105,
    ...                          13.297,  10.635,  21.777,  20.715])

    >>> #: The regressor that we will use to model the data.
    >>> clammy = np.array([ 0.422,  0.406,  0.061,  0.962,  4.715,
    ...                     1.398,  1.952,  5.095, 8.092,  5.685,
    ...                     5.167,  7.257])

:math:`\newcommand{\yvec}{\vec{y}} \newcommand{\xvec}{\vec{x}} \newcommand{\evec}{\vec{\varepsilon}}`

Our simple linear model can be expressed by:

.. math::

    y_i = c + bx_i + e_i`

or, in vector notation:

.. math::

    \yvec = c + b \xvec + \evec

where $\yvec$ is the vector of values $[y_1, y_2, ... y_n]$ we want to explain
(psychopathy), $\xvec$ is the vector of values $[x_1, x_2, ... x_n]$
containing our explanatory variable (clammy), and $\evec$ is the vector of
remaining data unexplained by $c + b \xvec$.

:math:`\newcommand{Xmat}{\boldsymbol X} \newcommand{\bvec}{\vec{\beta}}`

The same model can also be expressed using a design *matrix* $\Xmat$:

.. math::

   \yvec = \Xmat \bvec + \evec

where $\Xmat$ has two columns, the first being a length $n$ vector of ones,
and the second being $\xvec$. $\bvec$ is column vector containing two values,
$[c, b]$ that are the intercept and slope of the fitted line.

Now define the *mean* of $\vec{x}$ as:

.. math::

    \bar{x} = \frac{1}{n} \sum_{i=1}^n x_i

Define two new vectors, $\vec{x^c}, \vec{y^c}$ that contain the values in
$\vec{x}, \vec{y}$ with their respective means subtracted:

.. math::

    \vec{x^c} = [x_1 - \bar{x}, x_2 - \bar{x}, ... , x_n - \bar{x}]

    \vec{y^c} = [y_1 - \bar{y}, y_2 - \bar{y}, ... , y_n - \bar{y}]

We found in `introduction to the general linear model`_ that, for the case of
a full-rank matrix $\Xmat$, the least squares estimate for $\bvec$ is given
by:

.. math::

    \newcommand{\bhat}{\hat{\bvec}} \newcommand{\yhat}{\hat{\yvec}}
    \bhat = (\Xmat^T \Xmat)^{-1} \Xmat^T \yvec

**************************************
Correlation coefficient and regression
**************************************

Create the $\Xmat$ matrix from a vector of ones and the vector of ``clammy``
scores:

.. nbplot::

    >>> #- Create X design matrix fron column of ones and clammy vector
    >>> n = len(clammy)
    >>> X = np.ones((n, 2))
    >>> X[:, 1] = clammy
    >>> X
    array([[ 1.   ,  0.422],
           [ 1.   ,  0.406],
           [ 1.   ,  0.061],
           [ 1.   ,  0.962],
           [ 1.   ,  4.715],
           [ 1.   ,  1.398],
           [ 1.   ,  1.952],
           [ 1.   ,  5.095],
           [ 1.   ,  8.092],
           [ 1.   ,  5.685],
           [ 1.   ,  5.167],
           [ 1.   ,  7.257]])

Are the columns of ``X`` orthogonal to each other?

.. nbplot::

    >>> #- Check whether the columns of X are orthogonal
    >>> X.T.dot(X)
    array([[  12.    ,   41.212 ],
           [  41.212 ,  232.3887]])

Is $\Xmat^T \Xmat$ invertible?

.. nbplot::

    >>> #- Check whether X.T.dot(X) is invertible
    >>> iXtX = npl.inv(X.T.dot(X))  # No error in inversion

Calculate $(\Xmat^T \Xmat)^{-1} \Xmat^T$.  What shape is it?

.. nbplot::

    >>> #- Calculate (X.T X)^-1 X.T (the pseudoinverse)
    >>> piX = iXtX.dot(X.T)
    >>> piX.shape
    (2, 12)

Calculate the least squares fit value for $\bvec$:

.. nbplot::

    >>> #- Calculate least squares fit for beta vector
    >>> B = piX.dot(psychopathy)
    >>> B
    array([ 9.8016,  0.8074])

Calculate the fitted values $c + b \xvec$, and the residuals $\evec$:

.. nbplot::

    >>> #- Calculate the fitted values
    >>> fitted = X.dot(B)
    >>> residuals = psychopathy - fitted

Confirm that the mean of the residuals is close to zero:

.. nbplot::

    >>> #- mean of residuals near zero
    >>> np.allclose(residuals.mean(), 0)
    True

Confirm that residuals are orthogonal to both columns of the design matrix:

.. nbplot::

    >>> #- Residuals orthogonal to design
    >>> X.T.dot(residuals)
    array([-0., -0.])

We will not modify the design to see what happens to the parameters and the
fitted values.

To keep our calculations for the original and new designs, start by copying
``X`` to make a new array ``X_o``.  Hint: tab complete on the array object in
IPython.

.. nbplot::

    >>> #- Copy X to new array X_o
    >>> X_o = X.copy()

We found that above that the columns of ``X`` are not orthogonal.  How can we
modify the second column of ``X`` to make it orthogonal to the first?  Hint:
write out the dot product of the first column with the second as a sum, and
simplify. Use that result to work out what to subtract from the second column
so the dot product is 0.

.. nbplot::

    >>> #- Make second column orthogonal to first. Confirm orthogonality
    >>> X_o[:, 1] = X_o[:, 1] - X_o[:, 1].mean()
    >>> X_o.T.dot(X_o)
    array([[ 12.    ,   0.    ],
           [  0.    ,  90.8529]])


Look at the diagonal values of the matrix ``X_o.T.dot(X_o)``.  What is the
relationship of these values to the lengths of the vectors in the first and
second columns of ``X_o``?

.. admonition:: Answer

.. solution-start

    The diagonal contains the squared vector lengths of the columns of
    ``X_o``.

.. solution-replace

    ?

.. solution-replace-code

    """ What is the relationship between the values on the diagonal of
    X_o.T.dot(X_o) and the lengths of the vectors in the first and second
    columns of X_o?

    """

.. solution-end

Use ``numpy.linalg.inv`` to find $(\Xmat^T \Xmat)^{-1}$ |--| the inverse of
``X_o.T.dot(X_o)``. Now what is the relationship of the values in the diagonal
of the inverse matrix to the lengths of the vectors in the first and second
columns of ``X_o``?  Hint: $A^{-1} \cdot A = I$; if $A$ has all zeros off the
diagonal, what must $A^{-1}$ be for this to be true?

.. admonition:: Answer

.. solution-start

    The diagonal contains the reciprocal of the squared vector lengths of the
    columns of ``X_o``.

.. solution-replace

    ?

.. solution-replace-code

    """ What is the relationship between the values on the diagonal of the
    *inverse* of X_o.T.dot(X_o) and the lengths of the vectors in the first
    and second columns of X_o?

    """

.. solution-end

Make a new data vector ``y_c`` by subtracting the mean from the psychopathy
vector:

.. nbplot::

    >>> #- Make mean-centered version of psychopathy vector
    >>> y_c = psychopathy - psychopathy.mean()

Calculate a new ``B_o`` parameter vector for the least-squares fit of ``X_o``
to ``y_c``:

.. nbplot::

    >>> #- Calculate fit of X_o to y_o
    >>> iXtX = npl.inv(X_o.T.dot(X_o))
    >>> B_o = iXtX.dot(X_o.T).dot(y_c)
    >>> B_o
    array([-0.    ,  0.8074])

The first parameter has changed compared to your previous estimate.  Can you
explain its new value?

.. admonition:: Answer

.. solution-start

    We are working on:

    .. math::

        \bhat = (\Xmat^T \Xmat)^{-1} \Xmat^T \yvec

    Consider $\vec{p} = \Xmat^T \yvec$. Because the first column in the design
    is a column of ones, the dot product of this vector with any other is the
    sum of the values in the other vector.  The data has mean and therefore
    sum 0.  Therefore the first value in $\vec{p}$ must be zero.  Because
    $\Xmat^T \Xmat$ is diagonal, the first value in $\bhat$ is just a scalar
    multiple of the first value in $\vec{p}$, and is therefore also 0.

.. solution-replace

    ?

.. solution-replace-code

    """ Explain the new value of the first element of the parameter estimate
    vector.

    """

.. solution-end

Calculate the correlation coefficient between ``y_c`` and the second column of
``X_o``:

.. nbplot::

    >>> #- Correlation coefficient of y_c and the second column of X_o
    >>> r_xy = np.corrcoef(y_c, X_o[:, 1])[0, 1]
    >>> r_xy
    0.42245241...

What is the relationship between this correlation coefficient and ``B_o[1]``?
Hint: what is the relationship of the correlation coefficient to vector dot
products?  See: `correlation and projection`_ for a reminder.

.. admonition:: Answer

.. solution-start

    `Remember that <correlation and projection_>`_ the correlation coefficient
    can be written as:

    .. math::

        r_{xy} = \frac{\vec{x^c} \cdot \vec{y^c}} {\VL{x^c} \VL{y^c}}

    Set:

    .. nbplot::

        >>> x_c = X_o[:, 1]

    From the derivation of ``y_c`` and ``x_c``, and the formula for deriving
    $\bvec$:

    .. math::

        \texttt{B_o[1]} = \frac{\vec{x^c} \cdot \vec{y^c}}{\VL{x_c}^2} \\
        = r_{xy} \frac{\VL{y_c}}{\VL{x_c}}

    Let's check that:

    .. nbplot::

        >>> def vector_length(vec):
        ...     return np.sqrt(np.sum(vec ** 2))

        >>> B_o
        array([-0.    ,  0.8074])
        >>> r_xy * vector_length(y_c) / vector_length(x_c)
        0.8074...

.. solution-replace

    ?

.. solution-replace-code

    """ What is the relationship between the correlation coefficient "r_xy"
    and the second element in the parameter vector "B_o[1]"?

    """

.. solution-end

Now try calculating $\bvec$ fitting the ``X_o`` design to the original
psychopathy data (not the mean-centered version).

.. nbplot::

    >>> #- Fit X_o to psychopathy data
    >>> B_o = iXtX.dot(X_o.T).dot(psychopathy)
    >>> B_o
    array([ 12.5746,   0.8074])

Compare the first value in the new ``B_o`` parameter vector with the mean of
the ``psychpathy`` vector.

.. nbplot::

    >>> psychopathy.mean()
    12.57458...

Can you explain the relationship?

.. admonition:: Answer

.. solution-start

    We are working on:

    .. math::

        \bhat = (\Xmat^T \Xmat)^{-1} \Xmat^T \yvec

    Consider $\vec{p} = \Xmat^T \yvec$.

    .. math::

        p_1 = \vec{1} \cdot \yvec \\ = \sum_i{y_i}

    Now consider left matrix multiplication by the inverse:

    .. math::

        Q = (\Xmat^T \Xmat) \\
        R = Q^{-1} \\

        q_{1, 1} = n \\
        r_{1, 1} = \frac{1}{n} \\

        \bhat_1 = \frac{1}{n} \sum_i {y_i} = \bar{y}.

.. solution-replace

    ?

.. solution-replace-code

    """ Explain the relationship between the mean of the psychopathy values
    and the first element of the parameter estimate vector.

    """

.. solution-end

For extra points, can you explain why the second value in ``B_o`` did not
change when we estimated for ``psychopathy`` rather than the mean-centered
version ``y_c``?  Hint: remember $(\vec{a} + \vec{b}) \cdot \vec{c} = \vec{a}
\cdot \vec{c} + \vec{b} \cdot \vec{c}$.

.. admonition:: Answer

.. solution-start

    Consider $\vec{p} = \Xmat^T \yvec$.

    .. math::

        p_2 = \vec{x_c} \cdot \yvec

    I can also write:

    .. math::

        \yvec = \vec{y_c} + \bar{y} \\
        = \vec{y_c} + \bar{y} \vec{1}

    So:

    .. math::

        p_2 = \vec{x_c} \cdot (\vec{y_c} + \bar{y} \vec{1}) \\
        = \vec{x_c} \cdot \vec{y_c} + \vec{x_c} \cdot \bar{y} \vec{1}) \\
        = \vec{x_c} \cdot \vec{y_c} + 0

    So $p_2$ is the same for $\vec{y_c}$ or $\yvec$.  Because $\Xmat$ is the
    same in both cases, both $\vec{y_c}$ and $\yvec$ must give the same output
    $\beta_2$.

.. solution-replace

    ?

.. solution-replace-code

    """ Why is the second value in B_o the same when estimating against "y_c"
    and "psychopathy"?
    """

.. solution-end

Calculate the fitted values for the ``X_o`` model, and compare them to the
fitted values for the original model:

.. nbplot::

    >>> fitted_X_o = X_o.dot(B_o)
    >>> np.allclose(fitted_X_o, fitted)
    True

For even more extra points, explain the relationship between the fitted values
for the original model and those for the new model, where the clammy regressor
is mean centered.

.. admonition:: Answer

.. solution-start

    Call the second column of the original design $\vec{x}$.  These are the
    values of ``clammy`` in our case.  $\vec{x_c} = \vec{x} - \bar{x}$.  So
    $\vec{x}$, which is the second column of our original design, can also be
    written as the sum of two vectors:

    .. math::

        \Xmat_{:,1} = \vec{x} = \vec{x_c} + \bar{x} \vec{1}

    A fit to the original design, for particular values of $c$ and $b$ will
    be:

    .. math::

        c + b \vec{x} \\
        = c + b (\vec{x_c} + \bar{x} \vec{1}) \\
        = c + b \vec{x_c} + b \bar{x}

    Therefore any fit possible with the original model can be achieved with
    the mean-centered model, by adjusting the value of $c$ to include the $b
    \bar{x}$ term.  Specifically:

    .. nbplot::

        >>> # Fit again to original model
        >>> y = psychopathy
        >>> B = npl.inv(X.T.dot(X)).dot(X.T).dot(y)
        >>> B
        array([ 9.8016,  0.8074])

        >>> # Fit again to mean-centered model
        >>> B_o = npl.inv(X_o.T.dot(X_o)).dot(X_o.T).dot(y)
        >>> B_o
        array([ 12.5746,   0.8074])

        >>> # The difference in B_o[0] (c) is b * X[:, 1].mean()
        >>> B[1] * X[:, 1].mean()
        2.7729...
        >>> B[0] + B[1] * X[:, 1].mean()
        12.57458...

.. solution-replace

    ?

.. solution-code-replace:

    """ Explain the relationship between the fitted values for the original
    model and those for the new model, where the clammy regressor is mean
    centered.

    """

.. solution-end
