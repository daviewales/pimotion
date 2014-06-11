# Readme

This repo contains simple motion detection code for the Raspberry Pi written in Python with picamera and numpy.

*Note:*
This code works best in a bright room, with a light coloured background.
Make sure that the camera is stationary, and there is a good light source.

## Settings

    python3 motion.py -h

This program is designed to be used with a remote database through a json api.
You need to create a file called `config.json`,
and populate the `url`, `image_url`, and `apikey` fields.
An example file called `example_config.json` is included in the
`pimotion` directory.

You can specify the path to your config file with the `-c` flag.

If you don't want to work with a remote website,
or you want to create your own interface,
just use `backend.py` as a module, and replace `motion.py` with your own code.

## Running

    python3 motion.py

Make sure you have the required dependencies, which  are as follows:

* python3
* numpy
* picamera

If you have Python 3 and pip3, you should be able to install the dependencies using the following commands after navigating to the project directory:

    sudo apt-get build-dep python-numpy

    sudo pip3 install -r requirements.txt

Note that `pip3` may possibly be called `pip-3.2`, or `pip-3.3`, etc. Find out your Python version using `python3 -V`.

Also note that while the dependencies for this project can be satisfied by running *just* the second line, users
are advised to include the first line for best performance.
`sudo apt-get build-dep python-numpy` installs a lot of very fast maths
libraries for `numpy`, which **greatly** improve performance.

To run, Navigate to the `pimotion` directory, and run `python3 motion.py`.

## More Info

Travis test status is [here.](https://travis-ci.org/daviewales/pimotion)

[![Build Status](https://travis-ci.org/daviewales/pimotion.svg?branch=master)](https://travis-ci.org/daviewales/pimotion)
