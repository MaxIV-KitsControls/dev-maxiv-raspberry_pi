import tango

dev_info = tango.DbDevInfo()
dev_info.server = "RaspberryPiIO/test"
dev_info._class = "RaspberryPiIO"
dev_info.name = "test/r_pi_io/1"

db = tango.Database()
db.add_device(dev_info)
