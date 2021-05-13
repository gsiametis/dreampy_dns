### dreampy_dns python script
Python script for updating Dreamhost.com DNS custom records.

This is a simple python script for updating the
DNS Custom Records in Dreamhost.com Nameservers using
Dreamhost API commands.

## License
Provided under the MIT License (MIT). See LICENSE for details.

## Requirements

Python 3 with urllib. Should be installed by default, if not use your package manager.

## Usage

First, you need a [DreamHost API key](https://panel.dreamhost.com/?tree=home.api) with full DNS permissions.

Next, you'll need to set the API key and domain that will be updated. If you are updating a subdomain, you don't need to have the record pre-set in the Dreamhost UI.

You can execute the script in two ways:

* Update the variables within the python script
* Set the `DREAMHOST_API_KEY` and `DREAMHOST_UPDATE_DOMAIN` environment variables

Script runs from CLI in the usual way, eg.:

```
DREAMHOST_API_KEY=key DREAMHOST_UPDATE_DOMAIN=domain python3 ./dreampy_dns.py
```

Or you can run it directly after making it executable:

```
chmod +x ./dreampy_dns.py
./dreampy_dns.py
```


## IPv6

You can update your domain with an IPv6 (AAAA) record also, if you would like to do so.
In that case, CHECKIPV6 variable must be set to anything other than the default 0.

## Comments

The script may seem a bit crude and dirty -and it is. This is a script I wrote for personal use
when I had minimal experience with Python and I decided to make it publicly available, in case anyone else needed it.
If memory serves, this project started when a similar script I was using and was written in Perl stopped working around 2012. So, I decided to write my own script to update my dynamic IP address home server domain.
As of January 2019 I am no longer using Dreamhost so I can't verify anymore that it does work. However, APIs do not change often, and I hope that this little piece of code will be useful for many more years to anyone that needs it.

## Kudos
Thanks to [pfidr34](https://github.com/pfidr34) for his commits.
Special thanks to [Bryan Sutula](https://github.com/sutula) for his feedback, his commits and for validating my changes worked correctly.

## Bugs
No serious (if any) bugs reported. If you find one, and corrected it, please make a pull request. If you don't know how to correct it, you can raise an issue on github.

## Donations
Bitcoin address: 1MXXVw5zyGJZ8rRxXLbUxF4wpqhZ24YMDk<br/>
Paypal: \<github nickname\> at Gmail.

## Related

* https://github.com/clempaul/dreamhost-dynamic-dns