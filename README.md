## Description
Contains different methods of uploading/installing RPMs to F5 BIG-IP.

1. Python script which loops over variable of BIG-IPs in the script.
2. Shell script which loops over a list of BIG-IPs and runs icrdk.
3. Ansible- tbd

This repo contains AS3 3.8 as an example RPM for F5 within its folder structure in `./files/`

#### Python

* `cd python/`
* Set VARS in the script starting around line 55.
* Run `python rpm_install.py`
* The script will loop over each BIG-IP defined within the scripts *bigips* var.


#### Shell/ICRDK

* `cd shell/`
* ICRDK is a tool for managing RPMs on a BIG-IP (view, deploy, delete, etc)
* Please view additional details for using the icrdk tool at https://github.com/f5devcentral/f5-icontrollx-dev-kit
  - rpmbuild must be installed on the machine running the script
  - Install icrdk with `icrdk@https://github.com/f5devcentral/f5-icontrollx-dev-kit.git -g`
* Update shell script to include correct variables at the top.
* Create a txt file in the current directory called “bigips.txt” which includes the desired bigips to have the RPM installed.
* Run `./rpm_install.sh`
