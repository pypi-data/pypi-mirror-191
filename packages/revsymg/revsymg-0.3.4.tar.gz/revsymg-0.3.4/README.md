# Reverse Symmetric Graph: a Python3 API to store succession relationships between DNA oriented fragments in an oriented graph

[![Latest release](https://gitlab.com/vepain/pyrevsymg/-/badges/release.svg)](https://gitlab.com/vepain/pyrevsymg/-/releases)
[![PyPI version](https://badge.fury.io/py/revsymg.svg)](https://badge.fury.io/py/revsymg)
[![Coverage report](https://gitlab.com/vepain/pyrevsymg/badges/master/coverage.svg)](https://gitlab.com/vepain/pyrevsymg/-/commits/master)
[![Pylint score](https://gitlab.com/vepain/pyrevsymg/-/jobs/artifacts/master/raw/pylint/pylint.svg?job=pylint)](https://gitlab.com/vepain/pyrevsymg/-/commits/master)
[![Mypy](https://gitlab.com/vepain/pyrevsymg/-/jobs/artifacts/master/raw/mypy/mypy.svg?job=mypy)](https://gitlab.com/vepain/pyrevsymg/-/commits/master)
[![Pipeline status](https://gitlab.com/vepain/pyrevsymg/badges/master/pipeline.svg)](https://gitlab.com/vepain/pyrevsymg/-/commits/master)


 <img src="https://gitlab.com/vepain/pyrevsymg/-/raw/master/docs/img/revsymg_logo_transp.png" alt="revsymg logo"
width="200" height="200">

`revsymg` is a Python3 API to store succession relationships between oriented fragments (in forward or reverse orientation) that have been sequenced from nucleotide sequence(s) in an oriented graph.
For example, this API can be used for a genome assembly overlap-layout-consensus method.


You can find the complete [documentation here](https://pyrevsymg.readthedocs.io)


## Quick installation

To install the `revsymg` package from the [PyPI repository](https://pypi.org/project/revsymg/), run the `pip` command :
```sh
pip install revsymg
```

You can find more installation details in the [docs/INSTALL.md](docs/INSTALL.md) file.


## Quick usage example

```python
from revsymg.graphs import RevSymGraph
from revsymg.lib import FORWARD_INT, REVERSE_INT


#
# Create an empty graph
#
graph = RevSymGraph()
vertices = graph.vertices()
edges = graph.edges()

#
# Add two vertices v and w that represents e.g. DNA fragments
#
frag_1_index = vertices.add()  # = 0
frag_2_index = vertices.add()  # = 1

#
# Add to the graph the overlap v reverse overlaps w forward
#
frag_1_r = (frag_1_index, REVERSE_INT)
frag_2_f = (frag_2_index, FORWARD_INT)
overlap_index = edges.add(frag_1_r, frag_2_f)  # = 0

for u, v, edge_index in edges:
    print(
        f'Predecessor:\t{u}\n'
        f'Successor:\t{v}\n'
        f'Edge index:\t{edge_index}\n',
    )
# The for-loop print this:
#
#   Predecessor:    (1, 1)
#   Successor:      (0, 0)
#   Edge index:     0
#
#   Predecessor:    (0, 1)
#   Successor:      (1, 0)
#   Edge index:     0
#
```


## Changelog

You can refer to the [docs/CHANGELOG.md](docs/CHANGELOG.md) file for details.


## What next?

Find a list of ideas in the [docs/TODO.md](docs/TODO.md) file.


## Contributing

* If you find any errors, missing documentation or test, or you want to discuss features you would like to have, please post an issue (with the corresponding predefined template) [here](https://gitlab.com/vepain/pyrevsymg/-/issues).
* If you want to help me code, please post an issue or contact me. You can find coding convention in the [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) file.


## References

* The implemented structure is described as **DGF** in this preprint:
    > 📰 Victor Epain, ‘Overlap Graph for Assembling and Scaffolding Algorithms: Paradigm Review and Implementation Proposals’, 2022, https://hal.inria.fr/hal-03815190
* Inspired by [graph-tool](https://graph-tool.skewed.de/)


## Licence

This work is licensed under a [GNU-GPLv3 licence](LICENCE).