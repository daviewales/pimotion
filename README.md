# Readme

This repo contains simple motion detection code for the Raspberry Pi written in Python with picamera and numpy.

## Settings

This program is designed to be used with a remote database through a json api.
You need to create a file called `settings.json`, and populate the `url` and `apikey` fields.
An example file called `example_settings.json` is included in the  `src` directory.

If you don't want to work with a remote website, or you want to create your own interface,
just use `backend.py` as a library, and replace `motion.py` with your own code.

## Running

Make sure you have the required dependencies, which  are as follows:

* python3
* numpy
* picamera

If you have Python 3 and pip3, you should be able to install the dependencies using the following commands after navigating to the project directory:

    sudo apt-get build-dep python-numpy

    sudo pip3 install -r requirements.txt

(Note that `pip3` may possibly be called `pip-3.2`, or `pip-3.3`, etc. Find out your Python version using `python3 -V`.)

To run, Navigate to the `src` directory, and run `python motion.py`.
