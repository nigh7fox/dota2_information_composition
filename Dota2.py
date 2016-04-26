""""
This is dota2. All dota2 related functions are in here.
"""
import datetime
from Download import download_xml as download_xml
import xml.etree.ElementTree as et


def get_user_match_items(match_id, account_id):
    """"
    This function returns a list of all the account_id's, items_id's.
    """
    item_ids = []
    steam_xml_file = et.parse("hero_info.xml")
    steam_xml_root = steam_xml_file.getroot()
    for players in steam_xml_root:
        for player in players:
                find_my_id = str(player.find("account_id").text)
                if find_my_id == str(account_id):
                    item_ids.append(player.find("item_0").text)
                    item_ids.append(player.find("item_1").text)
                    item_ids.append(player.find("item_2").text)
                    item_ids.append(player.find("item_3").text)
                    item_ids.append(player.find("item_4").text)
                    return item_ids


def get_item_name(item_id):
    """
    This function returns the chosen item name -> compares it with item_id
    """
    steam_xml_file = et.parse("item_info")
    steam_xml_root = steam_xml_file.getroot()
    for items in steam_xml_root:
        for item in items:
            if item_id == str(item.find("id").text):
                chosen_item = item.find("name").text
                return chosen_item


def convert_hero_items():
    """"
    This functions converts item id into item text and print's it.
    """
    list_user_item_ids = get_user_match_items("2310565859", "19838652")
    for x in list_user_item_ids:
        print(str(get_item_name(x)).upper())


def get_match_result(match_id, account_id):
    """
    Returns the given match, matched with the given account_id's wins in text. -> "win" or "loss"
    """
    steam_xml_file = download_xml(4, match_id)
    radiant_xml_result = str(steam_xml_file.find("radiant_win").text).upper()
    player_side = ""
    player_result = ""

    for players in steam_xml_file:
        for player in players:
            xml_account_id = player.find("account_id").text
            if xml_account_id == account_id:
                player_slot = player.find("player_slot").text
                if int(player_slot) < 5:
                    player_side = "Radiant"
                else:
                    player_side = "Dire"

    if player_side == "Radiant" and radiant_xml_result == "TRUE":
        player_result = str("win").upper()
    elif player_side == "Dire" and radiant_xml_result == "FALSE":
        player_result = str("win").upper()
    else:
        player_result = str("loss").upper()
    return player_result


def get_wins(account_id):
    """
    This method returns the amount of wins per 10 games of the given account_id.
    To increase the amount of games checked increase amount_of_games in modulo of 2.
    """
    answer = 0
    i = 0
    amount_of_games = 20
    match_data = get_match_data()
    while i is not amount_of_games:
        result = get_match_result(match_data[i], account_id)
        if result == "WIN":
            answer += 1
        else:
            None
        i += 2
    return answer


def get_user_hero_id(account_id):
    """
    This functions returns a list containing the ID that the give account_id user, has played.
    It fills up after completing all for loops, otherwise it will only remember the first input hero_id
    """
    # MAGIC
    steam_xml_file = download_xml(2, "")
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
    steam_xml_file = download_xml(1, "")
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
    steam_xml_file = download_xml(2, "")
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
    steam_xml_file = download_xml(3, "")
    news_list = []

    for news_items in steam_xml_file:
        for news_item in news_items:
            news_list.append(news_item.find("title").text)
            news_list.append(news_item.find("url").text)
            news_list.append(news_item.find("contents").text)
    return news_list


def display_dota2_news(account_id):
    """
    This function output's the news using the get_dota2_news list.
    This is function is optional.
    """
    case_positive = "This user is on a winning streak he's won " + get_wins(account_id) + " out of 10 games."
    case_negative = "This user is on a losing streak he's won " + get_wins(account_id) + " out of 10 games."

    if get_wins(account_id) > 5:
        case = case_positive
    else:
        case = case_negative

    print(case)
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
              "\nMATCH HERO: " + str(chosen_hero).upper())
        print(get_match_result(match_data[i], account_id) + "\n")
        i += 2
        # modulo of 2 represent each game -> (i = 4) is 2 games, (i = 6) is 3 games, (i = 8) is 4 games and so on.
        if i is 6:
            break



