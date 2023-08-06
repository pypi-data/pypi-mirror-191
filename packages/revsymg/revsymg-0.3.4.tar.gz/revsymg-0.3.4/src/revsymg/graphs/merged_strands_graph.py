# -*- coding=utf-8 -*-

"""Merged strands overlaps graph class module."""

from __future__ import annotations

from revsymg.graphs.revsym_graph import RevSymGraph


# DOC: do doc for MergedStrandsRevSymGraph
# ============================================================================ #
#                         MERGED STRANDS OVERLAPS GRAPH                        #
# ============================================================================ #
MergedStrandsRevSymGraph = RevSymGraph
r"""Weakly connected overlaps graph containing a merge of DNA strands.

This graph :math:`G = (V, E)` contains only one weakly connected component where
there are the two DNA strands.
Thus:

- :math:`\forall v \in V, \bar{v} \in V`
- :math:`\forall e \in E, \bar{e} \in E`
"""
