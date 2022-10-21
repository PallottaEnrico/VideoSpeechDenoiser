# Video Speech Denoiser

This repo contains a Python script that denoises speeched voice of an mp4 file. The script extracts the audio from the video, it divides the video into segments and uses the trained model of [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) to denoise the audio track, then it reverses the process. It can be useful since most hardware cannot process the entire audio using DeepFilterNet.

## Installation

You shall clone this repo on your machine and move to the project directory:
```shell
git clone https://github.com/yurinoviello/VideoSpeechDenoiser
cd VideoSpeechDenoiser
```

You need to install [PyTorch](https://pytorch.org/get-started/locally/) and (eventually) the [CUDA](https://developer.nvidia.com/cuda-zone) version suited to your machine. E.g. using conda:
```shell
conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge
```

Then you need to install the dependecies:
```shell
# I encountered some problems with the latest version
pip install -Iv deepfilternet==0.2.5
pip install progress
pip install pydub
pip install ffmpeg
```
If you use conda, run also the following command, since PyTorch creates some issues with ffmpeg:
```shell
conda update ffmpeg
```
## Usage

The script create a new video file with denoised audio.
```
USAGE:
    python videoDenoiser.py [OPTIONS] FILE

ARGS:
    FILE
    	    Video to denoise

OPTIONS:
    -l, --len
            Length in minutes of each segment of the splitted audio track (5 default)
    -h, --help
            Print help information
    -o, --outDir
            The directory path where you want to save the new video file (current dir default)
```
E.g.
```shell
cd VideoSpeechDenoiser
python videoDenoiser.py video.mp4
```
