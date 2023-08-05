Description
-----------
Code for the `videosum` Python package. Given a video file, this package produces a single-image storyboard that summarises the video.


Install dependencies
--------------------
* Ubuntu/Debian:
```
$ sudo apt install ffmpeg
```

Install with pip
----------------
```
$ python3 -m pip install videosum --user
```


Install from source
-------------------
```
$ python3 setup.py install --user
```


Run video summarisation on a single video
-----------------------------------------
```
$ python3 -m videosum.run --input video.mp4 --output collage.jpg --nframes 100 --height 1080 --width 1920 --algo time
```
Options:
  * `--input`: path to the input video file.
  * `--output`: path where the output collage will be saved.
  * `--nframes`: number of frames that you want to see in the collage image.
  * `--height`: height of the collage image.
  * `--width`: width of the collage image.
  * `--time-segmentation`: set it to either `0` or `1`. If 1, the clustering results are displayed in a bar underneath the collage (i.e. the columns of the bar represent the frames of the video, and the colours represent the clustering label).
  * `--fps`: number of frames you want to read per second of video, used to downsample the input video and have less frames to describe and cluster.
  * `--time-smoothing`: weight in the range `[0.0, 1.0]` that regulates the importance of time for clustering frames. A higher weight will result in a segmentation of frames over time closer to that of the `time` method.
  * `--processes`: number of processes to use when summarising a folder of videos.
  * `--algo`: algorithm used to select the key frames of the video.
    * `time`: evenly spaced frames are selected.
    * `inception`: k-medoids clustering (l2-norm metric) on InceptionV3 latent space vectors.
    * `fid` : k-medoids clustering ([Frechet Inception Distance](https://en.wikipedia.org/wiki/Fr%C3%A9chet_inception_distance) metric) on InceptionV3 latent space vectors.
    * `scda`: k-medoids clustering (l2-norm metric) on SCDA image descriptors ([Wei et al. 2017 Selective Convolutional Descriptor Aggregation for Fine-Grained Image Retrieval](https://arxiv.org/abs/1604.04994)). InceptionV3 was trained on ImageNet as opposed to Wei et al. where authors used VGG-16.


Run video summarisation on multiple videos
------------------------------------------

Pointing the command line parameter `-i` or `--input` to a folder of videos is enough. In this case, the path indicated by `-o` or `--output` will be used as output folder, each video summary will have the same filename as the video but a `.jpg` file extension. 

The parameter `--processes` allows you to select the number of videos to summarise in parallel. This is necessary because some of the summarisation methods use GPU memory, which is typically a limiting factor. If the number of processes is too high you might get a CUDA out of memory error.

```bash
$ python3 -m videosum.run -i <input_folder> -o <output_folder> -n 16 --width 1920 --height 1080 -a inception --fps 1 --time-segmentation 1 --processes 5
```


Exemplary code snippet
----------------------
```python
import cv2
import videosum

# Choose the number of frames you want in the summary
nframes = 100

# Choose the dimensions of the collage
widtth = 1920
height = 1080

# Choose the algotrithm that selects the key frames
algo = 'inception'  # The options are: 'time', 'inception', 'fid', 'scda'

# Create video summariser object
vs = videosum.VideoSummariser(algo, nframes, width, height)

# Create collage image
im = vs.summarise('video.mp4')

# Save collage to file
cv2.imwrite('collage.jpg', im)

# Retrieve a list of Numpy/OpenCV BGR images corresponding to the key frames of the video
key_frames = vs.get_key_frames('video.mp4')       

# Print the video frame indices of the key frames, available after calling summarise() or get_key_frames()
print(vs.indices_)

# Print the video frame cluster labels, available after calling summarise() or get_key_frames()
print(vs.labels_)
```


Exemplary result
----------------

The storyboards have a bar underneath that is produced when the `--time-segmentation 1` option is passed. 
This bar shows how frames have been clustered over time, with a colour for each cluster, and black vertical lines representing the key frames.

* Exemplary video: [here](https://raw.githubusercontent.com/luiscarlosgph/videosum/main/test/data/video.mp4)

* Summary based on `time` algorithm: 

```
$ python3 -m videosum.run --input test/data/video.mp4 --output test/data/time.jpg --nframes 16 --height 1080 --width 1920 --algo time --time-segmentation 1
```

![](https://github.com/luiscarlosgph/videosum/blob/main/test/data/time.jpg) 

* Summary based on `inception` algorithm:

```
$ python3 -m videosum.run --input test/data/video.mp4 --output test/data/inception.jpg --nframes 16 --height 1080 --width 1920 --algo inception --time-segmentation 1
```

![](https://github.com/luiscarlosgph/videosum/blob/main/test/data/inception.jpg) 

* Summary based on `fid` algorithm:

```
$ python3 -m videosum.run --input test/data/video.mp4 --output test/data/fid.jpg --nframes 16 --height 1080 --width 1920 --algo fid --time-segmentation 1
```

![](https://github.com/luiscarlosgph/videosum/blob/main/test/data/fid.jpg) 

* Summary based on `scda` algorithm:

```
$ python3 -m videosum.run --input test/data/video.mp4 --output test/data/scda.jpg --nframes 16 --height 1080 --width 1920 --algo scda --time-segmentation 1
```

![](https://github.com/luiscarlosgph/videosum/blob/main/test/data/scda.jpg) 


Run unit testing
----------------

```
$ python3 setup.py test
```


Run timing script
-----------------

```bash
$ python3 -m videosum.timing 
```

| Method | Time for a 1h video sampled at 1fps |
| ------ | ----------------------------------- |
| time       | 13s |
| inception  | 86s |
| fid        | 216s |
| scda       | 74s |


Author
------
Luis Carlos Garcia Peraza Herrera (luiscarlos.gph@gmail.com), 2022.


License
-------

This code repository is shared under an [MIT license](https://github.com/luiscarlosgph/videosum/blob/main/LICENSE).

