# MASHUP of multiple songs - Python

**Assignment 2 : UCS654**

Submitted By: **Samarjot Singh 102003242**

***

## Mashup

Mashup is a Python package that combines the power of `pytube` and `pydub` to create amazing audio and video mashups. With Mashup, you can easily download and manipulate audio and video files from YouTube and other sources, allowing you to create custom remixes, soundtracks, and more.

<br>

## Features

- Download videos and audio files from YouTube using `pytube`
- Manage and manipulate audio files using `pydub`
- Merge and layer audio and video files to create custom mashups
- Export mashups as MP3, MP4, or other file formats

<br>

## How to run this package:

MASHUP-Samar 102003242  can be used by running following command in CMD:

```
>> mashup "Sidhu Moose Wala" 10 20 102003242-output.mp3
```

<br>

## Getting started

To get started with Mashup, you'll need to install both `pytube` and `pydub`. You can do this by running the following commands:

```cmd
>> pip install pytube pydub
>> pip install pytube pytube
```

<br>

Next, you'll need to import the `pytube` and `pydub` libraries into your project. Here's an example of how you might do this:

```python
from pytube import YouTube
from pydub import AudioSegment
```

<br>

Once you have the libraries imported, you're ready to start downloading and manipulating audio and video files. Here's an example of how you might download a video from YouTube using pytube:

```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url)
video = yt.streams.first()
video.download("/path/to/save/video")
audio = AudioSegment.from_file("/path/to/audio/file.mp3")
```

<br>

## Export the audio file

```python
fin_sound.export(output_name, format="mp3")
```

With these building blocks, you can create all sorts of amazing audio and video mashups!

<br>

## Documentation
For more information on how to use pytube and pydub, be sure to check out their official documentation:

[pytube Documentation](https://python-pytube.readthedocs.io/en/latest/)
[pydub Documentation](http://pydub.com/)