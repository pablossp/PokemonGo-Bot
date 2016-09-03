# -*- coding: utf-8 -*-

from random import uniform
from pokemongo_bot.human_behaviour import sleep
from pokemongo_bot.walkers.step_walker import StepWalker
from polyline_generator import PolylineObjectHandler
from pokemongo_bot.cell_workers.utils import distance
from pokemongo_bot.constants import Constants

class PolylineWalker(StepWalker):

    def __init__(self, bot, dest_lat, dest_lng):
        super(PolylineWalker, self).__init__(bot, dest_lat, dest_lng)

        self.actual_pos = tuple(self.api.get_position()[:2])

        self.dist = distance(
            self.bot.position[0],
            self.bot.position[1],
            dest_lat,
            dest_lng
        )

    def step(self):
        self.polyline_walker = PolylineObjectHandler.cached_polyline(self.actual_pos,
                                        (self.destLat, self.destLng), self.speed, google_map_api_key=self.bot.config.gmapkey)

        if self.dist < 10: # 10m, add config? set it at constants?
            return True

        self.polyline_walker.unpause()
        sleep(1)
        self.polyline_walker.pause()

        cLat, cLng = self.polyline_walker.get_pos()
        cAlt = self.polyline_walker.get_alt()
        self.api.set_position(cLat, cLng, cAlt)
        self.actual_pos = (cLat, cLng) # might be a case this instance is reused in the future...

        self.bot.heartbeat()
        return False
