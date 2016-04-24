""""
This is dota2. All dota2 related functions are in here.
"""
import datetime
from Download import download_xml as download_xml
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


def get_dota2_news():
    """
    This function downloads the xml file and adds the chosen items into a list.
    It then returns this list with current dota2 news.
    """
    steam_xml_file = download_xml(3)
    news_list = []

    for news_items in steam_xml_file:
        for news_item in news_items:
            news_list.append(news_item.find("title").text)
            news_list.append(news_item.find("url").text)
            news_list.append(news_item.find("contents").text)
    return news_list


def display_dota2_news():
    """
    This function output's the news using the get_dota2_news list.
    This is function is optional.
    """
    print("Also.. Here's some dota2 news!\n")
    for news in get_dota2_news():
        print(news)


def display_information(account_id):
    """
    This function is used to merely display data.
    """
    i = 0
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
        if i is 6:
            break