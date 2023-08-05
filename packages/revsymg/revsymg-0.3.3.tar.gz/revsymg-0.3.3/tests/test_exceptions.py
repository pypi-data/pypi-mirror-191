# -*- coding=utf-8 -*-

"""Tests for exceptions."""

from revsymg.exceptions import (
    NoConnectedComponentId,
    NoEdge,
    NoEdgeIndex,
    NoEdgesAttribute,
    NoGraphAttribute,
    NoIndicesEdge,
    NoReadId,
    NotNoneCCompId,
    NoVertexIndex,
    NoVerticesAttribute,
    WrongAttributeType,
    _NoAttribute,
    _NoKey,
)


# ============================================================================ #
#                                TEST FUNCTIONS                                #
# ============================================================================ #
def test_nokey():
    """Test _NoKey exc."""
    assert (
        str(_NoKey(0))
        == 'There is no key `0` in attributes container.'
    )


def test_noattribute():
    """Test _NoAttribute exc."""
    assert (
        str(_NoAttribute('attr'))
        == 'There is no attribute nammed `attr` for the objects.'
    )


def test_nographattribute():
    """Test NoGraphAttribute exc."""
    assert (
        str(NoGraphAttribute('attr'))
        == 'There is no attribute nammed `attr` for the graph.'
    )


def test_noverticesattribute():
    """Test NoVerticesAttribute exc."""
    assert (
        str(NoVerticesAttribute('attr'))
        == 'There is no attribute nammed `attr` for the vertices.'
    )


def test_noedgesattribute():
    """Test NoEdgesAttribute exc."""
    assert (
        str(NoEdgesAttribute('attr'))
        == 'There is no attribute nammed `attr` for the edges.'
    )


def test_wrongattributetype():
    """Test WrongAttributeType exc."""
    assert (
        str(WrongAttributeType(45, str))
        == (
            '`45` is type `int`'
            ' while type `str` is expected.'
        )
    )


def test_novertexindex():
    """Test NoVertexIndex exc."""
    assert (
        str(NoVertexIndex(2))
        == '2 is not in the vertices container.'
    )


def test_noedgeindex():
    """Test NoEdgeIndex exc."""
    assert (
        str(NoEdgeIndex(42))
        == '`42` is not in the edge index.'
    )


def test_noedge():
    """Test NoEdge exc."""
    assert (
        str(NoEdge((2, 0), (45, 1), 8))
        == (
            'There is no edge `((2, 0), (45, 1))` with edge index'
            '`8` in the edges container.'
        )
    )


def test_noindicesedge():
    """Test NoIndicesEdge exc."""
    assert (
        str(NoIndicesEdge(2, 6, 8))
        == (
            'There is no edge `(2, 6)` with edge index'
            '`8` in the edges container.'
        )
    )


def test_noreadid():
    """Test NoReadId exc."""
    assert (
        str(NoReadId(0))
        == "There is no read's identifier `0` in container."
    )
    assert (
        str(NoReadId('id'))
        == "There is no read's identifier `id` in container."
    )


def test_noconnectedcomponentid():
    """Test NoConnectedComponentId exc."""
    assert (
        str(NoConnectedComponentId((0, 1)))
        == 'Vertex `(0, 1)` is not associated with any connected component.'
    )


def test_notnoneccompid():
    """Test NotNoneCCompId exc."""
    assert (
        str(NotNoneCCompId((4, 0), None, (5, 1), 5))
        == (
            'At least one of `(4, 0)` or `(5, 1)` has no connected'
            ' component identifier (= None), see:\n'
            '\t- cc id of `(4, 0)` = `None`\n'
            '\t- cc id of `(5, 1)` = `5`'
        )
    )
