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



A package to create STAC metadata catalog using The Fraunhofer Open-source SensorThings Server (Frost Server)


* Free software: EUPL-1.2
* Documentation: https://frost2stac.readthedocs.io.


Features
--------
Use case:


.. code:: python

        from frost2stac import frost2stac

        frost2stac.Converter(
                "https://sensorthings.imk-ifu.kit.edu/",
                stac=True,
                stac_id="an ID for the main STAC catalog",
                stac_dir="/path/to/save/stac/catalogs/",
                stac_description="Description for the main STAC catalog",
        )       

        output:

        Things ID:  65  - FeatureOfInterest ID: 27
        Things ID:  66  - FeatureOfInterest ID: 28
        Things ID:  67  - FeatureOfInterest ID: 30
        Things ID:  68  - FeatureOfInterest ID: 29
        Things ID:  69  - FeatureOfInterest ID: 33
        Things ID:  70  - FeatureOfInterest ID: 34
        Things ID:  71  - FeatureOfInterest ID: 35
        Things ID:  111  - FeatureOfInterest ID: 36
        Things ID:  112  - FeatureOfInterest ID: ❌
        [[65, 27], [66, 28], [67, 30], [68, 29], [69, 33], [70, 34], [71, 35], [111, 36]] 

Copyright
---------
Copyright © 2023 Karlsruher Institut für Technologie

Licensed under the EUPL-1.2-or-later

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the EUPL-1.2 license for more details.

You should have received a copy of the EUPL-1.2 license along with this
program. If not, see https://www.eupl.eu/.
