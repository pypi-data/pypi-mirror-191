==================================================
README
==================================================

The goal of this project is to develop computational approaches to analyse the links and overlaps between environmental factors, their molecular targets, and rare diseases pathways.

The `ODAMNet documentation <https://odamnet.readthedocs.io/>`_ is available in ReadTheDocs. 

Installation 
----------------

From PyPi - *It's on going*
""""""""""""""""""""""""""""""""

ODAMNet is available as python package. You can easily install it using `pip`.

.. code-block:: bash

   pip install odamnet

From Conda - *It's on going*
""""""""""""""""""""""""""""""

You can also install it from `bioconda <https://bioconda.github.io/index.html>`_.

.. code-block:: bash

   conda install odamnet

From Github
"""""""""""""""""""""

1. Clone the repository from Github

.. code-block:: bash

   git clone https://github.com/MOohTus/ODAMNet.git

2. Then, install it

.. code-block:: bash

   pip install -e ODAMNet/

Usage
----------------

Three different approaches are available to analyse your data: 

- Overlap analysis
- Active Module Identification (using DOMINO)
- Random Walk with Restart (using multiXrank)

.. code-block:: bash

   odamnet [overlap|domino|multixrank|networkCreation] [ARGS]

Examples
----------------

Three approaches are implemented to study the relationships between Rare Diseases (from WikiPathways (WP)) and genes targeted by chemicals factors (extracted
from CTD database):

Overlap analysis
"""""""""""""""""""""

This method computes the overlap between target genes and Rare Disease pathways. It is looking for direct associations, i.e., target genes that are part of pathways.

.. code-block:: bash

   odamnet overlap ----chemicalsFile FILENAME

Active Module Identification
"""""""""""""""""""""""""""""""""

Target genes are defined as "active genes" to search for Active Modules (AM) on a molecular network (e.g.
Protein-Protein Interaction network, PPI). Then, an overlap analysis is performed between AM (containing target genes + linked genes)
and Rare Disease pathways.

.. code-block:: bash

   odamnet domino --chemicalsFile FILENAME --networkFile FILENAME

Random Walk with Restart
""""""""""""""""""""""""""""

Network and bipartite creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To perform a Random Walk with Restart through molecular multilayer and diseases network, you need to create a disease network
and link it to the multilayer (i.e. with the bipartite). This network will not have connection between diseases (i.e. disconnected network).
Diseases will be only connected with genes (in the multilayer) that are involved in disease pathways.

.. code-block:: bash

   odamnet networkCreation --networksPath PATH --bipartitePath PATH

multiXrank
^^^^^^^^^^^^^^^^^^

The third approach mesures the proximity of every nodes (g.e. genes, diseases) to the target genes within a multilayer network.
The walk starts from target genes and diffuses through the multilayer composed of different molecular interactions to the disease.

.. code-block:: bash

   odamnet multixrank --chemicalsFile FILENAME --configPath PATH --networksPath PATH --seedsFile FILENAME --sifFileName FILENAME
