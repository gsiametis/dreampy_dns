""" This is a simple python script for updating the
    DNS Custom Records in Dreamhost Nameservers using
    Dreamhost API commands.
    
    Provided under the MIT License (MIT). See LICENSE for details.

    """

#Python version check
import sys
if sys.version_info.major < 3:
    sys.exit("ERROR:\n Python 3 required. I refuse to run!")

import http.client
import re
import ssl
import uuid


#### We only need API Key and the domain to be updated.
####

API_Key = ""
domain = ""

# Set this to 1 if you want to update IPv6 record.
CHECKIPV6=0

### START

API_url = "api.dreamhost.com"
IP_Addr = ""
IPv6_Addr = ""
DNS_IP = ''
DNS_IPV6 = ''
current_records = ""


def rand_uuid():
    unique_id = str(uuid.uuid4())
    return unique_id

def get_dns_ip(records, protocol='ip'):
    """str->str"""
    if protocol == "ipv6":
        rec_type = "AAAA"
    else:
        rec_type = "A"
    for line in records:
        values = line.expandtabs().split()
        if values[3]==rec_type:
            return values[-2]
    return "NO_RECORD"

def get_dns_records():
    response = speak_to_DH("dns-list_records")
    relevant_records = []
    for line in response.splitlines():
        if domain in line:
            relevant_records.append(line)
    return relevant_records
    
def del_dns_record(protocol='ip'):
    if protocol == 'ipv6':
        rec_type = 'AAAA'
        Address = DNS_IP
    else:
        rec_type = 'A'
        Address = DNS_IPV6
        command = "dns-remove_record&record=" + domain + "&type=" + rec_type + "&value=" + Address
    response = speak_to_DH(command)
    return response

def add_dns_record(protocol='ip'):
    if protocol == "ipv6":
        rec_type = "AAAA"
        Address = IPv6_Addr
    else:
        rec_type = "A"
        Address = IP_Addr
    command = "dns-add_record&record=" + domain + "&type=" + rec_type + "&value=" + Address
    response = speak_to_DH(command)
    return response

def update_dns_record(protocol='ip'):
    if protocol == 'ipv6':
        dns_check = DNS_IPV6
    else:
        dns_check = DNS_IP
    if dns_check != "NO_RECORD":
        add_dns_record(protocol)
    else:
        del_dns_record(protocol)
        add_dns_record(protocol)

def make_url_string(command):
    """"str->str"""
    url = "/?key=" + API_Key + "&cmd=" +command + "&unique_id=" + rand_uuid()
    return url

def speak_to_DH(command):
    """str->str"""
    substring = make_url_string(command)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    conn = http.client.HTTPSConnection(API_url, 443, context=context)
    conn.request("GET", substring)
    body = conn.getresponse().read().decode('UTF-8')
    return body

def get_host_IP_Address(protocol='ip'):
    if protocol == 'ipv6':
        conn = http.client.HTTPConnection('checkipv6.dyndns.com')
        conn.request("GET","/index.html")
    else:
        conn = http.client.HTTPConnection('checkip.dyndns.com')
        conn.request("GET", "/index.html")
    body = cleanhtml(conn.getresponse().read().decode("UTF-8"))
    IP_Addr_list = body.rsplit()
    IP_Addr = IP_Addr_list[-1]
    return IP_Addr

def cleanhtml(raw_html):
  cleanr =re.compile('<.*?>')
  cleantext = re.sub(cleanr,'', raw_html)
  return cleantext

def make_it_so():
    if API_Key == '' or domain == '':
        sys.exit("ERROR:\n API_Key and/or domain empty. Nothing to do.")
    current_records = get_dns_records()
    DNS_IP = get_dns_ip(current_records)
    IP_Addr = get_host_IP_Address()
    if DNS_IP != IP_Addr:
        update_dns_record()
    if CHECKIPV6==1:
        DNS_IPV6 = get_dns_ip(current_records, "ipv6")
        IPv6_Addr = get_host_IP_Address('ipv6')
        if DNS_IPV6 != IPv6_Addr:
                update_dns_record('ipv6')

#### Let's do it!

make_it_so()
