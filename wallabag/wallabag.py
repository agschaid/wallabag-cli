#!/usr/bin/env python3

import conf
import getopt
import platform
import subprocess
from sys import argv
from sys import exit
from wallabag_help import show as help
import wallabag_add
import wallabag_config
import wallabag_delete
import wallabag_list
import wallabag_update

PROGRAM_VERSION = "0.3.0-alpha"

command = None
need_config = False

# Workaround for default non-unicode encodings in the Windows cmd and Powershell
# -> Analyze encoding and set to utf-8
if(platform.system() == "Windows"):
    codepage = subprocess.check_output(['chcp'], shell=True).decode()
    if "65001" not in codepage:
        subprocess.check_output(['chcp', '65001'], shell=True)

# Determine command or general standalone option
if len(argv) == 1 or argv[1] in {'-h', '--help'}:
    help(argv[0])
    exit(0)
elif argv[1] in {'-v', '--version'}:
    print(PROGRAM_VERSION)
    exit(0)
elif argv[1] in {'--about'}:
    print("wallabag-cli")
    print("© 2016 by Michael Scholz (https://mischolz.de)")
    print()
    print("This software is licensed under the GPLv3.")
    exit(0)
elif argv[1] in ["config", "add", "update", "delete", "list"]:
    command = argv[1]
    need_config = command != "config"
elif argv[1][0] != '-':
    print("Error: Invalid command \"{0}\".".format(argv[1]))
    print("Use \"{0}\" to see a full list of commands.".format(argv[0]))
    exit(-1)
else:
    print("Invalid option \"{0}\".".format(argv[1]))
    print("Use \"{0}\" to see a full list of options.".format(argv[0]))
    exit(-1)

if need_config and not conf.is_valid():
    i = input(
        "Could not find a valid config. Would you like to create it now? [Y/n] ")
    if str.lower(i) in ["y", "yes", ""]:
        wallabag_config.start()
    else:
        exit(0)

if command == "config":
    optionlist = argv[2:len(argv)]
    password = False
    oauth = False

    try:
        args = getopt.getopt(optionlist, "hcpo", [
                             "help", "check", "password", "oauth"])[0]
    except getopt.GetoptError as e:
        print("Error: Invalid option \"{0}\"".format(e.opt))
        print()
        exit(-1)
    for opt, arg in args:
        if opt in ('-h', '--help'):
            help(argv[0], command)
            exit(0)
        if opt in ('-c', '--check'):
            wallabag_config.check()
            exit(0)
        elif opt in ('-p', '--password'):
            password = True
        elif opt in ('-o', '--oauth'):
            oauth = True
    if password or oauth:
        if not conf.is_valid():
            print("Invalid existing config. Therefore you have to enter all values.")
            wallabag_config.start()
        else:
            wallabag_config.start(False, False, password, oauth)
    else:
        wallabag_config.start()

if command == "add":
    if "-h" in argv[2:len(argv)] or "--help" in argv[2:len(argv)]:
        help(argv[0], command)
        exit(0)

    if len(argv) < 3:
        print("Error: Missing URL to add")
        print()
        exit(-1)

    optionlist = argv[2:len(argv) - 1]
    url = argv[len(argv) - 1]
    title = None
    star = False
    read = False

    try:
        args = getopt.getopt(optionlist, "ht:sr", [
            "help", "title=", "starred", "read"])[0]
    except getopt.GetoptError as e:
        print("Error: Invalid option \"{0}\"".format(e.opt))
        print()
        exit(-1)
    for opt, arg in args:
        if opt in ('-t', '--title'):
            title = arg
        if opt in ('-s', '--starred'):
            star = True
        if opt in ('-r', '--read'):
            read = True
    wallabag_add.add(url, title, star, read)

if command == "update":
    if "-h" in argv[2:len(argv)] or "--help" in argv[2:len(argv)]:
        help(argv[0], command)
        exit(0)

    if len(argv) < 3:
        print("Error: Missing entry-id.")
        print()
        exit(-1)

    optionlist = argv[2:len(argv) - 1]
    entry_id = argv[len(argv) - 1]
    title = None
    toggle_star = False
    toggle_read = False
    set_required_parameter = False

    try:
        args = getopt.getopt(optionlist, "ht:sr", [
            "help", "title=", "starred", "read"])[0]
    except getopt.GetoptError as e:
        print("Error: Invalid option \"{0}\"".format(e.opt))
        print()
        exit(-1)
    for opt, arg in args:
        if opt in ('-t', '--title'):
            title = arg
            set_required_parameter = True
        if opt in ('-s', '--starred'):
            toggle_star = True
            set_required_parameter = True
        if opt in ('-r', '--read'):
            toggle_read = True
            set_required_parameter = True
    if not set_required_parameter:
        print("Error: No parameter given.")
        print()
        exit(-1)
    wallabag_update.update(entry_id, toggle_read, toggle_star, title)

if command == "delete":
    if "-h" in argv[2:len(argv)] or "--help" in argv[2:len(argv)]:
        help(argv[0], command)
        exit(0)

    if len(argv) < 3:
        print("Error: Missing entry-id.")
        print()
        exit(-1)

    optionlist = argv[2:len(argv) - 1]
    entry_id = argv[len(argv) - 1]
    force = False

    try:
        args = getopt.getopt(optionlist, "hf", [
            "help", "force"])[0]
    except getopt.GetoptError as e:
        print("Error: Invalid option \"{0}\"".format(e.opt))
        print()
        exit(-1)
    for opt, arg in args:
        if opt in ('-f', '--force'):
            force = True
    wallabag_delete.delete(entry_id, force)

if command == "list":
    if "-h" in argv[2:len(argv)] or "--help" in argv[2:len(argv)]:
        help(argv[0], command)
        exit(0)

    filter_starred = None
    filter_read = False
    count = None
    oldest = False

    optionlist = argv[2:len(argv)]
    url = argv[len(argv) - 1]

    try:
        args = getopt.getopt(optionlist, "hsurac:o", [
            "help", "starred", "unstarred", "read", "unread", "all", "count=", "oldest"])[0]
    except getopt.GetoptError as e:
        print("Error: Invalid option \"{0}\"".format(e.opt))
        print()
        exit(-1)

    for opt, arg in args:
        if opt in ('-s', '--starred'):
            filter_starred = True
        if opt in ('-u', '--unstarred'):
            filter_starred = False
        if opt in ('-r', '--read'):
            filter_read = True
        if opt in ('-a', '--all'):
            filter_read = None
        if opt in ('-a', '--all'):
            filter_read = None
        if opt in ('-c', '--count'):
            if arg == "all":
                arg = 65535
            try:
                arg = int(arg)
            except ValueError:
                print(
                    "Error: the argument for {0} has to be \"all\" or a number.".format(opt))
                exit(-1)
            count = arg
        if opt in ('-o', '--oldest'):
            oldest = True

    wallabag_list.list_entries(count, filter_read, filter_starred, oldest)
