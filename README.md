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

* python
* numpy
* picamera

If you have Python and pip, you should be able to install the dependencies using the following commands after navigating to the project directory:

    sudo apt-get build-dep python-numpy

    sudo pip install -r requirements.txt

To run, Navigate to the `src` directory, and run `python motion.py`.
