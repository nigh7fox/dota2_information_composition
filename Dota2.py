""""
This is dota2. All dota2 related functions are in here.
"""
import datetime
from Download import download_xml as download_xml
import xml.etree.ElementTree as et
import time
import urllib.request as url


class DotaData(object):

    def __init__(self, account_id):
        self.account_id = account_id

    def get_account_id(self):
        return self.account_id

    def get_user_match_items(self, account_id):
        """"
        This function returns a list of all the account_id's, items_id's.
        !!FUNCTION NEEDS WORK!!
        """
        item_ids = []
        steam_xml_file = et.parse("hero_info.xml")
        steam_xml_root = steam_xml_file.getroot()
        for players in steam_xml_root:
            for player in players:
                    find_my_id = str(player.find("account_id").text)
                    if find_my_id == str(self.account_id):
                        item_ids.append(player.find("item_0").text)
                        item_ids.append(player.find("item_1").text)
                        item_ids.append(player.find("item_2").text)
                        item_ids.append(player.find("item_3").text)
                        item_ids.append(player.find("item_4").text)
                        return item_ids

    def get_item_name(self, item_id):
        """
        This function returns the chosen item name -> compares it with item_id
        !!NEEDS WORK!!
        """
        steam_xml_file = et.parse("item_info.xml")
        steam_xml_root = steam_xml_file.getroot()
        for items in steam_xml_root:
            for item in items:
                if item_id == str(item.find("id").text):
                    chosen_item = item.find("name").text
                    return chosen_item

    def convert_hero_items(self):
        """"
        This functions converts item id into item text and print's it.
        !!NEEDS WORK!!
        """
        list_user_item_ids = self.get_user_match_items(self.account_id)
        for x in list_user_item_ids:
            print(str(self.get_item_name(x)).upper())

    def get_match_result(self, match_id, account_id):
        """
        Returns the given match, matched with the given account_id's wins in text. -> "win" or "loss"
        """
        steam_xml_file = download_xml(4, match_id)
        radiant_xml_result = str(steam_xml_file.find("radiant_win").text).upper()
        player_side = ""

        for players in steam_xml_file:
            for player in players:
                xml_account_id = player.find("account_id").text
                if xml_account_id == self.account_id:
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

    def get_wins(self, account_id):
        """
        This method returns the amount of wins per 10 games of the given account_id.
        To increase the amount of games checked increase amount_of_games in modulo of 2.
        """
        answer = 0
        i = 0
        amount_of_games = 20
        match_data = self.get_match_data()
        while i is not amount_of_games:
            result = self.get_match_result(match_data[i], self.account_id)
            if result == "WIN":
                answer += 1
            i += 2
        return answer

    def get_user_hero_id(self, account_id):
        """
        This functions returns a list containing the ID of the hero that the given account_id user, has played.
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
                    if player.find("account_id").text == self.account_id:
                        user_match_data_list.append(player.find('hero_id').text)
        return user_match_data_list

    def get_hero_information(self, hero_id):
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

    def get_match_data(self):
        """
        This function returns the match_id and time in timestamp.
        Converting of timestamp happens when outputting.
        """
        # MAGIC
        steam_xml_file = download_xml(2, str(self.account_id))
        #   steam_xml_parser = et.parse("mylog.xml")

        steam_xml_root = steam_xml_file
        steam_xml_matches = steam_xml_root.find('matches')
        match_data_list = []

        #   i am so good.
        for match in steam_xml_matches:
            for m_id in match.findall('match_id'):
                match_data_list.append(m_id.text)
                match_data_list.append(match.find('start_time').text)
        return match_data_list

    def get_dota2_news(self):
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

    def display_dota2_news(self):
        """
        This function output's the news using the get_dota2_news list.
        This is function is optional.
        """
        wins_amount = self.get_wins(self.account_id)
        dota_news_list = self.get_dota2_news()
        wins_total = 10
        case_positive = "This user is on a winning streak he's won " + str(wins_amount) + " out of 10 games."
        case_negative = "This user is on a losing streak he's won " + str(wins_amount) + " out of 10 games."

        if wins_amount > (wins_total/2):
            case = case_positive
        else:
            case = case_negative

        print(case + "\n")
        print("Also.. Here's some dota2 news!\n")
        for news in dota_news_list:
            print(news)

    def display_information(self):
        """
        This function is used to merely display data.
        The first half of the current total output.
        This will be changed / removed.
        """
        i = 0
        user_match_data_list = self.get_user_hero_id(self.account_id)
        match_data = self.get_match_data()
        for info in user_match_data_list:
            match_result = self.get_match_result(match_data[i], self.account_id)
            chosen_hero = self.get_hero_information(str(info))
            print("ACCOUNT_ID INFORMATION: " + self.account_id)
            print("MATCH ID: " + match_data[i] +
                  "\nTIME PLAYED: " + datetime.datetime.fromtimestamp(int(match_data[i+1])).strftime('%Y-%m-%d %H:%M:%S') +
                  "\nMATCH HERO: " + str(chosen_hero).upper())
            print(match_result + "\n")
            i += 2
            # modulo of 2 represent each game -> (i = 4) is 2 games, (i = 6) is 3 games, (i = 8) is 4 games and so on.
            if i is 6:
                break

    def display_all_data(self):
        error = True
        first_part = True
        reconnect_tries = 0
        sleep_timer = 5
        while error is True:
            try:
                self.display_information()
                error = False
                while first_part is True:
                    try:
                        self.display_dota2_news()
                        first_part = False
                        break
                    except url.HTTPError:
                        reconnect_tries += 1
                        print("HTTPError has occurred while downloading data xml data." +
                              "\nTrying to reconnect.." + "(" + str(reconnect_tries) + ")"  "\n")
                        time.sleep(sleep_timer)
            except url.HTTPError:
                reconnect_tries += 1
                print("HTTPError has occurred while downloading data xml data." +
                      "\nTrying to reconnect.." + "(" + str(reconnect_tries) + ")"  "\n")
                time.sleep(sleep_timer)
            else:
                None
