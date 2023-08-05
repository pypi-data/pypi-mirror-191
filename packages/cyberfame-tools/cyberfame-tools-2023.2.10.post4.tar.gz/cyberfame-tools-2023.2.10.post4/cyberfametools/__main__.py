from time import time
import ipaddress
import sys

from . import IdentificationTool


tool = IdentificationTool()

# @TODO: Add a proper argparser handling here.
if len(sys.argv) == 2:
    if sys.argv[1] == "generate":
        start_t = time()
        tool.export_packed()
        print("EXPORT TIME:", round(time() - start_t, 2))

else:
    # Testing
    start_t = time()
    ip = int(ipaddress.ip_address("204.152.18.71"))
    vendor = tool.get_vendor_by_ip(ip)
    print("TIME:", round(time() - start_t, 2), "VENDOR:", vendor)

    start_t = time()
    ip = int(ipaddress.ip_address("2405:8100:1111::"))
    vendor = tool.get_vendor_by_ip(ip)
    print("TIME:", round(time() - start_t, 2), "VENDOR:", vendor)

