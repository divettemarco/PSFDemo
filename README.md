# Pragmatic Similarity Finder Demo
## Authors: Andy Segura, Divette Marco
## UTEP 2024

## Description
The psf demo demonstrates our metric for detecting pragmatic similarity
The way it works is that it records someone speaking and chops up
their utterances into different .wav files. Each utterance is then
compared to all of the clips in one of our datasets. It then shows
clips of differing levels of similarity. To understand further how the [PSF demo](https://www.youtube.com/watch?v=2AmYXQwEi0E) works, you can view the linked video.

## Environment Setup
To create the environment in which to run the demo, download [Anaconda](https://www.anaconda.com/). Once downloaded, go to the "Environments" tab and open a terminal using the base(root) environment. In the command line enter, `conda env create -f psf_demo.yml` which will create the environment with all the package requirements needed for the demo. Once the environment is ready, you can enter `conda activate psf_demo` in the command line to activate it or open it through the "Environments" tab in Anaconda. Using Anaconda is strongly recommended to get all the necessary packages for the demo, but a requirements.txt is also included.

## Run Demo
Once the project is downloaded, you will have the python code and some clips. The clips included are from the DRAL corpus and are stored in the "DRAL-All-Short" subdirectory. If you wish to use other clips, each should be stored in their own dataset subdirectory. All dataset metadata files are stored in subdirectory "data".

To run, first set up an audio input device, then open a terminal in Anaconda using the psf_demo environment that was previously set up and enter `python demo_command.py`. Any clips that are recorded during the demo are stored in subdirectory "clips".

## Datasets

[DRAL (UTEP)](https://www.cs.utep.edu/nigel/dral/): A collection of conversations with students from UTEP

SWBD (Texas Instruments): A collection of conversations mostly from people
in the East Texas area. Can choose whether to compare only male or female 
voices for this dataset. Due to license issues, this is not included.

ASD/NT (NMSU): A collection of conversations with children with autism
spectrum disorder and neurotypical development. Due to privacy issues
this is not included.

## Device Inputs and Outputs
The input device is set as the default input of the system. If using a laptop microphone then utterances might not be clipped correctly, so consider using another input device (ex. Audio Volt).

The laptop speakers are set as the output device.

If the indices of the devices on your laptop differ from the ones that are hardcoded, change the int values in lines 38-40 to the device indices. Also change the name string of the device in line 38 if it differs from your desired output device.
