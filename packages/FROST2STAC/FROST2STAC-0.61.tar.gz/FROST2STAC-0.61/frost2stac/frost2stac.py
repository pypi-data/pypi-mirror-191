"""Main module."""
# import json
import os
from datetime import datetime

import pystac
import pytz

from . import constants, funcs

# from urllib.request import urlopen

# from tqdm import tqdm


# I should define a
class Converter(object):
    def __init__(
        self,
        main_url,  # SensorThingsAPI address
        stac=False,  # Permitting creation of STAC catalogs
        stac_dir=None,  # Directory saving of created STAC catalogs
        stac_id=None,  # STAC catalog ID
        stac_description=None,  # STAC catalog description
        datetime_filter=None,  # Filter harvesting dataset according to modified date in TDS
        stapi_version=None,
        stac_catalog_dynamic=False,  # Choosing STAC catalog type between Static and Dynamic
    ):
        # self.Things_id = []
        # self.Datastream_id = []
        # self.FeatureOfInterest_id = []
        self.Things_FeatureOfInterest_id = []
        self.phenomenonTime_data = []
        # https://sensorthings.imk-ifu.kit.edu/v1.1/Things?$select=@iot.id&$expand=Datastreams($select=@iot.id;$top=1;$expand=Observations($top=1;$select=@iot.id))
        # https://sensorthings.imk-ifu.kit.edu/v1.1/Observations(2758716)/FeatureOfInterest
        self.catalog = dict()  # Main STAC catalog
        # Things_resonse = urlopen(funcs.address_finder(main_url))
        # Things_json_data = json.loads(Things_resonse.read())
        if stapi_version is not None:
            self.stapi_version = stapi_version
        else:
            self.stapi_version = None
        self.id_detector(main_url)
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
            self.stac_creator(main_url)
            self.catalog[stac_id].normalize_hrefs(
                os.path.join(stac_dir, "stac")
            )
            self.catalog[stac_id].save(
                catalog_type=pystac.CatalogType.SELF_CONTAINED
            )
        # if stac is not None:

    def id_detector(self, url):
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

        # for i in tqdm(range(json_content["@iot.count"]),colour="red"):
        #     #self.Things_id.append(json_content["value"][i]["@iot.id"])
        #     datastream_response = urlopen(json_content["value"][i]["Datastreams@iot.navigationLink"])
        #     datastream_json_data = json.loads(datastream_response.read())

        #     for j in tqdm(range(datastream_json_data["@iot.count"]),colour="blue"):
        #         #self.Datastream_id.append(datastream_json_data["value"][j]["@iot.id"])
        #         observation_response = urlopen(datastream_json_data["value"][j]["Observations@iot.navigationLink"])
        #         observation_json_data = json.loads(observation_response.read())

        #         if observation_json_data["@iot.count"] != 0:

        #             FeatureOfInterest_response = urlopen(observation_json_data["value"][0]["FeatureOfInterest@iot.navigationLink"])
        #             FeatureOfInterest_json = json.loads(FeatureOfInterest_response.read())
        #             #self.FeatureOfInterest_id.append(FeatureOfInterest_json["@iot.id"])
        #             if self.stac is not False:
        #                 print("I have to add up collections and items creater")
