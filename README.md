# Network Cable Analyzer

## Context

As a network engineer who is learning Python programming, I often encounter situations where network cables are left connected to switches but are no longer in use. To address this issue, I have developed this script to identify network interfaces that have been inactive for an extended period, specifically 3 weeks or more. By generating a text file with the relevant information, the network team or helpdesk can easily locate and remove the unused cables.

The script utilizes the Netmiko library to establish SSH connections to network devices and retrieve interface information by using Cisco CLI commands. It analyzes the last input value (from the 'sh int' command) of each not connected interface and identifies those that have not received any input for at least 3 weeks. The results are then written to a text file for further action.

## Installation

To run the script, please install a virtual env and the required deps :

```
cd /path/to/the/project
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If Python is not installed :

```
brew install python
```

If Homebrew is not installed :

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

If permissions need to be updated :

```
chmod -R 755 /path/to/the/project
```

## Usage

### YAML Configuration (csr.yaml)

Before running the script, make sure to replace the following placeholders (normally correct for HEP-VD usage ins csr-hep.yaml) :

- 'insert_switch_name' : replace with the name of the switch
- 'insert_ip' : replace with the IP address or FQDN

### Run

```
cd /path/to/the/project
source .venv/bin/activate
python app/main.py
```

### When running

- When running, the script will ask you to enter a username with privileged EXEC mode access on switches
- The script will also ask you to enter the username's password