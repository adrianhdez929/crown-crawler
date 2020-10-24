#!/bin/bash
# --- crown mainnet: b8ebb3df (db = 0) ---
/usr/bin/nice -n 19 python2.7 -u crawl.py conf/crawl.conf.default master > log/crawl.b8ebb3df.master.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u crawl.py conf/crawl.conf.default slave > log/crawl.b8ebb3df.slave.1.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u crawl.py conf/crawl.conf.default slave > log/crawl.b8ebb3df.slave.2.out 2>&1 &

/usr/bin/nice -n 19 python2.7 -u ping.py conf/ping.conf.default master > log/ping.b8ebb3df.master.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u ping.py conf/ping.conf.default slave > log/ping.b8ebb3df.slave.1.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u ping.py conf/ping.conf.default slave > log/ping.b8ebb3df.slave.2.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u ping.py conf/ping.conf.default slave > log/ping.b8ebb3df.slave.3.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u ping.py conf/ping.conf.default slave > log/ping.b8ebb3df.slave.4.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u ping.py conf/ping.conf.default slave > log/ping.b8ebb3df.slave.5.out 2>&1 &

/usr/bin/nice -n 19 python2.7 -u resolve.py conf/resolve.conf.default > log/resolve.b8ebb3df.out 2>&1 &

/usr/bin/nice -n 19 python2.7 -u export.py conf/export.conf.default > log/export.b8ebb3df.out 2>&1 &

/usr/bin/nice -n 19 python2.7 -u seeder.py conf/seeder.conf.default > log/seeder.b8ebb3df.out 2>&1 &

/usr/bin/nice -n 19 python2.7 -u pcap.py conf/pcap.conf.default > log/pcap.b8ebb3df.1.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u pcap.py conf/pcap.conf.default > log/pcap.b8ebb3df.2.out 2>&1 &
/usr/bin/nice -n 19 python2.7 -u pcap.py conf/pcap.conf.default > log/pcap.b8ebb3df.3.out 2>&1 &
