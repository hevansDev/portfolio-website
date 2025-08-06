---
title: Smart Bird Feeder Part 2 - How can automatically I identify bird species from an image? - Using Tensorflow and a webcam to spot birds
tags: [RaspberryPi, Python, Hardware, Kafka, Article]
layout: post
image: /assets/images/bird_seo.jpg
---

![An image of robins eating bird seed off a wii fit balance board with the caption meanwhile in suburban south london]({{ site.baseurl }}/assets/images/bird_seo.jpg)

In [the previous entry in this series]({{ site.baseurl }}/load-cell-raspberry-pi) I built a smart bird feeder that could weigh birds with the goal of figuring out how heavy a particularly portly looking robin was. This only got my part of the way to my goal of once and for all answering the question: is this an abnormally huge robin?

The next step is to collect pictures of birds that visit my bird feeder and automatically label them with the species to check to see if the image is of a Robin or not, this will let me track just the weights of Robin's so I can easily spot any abnormally heavy birds.

The below guide will talk you through step by step everything you need to do to take a picture of a bird using a cheap webcam and a Raspberry Pi and then using an image classifier model to identify the bird species. 

---

## What is an image classifier model?

Why do we need an image classifier model at all? Our bird feeder can now weigh visiting birds, but weight alone doesn't tell us the species: a 60g bird could be an enormous robin or a tiny pigeon. An image classifier model can analyze a photo from our webcam and automatically identify the bird species so we can track weights by species.

The model works by analyzing the mathematical patterns in the image data that distinguish one bird species from another. Rather than training our own model (which would require thousands of labeled bird photos), we'll use a pre-trained model that already knows how to identify hundreds of British bird species.

---

## Hardware Setup

If you tried setting up your own bird feeder from the first part of this series you'll have everything you need already apart from the camera, if not you can get everything you need from the list below.

### Hardware shopping list

- [Raspberry Pi 3](https://amzn.to/43Fst45) (£35) - or any similarly capable computer with soldered headers for GPIO, you can pick Raspberry Pi 3s now for as little as £10 second hand. *Note: Raspberry Pi 3s won't be able to run the classifier model without appropriate cooling, I chose to run the model on my laptop instead but you should consider alternatives to the Pi 3 if you want to run the model on device).
- [Micro SD Card](https://amzn.to/43C0nXh) (£10) - These get cheaper all the time, here I've linked to a 128GB card that's relatively good value but really anything over 16GB will be fine as long as you can write to it properly, for more information on picking an appropriate SD card see [this great article by Chris Dzombak](https://www.dzombak.com/blog/2023/12/choosing-the-right-sd-card-for-your-pi/).
- [Webcam](https://amzn.to/44Z1MJx) (£40) - Relatively cheap 1080p USB Webcam, I've linked to the one I used because it's nice to mount but I already had this one lying around and I suspect you can find one going spare at work or elsewhere if you're on a budget.
- [Suction cups](https://amzn.to/4l6OFuJ) (£7) - These make it really easy to stick your webcam to a window for simple mounting and adjustment. The threaded bolt part fits into the standard ISO insert in the webcam above.
- [Micro USB Power Supply](https://amzn.to/43C0nXh) (£15) - make sure to pick a reliable power supply that consistently delivers 5V/2.5A, I've linked to the official power supply here but almost any half decent Micro USB power supply will do.
- Optional: [window mounted bird feeder](https://amzn.to/4lKy14S) (£30) - This is the bird feeder I used, having it mount on a window makes it much easier to get clear pictures by sticking your webcam on the other side of the glass.

## Setup

1) Flash your SD card and setup your Raspberry Pi. For instructions on how to do this properly check out [this guide on the Raspberry Pi website](https://www.raspberrypi.com/documentation/computers/getting-started.html). Connect your webcam to a USB port on your Raspberry Pi.

![Diagram showing webcam connected to USB port on a raspberry pi]({{ site.baseurl }}/assets/images/plug-in-webcam.png)

2) Screw one of the suction cups into the threaded insert in your webcam - this will make it easy to position and adjust your webcam in your window.

![Diagram showing a suction sub with a thread bolt being inserted into a threaded brass insert in the base of a webcam]({{ site.baseurl }}/assets/images/insert-suction-cup.png)

3) Stick your webcam somewhere with a good view of your bird feeder, the closer the lens is to the glass the less glare you'll have in your images. Camera positioning is crucial for accurate bird identification:

- Position the camera as close as you can to bird feeder. If the camera is too far away details can become unclear for classification.
- Natural daylight works best. Avoid positioning the camera where it captures direct sunlight or creates harsh shadows on the feeder. North-facing windows often provide the most consistent lighting throughout the day.
- A simple, uncluttered background helps the model focus on the bird. If your view is busy with garden furniture or complex foliage, consider adding a plain backdrop behind your feeder.
- Most webcams have fixed focus, so test your setup by taking a few photos of objects placed where birds typically perch. Adjust the camera distance until birds in the center of the frame appear sharp.
- Position the camera to capture birds from the side rather than head-on or from behind - side profiles show the most distinguishing features like breast markings, wing patterns, and body shape.

Remember that the model was trained on a variety of lighting conditions and angles, so don't worry about getting perfect shots every time - even a blur of a Robin in motion can classify correctly!

![A diagram showing a view of a window from the outside with a webcam stuck facing a bird feeder]({{ site.baseurl }}/assets/images/view-of-a-bird-feeder.png)

4) Now that we've got a nice little bird photo-booth set up we can start taking some pictures (if you're following along from part 1 you can update your code to take a photo when a bird is detected [see my source code on GitHub for reference](https://github.com/hevansDev/bird-kafka-demo/blob/main/bird_weights/bird_weights.py)), lets install [OpenCV](https://opencv.org/) for capturing and processing pictures from the webcam.

```bash
python3 -m pip install opencv-python-headless==4.8.1.78
```

5) Create a new script called `take_picture.py` with the following Python code:

```python
import time
from datetime import datetime
import sys
import cv2

def take_photo():
    """Take a photo when a bird lands"""
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        # Let camera adjust
        for i in range(5):
            ret, frame = cap.read()
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bird_{timestamp}.jpg"
            cv2.imwrite("./images/"+filename, frame)
            print(f"📸 Photo: {filename}")
        cap.release()

take_photo()
```

This script will take a picture and save it to the `images` directory, lets create that dir now and test our script out.

```bash
mkdir images
python take_picture.py
```

You should end up with a picture like the example below in the `images` dir (for those following on from part 1 your images will also include the weight measured when the photo was taken).

![A picture of a robin on a bird feeder]({{ site.baseurl }}/assets/images/bird_20250801_120750_19.5g.jpg)
*images/bird_20250801_120750.jpg*

6) Now that we have an image of a bird we can use a classifier model to predict the species of the bird in the image. 

**It is unlikely that your Raspberry Pi will be able to run the model due to how computationally intensive it can be to run - I suggest copying your `images` dir from the previous step to your laptop or more powerful computer!**

For this we'll use the pre-trained uk garden birds model from [secretbatcave](https://github.com/secretbatcave/Uk-Bird-Classifier). Download the saved model (the `.pb` stands for [ProtoBuff](https://www.tensorflow.org/guide/saved_model#the_savedmodel_format_on_disk) format) and the classes with:

```bash
mkdir models
curl -o models/ukGardenModel.pb https://raw.githubusercontent.com/secretbatcave/Uk-Bird-Classifier/master/models/ukGardenModel.pb
curl -o models/ukGardenModel_labels.txt https://raw.githubusercontent.com/secretbatcave/Uk-Bird-Classifier/master/models/ukGardenModel_labels.txt
```

7) Install tensorflow and its dependencies. [Tensorflow](https://www.tensorflow.org/learn) is a software library for machine learning that was used to produce the model we're working with here, we'll use it now to run the model to make a bird species prediction.

```bash
pip install tensorflow "numpy<2"  protobuf==5.28.3
```

8) Create a new Python script called `identify_bird.py` with the following Python code:

```python
import os
import sys
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.disable_v2_behavior()

# Load model
with tf.io.gfile.GFile('models/ukGardenModel.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

# Load labels
with open('models/ukGardenModel_labels.txt', 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Read image
image_path = sys.argv[1]
with open(image_path, 'rb') as f:
    image_data = f.read()

# Run inference
with tf.Session() as sess:
    predictions = sess.run('final_result:0', {'DecodeJpeg/contents:0': image_data})
    bird_class = labels[np.argmax(predictions)]
    print(bird_class)
```

Note the use of `tensorflow.compat.v1`: this is an older model (from 7+ years ago) so we're using the version 1 compatibility module rather than `tensorflow` to ensure everything works correctly (this is also why we're using the `"numpy<2"` and `protobuf==5.28.3` downgrades).

Lets try making a prediction with one of your photos to see if everything is working correctly:

```bash
python identify_bird.py images/bird_20250801_120750.jpg
```

You should see a result like:

```
WARNING:tensorflow:From /Users/hugh/test/.venv/lib/python3.13/site-packages/tensorflow/python/compat/v2_compat.py:98: disable_resource_variables (from tensorflow.python.ops.resource_variables_toggle) is deprecated and will be removed in a future version.
Instructions for updating:
non-resource variables are not supported in the long term
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1754516598.102893 5536073 mlir_graph_optimization_pass.cc:437] MLIR V1 optimization pass is not enabled
robin
```

You should see a predicted bird species on the last line of the output.

---

### Quick Troubleshooting



## Conclusion and Next Steps

## Further Reading