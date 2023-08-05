# -*- coding=utf-8 -*-

"""Split strands vertices container class module."""

from __future__ import annotations

from typing import Any, Iterable, Iterator

from bitarray import bitarray

from revsymg.exceptions import (
    NoVertexIndex,
    NoVerticesAttribute,
    WrongAttributeType,
    _NoAttribute,
    _NoKey,
)
from revsymg.graphs._adjancy_table import _AdjsIndT, _shift_indices_adj_table
from revsymg.graphs.attributes import AttributesContainer
from revsymg.lib.index_lib import (
    IND,
    OR,
    PRED_IND,
    SUCC_IND,
    IndexT,
    IndOrT,
    OrT,
)


# DOC: do doc for SplitStrandsVertices
# ============================================================================ #
#                     REVERSE SYMMETRIC VERTICES CONTAINER                     #
# ============================================================================ #
class SplitStrandsVertices():
    r"""Unique oriented vertices container.

    This vertices container is containing only one orientation for each of its
    vertex *i.e.* :math:`\forall v \in V, \bar{v} \notin V`

    Warnings
    --------
    You must not call this class.
    Use it only for typing or get an already existing object.
    """

    def __init__(self, _adjs: _AdjsIndT, _cc: bitarray):
        """Initializer."""
        # Adjancy tables ---
        self._adjs: _AdjsIndT = _adjs
        # Describe the vertices' orientation
        #   [v_ind]: FORWARD_INT | REVERSE_INT
        self._cc: bitarray = _cc
        # Attributes for vertices
        self._attributes: AttributesContainer = AttributesContainer()

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

    # -*- Orientation -*-

    def contains_indor(self, vertex: IndOrT) -> bool:
        """Answer if oriented vertex in vertices container.

        Parameters
        ----------
        vertex : IndOrT
            Oriented vertex

        Returns
        -------
        bool
            Oriented vertex in vertices container
        """
        if vertex[IND] < len(self._cc):
            return vertex[OR] == self._cc[vertex[IND]]
        return False

    def orientation(self, vertex_index: IndexT) -> OrT:
        """Return the orientation of vertex's index.

        Parameters
        ----------
        vertex_index : IndexT
            Vertex's index

        Returns
        -------
        OrT
            Vertex's index orientation

        Raises
        ------
        NoVertexIndex
            If there is no vertex index
        """
        try:
            return self._cc[vertex_index]  # type: ignore
        except IndexError as index_err:
            raise NoVertexIndex(vertex_index) from index_err

    # -*- Getter -*-

    def cc_record(self) -> bitarray:
        """Getter for connected component record.

        Returns
        -------
        bitarray
            For each index store the orientation which is in the arbitrarly
            choosen connected component

        Warnings
        --------
        You should not use this method, use instead:
        ```python
        >>> vertex in vertices
        ```

        :meta private:
        """
        # XXX: necessary?
        return self._cc

    # -*- Setter -*-

    def add(self, orientation: OrT) -> IndexT:
        """Add the vertex to the connected component record.

        Parameters
        ----------
        orientation : OrT
            New orientation to add to vertices container

        Returns
        -------
        IndexT
            Last vertex's index
        """
        self._cc.append(orientation)
        self._adjs[PRED_IND].append([])
        self._adjs[SUCC_IND].append([])
        return len(self._cc) - 1

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
        But concerning edge indices are not.
        """
        #
        # Exceptions
        #
        if vertex_index >= len(self._cc):
            raise NoVertexIndex(vertex_index)
        #
        # Forward and reverse deletion
        #
        for index in range(vertex_index):
            for adj_ind in (PRED_IND, SUCC_IND):
                self._adjs[adj_ind][index] = list(
                    _shift_indices_adj_table(
                        self._adjs[adj_ind][index],
                        vertex_index,
                    ),
                )
        for index in range(vertex_index, len(self._cc) - 1):
            for adj_ind in (PRED_IND, SUCC_IND):
                self._adjs[adj_ind][index] = list(
                    _shift_indices_adj_table(
                        self._adjs[adj_ind][index + 1],
                        vertex_index,
                    ),
                )
        for adj_ind in (PRED_IND, SUCC_IND):
            self._adjs[adj_ind].pop()
        self._cc = self._cc[:vertex_index] + self._cc[vertex_index + 1:]
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
        At the oposite of :meth:`~revsymg.SplitStrandsVertices.delete`
        method, it is not necessary to sort `vertex_indices`.
        This is done internally.

        All next vertex indices are decreased in edges they belong.
        But concerning edge indices are not.
        """
        for vertex_index in sorted(vertex_indices, reverse=True):
            #
            # Exceptions
            #
            if vertex_index >= len(self._cc):
                raise NoVertexIndex(vertex_index)
            #
            # Forward and reverse deletion
            #
            for index in range(vertex_index):
                for adj_ind in (PRED_IND, SUCC_IND):
                    self._adjs[adj_ind][index] = list(
                        _shift_indices_adj_table(
                            self._adjs[adj_ind][index],
                            vertex_index,
                        ),
                    )
            for index in range(vertex_index, len(self._cc) - 1):
                for adj_ind in (PRED_IND, SUCC_IND):
                    self._adjs[adj_ind][index] = list(
                        _shift_indices_adj_table(
                            self._adjs[adj_ind][index + 1],
                            vertex_index,
                        ),
                    )
            for adj_ind in (PRED_IND, SUCC_IND):
                self._adjs[adj_ind].pop()
            self._cc = self._cc[:vertex_index] + self._cc[vertex_index + 1:]
            self._attributes.delete_key(vertex_index)

    # -*- Overloaded built-in -*-

    def __iter__(self) -> Iterator[IndexT]:
        """Iterate on oriented vertices.

        Yields
        ------
        IndexT
            Vertices
        """
        yield from range(len(self._cc))

    def __contains__(self, vertex: IndexT) -> bool:
        """Answer if vertex is in vertices container.

        Returns
        -------
        bool
            Vertex is in vertices container
        """
        return vertex < len(self._cc)

    def __len__(self) -> int:
        """Return the number of oriented vertices.

        Returns
        -------
        int
            Number of orient
        """
        return len(self._cc)
