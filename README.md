# PowerUp
PowerUp is a small application that prevents your local/remote machine from going to sleep, shutdown and screen lock.

**In case you want to run binary app direcly:**
  1. Download the release zipped file.
  2. Double click PowerUp_GUI.exe if you want to run in GUI or open a terminal and run PowerUp_CLI.exe if you wan to run in CLI mode.
  
**In case you want to convert source code manually to binary app:**
  1. Make sure you have python installed on your machine (run in cmd: python --version to check).
  2. Clone or download the repo and install required external libraries using: pip install -r requirements.txt
  3. Convert to GUI by running the follwoing comand : pyinstaller GUI.py --icon=icon.ico --clean --name=PowerUp_GUI.exe --onefile --noconsole, binary will be in dist folder
  4. Convert to CLI by running the follwoing comand : pyinstaller CLI.py --icon=icon.ico --clean --name=PowerUp_CLI.exe --onefile --console, binary will be in dist folder
