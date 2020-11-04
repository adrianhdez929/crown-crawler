from peewee import *


db = SqliteDatabase('crawler.db')

class Peer(Model):
    ip = IPField()
    port = IntegerField()
    protocol_version = IntegerField(default=0)
    client_version = CharField(null=True)
    last_height = IntegerField(default=0)
    last_timestamp = IntegerField(default=0)

    class Meta:
        database = db

    @staticmethod
    async def dump(ip, port, proto, version, height, timestamp):
        try:
            peer = Peer.select().where(Peer.ip == ip).get()
            peer.port = port 
            peer.protocol_version = proto
            peer.client_version = version
            peer.last_height = height
            peer.last_timestamp = timestamp
            peer.save()
        except OperationalError as err:
            if err.__str__().__contains__('no such table'):
                db.create_tables([Peer])
                peer = Peer.create(
                    ip=ip, 
                    port=port, 
                    protocol_version=proto,
                    client_version=version,
                    last_height=height,
                    last_timestamp = timestamp
                )
            return None
        except DoesNotExist:
            peer = Peer.create(
                ip=ip, 
                port=port, 
                protocol_version=proto,
                client_version=version,
                last_height=height,
                last_timestamp = timestamp
            )
            peer.save()
        
def test():
    peers = Peer.select()
    for peer in peers.iterator():
        print("({}, {}, {}, {})".format(peer.ip, peer.client_version, peer.last_height, peer.last_timestamp))
    print(len(peers))
