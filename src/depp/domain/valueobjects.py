from typing import List, Any


class ValueObject:
    def __repr__(self) -> str:
        return "<{}: {}>".format(self.__class__.__name__, self)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return str(self) == str(other)
        else:
            return False

    def __hash__(self) -> int:
        return hash(str(self))


class Module(ValueObject):
    """
    A Python module.
    """
    def __init__(self, name: str) -> None:
        """
        Args:
            name: The fully qualified name of a Python module, e.g. 'package.foo.bar'.
        """
        self.name = name

    def __str__(self) -> str:
        return self.name

    def package_name(self) -> str:
        return self.name.split('.')[0]


class SafeFilenameModule(Module):
    """
    A Python module whose filename can be known safely, without importing the code.
    """
    def __init__(self, name: str, filename: str) -> None:
        """
        Args:
            name: The fully qualified name of a Python module, e.g. 'package.foo.bar'.
            filename: The full filename and path to the Python file,
            e.g. '/path/to/package/one.py'.
        """
        self.filename = filename
        super().__init__(name)

    def __repr__(self) -> str:
        return "<{}: {} ({})>".format(self.__class__.__name__, self.name, self.filename)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.name, self.filename))

    def as_module(self) -> Module:
        """
        Casts as a Module rather than as a SafeFilenameModule.
        """
        return Module(name=self.name)


class DirectImport(ValueObject):
    """
    An import between one module and another.
    """
    def __init__(self, importer: Module, imported: Module) -> None:
        self.importer = importer
        self.imported = imported

    def __str__(self) -> str:
        return "{} <- {}".format(self.importer, self.imported)


class ImportPath(ValueObject):
    """
    A flow of imports between two modules, from upstream to downstream.
    """
    def __init__(self, *modules: List[Module]) -> None:
        self.modules = modules

    def __str__(self) -> str:
        return ' <- '.join(
            reversed([str(m) for m in self.modules])
        )
