=====
Usage
=====

Overview
-------------

To use FROST2STAC in a project::

    import frost2stac
    from frost2stac import frost2stac

    frost2stac.Converter(
            main_url="https://sensorthings.imk-ifu.kit.edu/",
            stac=True,
            stac_id="an ID for the main STAC catalog",
            stac_dir="/path/to/save/stac/catalogs/",
            stapi_version="1.1" or "1.0",
            stac_description="Description for the main STAC catalog",
            stac_catalog_dynamic=True,
    )


Output::

    Things ID:  65  - FeatureOfInterest ID: 27
    Things ID:  66  - FeatureOfInterest ID: 28
    Things ID:  67  - FeatureOfInterest ID: 30
    Things ID:  68  - FeatureOfInterest ID: 29
    Things ID:  69  - FeatureOfInterest ID: 33
    Things ID:  70  - FeatureOfInterest ID: 34
    Things ID:  71  - FeatureOfInterest ID: 35
    Things ID:  111  - FeatureOfInterest ID: 36
    Things ID:  112  - FeatureOfInterest ID: ❌



main_url
----------------
The `main_url` for harvesting from Frost Server's SensorThingsAPI is provided. It is important to note that in FROST2STAC, Things are treated as STAC Items and FeatureOfInterests acts as a STAC Collection.
It's a string type url.


stac
----------------
The boolean feature `stac` is used to permit creation of STAC Catalog, Collections, and Items.


stac_id
----------------
This feature is used to name STAC catalog ID.


stac_dir
----------------
The Directory for saving created STAC Catalogs, Collections, and Items


stapi_version
----------------
There are two options for the string type feature `stapi_version`: "1.0" and "1.1". 
Otherwise, SensorThingsAPI version 1.1 is used by FROST2STAC.


stac_description
------------------
This option is used to add STAC Catalog description.


stac_catalog_dynamic
-----------------------
The `stac_catalog_dynamic` option enables us to choose between the Static and Dynamic STAC Catalog types.

