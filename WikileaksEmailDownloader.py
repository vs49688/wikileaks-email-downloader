#! /usr/bin/env python

import os, errno, argparse, urllib2
from sys import argv as argv

email_db = {
	"podesta": {
		"download-id":"podesta-emails",
		"count":59028
    },
	"dnc": {
		"download-id":"dnc-emails",
		"count":44053
	},
	# Clinton emails use a different format, will implement later
	#"clinton": {
	#	"download-id":"clinton-emails",
	#	"count":30945
	#}
}

#curl -OJL https://wikileaks.org/dnc-emails//get/<id-here>
parser = argparse.ArgumentParser(description="Download emails from wikileaks.")
parser.add_argument("set", metavar="<email set>", type=str, help="The email set. Can be one of {0}".format(email_db.keys()))

parser.add_argument("--start", nargs=1, type=int, default=[1], help="The email index to start from (default: 0)")
parser.add_argument("--end", nargs=1, type=int, default=[-1], help="The email index to stop at. -1 = all of them (default: -1)")
parser.add_argument("--retries", nargs=1, type=int, default=[5], help="The retry count if downloading fails (default: 5)")

#args = vars(parser.parse_args(["--start", "4", "--end", "15", "podesta"]))
args = vars(parser.parse_args())
args["start"] = args["start"][0]
args["end"] = args["end"][0]
args["retries"] = args["retries"][0]

if args["retries"] < -1:
	args["retries"] = -1

if args["set"].lower() not in ["podesta", "dnc", "clinton"]:
	print "Invalid value for email set. Expected [\"podesta\", \"dnc\", \"clinton\"]"
	exit(1)

email_set = email_db[args["set"]]

if args["start"] > email_set["count"] or args["start"] < 1:
	print "Invalid value for start. %d >= %d or %d < 0" % (args["start"], email_set["count"], args["start"])
	exit(1)

if args["end"] < 1:
	args["end"] = email_set["count"]

if args["end"] > email_set["count"]:
	print "Invalid value for end. %d >= %d" % (args["end"], email_set["count"])
	exit(1)

print "Parameters: {0}".format(args)
print "Email Set:  {0}".format(email_set)

base_url = "https://wikileaks.org/{0}//get".format(email_set["download-id"])

try:
	os.mkdir(args["set"])
except OSError as e:
	if e.errno != errno.EEXIST:
		raise

for i in range(args["start"], args["end"] + 1):
	print "Downloading {0}".format(i)

	for r in range(0, args["retries"]):
		print "* Try {0}...".format(r + 1)
		try:
			email_url = "{0}/{1}".format(base_url, i)
			u = urllib2.urlopen(email_url)

			email_name = u.info()["Content-Disposition"].split('filename=')[1]
			if email_name[0] in ["\"", "'"]:
				email_name = email_name[1:-1]

			file_name = "{0}/{1:05d}_{2}".format(args["set"], i, email_name)

			with open(file_name, "w") as f:
				f.write(u.read())

			break
		except Exception as e:
			print " * Failed to download: {0}".format(e)

