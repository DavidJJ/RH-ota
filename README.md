

Easy mange and update your RotorHazard installation. 

Additional features like nodes flashing also included.


If you want all hardware functionalities - visit:

[Instructables page](https://www.instructables.com/id/RotorHazard-Updater/)

or check how_to folder - look for PDF file.

Yo may also check [update-notes](update-notes.md)
Software is designed to run using python 2.7.
Will be updated to be python 3 friendly, when
RotorHazard software will be converted as well.

Commands to download the repo onto Raspberry Pi or Linux system:

	cd ~
	sudo apt install zip unzip
	wget https://codeload.github.com/szafranski/RH-ota/zip/master -O tempota.zip
	unzip tempota.zip
	rm tempota.zip
	mv RH-ota-* RH-ota

Commands to open the software:
	
	sudo apt install python --> if needed
	
	cd ~/RH-ota
	python update.py
