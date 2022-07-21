import hid
import time

for h in hid.enumerate():
	print(hex(h['vendor_id']),hex(h['product_id']))