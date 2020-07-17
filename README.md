## Date Availability for Appointment

### Instructions to setup

These steps need to be run only once:
* Install chromedriver https://sites.google.com/a/chromium.org/chromedriver/downloads
  * Make sure you add path of chromedriver.exe to PATH.
* Install Python 3.x https://www.python.org/downloads/
  * Make sure you select the option for adding python to PATH.
  * Make sure you also select the option for installing pip. Both these options will be asked during setup.
* Make a new Gmail account and allow less secure app https://myaccount.google.com/lesssecureapps. New account is recommended but not necessary.
* Open new CMD or Powershell:
  * Go to the directory where the script is present. (You can go the directory in the File Explorer and then press `Shift+Right Click` and select "Open Powershell window here" or same for CMD)
  * Run the command `pip install selenium yagmail coloredlogs --user`
  * Run `python` so that the python interpreter is opened. Type the following commands in it.
  * `import yagmail`
  * `yagmail.register('mygmailemail', 'mygmailpassword')`
  * The last step needs to be done only once and it will save your password on your system so that it doesn't have to be stored in plaintext in the code.
  * Run `exit()` to exit.
* Change the to and from emails in the ENVIRONMENT CONFIG section of the code. Here you can also configure the sleep time in between checks.

### How to run

* Open CMD or Powershell and go to the directory where the script is located. (You can go the directory in the File Explorer and then press `Shift+Right Click` and select "Open Powershell window here" or same for CMD)
* Run `python main.py`
  
**Note:** The script can be **stopped** by pressing `Ctrl+C` anytime. To change the sleep time or any other config, first stop the script, change the required config and run it again.
