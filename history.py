import json
from match import Match
from util import do_slowly
import time

class MatchHistory:

    fname = 'mh_*.json'

    def __init__(self, accountId=-1):
        self.items = []
        self.accountId = accountId

    def __len__(self):
        return len(self.items)

    def build_history(self, region, accountId, watcher):
        max_items = 100
        count = 0
        matches = []
        self.accountId = accountId

        while True:
            print(len(self.items))

            do_slowly('riot_api', initial_count=1)
            matches = watcher.match.matchlist_by_account(region, accountId, begin_index=count * max_items)['matches']

            if not matches:
                break

            for match in matches:
                if match in self.items:
                    break
                else:
                    self.items.append(match)
            count += 1
        print('{} Spiele gefunden.'.format((max(0, count - 1)) * max_items + len(matches)))

    def save(self):
        with open(MatchHistory.fname.replace('*', str(self.accountId)), 'w') as out:
            json.dump({'data': list(self.items)}, out)

    def load(self):
        with open(MatchHistory.fname.replace('*', str(self.accountId))) as inp:
            self.items += json.load(inp)['data']
        self.items.sort(key=lambda x: -x['timestamp'])
