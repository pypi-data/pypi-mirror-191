from pythonpoet.types import Builder


class Import:
    """
    Represents import.

    .. warning::

        You shouldn't initialize this class via the `__init__`. Use :class:`ImportBuilder` instead.

    Attributes
    ----------
    class_name : str
        Name of the class to be imported.
    module_name : str
        Path to the module to import from.
    """

    def __init__(self, class_name: str, module_name: str) -> None:
        self.class_name = class_name
        self.module_name = module_name

    def to_string(self) -> str:
        return f"from {self.module_name} import {self.class_name}\n"

    def __repr__(self) -> str:
        return f"<Import class_name={self.class_name}, module_name={self.module_name}>"

    def __str__(self) -> str:
        return self.__repr__()


class ImportBuilder(Builder):
    """
    Builder for the :class:`Import`.

    Attributes
    ----------
    class_name : str
        Name of the class to be imported.
    module_name : str
        Path to the module to import from.
    """

    def __init__(self) -> None:
        self.class_name: str | None = None
        self.module_name: str | None = None

    def set_class_name(self, class_name: str) -> "ImportBuilder":
        """
        Sets a new class' name for the import.

        Parameters
        ----------
        class_name : str
            New class' name.

        Returns
        -------
        :class:`ImportBuilder`
            Updated builder's instance.
        """
        self.class_name = class_name
        return self

    def set_module_name(self, module_name: str) -> "ImportBuilder":
        """
        Sets a new module's  name for the import.

        Parameters
        ----------
        module_name : str
            New module's name.

        Returns
        -------
        :class:`ImportBuilder`
            Updated builder's instance.
        """
        self.module_name = module_name
        return self

    def build(self) -> Import:
        if self.class_name is None:
            raise ValueError("Import's class name cannot be None.")
        elif self.module_name is None:
            raise ValueError("Import's module name cannot be None.")

        return Import(self.class_name, self.module_name)
