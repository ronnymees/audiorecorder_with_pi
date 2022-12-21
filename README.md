# Audiorecorder with Pi and Zoom H1

## Goal
In order to record audio as data samples for training a AI model we needed a device that we can setup in the productionline and can be started and stopped as needed. All recordings are by default pass, when a faulty product is recorded this must be labeled as so.

## Functionality
This python program starts recording audio when a button is pushed.
The recordings are being writed to .WAV files of a predefined size.
The recordings can be stopped and started again as needed.
Start en stop times are logged to a log file.
When the device is recording this is indicated by a led.
When a faulty producted has been recorded, the operator pushes a second button, when doing so the time is also logged to the logfile with a fault label.

## Use of recordings
We aim to use Edge Impulse to cut the data in samples and label them pass and fault.
