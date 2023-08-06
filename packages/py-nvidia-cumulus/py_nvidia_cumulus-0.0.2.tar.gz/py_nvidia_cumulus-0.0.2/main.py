# from cumulus.api import Cumulus
from cumulus import Cumulus

api = Cumulus(
    # url="http://worker01.air.nvidia.com:12544",  # leaf01
    url="http://worker07.air.nvidia.com:20269",  # rack02-leaf01
    auth=("cumulus", "something")
)
api.http_session.verify = False

print(api.root.get(endpoint_params={"rev": "applied", "diff": "1"}))
# print(api.revision.get())

# STEP 1
# interface = api.interface.get("lo")

# interface.patch(api.revision.rev,
#                 data={"10.255.255.2/32": {}},
#                 target_path="ip/address")

# api.system.create(data={"hostname": "leaf02"}, rev=api.revision.rev)

# # STEP 2
# config = {"bond0": {"bond": {"member": {"swp49": {}, "swp50": {}}}}}
# api.interface.create(config, api.revision.rev)

# # STEP 3
# config = {"domain": {"br_default": {"vlan": {"10": {}, "20": {}}}}}
# api.bridge.create(config, api.revision.rev)

# config = {"swp2": {"bridge": {"domain": {"br_default": {}}}},
#           "bond0": {"bridge": {"domain": {"br_default": {}}}}}

# api.interface.create(config, api.revision.rev)

# config = {"swp2": {"bridge": {"domain": {"br_default": {"access": 20}}}}}

# api.interface.create(config, api.revision.rev)

# # STEP 4
# config = {"vlan10": {"ip": {"address": {"10.0.10.3/24": {}}}},
#           "vlan20": {"ip": {"address": {"10.0.20.3/24": {}}}}}
# api.interface.create(config, api.revision.rev)

# interface = api.interface.get("vlan10", rev=api.revision.rev)
# config = {"vrr": {"address": {"10.0.10.1/24": {}},
#                   "mac-address": "00:00:00:00:1a:10",
#                   "state": {"up": {}}}}
# interface.patch(rev=api.revision.rev, data=config, target_path="ip")

# interface = api.interface.get("vlan20", rev=api.revision.rev)
# config = {"vrr": {"address": {"10.0.20.1/24": {}},
#                   "mac-address": "00:00:00:00:1a:20",
#                   "state": {"up": {}}}}
# interface.patch(rev=api.revision.rev, data=config, target_path="ip")

# api.revision.apply()
