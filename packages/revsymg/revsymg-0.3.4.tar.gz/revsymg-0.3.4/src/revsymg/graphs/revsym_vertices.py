# -*- coding=utf-8 -*-

"""Global vertices container class module."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, Iterable

from revsymg.exceptions import (
    NoVertexIndex,
    NoVerticesAttribute,
    WrongAttributeType,
    _NoAttribute,
    _NoKey,
)
from revsymg.graphs._adjancy_table import _AdjsT, _shift_rev_sym_adj_table
from revsymg.graphs.attributes import AttributesContainer
from revsymg.lib.index_lib import (
    FORWARD_INT,
    PRED_IND,
    REVERSE_INT,
    SUCC_IND,
    IndexT,
    IndOrT,
)


# ============================================================================ #
#                              VERTICES CONTAINER                              #
# ============================================================================ #
class Vertices():
    r"""Vertices container class for both vertices' orientations.

    For each raw read :math:`r \in \mathcal{R_{aw}}` there is one vertex for
    each orientation :math:`v \in V` and :math:`\bar{v} \in V`.

    Warnings
    --------
    You must not instantiate a Vertices object.
    Use it only for typing or get an already instanciated object.
    """

    # DOC: change read by something else

    def __init__(self, _adjs: _AdjsT):
        """The Initializer."""
        #
        # Adjacency tables
        #
        self._adjs: _AdjsT = _adjs
        #
        # Attributes for vertices
        #
        self._attributes: AttributesContainer = AttributesContainer()
        #
        # Number of forward vertices
        #
        self._card_vf: int = 0

    # -*- Attributes -*-

    def attr(self, vertex_index: IndexT, attrname: str) -> Any:
        """Return the value associated to `vertex` attribute `attrname`.

        Parameters
        ----------
        vertex_index : IndexT
            Vertex's index
        attrname : str
            Attribute name

        Returns
        -------
        Any
            Attribute value corresponding to the attribute name

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        NoVerticesAttribute
            If there is no attribute nammed like this for vertices
        """
        try:
            return self._attributes.get(vertex_index, attrname)
        except _NoAttribute as exc:
            raise NoVerticesAttribute(attrname) from exc
        except _NoKey as exc:
            raise NoVertexIndex(vertex_index) from exc

    def attrs(self, vertex_index: IndexT) -> Iterator[tuple[str, Any]]:
        """Iterate over all vertex's attributes.

        Parameters
        ----------
        vertex_index: IndexT
            Vertex's index

        Yields
        ------
        str
            Attribute's name
        Any
            Attribute's value

        Raises
        ------
        NoVertexIndex
            If there is no vertex index
        """
        try:
            yield from self._attributes.get_all(vertex_index)
        except _NoKey as _no_key:
            raise NoVertexIndex(vertex_index) from _no_key

    def new_attr(self, attrname: str, default: Any):
        """Add an attribute entry.

        Parameters
        ----------
        attrname : str
            Attribute's name
        default : Any
            Default attribute value

        Note
        ----
        Before setting attribute to one vertex, it is necessary to add
        an attribute entry using this method.
        """
        self._attributes.new_attr(attrname, default)

    def set_attr(self, vertex_index: IndexT, attrname: str, attrvalue: Any):
        """Change the value of the attributes else create them.

        Parameters
        ----------
        vertex_index : IndexT
            Vertex's index
        attrname : str
            Attribute's name
        attrvalue : Any
            Attribute's value

        Raises
        ------
        NoVerticesAttribute
            If there is no attribute nammed like this for vertices
        WrongAttributeType
            Given value does not correspond to attribute's type
        NoVertexIndex
            If there is no vertex index

        Note
        ----
        Be sure having added an attribute entry using the method
        :meth:`~revsymg.Vertices.new_attr`
        """
        try:
            self._attributes.set_attr(vertex_index, attrname, attrvalue)
        except _NoAttribute as _no_attr:
            raise NoVerticesAttribute(attrname) from _no_attr
        except WrongAttributeType as wrong_attr_type:
            raise wrong_attr_type
        except _NoKey as _no_key:
            raise NoVertexIndex(vertex_index) from _no_key

    # -*- Getter -*-

    def card_index(self) -> int:
        """Returns the number of distinct indices.

        Note
        ----

        The cardinality of indices set :math:`V_{ind}`
        is equal to :math:`|V_{ind}|`

        Returns
        -------
        int
            Number of distinct indices
        """
        return self._card_vf

    # -*- Setter -*-

    def add(self, number: int = 1) -> IndexT:
        """Add vertices to vertices container.

        Parameters
        ----------
        number : int, default 1
            Number of vertices to add

        Returns
        -------
        IndexT
            Last vertex's index (non-oriented)
        """
        self._adjs[PRED_IND].extend([[] for _ in range(number)])
        self._adjs[SUCC_IND].extend([[] for _ in range(number)])
        self._attributes.add_keys(number)
        self._card_vf += number
        return self._card_vf - 1

    def delete(self, vertex_index: IndexT):
        """Remove vertex from vertices container.

        Parameters
        ----------
        vertex_index : IndexT
            Vertex to delete

        Raises
        ------
        NoVertexIndex
            If vertex does not exist

        Warning
        -------
        This operation may invalidate vertex indices.
        In fact, deleting one vertex implies shifting all next indices.
        Because of this,
        keys should always be removed in decreasing index order:

        >>> for vertex in sorted(vertices_to_del, reverse=True):
        >>>     graph.vertices().delete(vertex)

        Note
        ----
        All next vertex indices are decreased in edges they belong.
        But concerned edges' indices are not.
        """
        #
        # Exceptions
        #
        if vertex_index >= self._card_vf:
            raise NoVertexIndex(vertex_index)
        # OPTIMIZE: just move the last one to index, update its index and pop
        #
        # Forward and reverse deletion
        #
        for index in range(vertex_index):
            for adj_ind in (PRED_IND, SUCC_IND):
                self._adjs[adj_ind][index] = list(
                    _shift_rev_sym_adj_table(
                        self._adjs[adj_ind][index],
                        vertex_index,
                    ),
                )
        #
        # Update next vertices indices
        #
        for index in range(vertex_index, self._card_vf - 1):
            for adj_ind in (PRED_IND, SUCC_IND):
                self._adjs[adj_ind][index] = list(
                    _shift_rev_sym_adj_table(
                        self._adjs[adj_ind][index + 1],
                        vertex_index,
                    ),
                )
        for adj_ind in (PRED_IND, SUCC_IND):
            self._adjs[adj_ind].pop()
        self._card_vf -= 1
        self._attributes.delete_key(vertex_index)

    def delete_several(self, vertex_indices: Iterable[IndexT]):
        """Remove vertices from vertices container.

        Parameters
        ----------
        vertex_indices : iterable of IndexT
            Vertices to delete

        Raises
        ------
        NoVertexIndex
            If one vertex does not exist

        Warning
        -------
        This operation may invalidate vertex indices.
        In fact, deleting one vertex implies shifting all next indices.

        Notes
        -----
        At the oposite of :meth:`~revsymg.Vertices.delete`
        method, it is not necessary to sort `vertex_indices`.
        This is done internally.

        All next vertex indices are decreased in edges they belong.
        But concerned edges' indices are not.
        """
        for vertex_index in sorted(vertex_indices, reverse=True):
            #
            # Exceptions
            #
            if vertex_index >= self._card_vf:
                raise NoVertexIndex(vertex_index)
            #
            # Forward and reverse deletion
            #
            for index in range(vertex_index):
                for adj_ind in (PRED_IND, SUCC_IND):
                    self._adjs[adj_ind][index] = list(
                        _shift_rev_sym_adj_table(
                            self._adjs[adj_ind][index],
                            vertex_index,
                        ),
                    )
            for index in range(vertex_index, self._card_vf - 1):
                for adj_ind in (PRED_IND, SUCC_IND):
                    self._adjs[adj_ind][index] = list(
                        _shift_rev_sym_adj_table(
                            self._adjs[adj_ind][index + 1],
                            vertex_index,
                        ),
                    )
            for adj_ind in (PRED_IND, SUCC_IND):
                self._adjs[adj_ind].pop()
            self._card_vf -= 1
            self._attributes.delete_key(vertex_index)

    # -*- Overloaded built-in -*-

    def __iter__(self) -> Iterator[IndOrT]:
        """Iterate on oriented vertices.

        Yields
        ------
        IndOrT
            Oriented vertices
        """
        for ind in range(self._card_vf):
            yield ind, FORWARD_INT
            yield ind, REVERSE_INT

    def __contains__(self, vertex_index: IndexT) -> bool:
        """Return True if vertex index is in container, else False.

        Parameters
        ----------
        vertex_index : IndexT
            Vertex index

        Returns
        -------
        bool
            True if oriented vertex is in container, else False
        """
        return vertex_index < self._card_vf

    def __len__(self) -> int:
        """Return the number of oriented vertices.

        Returns
        -------
        int
            Number of oriented vertices
        """
        return 2 * self._card_vf
