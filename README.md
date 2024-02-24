# Kodi Historian

Keep track of your viewing history - without installing extra Kodi plugins.

## Getting Started

1. Checkout this project to your computer (or just copy `main.py`, `config-template.ini`
   and `requirements.txt`).
2. Make sure that at least Python 3.9 is installed.
3. Configure a [virtual environment](https://docs.python.org/3/library/venv.html) for
   Python to install the necessary libraries inside it. This way you won't need
   administrative access and you are independent of any changes in installed
   system Python libraries. Go to the directory where you put the files in step 1
   and execute the command:
   `python3 -m venv venv`
4. Now install the libraries with the command:
   `venv/bin/pip3 install -r requirements.txt`
5. Before running the script for the first time, prepare Kodi: go to Settings 
   → Services → Webserver and activate "Allow control of Kodi via HTTP". It's 
   advised to set a password or else anyone in your network will be able to control
   Kodi. More information can be found [here](https://kodi.wiki/view/Webserver).
6. Copy `config-template.ini` to `config.ini` and edit it to contain your data.
   Use the same values you entered in Kodi in the previous step.
7. Now you can run `main.py`, which will write its output to standard out.

## Infrastructure

For this to be useful, the script should run periodically. This may be achieved using Cron,
e.g. with a line like this in your user's crontab:

```
*/5 * * * * /path/to/kodi-historian/venv/bin/python3 /path/to/kodi-historian/main.py >>/writable/path/to/movies.log
```

With either of these, you will have a viewing history in steps of 5 minutes.
