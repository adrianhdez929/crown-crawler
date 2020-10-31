from protocol import *

NODE_LIST = []

def crawl(to_addr, to_services=TO_SERVICES):
    handshake_msgs = []
    addr_msgs = []
    #inv_msgs = []

    conn = Connection(to_addr, to_services=to_services)
    try:
        #print("open")
        conn.open()

        #print("handshake")
        handshake_msgs = conn.handshake()

        #print('mnvs')
        #inv_msgs = conn.getmnvs("0f3fb5f81707ca42c763a717034902ff9c7a04ab351a56573f5f239889adbc3b")
        #print("block")
        #inv_msgs = conn.getblocks(["0249d5f512b3b4ba2b216b5f5b8e4e1cb79d52a0c04f9f723cb5bcf48262b4a0",])
        #print("getaddr")
        addr_msgs = conn.getaddr()

    except (ProtocolError, ConnectionError, socket.error) as err:
        print("{}: {}".format(err, to_addr))

    #print("close")
    conn.close()

    if len(handshake_msgs) > 0:
        services = handshake_msgs[0].get('services', 0)
        if services != to_services:
            print('services ({}) != {}'.format(services, to_services))

    print(handshake_msgs)
    #print(inv_msgs)
    for msg in addr_msgs:
        if msg['addr_list']:
            for addr in msg['addr_list']:
                node = (addr['ipv4'], addr['port'])
                if node not in NODE_LIST:
                    NODE_LIST.append(node)
                crawl(node)
    #print(addr_msgs)

    return 0

def main():
    #to_addr = ("188.40.184.66", PORT)
    to_addr = ("92.60.46.21", PORT)
    crawl(to_addr)
    print(NODE_LIST)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(NODE_LIST)
