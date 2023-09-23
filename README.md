# DDNS for Cloudflare

Usage:
```bash
git clone <ddns-cloudflare>
cd ddns-cloudflare
vi config.json
{
    "email": "your mail",
    "key": "your key",
    "interface": "your interface for getting ip"
    "zone_name": "zone name",
    "a_name": "your record"
}
####
```


```bash
crontab -e
@reboot python3 /path/autoupdate.py
```
