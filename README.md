HLS-Segmenter-AWS-S3
====================

The is script for conver mp4 video file from source folder  to HLS streams and upload this stream to  to Amazon S3 bucket


install requrement

for script work you need boto modules for AWS 

#pip install boto

more datail about boto instalation -
http://boto.readthedocs.org/en/latest/getting_started.html

also script requred ffmpeg in you system
Best values compiled latest version from source

The is instruction for this

https://trac.ffmpeg.org/wiki/CompilationGuide

or simple install from repositories

Ubuntu debian
#sudo apt-get install ffmpeg 

CentOS
#sudo yum install ffmpeg





Configuration

in config.json you need set AWS credential 
path to source folder 
path for temp folder
path to ffmpeg
path to ffprobe

config in JSON format

{
"aws":{
		"access_key":"AWS Access Key",
		"secret_key":"AWS Secure Key",
		"s3bucket": "S3 bucket name"},
"tmp":"/tmp/tmp/",
"source":"/home/video/",
"log":"/home/log.log",
"ffmpeg": "/usr/bin/ffmpeg",
"ffprobe" : "/usr/bin/ffprobe"
}


Using

simple run 
./hls-segmenter.py
