---
title: How can I weigh things with a Raspberry Pi? - Using a HX711 ADC and load cell with a Raspberry Pi
tags: [RaspberryPi, Python, Hardware, Kafka, Article]
layout: post
image: /assets/images/flight-radar-banner.png
---

![Flight radar talk photo collage]({{ site.baseurl }}/assets/images/flight-radar-banner.png)

There is a very large robin than often visits the bird feeder on my office window. It's clear this robin is much heavier than other robins because when he lands the impact makes a loud *thwack* sound. I decided to see if I could build a simple setup to figure out exactly how heavy this robin is and in predictable fashion got carried away - this will be the first article in a three part series exploring: building a smart bird feeder than can weigh visiting birds, using AI to identify birds automatically, and bringing it all together with Kafka and Iceberg. 

In order to get the weight of birds on my bird feeder I would need to add a load cell to the feeder platform. Whenever I'm building something like this I tend to start with a Raspberry Pi as that's what I'm most familiar with, there's a lot of great guides online on how to use Arduinos and other micro controllers with load cells and amplifiers but there isn't a huge amount out there on Raspberry Pis other than [this great tutorial from Tutorials for Raspberry Pi](https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711) from several years ago. I was able to get a working setup with a cheap 5kg rated load cell and HX711 ADC as explained in the tutorial but I encountered few snags along the way so I thought in addition to documenting my bird feeder project I would write and updated version of the Tutorials for Raspberry Pi guide to help anyone else looking to work with load cells and the Raspberry Pi.

The below guide will talk you through step by step everything you need to do to weigh an object up to 5kg in weight with a Raspberry Pi including selecting components, assembly, and calibration.

---

## What is an HX711?

First though, why do we need an HX711 at all? Load cells convert forces applied to them into analog electrical signals via strain gauges (resistors that change their resistance when bent or stretched) that we can use to measure weight but these signals are both analog and too small to be detected by the Raspberry Pis GPIO (General Purpose Input Output) pins. The HX711 is an ADC (Analog to Digital Convertor) which takes the weak analog signal from the load cell and outputs a digital signal the Raspberry Pi can read.

![HX711 converts analog signals to digital signals]({{ site.baseurl }}/assets/images/hx711-signal.png)

---

## Hardware Setup

Setting up your HX711 will require some soldering, don't worry if you've not done soldering before this is a particularly simple soldering job (even I could do it!) If you follow the method I used you'll need to cut and drill the some parts to install your load cell - if you'd rather not do this you can buy a load cell and HX711 kit with these parts pre-made, for example [this kit with laser cut wooden sheets with mounting holes](https://amzn.to/4kqA6BJ). If you already have a soldering iron all the parts for this project new should set you back no more than £85 but you could save a fair bit if you pick up the Raspberry Pi second hand (or already have one laying around) and scavenge your bolts and rigid sheets rather than buying them new.

### Hardware shopping list

- [Raspberry Pi 3](https://amzn.to/43Fst45) (£35) - or any similarly capable computer with soldered headers for GPIO, you can pick Raspberry Pi 3s now for as little as £10 second hand
- [Load cells and HX711s](https://amzn.to/44PCFbR) (£8) - a pair of load cells and HX711s, these are cheap as chips and it's nice to have a spare in case you get over enthusiastic tightening bolts or testing later on.
- [Bolts and Washers](https://amzn.to/4lDKHtU) (£8) - the load cell I picked had 4 holes for mounting, two threaded for M(size) and two threaded for M(size) either way this selection should have everything you need including washers which are useful for making sure the strain gauges don't get pinched. I scavenged the bolts and washers I needed from some other projects.
- [Micro SD Card](https://amzn.to/43C0nXh) (£10) - These get cheaper all the time, here I've linked to a 128GB card that's relatively good value but really anything over 16GB will be fine as long as you can write to it properly, for more information on picking an appropriate SD card see [this great article by Chris Dzombak](https://www.dzombak.com/blog/2023/12/choosing-the-right-sd-card-for-your-pi/).
- [Micro USB Power Supply](https://amzn.to/43C0nXh) (£15) - make sure to pick a reliable power supply that consistently delivers 5V/2.5A, I've linked to the official power supply here but almost any half decent Micro USB power supply will do.
- [Acrylic](https://amzn.to/3TrxKaJ) / [Plywood-wood](https://amzn.to/4nBnRoE) sheets approximately 100x200mm (£6)- these will be used to mount your load cell and hold whatever it is you're weighing so anything cheap and rigid will do, I used some old plexiglass offcuts but I suspect even sturdy cardboard would work fine.
- [Female to female Dupont cables](https://amzn.to/4nx52mJ) (£4) - you only need 4 of these to connect your HX711 to the headers on your Raspberry Pi but its worth buying them in a big pack like the one linked as it's much cheaper than only buying 4 and dupont cables are always handy for projects like this.
- Optional: [Bird Feeder](https://amzn.to/4lKy14S) - You can install your load cell in whatever you want, I added mine to this bird feeder which has a handy removable tray which makes adding the load cell a breeze.

### Tools

Essential:
- Soldering iron
- Solder
- Scissors or snips

Handy for shaping your rigid sheets and making mounting holes:
- Dremel
- Coping saw
- File or sanding paper
- Drill

### Setup

1) Cut your sheets to size and drill two holes in each sheet to attach the load cell and bolt the load cell into place. Your sheets should look something like the diagram below with the holes for mounting the top sheet roughly centered and the hole for mounting the base towards the edge:

![A rough schematic of what your rigid sheets should look like with mounting holes]({{ site.baseurl }}/assets/images/rigid-sheets.png)

2) Solder the leads from the load cell to the correct pads on the HX711 Red: E+
Black: E-
Green: A-
White: A+
The pins labeled B+/B- remain empty.
3) Now you just have to connect the sensor to the Raspberry Pi. Since this also has only four connections, the wiring is quite simple:



![A schematic showing a red wire connected to E+, a black wire connected to E-, a green wire to A_, and a white wire to A+ on the terminal of a HX711]({{ site.baseurl }}/assets/images/solder-hx711.png)

4) Cut off a 4 ping long strip of the included headers, press them short end first into the holes in the board marked GND, DT, SCK, and VCC and solder them from the reverse of the board. This can be fiddly! I usually use a big blob of Blu Tack to hold my headers in place when soldering them but anything that can hold the headers square (i.e. a second pair of hands!) can be really helpful here.

![A diagram showing how to correctly orient the headers with the black part and long pins on the top of the board and the short pins pocking through the holes]({{ site.baseurl }}/assets/images/solder-headers-hx711.png)

5) Tear off a strip of four female to female dupont wires, (keeping the four stuck together can help keep your wiring tidy but it can help to tease the ends apart a bit to make it easier to plug them into your headers) and use them to connect the headers on the HX711 to the headers on your Raspberry Pi as follows: VCC to Raspberry Pi Pin 2 (5V),GND to Raspberry Pi Pin 6 (GND), DT to Raspberry Pi Pin 29 (GPIO 5), and SCK to Raspberry Pi Pin 31 (GPIO 6). The pin out of your Raspberry Pi may vary slightly depending on model, for reference check out this awesome resource over on [pinout.xyz/](https://pinout.xyz/).

![A diagram showing how to correctly connect hx711 to the raspberry pi with dupont connectors]({{ site.baseurl }}/assets/images/connect-hx711-to-pi.png)

5) Flash your SD card and setup your Raspberry Pi. For instructions on how to do this properly check out [this guide on the Raspberry Pi website](https://www.raspberrypi.com/documentation/computers/getting-started.html).

6) Get the library we need to control the HX711 with Python:

``` bash
git clone https://github.com/tatobari/hx711py
```

7) Finally we're ready to calibrate the load cell.



### Quick Troubleshooting


---

## Conclusion and Next Steps

## Further Reading