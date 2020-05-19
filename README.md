# Wikileaks Downloader

## This repo is archived, see https://github.com/vs49688/dnc-downloader


A simple script that downloads all the DNC and Podesta emails from Wikileaks into their original format, so they can be 
loaded into an email client for further perusal.

### How to run
* Just execute the script on any modern/semi-modern Linux system.
* I'd imagine that Cygwin would work too, but I haven't tested it.

### Usage
```
usage: WikileaksEmailDownloader.py [-h] [--start START] [--end END]
                                   [--retries RETRIES]
                                   <email set>

Download emails from wikileaks.

positional arguments:
  <email set>        The email set. Can be one of ['podesta', 'dnc']

optional arguments:
  -h, --help         show this help message and exit
  --start START      The email index to start from (default: 0)
  --end END          The email index to stop at. -1 = all of them (default:
                     -1)
  --retries RETRIES  The retry count if downloading fails (default: 5)
```