import requests
import pandas as pd
import pyarrow


def get_rank(encryptedID, api_key):
    api_url = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + encryptedID + "?api_key=" + api_key
    resp = requests.get(api_url)
    try:
        player_info = resp.json()[0]
        return f"{player_info['tier']} {player_info['rank']}"
    except:
        return "UNRANKED"


def update_ranks(lstofdicts, api_key):
    for i in range(len(lstofdicts)):
        lstofdicts[i]['rank'] = get_rank(lstofdicts[i]['encrypted_id'], api_key)
    return lstofdicts
