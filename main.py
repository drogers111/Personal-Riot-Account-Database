import requests
import pandas as pd
import pyarrow
import csv

import modCSV as mod
import GetRank as gr
import APIGen as apig

def main():
    api_key = ''
    mass_region = 'AMERICAS'
    region = 'na1'
    lstofdicts = mod.open_csv("names.csv")

    choice = '-1'
    while choice != '0':
        choice = input("\nWhat do you want to do? "
                       "\n'1' to add a summoner "
                       "\n'2' to remove a summoner"
                       "\n'3' to view all summoners "
                       "\n'4' to view all data "
                       "\n'5' to update all ranks "
                       "\n'0' to exit: ")
        print("")
        if choice == '1':
            lstofdicts = mod.add_account(lstofdicts, region, api_key)
            print("Account Added")
        elif choice == '2':
            lstofdicts = mod.removeAccount(lstofdicts, input('Enter the summoner name you want removed: '))
            print("Account removed")
        elif choice == '3':
            mod.display(lstofdicts)
        elif choice == '4':
            mod.superdisplay(lstofdicts)
        elif choice == '5':
            gr.update_ranks(lstofdicts, api_key)
            print("Ranks Updated")


    print('Updating csv and exiting program.')

    mod.write_to_csv(lstofdicts, 'names.csv')





if __name__ == "__main__":
    main()


    #summoner_name = input('Enter summoner name: ')
    #puuid = apig.get_puuid(summoner_name, region, api_key)
    #encryptedID = apig.get_encrypted_id(summoner_name, region, api_key)


    # match_ids = apig.get_match_ids(puuid, mass_region, api_key)
    #
    #
    # match_id = match_ids[0]
    # match_data = apig.get_match_data(match_id, mass_region, api_key)
    #
    # print(apig.find_player_data(match_data, puuid))
    #
    # df = apig.gather_all_data(puuid, match_ids, mass_region, api_key)
    #
    # print(df)
    #
    # df['win'] = df['win'].astype(int)
    #
    # print(df)
    #
    # # Find the averages
    # df.mean(numeric_only=True)  # numeric_only stops it trying to average the "champion" column
    #
    # # Get the averages per champion
    # print(df.groupby('champion').mean())
    #
    # # or maybe order your games by amount of kills
    # df.sort_values('kills')
    #
    # print(f.add(10))