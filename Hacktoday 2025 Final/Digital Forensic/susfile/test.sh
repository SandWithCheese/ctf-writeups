for i in $(awk '/^[ ]*[0-9]+:/{print $1}' vba.oledump.txt | tr -d ':'); do
  python ~/bin/oledump/oledump.py -s $i -v extracted/vbaProject.bin > stream_$i.vba
done