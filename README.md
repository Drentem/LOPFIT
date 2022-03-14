# Lots of Phrases Fit In This (LOPFIT)
## System Requirements
* Operating System
	* Windows >= 10
	* MacOS
* Browser
  * Google Chrome
  * **Note:** Other browsers may work. Google Chrome was the only browser tested. If you find another browser that works fine, please submit an ***Issue*** for this to be updated accordingly.
* Python >= 3.9
## Setup
Download LOPFIT.
	* Either download and extract the code as a ZIP file or pull it down via git
	`git repo clone Drentem/LOPFIT`
	 * **Note:** LOPFIT does not require anything to be installed by pip. They are included already in the includes folder. If you do run into a dependency issue, please create an ***Issue*** to have it resolved.
## How to use
1. Run LOPFIT from the base folder.
	* **Windows**
	`pythonw.exe LOPFIT.py`
	* **MacOS**
	`python3 LOPFIT.py &`
2. Use the Menu or System Tray icon to access LOPFIT's GUI. It will appear in your default web browser.
![System Tray Icon](LOPFIT/favicon.ico)
## Packages used (Thank you to the owning teams)
### GUI
* Webserver: [Flask](https://palletsprojects.com/p/flask/)
* Icon Font: [FontAwesome](https://fontawesome.com/)
* Text Editor: [Quill JS](https://quilljs.com/)
### Database
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy)
### Input detection
* [Keyboard](https://github.com/boppreh/keyboard)
* [pynput](https://github.com/moses-palmer/pynput)
### System Tray/Menu icon
* MacOS: [pystray](https://github.com/moses-palmer/pystray)
* Windows: [rumps](https://github.com/jaredks/rumps)
