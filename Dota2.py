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

    def get_user_match_items(self, amount):
        """"
        This function returns a list of all item_id's per amount games.
        """
        item_ids = []
        amount = (amount*2)
        x = 0
        match_data = self.get_match_data()
        while True:
            steam_xml_file = download_xml(4, match_data[x])
            for players in steam_xml_file:
                for player in players:
                        find_my_id = str(player.find("account_id").text)
                        if find_my_id == str(self.account_id):
                            item_ids.append(player.find("item_0").text)
                            item_ids.append(player.find("item_1").text)
                            item_ids.append(player.find("item_2").text)
                            item_ids.append(player.find("item_3").text)
                            item_ids.append(player.find("item_4").text)
                            item_ids.append(player.find("item_5").text)
            x += 2
            if x is amount:
                break
        return item_ids

    def get_item_name(self, item_id):
        """
        This function returns the chosen item name -> compares it with item_id
        !!NEEDS WORK!!
        """
        self.pass_static()
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
            player_result = 1
        elif player_side == "Dire" and radiant_xml_result == "FALSE":
            player_result = 1
        else:
            player_result = 0
        return player_result

    def get_wins(self, amount):
        """
        This method returns the amount of wins per 10 games of the given account_id.
        To increase the amount of games checked increase amount_of_games in modulo of 2.
        """
        answer = 0
        i = 0
        amount = (amount*2)
        match_data = self.get_match_data()
        while i is not amount:
            result = self.get_match_result(match_data[i], self.account_id)
            if result == 1:
                answer += 1
            i += 2
        return answer

    def get_user_hero_id(self, amount):
        """
        This functions returns a list containing the ID of the hero that the given account_id user, has played.
        It fills up after completing all for loops, otherwise it will only remember the first input hero_id
        """
        # MAGIC
        steam_xml_file = download_xml(2, "")
        steam_xml_root = steam_xml_file
        steam_xml_matches = steam_xml_root.find('matches')
        user_match_data_list = []
        x = 0
        for match in steam_xml_matches:
            for match_info in match:
                for player in match_info:
                    if player.find("account_id").text == self.account_id:
                        user_match_data_list.append(player.find('hero_id').text)
            x += 1
            if x is amount:
                break
        return user_match_data_list

    def get_hero_information(self, hero_id):
        """
        This function returns the hero in text. It is compared to the hero_id given by the list, user_match_data_list.
        From the function get_user_id()
        """
        # MAGIC
        self.pass_static()
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

    def get_hero_amount(self, hero_id, amount):
        hero_found = 0
        x = 0
        hero_list = self.get_user_hero_id(amount)
        for heroes in hero_list:
            if int(heroes) is int(hero_id):
                hero_found += 1
        return hero_found

    def get_match_data(self):
        """
        This function returns the match_id and time in timestamp.
        Converting of timestamp happens when outputting.
        """
        # MAGIC
        steam_xml_file = download_xml(2, str(self.account_id))

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
        self.pass_static()
        steam_xml_file = download_xml(3, "")
        news_list = []

        for news_items in steam_xml_file:
            for news_item in news_items:
                news_list.append(news_item.find("title").text)
                news_list.append(news_item.find("url").text)
                news_list.append(news_item.find("contents").text)
        return news_list

    def last_game_time(self):
        match_data = self.get_match_data()
        time_converted = datetime.datetime.fromtimestamp(int(match_data[1])).strftime('%Y-%m-%d %H:%M:%S')
        return time_converted

    def get_last_games(self, amount):
        """
        This will be changed / removed.
        """
        i = 0
        amount = (amount*2)
        user_match_data_list = self.get_user_hero_id(self.account_id)
        match_data = self.get_match_data()
        list_games = []
        for info in user_match_data_list:
            match_result = self.get_match_result(match_data[i], self.account_id)
            chosen_hero = self.get_hero_information(str(info))
            list_games.append(str(chosen_hero))
            list_games.append(self.account_id)
            list_games.append(match_data[i])
            list_games.append(datetime.datetime.fromtimestamp(int(match_data[i + 1])).strftime('%Y-%m-%d %H:%M:%S'))
            list_games.append(match_result)
            i += 2
            # modulo of 2 represent each game -> (i = 4) is 2 games, (i = 6) is 3 games, (i = 8) is 4 games and so on.
            if i is amount:
                break
        return list_games

    def pass_static(self):
        pass
