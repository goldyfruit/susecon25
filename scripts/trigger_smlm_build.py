#!/usr/bin/env python3

from datetime import datetime, timezone
from os import environ
from requests import get, post
from random import choice
from versioning import read_version, update_version

# SUSE Multi-Linux Manager variables
smlm_host = environ.get("SMLM_HOST", "https://localhost")
smlm_endpoint = f"{smlm_host}/rhn/manager/api"
smlm_ssl = True
smlm_login = environ.get("SMLM_USER", "admin")
smlm_password = environ.get("SMLM_PASSWORD", "changeme")

# Retrieve authentication cookies
payload = {"login": smlm_login, "password": smlm_password}
login_resp = post(f"{smlm_endpoint}/auth/login", json=payload, verify=smlm_ssl)
cookies = login_resp.cookies

# Retrieve the list of available build hosts
build_hosts = get(
    f"{smlm_endpoint}/system/listSystemsWithEntitlement?entitlementName=container_build_host",
    cookies=cookies,
    verify=smlm_ssl,
)

# Pick a build host from the list randomly
random_build_host = choice(build_hosts.json().get("result"))

# Retrieve the version from the version file and generate a tag
update_version("build", "version.py")
version = read_version("version.py")
tag = f"{version[0]}.{version[1]}.{version[2]}"

# Construct the payload for the build request
now = datetime.now(timezone.utc)
build_payload = {
    "profileLabel": "bci-py312-fastapi",
    "version": tag,
    "buildHostId": random_build_host["id"],
    "earliestOccurrence": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
}

# Trigger the build request based on the payload from above and retrieved cookies
build_resp = post(
    f"{smlm_endpoint}/image/scheduleImageBuild",
    cookies=cookies,
    verify=smlm_ssl,
    data=build_payload,
)

# Check the response status code and print the result
if build_resp.status_code == 200:
    print("Image build scheduled successfully:", build_resp.json())
else:
    print("Failed to schedule image build:", build_resp.status_code, build_resp.text)
