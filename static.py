import os
import json

class Static:

    file = 'league_static.json'
    maps_fname = 'language/8.12/en_us/maps.json'
    queues_fname = 'language/8.12/en_us/queues.json'
    data = {}
    maps = {}
    queues = {}

    def __init__(self, region, watcher=None):
        self.region = region
        self.watcher = watcher
        self.collect_static()

    def collect_static(self):
        if Static.data:
            return
        if os.path.isfile(self.file):
            print('Loading cached data from', self.file)
            with open(self.file) as inp:
                Static.data = json.load(inp)
        elif self.watcher is None:
            print('i have no watcher yet..')
            return
        else:
            print('Downloading static data...')
            Static.data = {}

            champs = self.watcher.static_data.champions(self.region)
            Static.data['champ_data'] = champs
            Static.data['champ_data']['data'] = {champ['id']: champ for champ in champs['data'].values()}

            with open(self.file, 'w') as out:
                json.dump(Static.data, out)

        if not Static.maps or not Static.queues:
            with open(Static.maps_fname) as maps, open(Static.queues_fname) as queues:
                Static.maps = {map['id']: map for map in json.load(maps)}
                Static.queues = json.load(queues)

    def get_champs(self):
        return Static.data['champ_data']['data']
    def get_champ(self, id):
        return self.get_champs()[str(id)]
    def get_map(self, id):
        return Static.maps[str(id)]
    def get_queue(self, id):
        return Static.queues[str(id)]
