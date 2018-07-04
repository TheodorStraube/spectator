import json
import time
from riotwatcher import RiotWatcher

from static import Static
from history import MatchHistory
from match import *
from util import do_slowly

#  https://mushroom.teemo.gg/

class Spectator:

    def __init__(self, api_key, region, summoner):

        self.API_KEY = api_key
        self.region = region
        self.summoner = summoner
        self.data = {}
        self.processing = {}

        self.watcher = RiotWatcher(self.API_KEY)

        self.me = self.watcher.summoner.by_name(self.region, self.summoner)

        #tim = self.watcher.summoner.by_name(self.region, 'Timmaable')

        #res = self.watcher.spectator.by_summoner(self.region, tim['id'])
        #print(res)

        self.static = Static(region, self.watcher)

    def load(self):
        self.history = MatchHistory()
        self.history.build_history(self.region, self.me['accountId'], self.watcher)
        self.history.save()

    def f(self):
        h = MatchHistory(self.me['accountId'])
        h.load()
        count = 0

        print(len(h))

        other_players = {}

        candidates = []
        for match in h.items:
            if match not in candidates:
                candidates.append(match)

        print(len(candidates))

        for match in candidates:
            count += 1
            print(count)
            do_slowly('riot_api', initial_count=1)
            players = self.watcher.match.by_id(self.region, match['gameId']['participantIdentities'])
            for player in players:
                if player['player']['accountId'] != self.me['accountId']:
                    if player['player']['summonerName'] in other_players:
                        n, ref = other_players[player['player']['summonerName']]
                        ref.append(match)
                        other_players[player['player']['summonerName']] = n + 1, ref
                    else:
                        other_players[player['player']['summonerName']] = 1, [match]
            print([(player, other_players[player][0]) for player in other_players if other_players[player][0] > 1])

spec = Spectator('RGAPI-0197ae7d-bca8-4bf1-8490-88480a80d571', 'euw1', 'Anzeige ist raus')
spec.load()
#for i in range(10000):
#    print(spec.do_slowly(max, range(i+1)))

#print(spec.static.get_champs())
