import Dota2 as d2
import urllib.request as url
import time

emp = d2.DotaData("19838652") # YOUR STEAM ID / SOME FUNCTIONS WORK WITH COMMUNITY URL
error = True
reconnect_tries = 0
sleep_timer = 5
games_list = []
while error is True:
    try:
        for i in emp.list_results(5, 0): # EXAMPLE FUNCTION
            print(i)
        error = False
    except url.HTTPError: # RECONNECT IF HTTPError is thrown.
        reconnect_tries += 1
        print("HTTPError has occurred while downloading data xml data." +
              "\nTrying to reconnect.." + "(" + str(reconnect_tries) + ")"  "\n")
        time.sleep(sleep_timer)
