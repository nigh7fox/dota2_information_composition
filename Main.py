import Dota2 as d2
import urllib.request as url

# Catch HTMLErorr.
def display_data():
    try:
        d2.display_information("19838652")
        d2.display_dota2_news("19838652")
    except url.HTTPError:
        print("Error has occurred while downloading data xml data.")
    else:
        None

display_data()


