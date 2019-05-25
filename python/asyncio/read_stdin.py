import sys
from datetime import datetime 
sin=sys.stdin.read()
now=datetime.now().strftime("%Y%m%d %H:%M")
with open("log.txt","w") as f:
    f.write(f"\n{now}\ntest.py sin:\n{sin}")
    
sys.stdout.write( f"\n{now} stdin.py ok")