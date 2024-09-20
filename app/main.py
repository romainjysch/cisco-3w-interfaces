#!/usr/bin/env python3

import yaml
import netmiko
import logging
import datetime

from functions import logs_configuration, get_username, get_password, get_csr_devices, launch_analysises


def main():
    logs_configuration()
    launch_analysises(get_csr_devices(username=get_username(), password=get_password()))


if __name__ == "__main__":
    main()
