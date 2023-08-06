from typing import Any

from pythonpoet.types import DeserializableType, Argumentable, Builder, Documentable
from pythonpoet.types.decorator import Decoratorable
from pythonpoet.types.import_ import ImportBuilder, Import


def _generate_arguments(arguments: list[list[str, Any]]) -> str:
    arguments_source_code = ""
    for argument in arguments:
        arguments_source_code += f"{argument[0]}: {argument[1]}"
    return arguments_source_code


def _generate_method_header(
        method_name: str, arguments: list[list[str, Any]], return_type: str, is_async: bool
) -> str:
    if return_type is not None:
        method_header = (
            f"def {method_name}({_generate_arguments(arguments)}) -> {return_type}:\n"
        )
    else:
        method_header = f"def {method_name}({_generate_arguments(arguments)}):\n"

    if is_async:
        method_header = f"async {method_header}"

    return method_header


class Method(DeserializableType):
    """
    Representation of a class method.

    .. warning::

        You shouldn't initialize this class via the `__init__`. Use :class:`MethodBuilder` instead.

    Attributes
    ----------
    name : str
        Method's name.
    imports: list[:class:`Import`]
        Method's required imports.
    arguments: list[list[str, :class:`Any`]]
        Method's arguments.
    return_type : str or None
        Method's return type.
    source : str
        Method's source code.
    comments : list[str]
        Method's comments.
    is_async : bool
        Should this method be async?
    """

    def __init__(
            self,
            name: str,
            arguments: list[list[str, Any]],
            imports: list[Import],
            return_type: str | None,
            source: str,
            comments: list[str],
            is_async: bool,
    ) -> None:
        self.name = name
        self.imports = imports
        self.arguments = arguments
        self.return_type = return_type
        self.source = source
        self.comments = comments
        self.is_async = is_async

    def get_imports(self) -> str:
        imports_source_code = ""
        for import_ in self.imports:
            imports_source_code += import_.to_string()
        return imports_source_code

    def deserialize(self) -> str:
        return (
                _generate_method_header(
                    self.name, self.arguments, self.return_type, self.is_async
                )
                + Documentable.generate_comments_source(self.comments, 2)
                + "\t\t"
                + self.source
                + "\n"
        )

    def __repr__(self) -> str:
        return (
            f"<Method name={self.name}, arguments={self.arguments}, "
            f"return_type={self.return_type}, source={self.source}, comments={self.comments},"
            f"is_async={self.is_async}>"
        )

    def __str__(self) -> str:
        return self.__repr__()


class MethodBuilder(Builder, Argumentable, Decoratorable, Documentable):
    """
    Builder for the class :class:`Method`.

    Attributes
    ----------
    name : str
        Method's name.
    imports: list[:class:`Import`]
        Method's required imports.
    arguments: list[list[str, :class:`Any`]]
        Method's arguments.
    return_type : str or None
        Method's return type.
    source : str
        Method's source code.
    comments : list[str]
        Method's comments.
    is_async : bool
        Should this method be async?
    """

    def __init__(self) -> None:
        super(Builder, self).__init__()
        super(Argumentable, self).__init__()
        super(Decoratorable, self).__init__()
        super(Documentable, self).__init__()

        self.name: str | None = None
        self.imports: list[Import] = []
        self.return_type: str | None = None
        self.source: str = "pass"
        self.is_async: bool = False

    def set_name(self, name: str) -> "MethodBuilder":
        """
        Sets a new method's name.

        Parameters
        ----------
        name : str
            New method's name.

        Returns
        -------
        :class:`MethodBuilder`
            Updated builder's instance.
        """

        self.name = name
        return self

    def add_import(self, import_: Import) -> "MethodBuilder":
        """
        Adds a new method's import.

        Parameters
        ----------
        import_ : :class:`Import`
            Required method's import.

        Returns
        -------
        :class:`MethodBuilder`
            Updated builder's instance.
        """
        self.imports.append(import_)
        return self

    def set_return_type(
        self, return_type: type, import_: ImportBuilder = None
    ) -> "MethodBuilder":
        """
        Sets a new return type.

        Parameters
        ----------
        return_type : :class:`type`
            New method's return type.
        import_ : :class:`ImportBuilder`, optional, default: None
            Return's type import.

        Returns
        -------
        :class:`MethodBuilder`
            Updated builder's instance.
        """
        self.return_type = return_type.__name__
        if import_ is not None:
            self.imports.append(import_.build())
        return self

    # TODO: use an abstraction instead of using str.
    def set_source_code(self, source: str) -> "MethodBuilder":
        """
        Sets a new method's source code.

        Parameters
        ----------
        source : str
            New method's source code.

        Returns
        -------
        :class:`MethodBuilder`
            Updated builder's instance.
        """
        self.source = source
        return self

    def set_async(self, is_async: bool = True) -> "MethodBuilder":
        """
        Sets this method into an async mode.

        Parameters
        ----------
        is_async : bool, default: True
            Should this method be async?

        Returns
        -------
        :class:`MethodBuilder`
            Updated builder's instance.
        """

        self.is_async = is_async
        return self

    def build(self):
        if self.name is None:
            raise ValueError("Method's name cannot be None.")

        return Method(
            self.name,
            self.arguments,
            self.imports,
            self.return_type,
            self.source,
            self.comments,
            self.is_async,
        )
