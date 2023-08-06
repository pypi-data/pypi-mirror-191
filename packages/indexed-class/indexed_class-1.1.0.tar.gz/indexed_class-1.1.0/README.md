# INDEXED CLASS

## Maintainer: aachn3 <n45t31@protonmail.com>
## Site: <https://gitlab.com/pyutil/indexed_class>
## Version: 1.1.0

### About

This package provides some metaclasses/class hierarchy roots capable of storing and
retrieving subclasses using arbitrary keys and registry types.

### Table of Contents

- [structure](#project-structure)
- [usage](#usage)
  - [examples](#code-samples)
- [support](#support)
  - [requirements](#prerequisites)
  - [installation](#installation)
- [tests](#testing-package-functionality)
  - [unit](#unit-tests)
  - [integration](#integration-tests)
  

### Project Structure

```
-NoRootClassError(TypeError)
-NoMatchingSubclassError(KeyError)
-SubclassValidationError(ValueError)
-defaultregistry(dict)
-IndexedClassMeta(type)
 -keys
 -operator[]
-IndexedClass(meta=IndexedClassMeta)
-DefaultIndexedClass(IndexedClass)
-AbstractIndexedClassMeta(IndexedClassMeta, ABCMeta)
-AbstractIndexedClass(meta=AbstractIndexedClassMeta)
-DefaultAbstractIndexedClass(AbstractIndexedClass)
```

### Usage

(Abstract)IndexedClassMeta exposes following parameters:
- key (optional, any type): the key under which the class is to be stored in the registry; 
  if the `__registry__` attribute is not defined anywhere in parent  hierarchy, a NoRootClassError 
  is raised
- root (optional, boolean): if set to True, the class defines a `__registry__` attribute as a new 
  instance of the ``@registry`_class` parameter
- registry\_class (optional, type exposing `__getitem__`, `__delitem__` and `__setitem__`): class
  used to initialise empty `__registry__` in root classes, defaults to `super().__registry_class__`,
  sets `__registry_class__`

Methods exposed by classes derived from (Abstract)IndexedClassMeta:
- keys (property): returns a set of all keys defined in `__registry__`; if this attribute is not
  defined anywhere in parent hierarchy, a NoRootClassError is raised; by default uses 
  `.__registry__.keys()` - override if your `registry_class` does not implement `keys()` method
- \_\_getitem\_\_(key): returns a class stored in `__registry__` under `@key`; if the `__registry__`
  attribute is not defined anywhere in parent hierarchy, a NoRootClassError is raised; if `@key` is
  not found in `__registry__`, a NoMatchingSubclassError is raised
- \_\_setitem\_\_(key, value): stores `@value` under `@key` in `__registry__`; if the `__registry__`
  attribute is not defined anywhere in parent hierarchy, a NoRootClassError is raised; if `@value`
  is not a valid subclass of calling class, a SubclassValidationError is raised
- \_\_delitem\_\_(key): deletes `@key` from `__registry__`; if the `__registry__` attribute is not
  defined anywhere in parent hierarchy, a NoRootClassError is raised; if `@key` is not found in
  `__registry__`, a NoMatchingSubclassError is raised

#### Code samples

Basic usecase

```python3
from indexed_class import AbstractIndexedClass, NoMatchingSubclassError
from abc import abstractmethod

import json
import pickle

class FileParser(AbstractIndexedClass, root=True):
    def __init__(self, filename: str):
        self.filename = filename

    @abstractmethod
    def fetch_content(self)->dict:
        raise NotImplementedError("abstract method requires override")

class JsonFileParser(FileParser, key="json"):
    def fetch_content(self)->dict:
        with open(self.filename, "r") as content:
            return json.load(content)

class PickleFileParser(FileParser, key="pickle"):
    def fetch_content(self)->dict:
        with open(self.filename, "rb") as content:
            return pickle.load(content)

### MAIN ###

# example settings:
#   filename: /some/path/data.json
#   filetype: json
with open("settings.json", "r") as file:
    settings = json.load(file)

try:
    data = FileParser[settings["filetype"]](settings["filename"]).fetch_content()
except NoMatchingSubclassError:
    data = None
...
```

#### Support

##### Prerequisites
- python >= 3.8.0

##### Installation
`pip3 install `

#### Testing package functionality

##### Unit tests

Format: pytest

##### Integration tests

Format: None
