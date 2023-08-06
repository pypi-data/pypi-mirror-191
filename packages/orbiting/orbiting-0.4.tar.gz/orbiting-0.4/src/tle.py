import requests
import ephem


def get(catnr):
    page = requests.get(f'http://www.celestrak.com/cgi-bin/TLE.pl?CATNR='+str(catnr))
    tle = page.text.split('\n')
    return tle[0].strip(), tle[1].strip(), tle[2].strip()


def parse(name, line1, line2):
    tle_rec = ephem.readtle(name, line1, line2)
    tle_rec.compute()
    return tle_rec
