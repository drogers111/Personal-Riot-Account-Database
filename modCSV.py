import requests
import pandas as pd
import pyarrow
import csv

import APIGen as apig
import GetRank as gr


def open_csv(filename):
    myList = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            myList.append(row)
    lstofdicts = []
    for i in myList:
        lstofdicts.append(
            {"summoner_name": i[0], "rank": i[1], "username": i[2], "password": i[3], "encrypted_id": i[4], "puuid": i[5]})
    return lstofdicts

def write_to_csv(lstofdicts, filename):
    with open(filename, mode="w") as csvfile:
        fieldnames = lstofdicts[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
        writer.writerows(lstofdicts)


def display(lstofdicts):
    pd.set_option('display.max_columns', 4)
    pd.options.display.max_colwidth = 25
    rankdict = {
        'CHALLENGER': -300,
        'GRANDMASTER': -200,
        'MASTER': -1,
        'DIAMOND': 0,
        'EMERALD': 4,
        'PLATINUM': 8,
        'GOLD': 12,
        'SILVER': 16,
        'BRONZE': 20,
        'IRON': 24
    }
    romanNumDict = {
        'I': 1,
        'II': 2,
        'III': 3,
        'IV': 4
    }
    data = {
        'accountname': [],
        'username': [],
        'password': [],
        'rank': [],
        'odr': []
    }
    for i in lstofdicts:
        data['accountname'].append(i['summoner_name'])
        data['username'].append(i['username'])
        data['password'].append(i['password'])
        data['rank'].append(i['rank'])

        ranksort = 1000

        if (i['rank'].split()[0] != 'UNRANKED'):
            ranksort = rankdict[i['rank'].split()[0]] + romanNumDict[i['rank'].split()[1]]

        data['odr'].append(ranksort)

    df = pd.DataFrame(data)
    df.sort_values(by='odr', ascending=True, inplace=True)
    print(df[['accountname', 'username', 'password', 'rank']])
    return
def superdisplay(lstofdicts):
    pd.set_option('display.max_columns', None)
    pd.options.display.max_colwidth = 100
    data = {
        'summoner_name': [],
        'rank': [],
        'username': [],
        'password': [],
        'encrypted_id': [],
        'puuid': []
    }
    for i in lstofdicts:
        data['summoner_name'].append(i['summoner_name'])
        data['username'].append(i['username'])
        data['password'].append(i['password'])
        data['rank'].append(i['rank'])
        data['encrypted_id'].append(i['encrypted_id'])
        data['puuid'].append(i['puuid'])

    df = pd.DataFrame(data)
    print(df)
    return

def add_account(lstofdicts, region, api_key):
    summoner_name = input('Enter summoner name: ')
    puuid = apig.get_puuid(summoner_name, region, api_key)
    encryptedID = apig.get_encrypted_id(summoner_name, region, api_key)
    rank = gr.get_rank(encryptedID, api_key)
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    lstofdicts.append({"summoner_name": summoner_name, "rank": rank, "username": username, "password": password, "encrypted_id": encryptedID, "puuid": puuid})
    return lstofdicts
def removeAccount(lstofdicts, name):
    for i in range(len(lstofdicts)):
        if lstofdicts[i]['summoner_name'].upper() == name.upper():
            del lstofdicts[i]
            return lstofdicts