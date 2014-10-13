#!/usr/bin/env python
#  upload to AWS S3 and clean up

# author Roman Sereda
# sereda.roman@gmail.com
#
# install dependenses
 
#sudo pip install boto


import json
import os.path
import logging
import subprocess
from boto.s3.connection import S3Connection
from boto.s3.key import Key


config_file = 'config.json'
json_data=open(config_file)
config = json.load(json_data)
json_data.close()

logging.basicConfig(filename=config['log'],level=logging.DEBUG)


###########################################################################
def s3_file_upload (config,filename,keyname):
	conn = S3Connection(config['aws']["access_key"],config['aws']["secret_key"])
	mybucket = conn.get_bucket(config['aws']["s3bucket"]) # select bucket
	k = Key(mybucket) # select key
	k.key = keyname #named new key
	k.set_contents_from_filename(filename) #upload new  file name
	k.set_acl('public-read') # set publis read access
	keylist = mybucket.list() # get list of files
	result = False
	ss= []
	for key in keylist:
		ss.append( key.name)
	if any(keyname in s for s in ss):
		logging.debug('s3_file_upload ' + 'Upload ' + keyname + "Completed")
		result = result | True
	rs = conn.close()
	return result


def isVideo (ffprobe,filename):
	if os.path.isfile(filename):
		command = [ ffprobe, "-v","quiet","-print_format","json","-show_format","-show_streams",  filename]
		process = subprocess.Popen(command, stdout=subprocess.PIPE)
		out, err = process.communicate()
		video_stat = json.loads(out)
		stat = []
		print video_stat
		if not len (video_stat) is 0 :
			if 'streams' in video_stat:
				logging.debug('isVideo ' + 'tested ' + filename )
				if len (video_stat['streams']) >= 2:
					logging.debug('isVideo ' + 'tested the is Vidoe' + filename )
					return video_stat
		return False


def s3_get_key_list (config):
	conn = S3Connection(config["aws"] ["access_key"], config["aws"] ["secret_key"])
	mybucket = conn.get_bucket(config["aws"] ["s3bucket"])
	key_list = []
	for key in mybucket.list():
		key_list.append(key.name)
	rs = conn.close()
	return key_list



def video_segmenter (ffmpeg, filepath , folder , stream_name):
	if os.path.isfile(filepath):
		command = [ ffmpeg, "-re" ,"-i",filepath,"-map","0","-codec:v","libx264","-codec:a","libfdk_aac","-codec:s", "copy", "-flags","-global_header","-f","segment","-segment_list",folder+"playlist.m3u8","-segment_time","10","-segment_format","mpegts",folder + "out%05d.ts"]
		process = subprocess.Popen(command, stdout=subprocess.PIPE)
		out, err = process.communicate()
		print out
		
		
def main (config):
	filelist =sorted( os.listdir(config["source"]))
	print filelist
	for filename in filelist:
		if isVideo (config["ffprobe"],config["source"] + filename):
			if filename.find('.') is -1:
				stream_name = filename.split('.',1)
			else :
				stream_name = filename
			video_segmenter (config["ffmpeg"], config["source"] + filename , config["tmp"] , stream_name)
			upload_list = sorted( os.listdir(config["tmp"]))
			if "playlist.m3u8" in upload_list and len (upload_list) > 2:
				 for ufile in upload_list:
					 logging.debug('main ' + 'procesed ' + " " + ufile )
					 if s3_file_upload (config,config["tmp"] + ufile, stream_name + "/" + ufile):
						 logging.debug('main ' + "Upload " + stream_name + "/" + ufile + "################" )
						 os.remove(config["tmp"] + ufile)
			
	print s3_get_key_list (config)



if __name__ == "__main__":
	main (config)
