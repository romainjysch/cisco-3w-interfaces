import os
import re
import sys
import yaml
import netmiko
import logging
import datetime


def logs_configuration():
    try:
        # Get the absolut path to the logs folder :
        log_directory = os.path.abspath("logs")
        # If logs folder does not exist, create it :
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        # Get the absolut path to the log file of the day :
        log_file_path = os.path.join(log_directory,
                                     datetime.date.today()
                                     .strftime("%Y-%m-%d") + "_cisco-3w-interfaces.log")
        # Logs configuration :
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename=log_file_path)
    except Exception as e:
        logging.error(f"A problem has occured : {e}")
        sys.exit()


def get_username():
    return input("Enter a username with privileged EXEC mode access : ")


def get_password():
    return input("Enter the username's password : ")



def get_csr_devices(username, password):
    try:
        # Read the YAML config file :
        with open("csr.yaml") as file:
            content = file.read()
        # Replace constants with username and password :
        content = content.replace("USERNAME_CONSTANT", username).replace("PASSWORD_CONSTANT", password)
        # Load CSR from the YAML config file :
        config = yaml.safe_load(content)
        # Return all CSR devices :
        return config["devices"]
    except FileNotFoundError:
        logging.error("CSR devices file not found.")
        sys.exit()
    except Exception as e:
        logging.error(f"A problem has occured : {e}")
        sys.exit()


def launch_analysises(devices):
    print("Script starting...")
    # Create file for the current analysis :
    filename = create_filename()
    # Loop through the CSR devices and perform analysis :
    with open(filename, "a") as file:
        for device in devices:
            perform_analysis(device["ip"], device["username"], device["password"], file)
    print("Script ending...")


def perform_analysis(ip, username, password, file):
    try:
        # Create the CSR object using the dictionnary :
        csr = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }
        # Establish the SSH connection :
        connection = netmiko.ConnectHandler(**csr)
        # Discover the hostname from the prompt :
        hostname = connection.send_command("sh run | i hostname")
        hostname, device = hostname.split(" ")
        print(f"Analysing interfaces for {device}...")
        # Write the current CSR hostname in the file :
        file.write(device + " :\n")
        # Get every not connected interface on the current CSR device on a table :
        notconnected_interfaces = connection.send_command("show int status | i notconnect").splitlines()
        # Loop through every element of the table in order to check the last input :
        for interface in notconnected_interfaces:
            # Get interface name :
            interface_name = interface.strip().split()[0]
            # If not never, write the last input in the file :
            if interface_name.startswith("T"):
                continue
            last_input_value = get_last_input_value(connection, interface_name)
            if not "not_applicable" in last_input_value:
                file.write(interface_name + " : " + last_input_value + "\n")
    except Exception as e:
        logging.error(f"A problem has occured : {e}")
        sys.exit()


def get_last_input_value(connection, interface_name):
    try:
        # Get the last input value for the current interface :
        last_input_value = connection.send_command("sh int " + interface_name) \
            .splitlines()[10].split(",")[0].split("Last input ")[1].strip()
        # Sort interfaces by 3w or more and return the last input value :
        match = re.search(r'(\d+)w', last_input_value)
        if match:
            value = int(match.group(1))
            if value >= 3:
                return last_input_value
            else:
                return "not_applicable"
        else:
            return "not_applicable"
    except Exception as e:
        logging.error(f"A problem has occured : {e}")
        sys.exit()


def create_filename():
    try:
        # Get the absolut path to the current file :
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Alter the path in order to include a new directory for the txt files :
        files_directory = os.path.join(current_directory, "files")
        # If files directory does not exist, create it :
        if not os.path.exists(files_directory):
            os.makedirs(files_directory)
        # Return a txt file with the day of the day :
        today = datetime.date.today().strftime("%Y-%m-%d")
        return os.path.join(files_directory, f"{today}_analysis.txt")
    except Exception as e:
        logging.error(f"A problem has occured : {e}")
        sys.exit()


def main():
    logs_configuration()
    devices = get_csr_devices(username=get_username(), password=get_password())
    launch_analysises(devices)


if __name__ == "__main__":
    main()
