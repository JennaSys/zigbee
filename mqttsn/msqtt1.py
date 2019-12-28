from mqttsn.client import Client, Callback  # https://github.com/iotcode/mqttsn.git

import sys


class MyCallback(Callback):
    def message_arrived(self, topic_name, payload, qos, retained, msgid):
        print(f'{self} | topic_name: {topic_name} | payload: {payload} | '
              f'qos {qos} | retained {retained} | msgid {msgid}',
              file=sys.stderr)

        return True


if __name__ == '__main__':
    aclient = Client("linh", port=1884)
    aclient.register_callback(MyCallback())
    aclient.connect()

    rc, topic1 = aclient.subscribe("topic1")
    print("topic id for topic1 is", topic1)

    rc, topic2 = aclient.subscribe("topic2")
    print("topic id for topic2 is", topic2)

    aclient.publish(topic1, "aaaa1", qos=0)
    aclient.publish(topic2, "bbbb2", qos=0)

    aclient.unsubscribe("topic1")
    # aclient.unsubscribe.unsubscribe.topic_name = "topic1"

    aclient.publish(topic2, "cccc3", qos=0)
    aclient.publish(topic1, "dddd4", qos=0)

    input("Press ENTER...")
    aclient.disconnect()