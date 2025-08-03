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

1) This guide assumes you have a directory of unlabeled images of birds called `images`, if you don't want to go the hassle of setting up your own bird feeder and webcam setup you can download and extract this archive of images from my bird feeder with:

```bash

```

If you're picking up from part 1, just connect your webcam to the USB port on your Raspberry Pi and update the `weigh_bird.py` script to add some new code to take a picture of a bird when it lands.

```python
import time
from datetime import datetime
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

import cv2 # Import open cv2 to handle capturing and processing images

bird_present = False

BIRD_THRESHOLD = 5 # Lightest british songbird Goldcrest 5g

def cleanAndExit():
    print("Cleaning...")
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

# Add a helper function for taking pictures
# We'll add the bird weight in the image name as we're not storing it anywhere yet
def take_photo(weight):
    """Take a photo when a bird lands"""
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        # Let camera adjust
        for i in range(5):
            ret, frame = cap.read()
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bird_{timestamp}_{weight:.1f}g.jpg"
            cv2.imwrite("../images/"+filename, frame)
            print(f" Photo: {filename}")
        cap.release()


hx.set_reading_format("MSB", "MSB")

referenceUnit = 416.71
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Waiting for birds...")

def bird_landed(weight):
    """Called when a bird lands on the feeder"""
    print(f"🐦 Bird landed at {current_time.isoformat()}! Weight: {weight:.2f}g")
    take_photo(weight) # Take a photo when a bird lands

def bird_left():
    """Called when a bird leaves the feeder"""
    print(f"🦅 Bird left!")
    time.sleep(2)
    print("Tare done! Waiting for birds...")
    hx.tare()

while True:
    try:
        current_weight = hx.get_weight(5)
        current_time = datetime.now()

        if not bird_present and current_weight > BIRD_THRESHOLD:
            bird_present=True
            bird_landed(current_weight)
        
        elif bird_present and current_weight < BIRD_THRESHOLD:
            bird_present=False
            bird_left()

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
```

Note the addition of `cv2` and a new `images` directory. If you leave your new script running for a while you should start to accrue a collection of bird photos in your `images` dir. Either way before moving on your should have a directory with a collection if images that look something like:

![A picture of a robin on a bird feeder]({{ site.baseurl }}/assets/images/bird_20250801_120750_19.5g.jpg)
*images/bird_20250801_120750_19.5g.jpg*

2) Next we need to download the pre-trained model, this comes in two parts...


### Quick Troubleshooting



## Conclusion and Next Steps

## Further Reading