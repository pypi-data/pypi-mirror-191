
# emtransmission
emtransmission is collecting data sysstem for Electronic monitoring reporter.
this system collect the image data in shipe and transfer the image data to system of shore side
using ftp

## Installing

Install from PyPI

    pip install emtransmission

## Usage

1. generate the config.ini file

[DEFAULT]
GEOMETRY = 1200x550
VIDEOCAPTURE = 0
PATH = recoding_file
TARGET_PATH = 
FTP_SERVER_IP = 
FTP_ID =
FTP_PASS =
#DIVX or XVID 
CODEC = DIVX
#Setting to AUTO or MANUAL
FPS = AUTO
#if u setting to AUTO it's not available
FPS_SET = 10
SETTING_FRAME_CNT = 1000
SNAP_FREQ = 10


[IP]
GEOMETRY = 1200x550
VIDEOCAPTURE = 
PATH = recoding_file
TARGET_PATH = 
FTP_SERVER_IP = 
FTP_ID = 
FTP_PASS = 
#DIVX or XVID
CODEC = DIVX
#Setting to AUTO or MANUAL
FPS = MANUAL
 #if u setting to AUTO it's not available
FPS_SET = 10
SETTING_FRAME_CNT = 1000
SNAP_FREQ = 10


2. import that package and run

```python
from emtransmission.fk_recoding import Fk_viewer
env ='default' # or 'ip'
t=Fk_viewer(env)

```
## TODO



