import requests
import pymysql
from sshtunnel import SSHTunnelForwarder


class stationInfoCrawler:
    _ssh_host = 'ipa-022.ucd.ie'
    _ssh_user = 'student'
    _ssh_pwd = 'garnidelia'
    _ssh_port = 22
    _sql_hostname = '127.0.0.1'
    _sql_port = 3306
    _sql_username = 'root'
    _sql_password = 'qwert2020'
    _sql_main_database = 'dublin_bus'

    def __init__(self, url):
        self.url = url

    def connect_db(self, func, *args):
        """Connect to the database by ssh tunnel and run the query"""
        # Connect by ssh tunnel
        with SSHTunnelForwarder(
                (self._ssh_host, self._ssh_port),
                ssh_username=self._ssh_user,
                ssh_password=self._ssh_pwd,
                remote_bind_address=(self._sql_hostname, self._sql_port)
        ) as tunnel:
            conn = pymysql.connect(
                host=self._sql_hostname,
                port=tunnel.local_bind_port,
                password=self._sql_password,
                user=self._sql_username,
                db=self._sql_main_database)

            # Run the query
            cur = conn.cursor()
            func(cur, *args)
            conn.commit()
            conn.close()

    def get_station_info(self):
        """Get stations information from the open API as json file"""
        result = requests.get(self.url).json()
        error_code = int(result['errorcode'])

        # Check whether the request is success
        if error_code:
            return False

        results = result['results']
        return results


if __name__ == '__main__':
    # Initialise a new object
    url = "https://data.smartdublin.ie/cgi-bin/rtpi/busstopinformation?stopid&format=json"
    sic = stationInfoCrawler(url)


    # Create the database
    def create_sql(cur):
        sql = "CREATE TABLE Stop_Info(id INT AUTO_INCREMENT PRIMARY KEY, " \
              "StopId VARCHAR(8), " \
              "StopName VARCHAR(30), " \
              "StopFullName VARCHAR(255)," \
              "StopLat FLOAT," \
              "StopLng FLOAT)"
        cur.execute(sql)


    sic.connect_db(create_sql)

    # Insert stop info
    rows = sic.get_station_info()


    def insert_info(cur, rows):
        sql = "INSERT INTO `Stop_Info` (`StopId`, `StopName`, `StopFullName`, `StopLat`, `StopLng`) VALUES (%s, %s, %s, %s, %s)"
        val = []
        for i, data in enumerate(rows):
            stop_id = data['stopid']
            stop_name = data['shortname']
            stop_fullname = data['fullname']
            stop_lat = data['latitude']
            stop_lng = data['longitude']
            # stop_route = data['operators'][0]['routes']
            val.append((stop_id, stop_name, stop_fullname, stop_lat, stop_lng))
        cur.executemany(sql, val)


    sic.connect_db(insert_info, rows)
