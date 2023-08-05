# -*- coding=utf-8 -*-

"""Library for overlaps graph objects."""

from __future__ import annotations

from typing import Union

from revsymg.graphs.merged_strands_graph import MergedStrandsRevSymGraph
from revsymg.graphs.revsym_graph import RevSymGraph
from revsymg.graphs.split_strands_graph import SplitStrandsGraph


# from revsymg.graphs.view.sub_graph import SubRevSymGraph


# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
GraphsT = Union[
    RevSymGraph,
    # SubRevSymGraph,
    MergedStrandsRevSymGraph,
    SplitStrandsGraph,
]
GraphsCnntedCompT = Union[
    SplitStrandsGraph,
    MergedStrandsRevSymGraph,
]
