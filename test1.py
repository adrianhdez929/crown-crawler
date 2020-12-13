import asyncio
from concurrent.futures import ThreadPoolExecutor
from models import Peer
from protocol import *

NODE_LIST = []
VISITED_NODES=[]

def crawl(to_addr, to_services=TO_SERVICES):
    handshake_msgs = []
    addr_msgs = []

    queue = []
    VISITED_NODES.append(to_addr)
    queue.append(to_addr)

    while queue:
        nodes = []
        to_addr = queue.pop(0)

        conn = Connection(to_addr, to_services=to_services, **{'socket_timeout': 1, })
        try:
            conn.open()
            handshake_msgs = conn.handshake()
            addr_msgs = conn.getaddr()
        except (ProtocolError, ConnectionError, socket.error) as err:
            print("{}: {}".format(err, to_addr))
        conn.close()

        if len(handshake_msgs) > 0:
            asyncio.run(Peer.dump(to_addr[0], to_addr[1], handshake_msgs[0]['version'],
                            handshake_msgs[0]['user_agent'].decode('utf-8'), handshake_msgs[0].get('services', 0),
                            handshake_msgs[0]['height'], handshake_msgs[0]['timestamp']))
            
        for msg in addr_msgs:
            if msg['addr_list']:
                for addr in msg['addr_list']:
                    node = (addr['ipv4'], addr['port'])
                    nodes.append(node)

        for n in nodes:
            if n not in VISITED_NODES:
                VISITED_NODES.append(n)
                queue.append(n)

def main():

    nodes = []

    dns = socket.gethostbyname("dnsseed2.crowncoin.org")
    to_addr = (str(dns), PORT)
    handshake_msgs = []
    addr_msgs = []

    conn = Connection(to_addr, to_services=TO_SERVICES, **{'socket_timeout': 1,})
    try:
        conn.open()
        handshake_msgs = conn.handshake()
        addr_msgs = conn.getaddr()
    except (ProtocolError, ConnectionError, socket.error) as err:
        #pass
        print("{}: {}".format(err, to_addr))

    conn.close()

    if len(handshake_msgs) > 0:
        asyncio.run(Peer.dump(to_addr[0], to_addr[1], handshake_msgs[0]['version'], 
                        handshake_msgs[0]['user_agent'].decode('utf-8'), handshake_msgs[0].get('services', 0),
                        handshake_msgs[0]['height'], handshake_msgs[0]['timestamp']))

    print(addr_msgs)

    for msg in addr_msgs:
        if msg['addr_list']:
            for addr in msg['addr_list']:
                if addr['ipv4'] == '':
                    continue
                node = (addr['ipv4'], addr['port'])
                nodes.append(node)

    VISITED_NODES.append(to_addr)
    with ThreadPoolExecutor() as pool:
        for node in nodes:
            pool.submit(crawl, node)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(len(VISITED_NODES))
        
