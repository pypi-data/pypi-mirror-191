import json
import os
from urllib.request import urlopen


def Things_url(url, version=None):
    """ This function serves as creating Things url"""
    if "/v1.0" not in url and "/v1.1" not in url:
        if version is not None:
            final_url = url + "/v" + version + "/Things"
        else:
            final_url = url + "/v1.1/Things"
    else:
        final_url = url + "/Things"
    return final_url


def FeaturesOfInterest_url(url, version=None):
    """ This function serves as creating FeaturesOfInterests url"""
    if "/v1.0" not in url and "/v1.1" not in url:
        if version is not None:
            final_url = url + "/v" + version + "/FeaturesOfInterest"
        else:
            final_url = url + "/v1.1/FeaturesOfInterest"
    else:
        final_url = url + "/FeaturesOfInterest"
    return final_url


def Observations_url(url, version=None):
    """ This function serves as creating Observations url"""
    if "/v1.0" not in url and "/v1.1" not in url:
        if version is not None:
            final_url = url + "/v" + version + "/Observations"
        else:
            final_url = url + "/v1.1/Observations"
    else:
        final_url = url + "/Observations"
    return final_url


def Datastreams_url(url, version=None):
    """ This function serves as creating Datastreams url"""
    if "/v1.0" not in url and "/v1.1" not in url:
        if version is not None:
            final_url = url + "/v" + version + "/Datastreams"
        else:
            final_url = url + "/v1.1/Datastreams"
    else:
        final_url = url + "/Datastreams"
    return final_url


def json_reader(url, additional):
    """ It reads json file and give back the content of json"""
    content = urlopen("".join((url + additional).split()))
    json_ = json.loads(content.read())

    return json_


def json_loader(dir, stac_cat_col_name):
    """ It reads json file and give back the path and content of json"""
    f = open(os.path.join(dir, stac_cat_col_name))
    path = os.path.join(dir, stac_cat_col_name)
    data = json.load(f)
    return path, data
