## Cython

<br>

### tl; dr

<br>

* **[cython](https://cython.org/)** is an **optimising static compiler** for both Python and the extended cython programming language, making writing C extensions for Python easier.
* it turns readable Python code into plain C performance by adding static type declarations in Python syntax.
* cython source file names consist of the name of the module followed by a `.pyx` extension.
* the setuptools extension provided with cython allows you to pass `.pyx` files directly to the `Extension` constructor in the setup file.
* to compile the extension for use in the current directory, you can use `python setup.py build_ext --inplace`

<br>

----

### cythonize example

<br>

* for typing variables, consider the following snippet in python:

<br>

```python
def f(x):
    return x ** 2- x

def integrate_f(a, b, N):

    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)

    return s * dx
```

* compiling this in cython already gives a ~35% speedup, but adding static types can make it up to 4x faster.
* to accomplish this, you can add type declarations, for example:

```python
def f(x: cython.double):
    return x ** 2 - x

def integrate_f(a: cython.double, b: cython.double, N: cython.int):

    i: cython.int
    s: cython.double
    dx: cython.double
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)

    return s * dx
```

* this is converted to cython as pure C-style code:

```python
def f(double x):
    return x ** 2 - x

def integrate_f(double a, double b, int N):

    cdef int i
    cdef double s
    cdef double dx
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)

    return s * dx
```

* since python functions can be expensive, the cython specific `cdef` statement, as well as `@cfunc` decorator can be used:

```python
cdef double f(double x) except? -2:
    return x ** 2 -x
```

<br>

