import blescan
import time
import bluetooth._bluetooth as bluez
import commands
import MySQLdb
import sys
import os

dev_id = 0
beacon_data_old = []
args = sys.argv

SERVER = args[1]
DATABASE = args[2]
USER = args[3]
PASS = args[4]
HOSTNAME = args[5]



def init():
    connector = MySQLdb.connect(host=SERVER ,db=DATABASE ,port=3307 ,user=USER ,passwd=PASS ,charset='utf8')
    cursor = connector.cursor()
    return cursor,connector

def commit_database(returnedList,cursor,connector):
    for beacon in returnedList:
            beacon_split = beacon.split(",")
            KEY_MAC = beacon_split[0]
            RSSI = int(beacon_split[5])
            DATE = time.strftime('%Y-%m-%d %H:%M:%S')
            insert_line = 'insert into wiss_data_2017.total_key_table(key_mac,rssi,base_station_hostname,date) values("%s","%d","%s","%s")' % (KEY_MAC,RSSI,HOSTNAME,DATE)
            print insert_line
            cursor.execute(insert_line)
    connector.commit()


if __name__ == "__main__":
    cursor,connector = init()
    returnedList = []
    try:
            sock = bluez.hci_open_dev(dev_id)
            print "ble thread started"

    except:
            print "error accessing bluetooth device..."
            sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

    while True:
            try:
                    returnedList = blescan.parse_events(sock, 10)
                    print "----------"
                    commit_database(returnedList,cursor,connector)
            except MySQLdb.OperationalError:
                    os.system("/home/pi/work/bluetooth/iBeacon-Scanner-/ressh.sh")
                    cursor,connector = init()
                    print("re-commit")
                    commit_database(returnedList,cursor,connector)

            time.sleep(5)
