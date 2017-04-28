#!/usr/bin/python

import os
import argparse
import urllib2
import json
import requests
import json

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c','--current_hostname')
	parser.add_argument('-n','--new_hostname')
	parser.add_argument('-p','--profile')
	args=vars(parser.parse_args())
	old= args['current_hostname']
	new= args['new_hostname']
	profile= args['profile']
	data={"current":old,"new":new,"profile":profile}
	return data


def set_ipam():
	i=get_args()
	m=i['current']
	print "Wroking on %s"%m
	url="http://<IPAM URL>/api/search/?hostname=.*%s.*&filter=itag,hostname,discovered_data"%m
	d=urllib2.urlopen(url).read().decode('utf-8')
        f=json.loads(d)
	data=f['result']
	itag=data[0]['itag']	
	print "Updating itag %s"%(itag)
	url='http://<URL>/api/hostprofile/set/'
	data=json.dumps({"itag":"%s"%(itag),"hostname":"%s"%(i['new']),"profile":"%s"%(i['profile'])})
	r=requests.post(url,data)
	print (r.status_code,r.text)

def set_dns():
	i=get_args()
	print "Updating DNS for %s"%(i['current'])
	dns=os.system('<script> -r A --host %s -n %s'%(i['current'],i['new']))
	print dns


def delete_old():
	i=get_args()
        print "Deleting DNS for %s"%(i['current'])
        dns=os.system('<script> -r A --host %s'%(i['current']))
        print dns



def main():
	set_ipam()
	set_dns()
        delete_old()


if __name__=="__main__":
	main()


