# -*- coding=utf-8 -*-

"""Exceptions classes module."""

from __future__ import annotations

from typing import Any, Optional

from revsymg.lib.index_lib import IndexT, IndOrT
from revsymg.lib.str_lib import IdT


# ============================================================================ #
#                             ATTRIBUTES EXCEPTIONS                            #
# ============================================================================ #
class _NoKey(Exception):
    """NoKey class."""

    def __init__(self, key: IndexT):
        super().__init__()
        self.__key = key

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return f'There is no key `{self.__key}` in attributes container.'


# ---------------------------------------------------------------------------- #
#                              Vertices And Edges                              #
# ---------------------------------------------------------------------------- #
class _NoAttribute(Exception):
    """NoAttribute class."""

    _object_name: str = 'objects'

    def __init__(self, attrname: str):
        super().__init__()
        self.__attrname = attrname

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            f'There is no attribute nammed `{self.__attrname}` for the'
            f' {self._object_name}.'
        )


class NoGraphAttribute(_NoAttribute):
    """NoGraphAttribute class for graph object."""

    _object_name: str = 'graph'


class NoVerticesAttribute(_NoAttribute):
    """NoVerticesAttribute class for vertices container."""

    _object_name: str = 'vertices'


class NoEdgesAttribute(_NoAttribute):
    """NoEdgesAttribute class for edges container."""

    _object_name: str = 'edges'


# ---------------------------------------------------------------------------- #
#                             Vertex And Edge Keys                             #
# ---------------------------------------------------------------------------- #
class WrongAttributeType(Exception):
    """WrongAttributeType class."""

    def __init__(self, attrvalue: Any, attrtype: type):
        """The Initializer."""
        super().__init__()
        self.__attrvalue = attrvalue
        self.__attrtype = attrtype

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            f'`{self.__attrvalue}` is type `{type(self.__attrvalue).__name__}`'
            f' while type `{self.__attrtype.__name__}` is expected.'
        )


# ============================================================================ #
#                                   VERTICES                                   #
# ============================================================================ #
class NoVertexIndex(Exception):
    """Vertex does not exist."""

    def __init__(self, vertex_index: IndexT):
        """The Initializer."""
        super().__init__()
        self.__vertex_index = vertex_index

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return f'{self.__vertex_index} is not in the vertices container.'


# ============================================================================ #
#                                     EDGES                                    #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                  Edges Index                                 #
# ---------------------------------------------------------------------------- #
class NoEdgeIndex(Exception):
    """Exception class for NoEdgeIndex error."""

    def __init__(self, edge_index: IndexT):
        """The Initializer."""
        super().__init__()
        self.__edge_index = edge_index

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return f'`{self.__edge_index}` is not in the edge index.'


# ---------------------------------------------------------------------------- #
#                                  RevSymEdges                                 #
# ---------------------------------------------------------------------------- #
class NoEdge(Exception):
    """Exception class for NoEdge error."""

    def __init__(self, first_vertex: IndOrT, second_vertex: IndOrT,
                 edge_index: IndexT):
        """The Initializer."""
        super().__init__()
        self.__edge = (first_vertex, second_vertex)
        self.__edge_index = edge_index

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            f'There is no edge `{self.__edge}` with edge index'
            f'`{self.__edge_index}` in the edges container.'
        )


# ---------------------------------------------------------------------------- #
#                                 IndicesEdges                                 #
# ---------------------------------------------------------------------------- #
class NoIndicesEdge(Exception):
    """Exception class for NoIndicesEdge error."""

    def __init__(self, first_vertex: IndexT, second_vertex: IndexT,
                 edge_index: IndexT):
        """The Initializer."""
        super().__init__()
        self.__edge = (first_vertex, second_vertex)
        self.__edge_index = edge_index

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            f'There is no edge `{self.__edge}` with edge index'
            f'`{self.__edge_index}` in the edges container.'
        )


# ============================================================================ #
#                               READS IDENTIFIERS                              #
# ============================================================================ #
class NoReadId(Exception):
    """No read's identifier exception class."""

    def __init__(self, read_id: IdT):
        """The Initializer."""
        super().__init__()
        self.__read_id = read_id

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return f"There is no read's identifier `{self.__read_id}` in container."


# ============================================================================ #
#                             CONNECTED COMPONENTS                             #
# ============================================================================ #
class NoConnectedComponentId(Exception):
    """Exception for vertex with no connected component identifier."""

    def __init__(self, vertex: IndOrT):
        """The Initializer."""
        super().__init__()
        self.__vertex = vertex

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            f'Vertex `{self.__vertex}` is not associated'
            ' with any connected component.'
        )


class NotNoneCCompId(Exception):
    """The NotNoneCCompId class."""

    def __init__(self, v: IndOrT, v_cc: Optional[int],
                 v_rev: IndOrT, v_rev_cc: Optional[int]):
        """The Initializer."""
        super().__init__()
        self.__v = v
        self.__v_cc = v_cc
        self.__v_rev = v_rev
        self.__v_rev_cc = v_rev_cc

    def __str__(self) -> str:
        """Print the exception message.

        Returns
        -------
        str
            Exception message
        """
        return (
            f'At least one of `{self.__v}` or `{self.__v_rev}` has no connected'
            f' component identifier (= None), see:\n'
            f'\t- cc id of `{self.__v}` = `{self.__v_cc}`\n'
            f'\t- cc id of `{self.__v_rev}` = `{self.__v_rev_cc}`'
        )
