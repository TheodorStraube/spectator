import json
import time
from riotwatcher import RiotWatcher

from static import Static
from history import MatchHistory
from match import *

#  https://mushroom.teemo.gg/

class Spectator:

    limit_1 = 20
    limit_2 = 100

    def __init__(self, api_key, region, summoner):

        self.API_KEY = api_key
        self.region = region
        self.summoner = summoner
        self.data = {}
        self.processing = {}

        self.watcher = RiotWatcher(self.API_KEY)

        self.me = self.watcher.summoner.by_name(self.region, self.summoner)

        self.static = Static(region, self.watcher)

    def do_slowly(self, func, *args, **kwargs):
        if func in self.processing:
            count, delta = self.processing[func]
        else:
            count = 0
            delta = []

        if delta:
            print(max(delta[-Spectator.limit_2:]) - min(delta[-Spectator.limit_2:]))

            if max(delta[-Spectator.limit_1:]) - min(delta[-Spectator.limit_1:]) < 1 and len(delta) >= Spectator.limit_1:
                print('nap')
                time.sleep(1)
            if max(delta[-Spectator.limit_2:]) - min(delta[-Spectator.limit_2:]) < 120 and len(delta) >= Spectator.limit_2:
                print('sleep')
                time.sleep(120 - (max(delta[-Spectator.limit_2:]) - min(delta[-Spectator.limit_2:])) + 1)
            if len(delta) > max(Spectator.limit_1, Spectator.limit_2):
                delta.remove(delta[0])

        delta.append(time.time())

        self.processing[func] = count + 1, delta
        return func(*args, **kwargs)


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
            players = self.do_slowly(self.watcher.match.by_id, self.region, match['gameId'])['participantIdentities']
            for player in players:
                if player['player']['accountId'] != self.me['accountId']:
                    if player['player']['summonerName'] in other_players:
                        n, ref = other_players[player['player']['summonerName']]
                        ref.append(match)
                        other_players[player['player']['summonerName']] = n + 1, ref
                    else:
                        other_players[player['player']['summonerName']] = 1, [match]
            print([(player, other_players[player][0]) for player in other_players if other_players[player][0] > 1])

spec = Spectator('RGAPI-89f6fc7e-3b3c-4c0e-9647-ff6ab382a276', 'euw1', 'Anzeige ist raus')
spec.f()
#for i in range(10000):
#    print(spec.do_slowly(max, range(i+1)))

#print(spec.static.get_champs())
