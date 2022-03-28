## Concurrency and Parallelism in Python

<br>

* [Read a detailed explanation on threads and multiprocessing in Python in my book](https://github.com/bt3gl-labs/Book-on-Python-and-Algorithms/blob/master/book/ebook_pdf/book_second_edition.pdf)

<br>

### Threading

* Threading is a feature usually provided by the operating system. 
* Threads are lighter than processes, and share the same memory space.
* With threading, concurrency is achieved using multiple threads, but due to the GIL only one thread can be running at a time.
* If your code is IO-heavy (like HTTP requests), then multithreading will still probably speed up your code.



### Multi-processing

* In multiprocessing, the original process is forked process into multiple child processes bypassing the GIL. 
* Each child process will have a copy of the entire program's memory.
* If your code is performing a CPU bound task, such as decompressing gzip files, using the threading module will result in a slower execution time. For CPU bound tasks and truly parallel execution, use the multiprocessing module.
* Higher memory overhead than threading.


### RQ: queueing jobs

* [RQ](https://python-rq.org/) is aimple but powerful library. 
* You first enqueue a function and its arguments using the library. This pickles the function call representation, which is then appended to a Redis list. 


### Celery: queueing jobs

* Celery is one of the most popular background job managers in the Python world. 
* Compatible with several message brokers like RabbitMQ or Redis and can act as both producer and consumer.
* Asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operations but supports scheduling as well. 

### concurrent.futures

* Using a concurrent.futures.ThreadPoolExecutor makes the Python threading example code almost identical to the multiprocessing module.
