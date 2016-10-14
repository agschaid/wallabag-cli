"""
Settings and configuration for wallabag-api.
"""
import json
from collections import OrderedDict

CONFIG_FILENAME = ".wallabag-cli"


class Configs():
    """
    Static struct for storing the global configs.
    """

    # wallabag server
    serverurl = ""
    username = ""
    password = ""

    # wallabag api oauth2
    client = ""
    secret = ""


def set_config(name, value):
    if hasattr(Configs, name):
        setattr(Configs, name, value)


def get_config(name):
    return getattr(Configs, name, None)


def __configs2dictionary():
    """
    Converts the configuration values to a json serializable dictionary.

    Returns
    -------
    dictionary
        Dictionary with the configurations
    """

    wallabag_api = OrderedDict()
    wallabag_api_oauth2 = OrderedDict()

    wallabag_api['serverurl'] = Configs.serverurl
    wallabag_api['username'] = Configs.username
    wallabag_api['password'] = Configs.password
    wallabag_api_oauth2['client'] = Configs.client
    wallabag_api_oauth2['secret'] = Configs.secret
    wallabag_api["oauth2"] = wallabag_api_oauth2

    return {"wallabag_api": wallabag_api}


def __dicionary2config(configdict):
    for item in configdict:
        if type(item) is str:
            set_config(item, configdict[item])
        elif type(item) is dict:
            __dicionary2config(item)


def save(path=CONFIG_FILENAME):
    """
    Saves the config into a file.

    Parameters
    ----------
    path : string
        Optional non default config filename.

    Returns
    -------
    bool
        True if successful
    """
    file = open(path, mode='w')

    jsonsave = json.dumps(__configs2dictionary(), indent=4)
    file.write(jsonsave)

    file.close()
    return True


def load(path=CONFIG_FILENAME):
    """
    Loads the config into a dictionary.

    Parameters
    ----------
    path : string
        Optional non default config filename.

    Returns
    -------
    bool
        True if successfull. Otherwise the config will be filles with default values
    """
    file = open(path, mode='r')

    filecontent = file.read()
    file.close()
    dic = json.loads(filecontent)
    __dicionary2config(dic['wallabag_api'])
    return True

load()