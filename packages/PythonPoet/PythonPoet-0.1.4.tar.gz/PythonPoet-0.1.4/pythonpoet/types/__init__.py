from typing import Any


class DeserializableType:
    """
    Represents types that can be deserialized.
    """

    def get_imports(self) -> str:
        """
        Returns type's imports required for deserialization.

        Returns
        -------
        str
            Type's imports.
        """
        raise NotImplementedError

    def deserialize(self) -> str:
        """
        Deserializes this type.

        Raises
        ------
        NotImplementedError
            If type hasn't overloaded this method.

        Returns
        -------
        str
            Deserialized (in source code) type.
        """
        raise NotImplementedError


class Builder:
    """
    Represents types' builders.
    """

    def build(self):  # TODO: return type
        """
        Builds this builder.

        Raises
        ------
        ValueError
            If one of the required fields is None.

        Returns
        -------
        T
            Built type's class instance.
        """
        raise NotImplementedError


class Argumentable:
    """
    Represents types that can have arguments.
    """

    def __init__(self) -> None:
        self.arguments: list[list[str, Any]] = []

    def add_argument(self, key: str, value: Any):  # TODO: return type
        """
        Adds a new argument to the list of arguments.

        Parameters
        ----------
        key : str
            Name of the argument.
        value : :class:`Any`
            Value of the argument.

        Examples
        --------
        .. code-block:: python3

            DecoratorBuilder()
            .set_name('secured')
            .add_argument('value', True)
            .build()
            # Result: @secured(value=True)


        Returns
        -------
        T
            Updated builder's class.
        """
        self.arguments.append([key, value])
        return self


class Documentable:
    """
    Represents types that can be documented.
    """

    def __init__(self) -> None:
        self.comments: list[str] = []

    def add_comment(self, comment: str):  # TODO: return type
        """
        Adds a new comment to the list of comments.

        Parameters
        ----------
        comment : str
            Comment to be added.

        Returns
        -------
        T
            Updated builder's class.
        """
        self.comments.append(comment)
        return self

    def add_newline(self):  # TODO: return type
        """
        Adds a newline (\n) to the list of comments.

        Returns
        -------
        T
            Updated builder's class.
        """
        return self.add_comment("\n")

    @staticmethod
    def generate_comments_source(comments: list[str], tabs: int = 1) -> str:
        """
        Generates source string from the list of the commands.

        Parameters
        ----------
        comments : list[str]
            List of comments to be generated.
        tabs : int, default: 1
            Amount of tabs to be added after comments.

        Returns
        -------
        str
            Generated comments source string.
        """
        if len(comments) > 0:
            quotes = '"""'

            generated_source_comments = ""
            for comment in comments:
                generated_source_comments += f"\t{comment}"

            tabs_code = "\t" * tabs
            return f"{tabs_code}{quotes}\n{generated_source_comments}\n{tabs_code}{quotes}\n"
        return ""
