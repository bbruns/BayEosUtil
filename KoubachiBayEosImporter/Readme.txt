
Command to start script
__________________________________________________________________________
python KoubachiBayEosImporter.py <baseFolder>
   <baseFolder> - specifies folder in which logging config-file "weatherStation.conf" resides


Development
____________________________________________
Scripts have been development with Visual Studio 2010 with Python Tools for Visual Studio (see Codeplex)


Deployment
________________________________________________________________________
currently deployed (sudo python /home/pi/Desktop/koubachiSensor/KoubachiBayEosImporter.py /home/pi/Desktop/koubachiSensor) at ibg2332 (Rasperry Pi)
invoked by crond -> see /etc/crontab (*/60 * * * * root python /home/pi/Desktop/koubachiSensor/KoubachiBayEosImporter.py /home/pi/Desktop/koubachiSensor)
logs to box.com logging-dir "Logs\koubachiImporter.txt" <-> https://www.box.com/files/0/f/662440797/Logs
