#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime
import shutil
from typing import List

# This is the original howto..
# We provide some example configuration which has to be modified by you
# ```
# for i in *.example.yml; do cp "$i" "${i/example.yml/override.yml}"; done
# cp .env.example .env
# cp enabled_services.example.sh enabled_services.sh
# cp landing/items.example.toml landing/items.toml
# cp health/checkup.sample.json health/checkup.json
# cp health/config.sample.js health/config.js
# ```
# 
# After this is done, you definitely should edit `.env`.


# source->target mapping for files of a first installation
localize = {
    "enabled_services.example.sh": "enabled_services.sh",
    ".env.example": ".env",
    "landing/items.example.toml": "landing/items.toml",
    "health/checkup.sample.json": "health/checkup.json",
    "health/config.sample.js": "health/config.js",
}

components = [
    ["fridolean", True],
    ["health", True],
    ["keycloak", True],
    ["landing", True],
    ["md", True],
    ["taiga", True],
    ["talk", True],
    ["woi", True],
]

# make sure that we will not override existing local files
def check_existing_files():
    existing = []
    for i in localize.values():
        if os.path.exists(i):
            existing += [i]
    return existing

def do_backup(folder, files):
    os.makedirs(folder)
    for f in files:
        if os.path.exists(f):
            try:
                os.makedirs(os.path.join(folder, os.path.dirname(f)))
            except:
                pass
            os.rename(f, os.path.join(folder, f))

def copy_example_files(disabled_components):
    for source, target in localize.items():
        install = True
        for item in disabled_components:
            if source.find(item) >= 0:
                install = False
        if install:
            shutil.copy2(source, target)

def write_enabled_services(components):
    enabled_services = [item for item, enabled in components if enabled]
    with open("enabled_services.sh", "w") as f:
        f.write("""#!/bin/bash
export ENABLED_S="%s"
""" % " ".join(enabled_services))

def update_env(domain, password, secret, port):
    data = ""
    with open(".env") as f:
        data = f.read()
    data = data.replace("example.org", domain)
    data = data.replace("your_password", password)
    data = data.replace("1234qwe123qwe456", secret)
    for i in range(30):
        data = data.replace("=40%0d" % i, "=%d" % (port + i))
    with open(".env", "w") as f:
        f.write(data)

def update_landing(domain : str, disabled_components : List[str]):
    with open("landing/items.toml") as f:
        data = f.read()
    data = data.replace("example.org", domain)
    lines = data.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("url"):
            for item in disabled_components:
                if line.find(item) >= 0:
                    j = i
                    while not line.startswith("[[items]]"):
                        line = lines[j]
                        lines[j] = "# " + lines[j]
                        j -= 1
    data = "\n".join(lines)
    with open("landing/items.toml", "w") as f:
        f.write(data)

def update_health(domain, disabled_components):
    data = ""
    with open("health/checkup.json") as f:
        data = f.read()
    data = data.replace("example.org", domain)
    lines = data.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        if line.strip().startswith('"endpoint_url'):
            for item in disabled_components:
                if line.find(item) >= 0:
                    j = i
                    while True:
                        line = lines[j]
                        if lines[j][0] != "/":
                            lines[j] = "// " + lines[j]
                        if line.strip(" /\t").startswith("{"):
                            break
                        j -= 1
                    while True:
                        line = lines[j]
                        if lines[j][0] != "/":
                            lines[j] = "// " + lines[j]
                        if line.strip(" /\t").startswith("}"):
                            break
                        j += 1
    data = "\n".join(lines)
    with open("health/checkup.json", "w") as f:
        f.write(data)

def main():
    print("Welcome to the LINC-installer")
    existing = check_existing_files()
    if existing != []:
        backup_target = "backup_"+datetime.datetime.now().strftime("%y_%m_%d_%s")
        while True:
            answer = input("Warning: this is not your first install.. should I backup existing files to %s? (Y/n) " % backup_target)
            if len(answer) < 1 or answer[0].upper() == "Y":
                do_backup(backup_target, existing)
                break
            elif answer[0].upper() == "N":
                break
    print("Select the components you want to install")
    while True:
        comp_str = []
        for idx, item in enumerate(components):
            comp_str += ["%d: [%s] %s" % (idx+1, (" ", "x")[item[1]], item[0])]

        print("Toggle the components by their number [x] means it will be installed. Continue by pressing Enter.")
        print(", ".join(comp_str))
        answer = input("")
        answer_int = False
        try:
            answer_int = int(answer)
        except:
            pass
        if answer_int != False:
            try:
                # toggle
                components[answer_int-1][1] ^= True
            except:
                pass
        else:
            answer = input("Are you sure with your selection? (Y/n) ")
            if len(answer) < 1 or answer[0].upper() == "Y":
                break
    disabled_components = [item for item, enabled in components if not enabled]

    copy_example_files(disabled_components)
    write_enabled_services(components)

    # configure .env
    domain = ""
    while True:
        print("What is your domain under which you want to host all? (e.g. example.com will then set up linc.example.com, woi.example.com etc.)")
        domain = input("")
        answer = input("Is '%s' correct? (Y/n) " % domain)
        if len(answer) < 1 or answer[0].upper() == "Y":
            break
    port = ""
    while True:
        print("Specify a start-port for which all the applications are set (e.g., 4000 will result in 4000,4001,4002..4030 assigned)")
        port = input("")
        try:
            port = int(port)
        except:
            port = 4000
        answer = input("Is '%d' correct? (Y/n) " % port)
        if len(answer) < 1 or answer[0].upper() == "Y":
            break
    password = ""
    while True:
        print("Password for admin-access (keycloak, rocketchat) - *Warning* will be displayed here")
        password = input("")
        answer = input("Is '%s' correct? (Y/n) " % password)
        if len(answer) < 1 or answer[0].upper() == "Y":
            break
    secret = ""
    while True:
        print("Secret string which is used internally in some services - *Warning* will be displayed here")
        secret = input("")
        answer = input("Is '%s' correct? (Y/n) " % secret)
        if len(answer) < 1 or answer[0].upper() == "Y":
            break
    print("updating env")
    update_env(domain, password, secret, port)
    if "landing" not in disabled_components:
        print("updating landing")
        update_landing(domain, disabled_components)
    if "health" not in disabled_components:
        print("updating health")
        update_health(domain, disabled_components)



if __name__ == "__main__":
    main()
