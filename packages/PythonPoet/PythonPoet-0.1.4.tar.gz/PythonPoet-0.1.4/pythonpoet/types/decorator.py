from typing import Any

from pythonpoet.types import Builder, DeserializableType, Argumentable
from pythonpoet.types.import_ import Import, ImportBuilder


class Decorator(DeserializableType):
    """
    Represents a decorator.

    .. warning::

        You shouldn't initialize this class via the `__init__`.
        Use :class:`DecoratorBuilder` instead.

    Attributes
    ----------
    name : str or None, default: None
        Decorator's class name.
    import_ : Import or None, default: None
        Decorator's import path.
    arguments : list[list[str, :class:`Any`]]
        Decorator's arguments.
    """

    def __init__(
        self, name: str, import_: Import | None, arguments: list[list[str, Any]]
    ) -> None:
        self.name = name
        self.import_ = import_
        self.arguments = arguments

    def get_imports(self) -> str:
        if self.import_ is None:
            return ""
        return self.import_.to_string()

    def deserialize(self) -> str:
        if self.arguments is None or len(self.arguments) == 0:
            return f"@{self.name}\n"
        else:
            arguments_source_code = ""
            for argument_pair in self.arguments:
                arguments_source_code += f"{argument_pair[0]}={argument_pair[1]},"

            return f"@{self.name}({arguments_source_code})\n"

    def __repr__(self) -> str:
        return f"<Decorator name={self.name}, import={self.import_}, arguments={self.arguments}>"

    def __str__(self) -> str:
        return self.__repr__()


class DecoratorBuilder(Builder, Argumentable):
    """
    Builder for the :class:`Decorator`.

    Attributes
    ----------
    name : str or None, default: None
        Decorator's class name.
    import_ : :class:`Import` or None, default: None
        Decorator's import path.
    """

    def __init__(self) -> None:
        super().__init__()
        self.name: str | None = None
        self.import_: Import | None = None

    def set_name(self, name: str) -> "DecoratorBuilder":
        """
        Sets a new decorator's class name.

        Parameters
        ----------
        name : str
            New decorator's class name.

        Returns
        -------
        :class:`DecoratorBuilder`
            Updated builder's instance.
        """
        self.name = name
        return self

    def set_import(self, import_: ImportBuilder) -> "DecoratorBuilder":
        """
        Sets a new decorator's import path.

        Parameters
        ----------
        import_ : ImportBuilder
            New decorator's import path.

        Returns
        -------
        :class:`DecoratorBuilder`
            Updated builder's instance.
        """
        self.import_ = import_.build()
        return self

    def build(self) -> Decorator:
        if self.name is None:
            raise ValueError("Decorator's class name cannot None.")

        return Decorator(self.name, self.import_, self.arguments)


class Decoratorable:
    """
    Represents type that can be decorated.

    Attributes
    ----------
    decorators : list[:class:`Decorator`]
        Type's decorators.
    """

    def __init__(self) -> None:
        self.decorators: list[Decorator] = []

    def add_decorator(self, builder: DecoratorBuilder):  # TODO: return type
        """
        Adds a new decorator to the type.

        Parameters
        ----------
        builder : :class:`DecoratorBuilder`
            Decorator's builder to be appended.

        Returns
        -------
        T
            Updated type's class instance.
        """
        self.decorators.append(builder.build())
        return self

    def get_decorators(self) -> list[Decorator]:
        """
        Get all applied decorators.

        Returns
        -------
        list[:class:`Decorator`]
            All applied decorators to this type's class instance.
        """
        return self.decorators
