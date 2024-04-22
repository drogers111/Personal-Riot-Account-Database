import requests
import pandas as pd
import pyarrow


# gets the puuid, given a summoner name and region
def get_puuid(summoner_name, region, api_key):
    api_url = (
            "https://" +
            region +
            ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
            summoner_name +
            "?api_key=" +
            api_key
    )

    print(api_url)

    resp = requests.get(api_url)
    player_info = resp.json()
    puuid = player_info['puuid']
    return puuid

def get_match_ids(puuid, mass_region, api_key):
    api_url = (
            "https://" +
            mass_region +
            ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
            puuid +
            "/ids?start=0&count=20" +
            "&api_key=" +
            api_key
    )
    resp = requests.get(api_url)
    match_ids = resp.json()
    return match_ids


def get_match_data(match_id, mass_region, api_key):
    api_url = (
            "https://" +
            mass_region +
            ".api.riotgames.com/lol/match/v5/matches/" +
            match_id +
            "?api_key=" +
            api_key
    )

    resp = requests.get(api_url)
    match_data = resp.json()
    return match_data

def find_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    player_data = match_data['info']['participants'][player_index]
    return player_data

def gather_all_data(puuid, match_ids, mass_region, api_key):
    # We initialise an empty dictionary to store data for each game
    data = {
        'champion': [],
        'kills': [],
        'deaths': [],
        'assists': [],
        'win': []
    }

    for match_id in match_ids:
        print(match_id)

        # run the two functions to get the player data from the match ID
        match_data = get_match_data(match_id, mass_region, api_key)
        player_data = find_player_data(match_data, puuid)

        # assign the variables we're interested in
        champion = player_data['championName']
        k = player_data['kills']
        d = player_data['deaths']
        a = player_data['assists']
        win = player_data['win']

        # add them to our dataset
        data['champion'].append(champion)
        data['kills'].append(k)
        data['deaths'].append(d)
        data['assists'].append(a)
        data['win'].append(win)

    df = pd.DataFrame(data)

    return df

def get_encrypted_id(summoner_name, region, api_key):
    api_url = (
            "https://" +
            region +
            ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
            summoner_name +
            "?api_key=" +
            api_key
    )
    resp = requests.get(api_url)
    player_info = resp.json()
    encryptedid = player_info['id']
    return encryptedid