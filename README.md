# uRADMonitorParser
A simple script to parse uRADMonitor KIT1 data from JSON page and save to MySQL.

## Making it work
Prepare your own database that will hold your uRADMonitor data. Mine has table called "Sensor" acting as a list of available sensors along with last value. Another table "Reading" contains all readings, while each one references table "Sensor". 

Modify the python source:
 * configure "config" variable with connection string to your DB
 * modify IP address of your uRADMonitor
 
## How to run
The script is intended to run via cron job, I do it this way - add following line to your crontab file:

* *     * * *   marty   python3 /home/marty/bin/uradmon_get.py

Of course modify your username and path to file. 


