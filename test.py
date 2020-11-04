import os
import asyncio
import subprocess
from protocol import *

NODE_LIST = []

async def ping(to_addr):
    FNULL = open(os.devnull, 'w')
    return subprocess.call(['ping', '-c', '1', '-W', '1', to_addr], stdout=FNULL, stderr=subprocess.STDOUT) == 0

async def available_nodes(addr_list):
    available_nodes = []

    for addr in addr_list:
        if await ping(addr['ipv4']):
            node = (addr['ipv4'], addr['port'])
            available_nodes.append(node)
    
    return available_nodes

async def crawl(to_addr, to_services=TO_SERVICES):
    handshake_msgs = []
    addr_msgs = []

    conn = Connection(to_addr, to_services=to_services)
    try:
        conn.open()
        handshake_msgs = conn.handshake()
        addr_msgs = conn.getaddr()
    except (ProtocolError, ConnectionError, socket.error) as err:
        print("{}: {}".format(err, to_addr))

    conn.close()

    if len(handshake_msgs) > 0:
        services = handshake_msgs[0].get('services', 0)
        if services != to_services:
            print('services ({}) != {}'.format(services, to_services))

    print(handshake_msgs)
    for msg in addr_msgs:
        if msg['addr_list']:
            for addr in msg['addr_list']:
                node = (addr['ipv4'], addr['port'])
                if node not in NODE_LIST:
                    NODE_LIST.append(node)
                await crawl(node)

    return 0

def main():
    loop = asyncio.get_event_loop()
    tasks = []

    to_addr = ("188.40.184.66", PORT)
    #to_addr = ("92.60.46.21", PORT)
    handshake_msgs = []
    addr_msgs = []

    conn = Connection(to_addr, to_services=TO_SERVICES)
    try:
        conn.open()
        handshake_msgs = conn.handshake()
        addr_msgs = conn.getaddr()
    except (ProtocolError, ConnectionError, socket.error) as err:
        print("{}: {}".format(err, to_addr))

    conn.close()

    if len(handshake_msgs) > 0:
        services = handshake_msgs[0].get('services', 0)
        if services != TO_SERVICES:
            print('services ({}) != {}'.format(services, TO_SERVICES))

    for msg in addr_msgs:
        if msg['addr_list']:
            for node in asyncio.run(available_nodes(msg['addr_list'])):
                if node not in NODE_LIST:
                    NODE_LIST.append(node)
                #tasks.append(crawl(node))
    #loop.run_until_complete(asyncio.wait(tasks))
    #loop.close()
    print(len(NODE_LIST))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(len(NODE_LIST))
