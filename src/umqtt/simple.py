#mock umqtt.simple module for testing
#use paho.mqtt.client to mock umqtt.simple

import paho.mqtt.client as mqtt

class MQTTException(Exception):
    pass

class MQTTClient:
    def __init__(
        self,
        client_id,
        server,
        port=0,
        user=None,
        password=None,
        keepalive=0,
        ssl=None,
    ):
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.sock = None
        self.server = server
        self.port = port
        self.ssl = ssl
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False
        self.mqttc = mqtt.Client(client_id=client_id)

    def set_callback(self, f):
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True, timeout=None):
        self.mqttc.connect(self.server, self.port, self.keepalive)
        return False

    def disconnect(self):
        self.mqttc.disconnect()

    def ping(self):
        pass

    def publish(self, topic, msg, retain=False, qos=0):
        self.mqttc.publish(topic, msg, qos, retain)

    def subscribe(self, topic, qos=0):
        self.mqttc.subscribe(topic)
        self.mqttc.message_callback_add(topic, self.cb)
        #self.mqttc.on_message = self.cb

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def wait_msg(self):
        self.mqttc.loop_forever()

    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def check_msg(self):
        self.mqttc.loop(timeout=1.0)
