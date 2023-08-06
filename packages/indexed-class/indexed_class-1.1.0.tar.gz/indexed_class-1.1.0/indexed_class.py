from abc import ABCMeta
from typing import Any, Callable, Iterable, Optional, Type


class NoRootClassError(TypeError):
    def __init__(self, cls: type):
        super().__init__(f"no registry class defined as root in {cls.__name__}.mro()")


class NoMatchingSubclassError(KeyError):
    def __init__(self, key: str):
        super().__init__(f"no class registered at key '{key}'")


class SubclassValidationError(ValueError):
    def __init__(self, cls: type, value: Any):
        super().__init__(f"'{value}' is not a subclass of {cls.__name__}")


class IndexedClassMeta(type):
    __registry_class__ = dict

    @classmethod
    def __prepare__(
        meta,
        clsname: str,
        bases: Iterable[type],
        key: Optional[str] = None,
        root: bool = False,
        registry_class: Optional[Type[dict]] = None,
        **kwargs,
    ):
        output = super().__prepare__(clsname, bases, **kwargs)
        output["root"] = root
        output["key"] = key
        return output

    def __new__(
        meta,
        clsname: str,
        bases: Iterable[type],
        attrs: dict,
        key: Optional[str] = None,
        root: bool = False,
        registry_class: Optional[Type[dict]] = None,
        **kwargs,
    ):
        if registry_class:
            attrs["__registry_class__"] = registry_class
        cls = super().__new__(meta, clsname, bases, attrs, **kwargs)
        if root:
            cls.__registry__ = cls.__registry_class__()
            try:
                cls.__registry__.owner = cls
            except:
                pass
        if key is not None:
            if not hasattr(cls, "__registry__"):
                raise NoRootClassError(cls)
            cls.__registry__[key] = cls
        return cls

    def __init__(
        cls,
        clsname: str,
        bases: Iterable[type],
        attrs: dict,
        key: Optional[str] = None,
        root: bool = False,
        registry_class: Optional[Type[dict]] = None,
        **kwargs,
    ):
        super().__init__(clsname, bases, attrs, **kwargs)

    @property
    def keys(cls) -> Iterable[Any]:
        if not hasattr(cls, "__registry__"):
            raise NoRootClassError(cls)
        return cls.__registry__.keys()

    def __getitem__(cls, key: str):
        if not hasattr(cls, "__registry__"):
            raise NoRootClassError(cls)
        try:
            return cls.__registry__[key]
        except KeyError:
            raise NoMatchingSubclassError(key)

    def __setitem__(cls, key: str, target: type):
        if not hasattr(cls, "__registry__"):
            raise NoRootClassError(cls)
        if not isinstance(target, IndexedClassMeta) or cls not in target.mro():
            raise SubclassValidationError(cls, target)
        cls.__registry__[key] = target

    def __delitem__(cls, key: str):
        if not hasattr(cls, "__registry__"):
            raise NoRootClassError(cls)
        try:
            del cls.__registry__[key]
        except KeyError:
            raise NoMatchingSubclassError(key)


class AbstractIndexedClassMeta(IndexedClassMeta, ABCMeta):
    pass


class IndexedClass(metaclass=IndexedClassMeta):
    pass


class AbstractIndexedClass(metaclass=AbstractIndexedClassMeta):
    pass


class defaultregistry(dict):
    @classmethod
    def subclass_name_factory(cls, owner: IndexedClassMeta, key: Any) -> str:
        if isinstance(key, str):
            return f"{key.capitalize()}{owner.__name__}"
        if isinstance(key, type):
            return f"{key.__name__}{owner.__name__}"
        return f"{owner.__name__}{id(key)}"

    def __getitem__(self, key: Any):
        try:
            return super().__getitem__(key)
        except KeyError:
            self[key] = subclass = type(self.owner)(
                self.subclass_name_factory(self.owner, key),
                (self.owner,),
                {"key": key},
            )
            return subclass


class DefaultIndexedClass(IndexedClass, registry_class=defaultregistry):
    pass


class DefaultAbstractIndexedClass(AbstractIndexedClass, registry_class=defaultregistry):
    pass
