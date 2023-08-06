"""Main module."""

import os
from datetime import datetime

import pystac
import pytz
from pypgstac.db import PgstacDB
from pypgstac.load import Loader, Methods

from . import config_pgstac, constants, funcs


class Converter(object):
    def __init__(
        self,
        main_url,  # SensorThingsAPI address
        stac=False,  # Permitting creation of STAC catalogs
        stac_dir=None,  # Directory saving of created STAC catalogs
        stac_id=None,  # STAC catalog ID
        stac_description=None,  # STAC catalog description
        stapi_version=None, #Choosing SensorThingsAPI version between 1.0 and 1.1
        stac_catalog_dynamic=False,  # Choosing STAC catalog type between Static and Dynamic
    ):


        self.Things_FeatureOfInterest_id = []
        self.phenomenonTime_data = []


        self.catalog = dict()  # Main STAC catalog


        if stapi_version is not None:
            self.stapi_version = stapi_version
        else:
            self.stapi_version = None
        
        #A function for harvesting the data
        self.id_detector(main_url)
        #Just for showing the summary in Terminal
        self.datetime_catch(main_url)

        self.stac = stac
        self.stac_id = stac_id

        if stac is True:
            """In this part STAC catalogs will be created"""

            # Main STAC catalog for linking other items and collections
            self.catalog[stac_id] = pystac.Catalog(
                id=stac_id,
                description=stac_description
                + "[Link to SensorThingsAPI]("
                + funcs.Things_url(main_url, version=self.stapi_version)
                + ")",
            )
            # Running the function for creating STAC Catalog, Collections , and Items
            self.stac_creator(main_url)
            # Saving Catalog in the local store
            self.catalog[stac_id].normalize_hrefs(
                os.path.join(stac_dir, "stac")
            )
            self.catalog[stac_id].save(
                catalog_type=pystac.CatalogType.SELF_CONTAINED
            )
        
        if stac_catalog_dynamic is True:
            """In this part STAC catalogs ingests into pgSTAC and STACFastAPI"""
            config_pgstac.run_all()  # This enables the confiduration of pgSTAC
            # First of all catalog should be opened
            catalog_json_path, catalog_json_data = funcs.json_loader(
                stac_dir, "stac/catalog.json"
            )
            # pgSTAC database will be loaded here
            loader = Loader(db=PgstacDB(dsn=""))
            # Each collection and item that are linked to the catalog through 'links' is extracted.
            for dc in catalog_json_data["links"]:
                if dc["rel"] == "item":
                    try:
                        loader.load_items(
                            str(
                                os.path.join(
                                    stac_dir,
                                    "stac/" + dc["href"].replace("./", ""),
                                )
                            ),
                            Methods.insert,
                        )
                    except:
                        continue
                    print("|____", dc["href"])
                # 'child' means Collection in Catalog json file
                if dc["rel"] == "child":
                    self.dynamic_ingester(
                        loader,
                        dc["href"],
                        stac_dir,
                        "stac/" + dc["href"].replace("./", ""),
                    )

    def dynamic_ingester(self, loaderx, param, stac_dirx, address_coll):
        """This is a function for ingesting collections
        into pgSTAC specifically for nested datasets"""
        collection_josn_path, collection_josn_data = funcs.json_loader(
            stac_dirx, address_coll
        )

        item_collection_list = [
            ci["rel"] for ci in collection_josn_data["links"]
        ]

        if (
            "child" in item_collection_list
        ):  # To ensure collection exists in 'links'
            item_collection_list = []  # Considered empty to prevent recursion

            for ci in collection_josn_data["links"]:
                if ci["rel"] == "child":
                    try:
                        self.dynamic_ingester(
                            loaderx,
                            ci["href"],
                            stac_dirx,
                            collection_josn_path.replace(
                                "collection.json", "/"
                            )
                            + ci["href"].replace("./", ""),
                        )
                    except:
                        continue
        else:
            item_collection_list = []  # Considered empty to prevent recursion
            loaderx.load_collections(
                str(os.path.join(stac_dirx, collection_josn_path)),
                Methods.insert,
            )
            print(param)
            for ci in collection_josn_data["links"]:
                if ci["rel"] == "item":
                    try:
                        loaderx.load_items(
                            str(
                                os.path.join(
                                    stac_dirx,
                                    collection_josn_path.replace(
                                        "collection.json", "/"
                                    )
                                    + ci["href"].replace("./", ""),
                                )
                            ),
                            Methods.insert,
                        )
                        print("|____", ci["href"])
                    except:
                        continue

    def id_detector(self, url):
        """ A function for harvesting Frost server time series data. 
        Things are considered STAC Items and FeatureOfInterests acts 
        as STAC Collections"""
        observation_json = funcs.json_reader(
            funcs.Things_url(url, version=self.stapi_version),
            constants.featureofinterest_id,
        )
        for thing in range(observation_json["@iot.count"]):
            if observation_json["value"][thing]["Datastreams"]:
                if observation_json["value"][thing]["Datastreams"][0][
                    "Observations"
                ]:
                    featureofinterest_json = funcs.json_reader(
                        funcs.Observations_url(url, self.stapi_version),
                        "("
                        + str(
                            observation_json["value"][thing]["Datastreams"][0][
                                "Observations"
                            ][0]["@iot.id"]
                        )
                        + ")/FeatureOfInterest",
                    )
                else:
                    datastream_json = funcs.json_reader(
                        funcs.Things_url(url, self.stapi_version),
                        "("
                        + str(observation_json["value"][thing]["@iot.id"])
                        + ")/Datastreams"
                        + constants.featureofinterest_id_empty,
                    )
                    for datastream in range(datastream_json["@iot.count"]):
                        if datastream_json["value"][datastream][
                            "Observations"
                        ]:
                            featureofinterest_json = funcs.json_reader(
                                funcs.Observations_url(
                                    url, self.stapi_version
                                ),
                                "("
                                + str(
                                    datastream_json["value"][datastream][
                                        "Observations"
                                    ][0]["@iot.id"]
                                )
                                + ")/FeatureOfInterest",
                            )
                print(
                    "Things ID: ",
                    observation_json["value"][thing]["@iot.id"],
                    " < - > FeatureOfInterest ID:",
                    featureofinterest_json["@iot.id"],
                )
                self.Things_FeatureOfInterest_id.append(
                    [
                        observation_json["value"][thing]["@iot.id"],
                        featureofinterest_json["@iot.id"],
                    ]
                )
            else:
                featureofinterest_json["@iot.id"] = "❌"
                print(
                    "Things ID: ",
                    observation_json["value"][thing]["@iot.id"],
                    " < - > FeatureOfInterest ID:",
                    featureofinterest_json["@iot.id"],
                )

    def datetime_catch(self, url):
        """ This function catchs `phenomenonTime` from
        Datastreams """
        phenomenonTime_json = funcs.json_reader(
            funcs.Things_url(url, self.stapi_version),
            constants.phenomenonTime_string,
        )
        for i in range(phenomenonTime_json["@iot.count"]):
            self.phenomenonTime_data = []

            for j in range(
                phenomenonTime_json["value"][i]["Datastreams@iot.count"]
            ):
                if (
                    "phenomenonTime"
                    in phenomenonTime_json["value"][i]["Datastreams"][j]
                ):
                    if (
                        "/"
                        in phenomenonTime_json["value"][i]["Datastreams"][j][
                            "phenomenonTime"
                        ]
                    ):
                        replaced1, replaced2 = phenomenonTime_json["value"][i][
                            "Datastreams"
                        ][j]["phenomenonTime"].split("/")
                        self.phenomenonTime_data.append(
                            datetime.strptime(
                                replaced1, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc)
                        )
                        self.phenomenonTime_data.append(
                            datetime.strptime(
                                replaced2, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=pytz.utc)
                        )
            for k in self.Things_FeatureOfInterest_id:
                if k[0] == phenomenonTime_json["value"][i]["@iot.id"]:
                    k.append(self.phenomenonTime_data)

    def stac_creator(self, url):
        """ A function for creating STAC Collections and Items"""
        # creation of collection
        for i in self.Things_FeatureOfInterest_id:
            thing_json = funcs.json_reader(
                funcs.Things_url(url, self.stapi_version),
                "(" + str(i[0]) + ")",
            )
            featureofinterest_json = funcs.json_reader(
                funcs.FeaturesOfInterest_url(url, self.stapi_version),
                "(" + str(i[1]) + ")",
            )

            collection_bbox = [
                featureofinterest_json["feature"]["coordinates"][0]
                - constants.epilon,
                featureofinterest_json["feature"]["coordinates"][1]
                - constants.epilon,
                featureofinterest_json["feature"]["coordinates"][0]
                + constants.epilon,
                featureofinterest_json["feature"]["coordinates"][1]
                + constants.epilon,
            ]

            collection_interval_time = sorted(i[2])

            collection_interval_final_time = [
                collection_interval_time[0],
                collection_interval_time[-1],
            ]
            spatial_extent = pystac.SpatialExtent(bboxes=[collection_bbox])
            temporal_extent = pystac.TemporalExtent(
                intervals=[collection_interval_final_time]
            )
            self.catalog[featureofinterest_json["name"]] = pystac.Collection(
                id=featureofinterest_json["name"],
                extent=pystac.Extent(
                    spatial=spatial_extent, temporal=temporal_extent
                ),
                description=thing_json["name"],
            )

            item = pystac.Item(
                id=thing_json["name"],
                geometry=featureofinterest_json["feature"],
                bbox=featureofinterest_json["feature"]["coordinates"],
                datetime=collection_interval_time[0],
                properties={},
            )

            # self.catalog[featureofinterest_json["name"]].extent = pystac.Extent(
            #     spatial=spatial_extent, temporal=temporal_extent
            # )
            item.add_asset(
                key=thing_json["name"],
                asset=pystac.Asset(
                    href=featureofinterest_json[
                        "Observations@iot.navigationLink"
                    ],
                    # title=without_slash,
                    media_type=pystac.MediaType.GEOJSON,
                ),
            )

            self.catalog[featureofinterest_json["name"]].add_item(item)
            self.catalog[self.stac_id].add_child(
                self.catalog[featureofinterest_json["name"]]
            )

