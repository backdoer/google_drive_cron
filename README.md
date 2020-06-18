# google_drive_cron

`drive_sync.py` pulls data from google drive takeout onto computer

`external_drive_sync.py` looks to see if there's an external hard drive available and then moves the takeout to it if so


Cron jobs:
```
0 * * * *  /usr/local/bin/python3 /Users/tylerdoermann/Documents/Random/drive_cron/drive_sync.py
30 * * * *  /usr/local/bin/python3 /Users/tylerdoermann/Documents/Random/drive_cron/external_drive_sync.py
```
