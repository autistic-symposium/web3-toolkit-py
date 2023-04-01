## decorators

<br>

### `@dataclass`

go from:

```
class Person():
    def __init__(self, first_name, last_name, age, job):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.job = job
```

to:

```
from dataclasses import dataclass

@dataclass
class Person:
     first_name: str
     last_name: str
     age: int
     job: str
```
