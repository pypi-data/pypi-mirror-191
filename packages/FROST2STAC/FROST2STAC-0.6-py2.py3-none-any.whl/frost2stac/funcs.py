import json
from urllib.request import urlopen


def Things_url(url):
    if "/v1.0" not in url and "/v1.1" not in url:
        final_url = url + "/v1.1/Things"
    else:
        final_url = url + "/Things"
    return final_url


def FeaturesOfInterest_url(url):
    if "/v1.0" not in url and "/v1.1" not in url:
        final_url = url + "/v1.1/FeaturesOfInterest"
    else:
        final_url = url + "/FeaturesOfInterest"
    return final_url


def Observations_url(url):
    if "/v1.0" not in url and "/v1.1" not in url:
        final_url = url + "/v1.1/Observations"
    else:
        final_url = url + "/Observations"
    return final_url


def Datastreams_url(url):
    if "/v1.0" not in url and "/v1.1" not in url:
        final_url = url + "/v1.1/Datastreams"
    else:
        final_url = url + "/Datastreams"
    return final_url


def json_reader(url, additional):
    content = urlopen("".join((url + additional).split()))
    json_ = json.loads(content.read())

    return json_
