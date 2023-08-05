from typing import Any, List, Dict, Optional, Tuple

import drb

from drb.core.node import DrbNode
from drb.nodes.abstract_node import AbstractNode
from drb.exceptions.core import DrbNotImplementationException, DrbException
from drb.core.path import ParsedPath
from drb.topics.resolver import resolve_children


class DrbImageListNode(AbstractNode):
    """
    This node is used to have one or many children of DrbNode but no value.
    Usually it will be a list of DrbImageSimpleValueNode.

    Parameters:
        parent (DrbNode): The node parent.
        name (str): the name of the data (usually a
                    value of DrbImageNodesValueNames)
    """
    def __init__(self, parent: DrbNode, name: str):
        super().__init__()

        self._name = name
        self._parent: DrbNode = parent
        self._children: List[DrbNode] = []
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
        Not use in this class.

        Returns:
            None
        """
        return None

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
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    @resolve_children
    def children(self) -> List[DrbNode]:
        """
        Return a list of DrbNode representing the children of this node.

        Returns:
            List[DrbNode]: The children of this node.
        """
        return self._children

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
        raise DrbNotImplementationException(f'no {impl} implementation found')

    def close(self) -> None:
        """
        Not use in this class.
        Do nothing.
        """
        pass

    def append_child(self, node: DrbNode) -> None:
        """
        Appends a DrbNode giving in argument to the list of children.

        Parameters:
            node (DrbNode): The node to add.
        """
        self._children.append(node)
