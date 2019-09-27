import requests
from datetime import datetime
import logging
import config

class GarminTracker( object ):

    def __init__(self, trackId, token, name, channel):
        self.trackId = trackId
        self.token = token
        self.name = name
        self.channel = channel
        self.lastPoll = None

    def runPoll(self):
        serviceResponse = requests.get(self._buildUrl())
        for point in serviceResponse.json():
            m = ','.join(str(x) for x in [point['latitude'], point['longitude'], self.name, datetime.fromtimestamp(point['timestamp']/1000)])
            logging.info('Got point: %s', m)
            self.channel.basic_publish(exchange=config.topicName, routing_key=self.name, body=m)
            self.lastPoll = point['timestamp']

    def _buildUrl(self):
        requestTime = self._getCurrentTimestamp()
        url = 'https://livetrack.garmin.com/services/trackLog/{}/token/{}?requestTime={}000'.format(self.trackId, self.token, requestTime)
        if self.lastPoll:
            url += '&from={}'.format(self.lastPoll)
        return url

    def _getCurrentTimestamp(self):
        return int(datetime.now().timestamp())