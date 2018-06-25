from static import Static
import pendulum

class History:
    def __init__(self):
        pass

class Match:

    # {'platformId': 'EUW1', 'gameId': 3662578527, 'champion': 55, 'queue': 450, 'season': 11, 'timestamp': 1528496526564, 'role': 'NONE', 'lane': 'JUNGLE'}]

    def __init__(self, platformId='', gameId=-1, champion=-1, queue=-1, season=-1, timestamp=-1, role='', lane=''):
        self.region = platformId
        self.id = gameId
        self.champion = champion
        self.queue = queue
        self.season = season
        self.timestamp = timestamp
        self.role = role
        self.lane = lane

        self.static = Static(self.region)

    def __repr__(self):
        champion = self.static.get_champ(self.champion)['name']
        queue = self.static.get_queue(self.queue)['name']
        date = self.get_date(self.timestamp)

        return '[{} - {}] on {}'.format(queue, date.strftime('%D, %T'), champion)

    def __hash__(self):
        return self.id

    def get_date(self, timestep):
        return pendulum.datetime(1970, 1, 1, 0).add(microseconds=timestep * 1000)

class Game:
    pass
