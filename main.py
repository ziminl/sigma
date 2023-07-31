import requests, time, pandas, json, datetime, pytz
from pandas.io.json import json_normalize

# Variables
REGION = 'na1'
TFTREGION = 'americas'
APIKEY = 'RGAPI-be31efae-g3at-3gh4-betr-3h4h236hset6'
MATCHES = '2'

# Class 
class Summoner:
    def __init__(self, name):
        if type(name) == list:
            for name in name:
                self.getpuuid(name)
        elif len(name) < 17:
            self.getpuuid(name)
        else:
            self.getname(name)

    def getpuuid(self, name):
        URL = 'https://' + REGION + '.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + name + '?api_key=' + APIKEY
        response = requests.get(URL)
        self.puuid = response.json()['puuid']

    def getname(self, puuid):
        URL = 'https://'+ REGION +'.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + puuid + '?api_key=' + APIKEY
        response = requests.get(URL)
        self.name = response.json()['name']

class Match:
    def __init__(self, Summoner):
        if type(Summoner) == list:
           for x in Summoner:
               self.matchhistory = self.getmatchhistory(x.puuid)
        else:
            self.matchhistory = self.getmatchhistory(Summoner.puuid)
        self.matchdetails = []
        self.matchdetails = self.getmatchdetails(self.matchhistory)
        self.data = []
        for match in self.matchdetails:
            self.data.append(pandas.io.json.json_normalize(match))
        self.data_dict = []
        for data in self.data:
            self.data_dict.append(data.to_dict())
    
    def getmatchhistory(self, puuid):
        URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?count=' + MATCHES + '&api_key=' + APIKEY
        response = requests.get(URL)
        return response.json()

    def getmatchdetails(self, matchid):
        for match in matchid:
            URL = 'https://' + TFTREGION + '.api.riotgames.com/tft/match/v1/matches/' + match + '?api_key=' + APIKEY
            response = requests.get(URL)
            self.matchdetails.append(response.json())
        return self.matchdetails
    
    def getfirstplace(self):
        for match in self.data_dict:
            print('Match Date ', self.getmatchdate(match))
            print('-------------------------')
            self.placement = []
            for x in match['info.participants'][0]:
                self.placement.append((Summoner(x['puuid']).name, str(x['placement'])))
            sorter(self.placement)
            for y in self.placement:
                print(y[0],' --> ',y[1])

    def getsetbuffs(self):
        for match in self.data_dict:
            print('Match ID = ', match['metadata.match_id'][0])
            print('-------------------------')
            z = 0
            for y in match['metadata.participants'][0]:
                print(Summoner(y).name)
                print('<----------------->')
                print(match['info.participants'][0][z]['traits'])
                print('<----------------->')
                z += 1

    def getitems(self):
        for match in self.data_dict:
            print('Match ID = ', match['metadata.match_id'][0])
            print('-------------------------')
            for x in match['info.participants'][0][0]['units']:
                print(x['name'])
                for y in x['items']:
                    with open('en_us_20191208.json') as json_file:
                        json_data = json.load(json_file)
                        json_data2 = pandas.io.json.json_normalize(json_data)
                        json_dict = json_data2.to_dict()
                    for x in json_dict['items'][0]:
                        if y == x['id']:
                            print('---> ' + x['name'])
                        

    def getmatchdate(self, match):
        ts = match['info.game_datetime'][0]
        pacific = datetime.timedelta(hours=8)
        return (datetime.datetime.utcfromtimestamp(ts/1000) - pacific).strftime('%Y-%m-%d %H:%M:%S')

# Useful functions
# Python code to sort the tuples using second element  
def sorter(list): 
    list.sort(key = lambda x: x[1]) 
    return list

def main():

    a_summoner = Summoner('DevonsMeat')
    #print(Match.getitems(Match(a_summoner)))
    #print(Match.getmatchdate(Match(a_summoner)))
    #print(Match.getsetbuffs(Match(a_summoner)))
    Match.getfirstplace(Match(a_summoner))
    #Match(a_summoner).getitems()
    #print('<-------------->')
    #Match(a_summoner).getsetbuffs()
    #print(Match(a_summoner).data_dict)
    #print(Match(a_summoner).matchhistory)
    
if __name__ == '__main__':
    main()
