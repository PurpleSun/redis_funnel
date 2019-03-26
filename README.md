# redis-funnel

A distributed funnel middleware based on redis, management ui included.

## Installation

You can install `redis-funnel` simply with `pip`:

```
pip install redis-funnel
```

## Getting Started

Suppose you have a function named `dummy` runs across many processes, and executes very quickly:

```python
import time

def dummy():
    return time.time()

while True:
    print dummy()
```

you wants to restrict its execution speed with a limited qps, e.g. 100:

```python
import time
from redis_funnel.distributed import qps_factory

qps = qps_factory(host="localhost", port=6379, db=0)

@qps("1000001", "test", 100)
def dummy():
    return time.time()

while True:
    print dummy()
```

> Warning: a redis server should be started first and listening on localhost:6379.

Also, if function `dummy` just runs in a single process, then you can just use `qps` decorator based on local memory, in which case you don't need a redis server running first:

```python
import time
from redis_funnel.local import qps

@qps(100)
def dummy():
    return time.time()

while True:
    print dummy()
```

## Management UI

TBD

## Author

redis-funnel is developed and maintained by fanwei.zeng (stayblank@gmail.com). It can be found here:

https://github.com/PurpleSun/redis_funnel
