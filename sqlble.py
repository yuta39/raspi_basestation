import blescan
import time
import bluetooth._bluetooth as bluez
import commands
import MySQLdb

dev_id = 0
beacon_data_old = []

SERVER = args[1]
DATABASE = args[2]
USER = args[3]
PASS = args[4]
HOSTNAME = args[5]

connector = MySQLdb.connect(host=SERVER ,db=DATABASE ,user=USER ,passwd=PASS ,charset='utf8')
cursor = connector.cursor()


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
                for beacon in returnedList:
                        beacon_split = beacon.split(",")
                        KEY_MAC = beacon_split[0]
                        RSSI = int(beacon_split[5])
                        DATE = time.strftime('%Y-%m-%d %H:%M:%S')
                        insert_line = 'insert into wiss_data_2017.total_key_table(key_mac,rssi,base_station_hostname,date) values("%s","%d","%s","%s")' % (KEY_MAC,RSSI,HOSTNAME,DATE)
                        print insert_line
                        cursor.execute(insert_line)

                connector.commit()
                time.sleep(5)

        except OperationalError:
                commands.getoutput("/home/pi/work/bluetooth/iBeacon-Scanner-/ressh.sh")

