from st2reactor.sensor.base import Sensor
import re
import json
import uuid
import requests
import ipaddress

class DockerEvent(Sensor):

    def run(self):
        r = requests.get('http://172.28.128.4:3376/events', stream=True)
        key = "REPLACE WITH SWARM KEY"
        for chunk in r.raw.read_chunked():
            event = json.loads(chunk)
            netwk_data = requests.get('http://172.28.128.4:3376/networks/%s' % event['Actor']['Attributes']['name'])
            if event['Action'] == 'create':
                netwk_data = json.loads(netwk_data.content)
                vlan =  re.findall('eth[0-9]+\.([0-9]+)', netwk_data['Options']['parent'])[0]
                network = ipaddress.ip_network(netwk_data['IPAM']['Config'][0]['Subnet'])
                data = dict(action=event['Action'],
                            rbridge="21",
                            subnet="%s/%s" % (network[1], network.prefixlen),
                            vlan=vlan,
                            channel=self._config.channel,
                            host=self._config.host,
                            username=self._config.username,
                            password=self._config.password)
                trigger = 'docker.NetworkEvent'
                trace_tag = uuid.uuid4().hex
                self._sensor_service.dispatch(trigger=trigger, payload=data,
                        trace_tag=trace_tag)
