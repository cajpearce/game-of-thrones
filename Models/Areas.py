class Area:
    def __init__(self,
                 area_id,
                 name,
                 island,
                 number_of_barrels,
                 number_of_crowns,
                 castle_level,
                 has_port,
                 is_ocean,
                 is_desert):

        self.area_id = area_id
        self.is_desert = is_desert
        self.island = island
        self.is_ocean = is_ocean
        self.name = name
        self.number_of_barrels = number_of_barrels
        self.number_of_crowns = number_of_crowns
        self.castle_level = castle_level
        self.has_port = has_port

        self.connected_areas = []

    def add_connected_area(self,area):
        if area is self:
            raise Exception("You cannot add an area as a connection of itself.")

        if type(area) is not Area:
            raise Exception("You can only add an area to connected areas.")

        self.connected_areas.append(area)

import sqlite3

class AreaDB:
    def __init__(self):
        # todo get rid of hard coded dependency
        self.connection = sqlite3.connect("got.db")
        cursor.execute("""SELECT NOW();""")