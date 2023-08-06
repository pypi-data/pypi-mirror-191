import requests

url = "http://consentiuminc.online/update"


class ThingsUpdate:
    payload = {}

    def __init__(self, key):
        self.key = key

    def sendREST(self, info_buff, sensor_val):
        sensor_num = len(sensor_val)

        if sensor_num == 1:
            self.payload = {'send_key': self.key,
                            'sensor1': sensor_val[0], 'info1': info_buff[0]}
        elif sensor_num == 2:
            self.payload = {'send_key': self.key,
                            'sensor1': sensor_val[0], 'info1': info_buff[0],
                            'sensor2': sensor_val[1], 'info2': info_buff[1]}
        elif sensor_num == 3:
            self.payload = {'send_key': self.key,
                            'sensor1': sensor_val[0], 'info1': info_buff[0],
                            'sensor2': sensor_val[1], 'info2': info_buff[1],
                            'sensor3': sensor_val[2], 'info3': info_buff[2]}
        elif sensor_num == 4:
            self.payload = {'send_key': self.key,
                            'sensor1': sensor_val[0], 'info1': info_buff[0],
                            'sensor2': sensor_val[1], 'info2': info_buff[1],
                            'sensor3': sensor_val[2], 'info3': info_buff[2],
                            'sensor4': sensor_val[3], 'info4': info_buff[3]}
        elif sensor_num == 5:
            self.payload = {'send_key': self.key,
                            'sensor1': sensor_val[0], 'info1': info_buff[0],
                            'sensor2': sensor_val[1], 'info2': info_buff[1],
                            'sensor3': sensor_val[2], 'info3': info_buff[2],
                            'sensor4': sensor_val[3], 'info4': info_buff[3],
                            'sensor5': sensor_val[4], 'info5': info_buff[4]}
        elif sensor_num == 6:
            self.payload = {'send_key': self.key,
                            'sensor1': sensor_val[0], 'info1': info_buff[0],
                            'sensor2': sensor_val[1], 'info2': info_buff[1],
                            'sensor3': sensor_val[2], 'info3': info_buff[2],
                            'sensor4': sensor_val[3], 'info4': info_buff[3],
                            'sensor5': sensor_val[4], 'info5': info_buff[4],
                            'sensor6': sensor_val[5], 'info6': info_buff[5]}
        elif sensor_num == 7:
            self.payload = {'send_key': self.key,
                            'sensor1': sensor_val[0], 'info1': info_buff[0],
                            'sensor2': sensor_val[1], 'info2': info_buff[1],
                            'sensor3': sensor_val[2], 'info3': info_buff[2],
                            'sensor4': sensor_val[3], 'info4': info_buff[3],
                            'sensor5': sensor_val[4], 'info5': info_buff[4],
                            'sensor6': sensor_val[5], 'info6': info_buff[5],
                            'sensor7': sensor_val[6], 'info7': info_buff[6]}

        r = requests.get(url, params=self.payload)
        return r.json()
