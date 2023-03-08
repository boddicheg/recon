import geoip2.database
import socket, struct, os

DB_NAME = "assets/geo/dbip-city-lite-2023-02.mmdb"

class GeoLocation():
    def __init__(self, ROOT):
        db = os.path.join(ROOT, DB_NAME)
        self.reader = geoip2.database.Reader(db)

    def ip2long(self, ip):
        packed = socket.inet_aton(ip)
        return struct.unpack("!L", packed)[0]

    def long2ip(self, iplong):
        return socket.inet_ntoa(struct.pack('!L', iplong))

    def get(self, ip):
        response = self.reader.city(ip)
        data = dict()
        data["cc"] = response.country.iso_code
        data["country"] = response.country.name
        data["city"] = response.city.name
        data["lat"] = response.location.latitude
        data["lon"] = response.location.longitude
        data["region"] = response.subdivisions.most_specific.name

        return data