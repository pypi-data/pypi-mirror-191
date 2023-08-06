import pandas as pd
import country_converter as coco
from math import radians, cos, sin, asin, sqrt, atan2
from orbit import satellite


def calc_year(year):
    twentieth = ('6', '7', '8', '9')
    twenty_first = ('0', '1', '2', '3', '4', '5')
    if year.startswith(twentieth):
        return "19%s" % year
    elif year.startswith(twenty_first):
        return "20%s" % year
    else:
        return year


df = pd.read_csv(r"rg_cities1000.csv")
class Coordinates:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def closest_city(self, accuracy=10):
        cities = df.values.tolist()
        citiesSortedByLong = list(sorted(cities, key=lambda x: x[1]))
        citiesSortedByLat = list(sorted(cities, key=lambda x: x[0]))

        searchLat1 = self.lat
        # searchLong1 = -0.13947
        searchLong1 = self.long

        closestCitiesLat = []
        closestLat = min(citiesSortedByLat, key=lambda x: abs(x[0] - searchLat1))
        closestLong = min(citiesSortedByLong, key=lambda x: abs(x[1] - searchLong1))

        minClosestLat = min(citiesSortedByLat, key=lambda x: abs(x[0] - (searchLat1 - accuracy/2)))
        maxClosestLat = min(citiesSortedByLat, key=lambda x: abs(x[0] - (searchLat1 + accuracy/2)))

        minClosestLong = min(citiesSortedByLong, key=lambda x: abs(x[1] - (searchLong1 - accuracy/2)))
        maxClosestLong = min(citiesSortedByLong, key=lambda x: abs(x[1] - (searchLong1 + accuracy/2)))

        closestCitiesList = citiesSortedByLat[citiesSortedByLat.index(minClosestLat): (citiesSortedByLat.index(maxClosestLat) + 1)]
        for city in citiesSortedByLong[citiesSortedByLong.index(minClosestLong): (citiesSortedByLong.index(maxClosestLong) + 1)]:
            closestCitiesList.append(city)


        closestCity = []
        closestDistance = 0

        index = 0

        for city in closestCitiesList:
            cityLat = city[0]
            cityLong = city[1]
            a = self.distance_between_two_coordinates(cityLat, cityLong)
            if index == 0:
                closestDistance = self.distance_between_two_coordinates(cityLat, cityLong)
                city[5] = coco.convert(names=city[5], to='name_short')
                closestCity = [city]
                index += 1
                continue

            if self.distance_between_two_coordinates(cityLat, cityLong) < closestDistance:
                closestDistance = self.distance_between_two_coordinates(cityLat, cityLong)
                city[5] = coco.convert(names=city[5], to='name_short')
                closestCity = [city]
                continue

            if self.distance_between_two_coordinates(cityLat, cityLong) == closestDistance:
                city[5] = coco.convert(names=city[5], to='name_short')
                closestCity.append(city)

        removeDuplicates = {tuple(city) for city in closestCity}

        return removeDuplicates

    def distance_between_two_coordinates(self, lat2, long2):
        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(self.long)
        lon2 = radians(long2)
        lat1 = radians(self.lat)
        lat2 = radians(lat2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        return c * r


from math import degrees

import tle


class Satellite(Coordinates):
    def __init__(self, catnr):
        self.tle_raw = tle.get(catnr)
        self.tle_parsed = tle.parse(self.tle_raw[0], self.tle_raw[1], self.tle_raw[2])
        self.name = self.find_name()
        self.catalog_number = self.find_catalog_number()
        self.elsat_classification = self.find_elsat_classification()
        self.launch_year = self.find_launch_year()
        self.tle = self.find_tle()
        self.lat = self.find_lat()
        self.long = self.find_long()
        self.elevation = self.find_elevation()
        self.is_eclipsed = self.find_eclipsed()
        super().__init__(self.lat, self.long)

    def find_name(self):
        return self.tle_raw[0].strip()

    def find_catalog_number(self):
        return self.tle_raw[1][2:7]

    def find_elsat_classification(self):
        return self.tle_raw[1][7]

    def find_launch_year(self):
        return calc_year(self.tle_raw[1][9:11])

    def find_tle(self):
        return [self.tle_raw[0], self.tle_raw[1], self.tle_raw[2]]

    def find_lat(self):
        return degrees(self.tle_parsed.sublat)

    def find_long(self):
        return degrees(self.tle_parsed.sublong)

    def find_elevation(self):
        return self.tle_parsed.elevation

    def find_eclipsed(self):
        return self.tle_parsed.eclipsed
