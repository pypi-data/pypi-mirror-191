import enum
from typing import List, Any, Dict, Tuple, Optional

from drb.core.node import DrbNode
from drb.nodes.abstract_node import AbstractNode
from drb.exceptions.core import DrbException, DrbNotImplementationException
from drb.core.path import ParsedPath


class DrbImageNodesValueNames(enum.Enum):
    """
    This enum  represent all metadata as heigth width ...
    """
    IMAGE = 'image'
    TAGS = 'tags'
    FORMAT = 'FormatName'
    WIDTH = 'width'
    HEIGHT = 'height'
    NUM_BANDS = 'NumBands'
    TYPE = 'Type'
    BOUNDARIES = 'Boundaries'
    CRS = 'crs'
    META = 'meta'


class DrbImageSimpleValueNode(AbstractNode):
    """
    This node is used to get simple value such as metadata
    an access the image data,
    usually the first child of the node.

    Parameters:
        parent (DrbNode): The node.
        name (str): the name of the data (usually
                    a value of DrbImageNodesValueNames)
        value (any): the value corresponding to the name.
    """

    def __init__(self, parent: DrbNode, name: str, value: any):
        super().__init__()
        self._name = name
        self._value = value
        self._parent: DrbNode = parent
        self._path = None

    @property
    def parent(self) -> Optional[DrbNode]:
        """
        Returns the parent of the node.

        Returns:
            DrbNode: the parent of the node
        """
        return self._parent

    @property
    def path(self) -> ParsedPath:
        """
        Returns the path of the node.

        Returns:
            ParsedPath: the full path of the node
        """
        if self._path is None:
            self._path = self.parent.path / self.name
        return self._path

    @property
    def name(self) -> str:
        """
        Return the name of the node.
        Usually the name is a value of the enum class DrbImageNodesValueNames.
        This name doesn't contain the path.

        Returns:
            str: the node name
        """
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        """
        Not use in this class.

        Returns:
            None
        """
        return None

    @property
    def value(self) -> Optional[Any]:
        """
        Return the value corresponding to the name of the node.

        Returns:
            Any: the value
        """
        return self._value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        """
        Not use in this class.

        Returns:
            Dict: an empty dict ({})
        """
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        """
        Not use in this class.

        Raise:
            DrbException
        """
        raise DrbException(f'No attribute {name} found')

    @property
    def children(self) -> List[DrbNode]:
        """
        Not use in this class.

        Returns:
            List: an empty dict ([])
        """
        return []

    def has_impl(self, impl: type) -> bool:
        """
        Not use in this class.

        Returns:
            bool: False
        """
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        """
        Not use in this class.

        Raise:
            DrbNotImplementationException
        """
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def close(self) -> None:
        """
        Not use in this class.
        Do nothing.
        """
        pass
