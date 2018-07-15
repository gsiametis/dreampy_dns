""" This is a simple python script for updating the
    DNS Custom Records in Dreamhost Nameservers using
    Dreamhost API commands.
    
    Provided under the MIT License (MIT). See LICENSE for details.

    """

#Python version check
import sys
import syslog
if sys.version_info.major < 3:
    msg = 'Python 3 required. I refuse to run!'
    syslog.syslog(syslog.LOG_ERR, msg)
    sys.exit(msg)

import http.client
import re
import ssl
import uuid
import logging
#### We only need API Key and domain to be updated.
#### Domain can be the root or a subdomain.
#### example.com or sub.exmple.com
####

API_Key = ""
domain = ""
#### Set the logging level.
logging.basicConfig(level=logging.ERROR)
# Set this to 1 if you want to update IPv6 record.
CHECKIPV6=0

### START

API_url = "api.dreamhost.com"
IP_Addr = ""
IPv6_Addr = ""
DNS_IP = ""
DNS_IPV6 = ""
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
        if values[2]==domain and values[3]==rec_type:
            logging.info('Current %s record for %s is: %s', protocol, domain,  values[-2])
            return values[-2]
        logging.warning('No %s record found for %s', protocol, domain)
    else:
        return "NO_RECORD"

def get_dns_records():
    response = speak_to_DH("dns-list_records")
    relevant_records = []
    for line in response.splitlines():
        if domain in line:
            relevant_records.append(line)
    logging.debug('All relevant DNS Records for %s: \n %s', domain, relevant_records)
    return relevant_records
    
def del_dns_record(protocol='ip'):
    global DNS_IPV6
    global DNS_IP
    record = ""
    if protocol == 'ipv6':
        rec_type = 'AAAA'
        record = DNS_IPV6
        print(record)
        print(DNS_IPV6)
    else:
        rec_type = 'A'
        record = DNS_IP
        print(record)
        print(DNS_IP)
    logging.info('The current %s record is: %s', protocol, record)
    if record == '':
        logging.error("Can't delete record, value passed is empty")
        sys.exit("Weird")
    command = "dns-remove_record&record=" + domain + "&type=" + rec_type + "&value=" + record
    response = speak_to_DH(command)
    if 'error' in response:
        logging.error('Error while deleting %s record: \n %s', protocol, response)
    logging.debug('Tried to del %s record and here is what Dreamhost responded: \n %s', protocol, response)

def add_dns_record(protocol='ip'):
    global IPv6_Addr
    global IP_Addr
    Address = ""
    if protocol == "ipv6":
        rec_type = "AAAA"
        Address = IPv6_Addr
    else:
        rec_type = "A"
        Address = IP_Addr
    logging.info('Our current %s address is: %s', protocol, Address)
    command = "dns-add_record&record=" + domain + "&type=" + rec_type + "&value=" + Address
    response = speak_to_DH(command)
    if 'error' in response:
        logging.error('Error while adding %s record: \n %s', protocol, response)
    logging.debug('Tried to add %s record and Dreamhost responded with: \n %s', protocol, response)

def update_dns_record(protocol='ip'):
    global DNS_IP
    global DNS_IPV6
    if protocol == 'ipv6':
        dns_check = DNS_IPV6
    else:
        dns_check = DNS_IP
    logging.debug('dns_check: %s', dns_check)
    if dns_check == "NO_RECORD":
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
    logging.debug('Will try to speak to Dreamhost, here is what I will tell: %s', command)
    substring = make_url_string(command)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    conn = http.client.HTTPSConnection(API_url, 443, context=context)
    conn.request("GET", substring)
    body = conn.getresponse().read().decode('UTF-8')
    logging.debug('Here is what Dreamhost responded: %s', body)
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
    global DNS_IP
    global DNS_IPV6
    global IP_Addr
    global IPv6_Addr
    if API_Key == '' or domain == '':
        msg = 'API_Key and/or domain empty. Edit dreampy_dns.py and try again.'
        syslog.syslog(syslog.LOG_ERR, msg)
        sys.exit(msg)
    current_records = get_dns_records()
    DNS_IP = get_dns_ip(current_records)
    logging.debug('DNS_IP: %s', DNS_IP)
    IP_Addr = get_host_IP_Address()
    logging.debug('IP_Addr: %s', IP_Addr)
    if DNS_IP != IP_Addr:
        logging.info('Address different, will try to update.')
        update_dns_record()
    else:
        logging.info('IP Record up-to-date.')
    if CHECKIPV6==1:
        DNS_IPV6 = get_dns_ip(current_records, "ipv6")
        IPv6_Addr = get_host_IP_Address('ipv6')
        if DNS_IPV6 != IPv6_Addr:
                update_dns_record('ipv6')
        else:
            logging.info('IPv6 Record up-to-date.')

#### Let's do it!

make_it_so()
