import urllib.request as url
import xml.etree.ElementTree as et
import datetime


def download_xml(type):
    """

        :XML File: root of hero information xml
        Remember to change the account id.
        """
    steam_key = "22FC2DC99B506FC251EB44AFBB83EB7F"
    account_id = "19838652"
    chosen_url = ""

    web_data = url.urlopen("http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v1/"
                           "?language=en"
                           "&key=" + steam_key + ""
                                                 "&format=xml")

    web_data_2 = url.urlopen("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/"
                         "?key=" + steam_key + ""
                                               "&account_id=" + account_id + ""
                                                                             "&format=xml")

    if type is 1:
        chosen_url = web_data
    elif type is 2:
        chosen_url = web_data_2

    # object carrying xml text.
    str_data = chosen_url.read()
    # convert from string.
    str_into_xml = et.fromstring(str_data)
    return str_into_xml


def get_user_hero_id(account_id):
    """
    This functions returns a list containing the ID that the give account_id user, has played.
    It fills up after completing all for loops, otherwise it will only remember the first input hero_id
    """
    # MAGIC
    steam_xml_file = download_xml(2)
    #   steam_xml_parser = et.parse("mylog.xml")
    steam_xml_root = steam_xml_file
    steam_xml_matches = steam_xml_root.find('matches')
    user_match_data_list = []

    for match in steam_xml_matches:
        for match_info in match:
            for player in match_info:
                if player.find("account_id").text == account_id:
                    user_match_data_list.append(player.find('hero_id').text)
    return user_match_data_list


def get_hero_information(hero_id):
    """
    This function returns the hero in text. It is compared to the hero_id given by the list, user_match_data_list.
    From the function get_user_id()
    """
    # MAGIC
    steam_xml_file = download_xml(1)
    #   steam_xml_parser = et.parse("herolog.xml")

    steam_hero_root = steam_xml_file
    steam_heroes_root = steam_hero_root.find('heroes')

    hero_list = []

    for all_heroes in steam_heroes_root:
        if hero_id == all_heroes.find("id").text:
            hero_list.append(all_heroes.find("localized_name").text)
            #    print(hero_id)
            #    print(all_heroes.find("localized_name").text)

    for selected_hero in hero_list:
        return selected_hero


def get_match_data():
    """
    This function returns the match_id and time in timestamp.
    Converting of timestamp happens when outputting.
    """
    # MAGIC
    steam_xml_file = download_xml(2)
    #   steam_xml_parser = et.parse("mylog.xml")

    steam_xml_root = steam_xml_file
    steam_xml_matches = steam_xml_root.find('matches')
    match_data_list = []

    #   i am so good.
    for match in steam_xml_matches:
        for x in match.findall('match_id'):
            match_data_list.append(x.text)
            match_data_list.append(match.find('start_time').text)
    return match_data_list


def display_information(account_id):
    """
    This function is used to merely display data.
    """
    i = 0
    while i < 10:
        user_match_data_list = get_user_hero_id("19838652")
        for info in user_match_data_list:
            match_data = get_match_data()
            chosen_hero = get_hero_information(str(info))
            print("ACCOUNT_ID INFORMATION: " + account_id)
            print("MATCH ID: " + match_data[i] +
                  "\nTIME PLAYED: " + datetime.datetime.fromtimestamp(int(match_data[i+1])).strftime('%Y-%m-%d %H:%M:%S') +
                  "\nMATCH HERO: " + str(chosen_hero).upper() + "\n")
            i += 2
            # modulo of 2 represent each game -> (i = 4) is 2 games, (i = 6) is 3 games, (i = 8) is 4 games and so on.


display_information("19838652")







