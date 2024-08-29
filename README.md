this is a basic script to run on Pi that let you input a hex code for a specific aircraft .
The script will monitor dump1090-fa
When the hex code is observed an email will be sent to you
It is set up for a Gmail account
You need a 16 digit Gmail app password that you get from your Gmail account
This is set up to run in a virtual environment at start up with the help of a systemd file
This is set up to monitor just one hex code
