## Notes on optimization in Python

<br>

### Peephole optimization

* optimization technique done at the compile time to improve code performance
* code is optimized behind the scenes and it's done either by pre-calculating constant expressions or using membership tests
* turn mutable constructs into immutable constructes
* turn both set and lists into constants

<br>

### Intern strings

* string objects in Python are sequences of Unicode characters, called text sequences
* when characters of different sizes are added to a string, its total size and weight increase, but not only by the size of the added character. Python also allocates extra information to store strings, which causes them to take up too much space.
* The idea behund string interning is to cache certain strings in memory as they are created, which has lot in common with shared objects. For instance, CPython loads shared objects into memory every time a Python interactive session is initialized.

<br>

### Profiling code

* use timeit
* use cProfile: advanced profiling, generates reports


<br>

### Use generators and keys for soring
 
- Generators dont' return ites such as iterators, but only one item at time.


<br>

### Use "C" equivalent of some Python libs

* they are the same features but with faster performance. Example: instead of Pickle, use cPickle, etc.
* Use PyPy package and Cytjon to optimiza a static compiler.


<br>


### Avoid using  Globals

* Ugh for spaghetti code...
* Or make a local copy before using them inside loops.


<br>

### Use technology stacks

* redis for cache
* rabbitmq or celert for job queues and exports








