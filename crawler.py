import sys
from protocol import *

CRAWLED_NODES = []
nodelist = lambda x: (n for n in x)

def check_crawl(ip):
    if ip not in CRAWLED_NODES:
        CRAWLED_NODES.append(ip)
        crawl((ip, PORT), TO_SERVICES)


def crawl(to_addr, to_services):
    handshake_msgs = []
    addr_msgs = []

    conn = Connection(to_addr, to_services=to_services)
    try:
        conn.open()
        handshake_msgs = conn.handshake()
        addr_msgs = conn.getaddr()

    except (ProtocolError, ConnectionError, socket.error) as err:
        pass

    conn.close()

    if len(handshake_msgs) > 0:
        services = handshake_msgs[0].get('services', 0)

    check_crawl(node) for node in addr_msgs[0]['addr_list']

    #for node in nodelist(addr_msgs[0]['addr_list']):
    #    if node['ipv4'] in CRAWLED_NODES:
    #        continue
    #    else:
    #        CRAWLED_NODES.append(node['ipv4'])
    #        crawl((node['ipv4'], PORT), TO_SERVICES)
    print(CRAWLED_NODES)
    return 0

def main():
    to_addr = ("92.60.46.21", PORT)
    to_services = TO_SERVICES

    crawl(to_addr, to_services)
    #handshake_msgs = []
    #addr_msgs = []

    #conn = Connection(to_addr, to_services=to_services)
    #try:
    #    print("open")
    #    conn.open()

    #    print("handshake")
    #    handshake_msgs = conn.handshake()

    #    print("getaddr")
    #    addr_msgs = conn.getaddr()

    #except (ProtocolError, ConnectionError, socket.error) as err:
    #    print("{}: {}".format(err, to_addr))

    #print("close")
    #conn.close()

    #if len(handshake_msgs) > 0:
    #    services = handshake_msgs[0].get('services', 0)
    #    if services != to_services:
    #        print('services ({}) != {}'.format(services, to_services))

    #print(handshake_msgs)
    #print(addr_msgs)

    #for node in addr_msgs[0]['addr_list']:
    #    if node['ipv4'] in CRAWLED_NODES:
    #        continue
    #    else:
    #        CRAWLED_NODES.append(node['ipv4'])
    #        crawl(node['ipv4'], TO_SERVICES)

    return 0


if __name__ == '__main__':
    sys.exit(main())

