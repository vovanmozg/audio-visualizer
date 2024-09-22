echo > filelist.txt
for f in 1/*.mp3; do echo "file '$f'" >> filelist.txt; echo "file 'silence.mp3'" >> filelist.txt; done
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp3