import requests
import os.path
import sys
import librato
import json

class LibratoChartMaker():
	def read_api_key(self, fileName):
		if os.path.exists(fileName):
			f = open(fileName, "r")
			api_key = f.read()
			if(len(api_key) != 0):
				return api_key
			else:
				return "Key file is empty. Exiting"
				sys.exit()
		else:
			print "Key file not found. Exiting"
	    	sys.exit()

	def make_request(self, chart_id, duration, user, api_key):
		url = "https://metrics-api.librato.com/v1/snapshots"
		param1 = "subject[chart][id]="+str(chart_id)
		param2 = "subject[chart][source]=*"
		param3 = "subject[chart][type]=stacked"
		param4 = "duration="+str(duration)

		snap = requests.post(url+"?"+param1+"&"+param2+"&"+param3+"&"+param4, auth = (user, api_key))
		return snap.text

	# def send_request(self, acc_name, iv_id, api_key):
	# 	r = requests.get("https://" + acc_name + ".app.invoicexpress.com/invoices/" + iv_id + ".xml?api_key=" + api_key)
	# 	return r.text

	# def main(self, acc_name, iv_id, apkeyfile):
	# 	api_key = self.read_api_key(apkeyfile)
	# 	output = self.send_request(acc_name, iv_id, api_key)
	# 	return output

	def main(self, chart_id, duration, user, apkeyfile):
		api_key = self.read_api_key(apkeyfile)
		output = self.make_request(chart_id, duration, user, api_key)
		output = json.loads(output)
		return output['href']

class LibratoChartSender():

	def read_api_key(self, fileName):
		if os.path.exists(fileName):
			f = open(fileName, "r")
			api_key = f.read()
			if(len(api_key) != 0):
				return api_key
			else:
				return "Key file is empty. Exiting"
				sys.exit()
		else:
			print "Key file not found. Exiting"
	    	sys.exit()

	def send_request(self, snap_url, user, api_key):
		url = snap_url

		snap = requests.get(url, auth = (user, api_key))
		print snap
		return snap.text

	def main(self, snap, user, apkeyfile):
		api_key = self.read_api_key(apkeyfile)
		output = self.send_request(snap, user, api_key)
		print output
		output = json.loads(output)
		return output['image_href']



# librato = LibratoChartSender().main("pawel-1", "8927119", "librato.key")
make_snap = LibratoChartMaker().main("3419", "604800", "systems@rupeal.com", "librato.key")
print make_snap
get_snap = LibratoChartSender().main(make_snap, "systems@rupeal.com", "librato.key")
print get_snap


