import io
from typing import Any, List, Optional, Dict, Tuple

import drb
import numpy
import rasterio as rasterio
import xarray
from rasterio.io import MemoryFile

from drb.core import DrbNode
from drb.nodes.abstract_node import AbstractNode
from drb.exceptions.core import DrbNotImplementationException
from drb.core.factory import DrbFactory
from drb.core.path import ParsedPath
from drb.topics.resolver import resolve_children

from .simple_node import DrbImageSimpleValueNode, DrbImageNodesValueNames
from .list_node import DrbImageListNode
from drb.exceptions.image import DrbImageNodeException


class DrbImageBaseNode(AbstractNode):

    def __init__(self, base_node: DrbNode):
        super().__init__()

        self.base_node = base_node
        self._data_set = None
        self._data_set_file_source = None
        self._data_xarray = None
        self._children: List[DrbNode] = None

    def _get_rasterio_impl(self):
        return self._get_data_set()

    def _get_numpy_ndarray_impl(self):
        return self._get_data_set().read()

    def get_xarray_impl(self):
        return self._get_data_xarray()

    supported_impl = {
        rasterio.DatasetReader: _get_rasterio_impl,
        numpy.ndarray: _get_numpy_ndarray_impl,
        xarray.DataArray: get_xarray_impl
    }

    @property
    def parent(self) -> Optional[DrbNode]:
        return self.base_node.parent

    @property
    def path(self) -> ParsedPath:
        return self.base_node.path

    @property
    def name(self) -> str:
        return self.base_node.name

    @property
    def namespace_uri(self) -> Optional[str]:
        return self.base_node.namespace_uri

    @property
    def value(self) -> Optional[Any]:
        return self.base_node.value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self.base_node.attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return self.base_node.get_attribute(name, namespace_uri)

    def close(self):
        if self._data_set is not None:
            self._data_set.close()
        if self._data_set_file_source is not None:
            self._data_set_file_source.close()
        if self._data_xarray is not None:
            self._data_xarray.close()
        self.base_node.close()

    def _get_data_set(self) -> rasterio.DatasetReader:
        """
        Retrieve the data set of the image.

        Returns:
            rasterio.DatasetReader:  the data set of the image
        """
        if self._data_set is None:
            self._get_file_impl()
            self._memory_file = MemoryFile(
                file_or_bytes=self._data_set_file_source)
            self._data_set = self._memory_file.open()

        return self._data_set

    def _get_data_xarray(self) -> rasterio.DatasetReader:
        """
        Retrieve the data as Xarray of the image.

        Returns:
            rasterio.DatasetReader:  the data as Xarray of the image
        """
        if self._data_xarray is None:
            self._get_data_set()
            self._data_xarray = xarray.open_rasterio(
                self._data_set)
        return self._data_xarray

    def _get_file_impl(self):
        """
        retrieve the implementation of the file corresponding to his parent.
        """
        if self._data_set_file_source is None:
            if self.base_node.has_impl(io.BufferedIOBase):
                self._data_set_file_source = self.base_node \
                    .get_impl(io.BufferedIOBase)
            elif self.base_node.has_impl(io.BytesIO):
                self._data_set_file_source = self.base_node \
                    .get_impl(io.BytesIO)
            else:
                raise DrbImageNodeException(f'Unsupported parent '
                                            f'{type(self.parent).__name__} '
                                            f'for DrbImageNode')

    def _add_node_value(self, node_name, value):
        """
        Add a DrbImageSimpleValueNode node the list of children

        Parameters:
            node_name (str): The node name.
            value (any): the value corresponding to the name.
        """
        node_value = DrbImageSimpleValueNode(self, node_name, value)
        self._children.append(node_value)

    def _add_node_value_from_dict(self, node_name, dictionary, key):
        """
        Add a DrbImageSimpleValueNode node the list of children

        Parameters:
            node_name (str): The node name.
            dictionary (Dict): The dict containing the value.
            key (str): the key of the value.
        """
        if key in dictionary:
            value = dictionary[key]
        else:
            value = None
        self._add_node_value(node_name, value)

    def _add_values_from_dict(self, list_name, dictionary):
        """
        Add a DrbImageListNode node to the list of children

        Parameters:
            list_name (str): The name of the node.
            dictionary (Dict): The dict containing the value.
        """
        list_node = DrbImageListNode(self, list_name)
        for node_name, value in dictionary.items():
            node_value = DrbImageSimpleValueNode(list_node, node_name, value)
            list_node.append_child(node_value)

        self._children.append(list_node)

    @property
    @resolve_children
    def children(self) -> List[DrbNode]:
        """
        Initiate the list of children containing some metadata,
        and the data of the image.

        Returns:
            List[DrbNode]: The list of children
        """
        if self._children is None:
            self._children = []
            data_set = self._get_data_set()

            self._add_node_value_from_dict(DrbImageNodesValueNames.FORMAT
                                           .value, data_set.meta, 'driver')

            self._add_node_value(DrbImageNodesValueNames.WIDTH.value,
                                 data_set.width)
            self._add_node_value(DrbImageNodesValueNames.HEIGHT.value,
                                 data_set.height)
            self._add_node_value(DrbImageNodesValueNames.NUM_BANDS.value,
                                 data_set.count)
            self._add_node_value_from_dict(DrbImageNodesValueNames.TYPE.value,
                                           data_set.meta, 'dtype')
            self._add_node_value_from_dict(DrbImageNodesValueNames.CRS.value,
                                           data_set.meta, 'crs')

            if data_set.tags() is not None:
                self._add_values_from_dict(DrbImageNodesValueNames.TAGS.value,
                                           data_set.tags())
            if data_set.tags() is not None:
                self._add_values_from_dict(DrbImageNodesValueNames.META.value,
                                           data_set.meta)
        return self._children

    def has_impl(self, impl: type) -> bool:
        if self.base_node.has_impl(impl):
            return True
        return impl in self.supported_impl.keys()

    def get_impl(self, impl: type) -> Any:
        if self.base_node.has_impl(impl):
            return self.base_node.get_impl(impl)
        try:
            return self.supported_impl[impl](self)
        except KeyError:
            raise DrbNotImplementationException(
                f'no {impl} implementation found')


class DrbImageFactory(DrbFactory):

    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, DrbImageBaseNode):
            return node
        return DrbImageBaseNode(base_node=node)
