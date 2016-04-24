import urllib.request as url
import xml.etree.ElementTree as et

"""
This functions is used to download the xml files, which we recieve as text and then convert into xml again.
This function hence returns a xml root file.
"""


def download_xml(tipo):

    steam_key = "22FC2DC99B506FC251EB44AFBB83EB7F"
    account_id = "19838652"
    chosen_url = ""

    #   URL FOR HEROES XML
    web_data = url.urlopen("http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1/"
                           "?language=en"
                           "&key=" + steam_key + ""
                                                 "&format=xml")

    #   URL FOR MATCH HISTORY XML
    web_data_2 = url.urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/"
                             "?key=" + steam_key + ""
                             "&account_id=" + account_id + ""
                             "&format=xml")

    web_data_3 = url.urlopen("http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/"
                             "?appid=570&count=3"
                             "&maxlength=300"
                             "&format=xml")

    if tipo is 1:
        chosen_url = web_data
    elif tipo is 2:
        chosen_url = web_data_2
    elif tipo is 3:
        chosen_url = web_data_3

    # object carrying xml text.
    str_data = chosen_url.read()
    # convert from string.
    str_into_xml = et.fromstring(str_data)
    return str_into_xml

