# pyquartic
Modified Ferrari's quartic solver and modified Cardano's cubic solver for Python (4th and 3rd order polynomials).  


## Features
- Original algorithms are modified so they provide stable and correct solutions to polynomials  
- Using modified algorithms from [quarticequations.com](https://quarticequations.com)
- Functions are optimized for fast computing (up to 20x faster than np.roots)  
- Numba and pure-python implementation


## Usage
[pyquartic_nonumba.py](pyquartic_nonumba.py) can be used in case where numba is available but should not be used.  
Output values are complex numbers in tuple, where each number is one root.  

### Cubic solver
```py
import pyquartic
roots = pyquartic.solve_cubic(a, b, c, d)
```
Where `a, b, c, d` are cubic equation coefficients:  
$`ax^3 + bx^2 + cx + d = 0`$

### Quartic solver
```py
import pyquartic
roots = pyquartic.solve_quartic(a, b, c, d, e)
```
Where `a, b, c, d, e` are quartic equation coefficients:  
$`ax^4 + bx^3 + cx^2 + dx + e = 0`$


## Speed analysis
Speed analysis can be performed by running [test_pyquartic.py](test_pyquartic.py).  
Numpy's polyroots solver computes eigenvalues of a companion matrix, formed from n-th order polynomial coefficients. This method is stable and accurate, but very slow and is not supported by numba.  
Tests are performed on large number of coefficients (10000) where coefficients range from -10000 to 10000, times shown are mean and best times from those iterations.  
Provided are three tests for cubic and quartic: numpy's polyroots, modified Ferrari's algorithm, and 'numbarized' modified Ferrari's algorithm.  
```
Cubic
np.root: 113.7076 us, best: 105.672 us
python : 14.3613 us, best: 13.075 us
numba  : 5.628 us, best: 5.095 us
```
```
Quartic
np.root: 116.1679 us, best: 108.099 us
python : 21.0779 us, best: 18.921 us
nmba   : 6.4158 us, best: 5.805 us
```


## Modifications to algorithms
Much more detailed versions and tutorials for this modifications are covered in this paper: [quarticequations.com](https://quarticequations.com).  
This project is only implementation of there described modified algorithms.  


### Cardano's method
Cardano's method has large round-off error at some specific cases (when parameter q approaches zero).  
While mathematically correct, when calculated on computer, where numbers are rounded, this can create large errors, that are later carried to quartic solver.  
To fix this, when there is only one real solution, solution from 'Numerical Recipes' is used.  
When there are three real solutions, Viète’s trigonometric method is used.  
More details [here](https://quarticequations.com/Cubic.pdf).  


### Ferrari's method
Ferrari's method uses one real root from cubic equation solved with Cardano's method.  
As this root approaches zero, algorithm becomes computationally unstable due to round-off error.  
Modified algorithm is called 'Modern generalization of Cardano’s Problem VIII'. It avoids this instability by adding one more calculation.  
More details [here](https://quarticequations.com/Quartic2.pdf).  
