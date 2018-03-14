avconv -i rtsp://10.2.2.19/live/ch01_0 -c copy -map 0 -f segment -segment_time 300 "capture-%03d.mp4"

ffmpeg -i rtsp://raspberrypi.local:8554/ -c copy -map 0 -f segment -segment_time 20 -segment_format mp4 -use_wallclock_as_timestamps 1 -reset_timestamps 1 "capture-%01d.mp4"