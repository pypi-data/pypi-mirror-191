==========
FROST2STAC
==========


.. image:: https://codebase.helmholtz.cloud/cat4kit/frost2stac/-/raw/main/frost2stac.png





=============================

.. image:: https://img.shields.io/pypi/v/frost2stac.svg
        :target: https://pypi.python.org/pypi/frost2stac


.. image:: https://readthedocs.org/projects/frost2stac/badge/?version=latest
        :target: https://frost2stac.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


STAC specification is a method of exposing spatial and temporal data collections in a standardized manner. Specifically, the `SpatioTemporal Asset Catalog (STAC) <https://stacspec.org/en>`_ specification describes and catalogs spatiotemporal assets using a common structure. 
This package creates STAC metadata by harvesting time series data from the `Fraunhofer Open-source SensorThings Server (Frost Server) <https://www.iosb.fraunhofer.de/en/projects-and-products/frost-server.html>`_. After creating STAC Catalogs, Collections, and Items, it imports them into `pgSTAC <https://stac-utils.github.io/pgstac/pgstac/>`_ and `STAC-FastAPI <https://stac-utils.github.io/stac-fastapi/>`_.


* Free software: EUPL-1.2
* Documentation: https://frost2stac.readthedocs.io.


Quick start
-------------

To install FROST2STAC, run this command in your terminal:

.. code-block:: console

    pip install frost2stac

Or for installing manually, you can either clone the public repository:
.. code-block:: console

    git clone git://codebase.helmholtz.cloud/CAT4KIT/frost2stac
    cd frost2stac
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements_dev.txt

Use case:

You may use the package by following the `link <https://codebase.helmholtz.cloud/cat4kit/frost2stac/-/blob/main/docs/usage.rst>`_ instructions. . 





Copyright
---------
Copyright © 2023 Karlsruher Institut für Technologie

Licensed under the EUPL-1.2-or-later

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the EUPL-1.2 license for more details.

You should have received a copy of the EUPL-1.2 license along with this
program. If not, see https://www.eupl.eu/.
