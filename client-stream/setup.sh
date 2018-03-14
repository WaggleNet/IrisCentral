apt-get install -y supervisor vlc
modprobe bcm2835-v4l2
raspivid -o - -t 0 -w 1920 -h 1080 -fps 30 -b 6000000 | cvlc -v stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264

# Get your stuff at rtsp://hostname:8554/

sudo rmmod bcm2835-v4l2
sudo modprobe bcm2835-v4l2
cvlc v4l2:///dev/video0 --v4l2-width 1920 --v4l2-height 1080 --v4l2-chroma h264 --sout '#standard{access=http,mux=ts,dst=0.0.0.0:12345}' :demux=h264



curl http://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -
# Add to sources.list
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main

sudo apt-get update
sudo apt-get install uv4l uv4l-raspicam

uv4l --driver raspicam --auto-video_nr --framerate 30 --extension-presence=0 --encoding=h264 --bitrate=6000000
cvlc v4l2c:///dev/video0:width=1920:height=1080:chroma=H264 --sout '#rtp{sdp=rtsp://:8554/}' --demux h264