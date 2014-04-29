### dreampy_dns python script
Python script for updating Dreamhost.com DNS custom records.

This is a simple python script for updating the
DNS Custom Records in Dreamhost.com Nameservers using
Dreamhost API commands.
    
## License
Provided under the MIT License (MIT). See LICENSE for details.

## Python version

Script uses Python v.3 and some standard modules. 

## Usage

No arguments required, all required info provided inside the script itself.
Script requires API_key and domain variables to be filled in. API_Key is the
API Key you have created in Dreamhost's control panel (it must have permission 
for the DNS commands). domain is the DNS record to be updated, eg. 
myawesomedyndomain.example.com.
Script runs from CLI with the usual way, eg.:
python3.3 /path/to/script/dreampy_dns.py


## IPv6

You can update your domain with an IPv6 (AAAA) record also, if you would like to do so.
In that case, CHECKIPV6 variable must be set to 1.

## Comments

The script may seem a bit crude and dirty. This is a script I wrote for personal use 
and decided to make it publicly available, in case anyone else needed it.

