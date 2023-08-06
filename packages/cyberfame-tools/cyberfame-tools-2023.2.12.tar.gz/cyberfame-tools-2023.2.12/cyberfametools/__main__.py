from time import time
import ipaddress
import sys

from . import IdentificationTool


tool = IdentificationTool()


def test_ip(idtool, rawip: str):
    start_t = time()
    ip = int(ipaddress.ip_address(rawip))
    vendor = idtool.get_vendor_by_ip(ip)
    print("TIME:", round(time() - start_t, 2), "IP:", rawip, "VENDOR:", vendor)


# @TODO: Add a proper argparser handling here.
if len(sys.argv) == 2:
    if sys.argv[1] == "generate":
        start_t = time()
        tool.export_packed()
        print("EXPORT TIME:", round(time() - start_t, 2))

else:
    # Testing
    test_ip(tool, "8.8.8.8")
    test_ip(tool, "204.152.18.71")
    test_ip(tool, "2405:8100:1111::")

