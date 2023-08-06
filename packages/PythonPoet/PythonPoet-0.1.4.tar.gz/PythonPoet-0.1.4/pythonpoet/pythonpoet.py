from pythonpoet.types import DeserializableType
from pythonpoet.types.class_ import Class, ClassBuilder


class PythonPoet(DeserializableType):
    """
    Main class for the PythonPoet. Builds the source code.
    """

    def __init__(self) -> None:
        self.classes: list[Class] = []

    def add_class(self, builder: ClassBuilder) -> "PythonPoet":
        """
        Adds new class to the PythonPoet.

        Parameters
        ----------
        builder : :class:`ClassBuilder`
            Class' builder.

        Raises
        ------
        ValueError
            If specified builder cannot be built.

        Returns
        -------
        :class:`PythonPoet`
            Updated PythonPoet's instance.
        """
        self.classes.append(builder.build())
        return self

    def get_imports(self) -> str:
        imports = ""
        for class_ in self.classes:
            imports += class_.get_imports()
        if len(imports) > 0:
            imports += "\n\n"
        return imports

    def deserialize(self) -> str:
        source_code = self.get_imports()
        for class_ in self.classes:
            source_code += class_.deserialize()
        return source_code
