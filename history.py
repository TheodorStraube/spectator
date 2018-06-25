import json
from match import Match
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

        t1 = t2 = time.time()

        while True:

            if count % limit_1 == limit_1 - 1 and time.time() - t1 > 1:
                time.sleep(1)
                t1 = time.time()

            if count % limit_2 == limit_2 - 1 and time.time() - t2 > 120:
                time.sleep(int(time.time() - t2 + 1))
                t2 = time.time()

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
