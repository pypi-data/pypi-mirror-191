from importlib import metadata


def get_requirements(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


"""
cat pyproject.toml | grep version | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1

cat ./redis_lock/__init__.py | grep version | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | head -n 1

"""

import re

with open("redis_lock/__init__.py", "r") as f:
    r = re.findall(
        r"__version__ = \"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\"", f.read()
    )
    print(r)
    # pattern = re.compile(r"^__version__ = \"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\"")
    # for line in f.readlines():
    #     r = pattern.findall(line)
    #     if r:
    #         print(r[0])


"""
# Redis Lock with PubSub

Redis distributed lock implementation for Python base on Pub/Sub messaging.

## 1. Features

- Ensure atomicity by using SETNX operation
- Pub/Sub messaging system
- Force timeout to avoid infinite loops when trying to acquire lock

"""


"""
python -m build
python -m twine upload dist/*
"""