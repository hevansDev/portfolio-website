---
title: Real-time analytics with Kafka, ClickHouse, and live aircraft data.
tags: [Data Engineering, Architecture, OSS, Kafka, ClickHouse, Article]
layout: post
image: /assets/images/flight-radar-banner.png
---

If you want to showcase real-time data architectures you need a data source that's live, high-volume, varied, and messy enough to showcase real-world challenges. This is an issue I've run into several times over the last year whilst giving talks about real-time analytics using Kafka, Druid, ClickHouse, and Grafana in various combinations. You could use a data generator like [ShadowTraffic](https://shadowtraffic.io/) but when trying to bring the sometimes dry topic of data engineering to life nothing beats real data. So when I'm building demos I've consistently turned to the same compelling dataset: ADS-B aircraft transmissions.

I was introduced to ADS-B (Automatic Dependent Surveillance–Broadcast) by my former colleague at Imply Hellmar Becker, and is one of the technologies aircraft use to relay data including their position, heading, and speed to air traffic controllers and to other aircraft. This creates a continuous stream of real-time data that's publicly accessible and rich with analytical possibilities. The dataset perfectly illustrates the complexities of streaming analytics—it arrives at high velocity, contains mixed data types, requires deduplication and enrichment, and benefits from both real-time alerting and historical analysis.

What makes ADS-B particularly valuable for demonstrations is its combination of technical complexity and intuitive appeal. Everyone understands aircraft movement, making it easy to visualize concepts like windowing, aggregation, and anomaly detection. Yet underneath this accessibility lies genuine engineering challenges: handling bursty traffic patterns, dealing with incomplete or duplicate messages, and correlating position data with aircraft metadata.

In this article, I'll walk through building a complete ADS-B ingestion pipeline—from setting up a simple antenna to producing clean, structured data to Kafka topics ready for real-time analysis. By the end, you'll have both the technical foundation and a rich dataset to explore your own streaming analytics architectures.

---

## Understanding ADS-B data

## Hardware Setup and Data Collection

You can be receiving live aircraft data for under £100 and have it running in 15 minutes. Here's my exact setup that's been reliably collecting ADS-B data for months.

### Hardware shopping list

- [Raspberry Pi 3](https://amzn.to/43Fst45) (£35) - or any similarly capable computer, you can pick Raspberry Pi 3s now for as little as £18 second hand
- [NooElec NESDR Mini USB RTL-SDR](https://amzn.to/4kwR9mk) (£35) - An easy to use and readily available ADS-B antenna that can be connected to your Pi via USB. The included antenna gets you 50-100km range, which is perfect for getting started.
- [Micro SD Card](https://amzn.to/43C0nXh) (£10) - These get cheaper all the time, here I've linked to a 128GB card that's relatively goodvalue but really anything over 16GB will be fine as long as you can write to it properly, for more information on picking an appropriate SD card see [this great article by Chris Dzombak](https://www.dzombak.com/blog/2023/12/choosing-the-right-sd-card-for-your-pi/).
- [Micro USB Power Supply](https://amzn.to/43C0nXh) (£15 ) - make sure to pick a reliable power supply that consistently delivers 5V/2.5A, I've linked to the official power supply here but almost any half decent Micro USB power supply will do.

### Setup

1. Install a supported OS on your Pi, I'm using a lite version (without a UI) of the official Debian Bookworm build, for details on how to do this follow the steps in the [guide on the Raspberry Pi website](https://www.raspberrypi.com/software/).

2. Install Docker on your Pi and give the Docker user the necessary permissions.

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
```

3. Create a new Docker compose called `docker-compose.yml` and define an ultrafeeder services as below. Note: this is a very basic ultrafeeder configuration, you may wish to consult the [setup guide in the ADS-B Ultrafeeder repo](https://github.com/sdr-enthusiasts/docker-adsb-ultrafeeder?tab=readme-ov-file#minimalist-setup) for a more in depth guide to setting up this part.

```yaml
services:
  ultrafeeder:
    image: ghcr.io/sdr-enthusiasts/docker-adsb-ultrafeeder
    container_name: ultrafeeder
    restart: unless-stopped
    device_cgroup_rules:
      - "c 189:* rwm"
    ports:
      - 8080:80     # Web interface
      - 30003:30003 # SBS output (for Kafka)
    environment:
      - READSB_DEVICE_TYPE=rtlsdr
      - READSB_RTLSDR_DEVICE={the serial of your ADS-B antenna device, usually 00000001}
      - READSB_LAT={the latitude of your antenna}
      - READSB_LON={the longitude of your antenna}
      - READSB_ALT={the altitude of your antenna}
    volumes:
      - /dev/bus/usb:/dev/bus/usb
```

4. Deploy your ultrafeeder services with `docker-compose up -d`.

5. Optionally: Add a flight radar 24 service to your docker compose and redeploy. You will need to register for a flight radar account. Sending data to flight radar 24 gives you free access to their services and provides a useful UI for troubleshooting your ADS-B data.

```yaml
{existing services}
...
  fr24feed:
    image: ghcr.io/sdr-enthusiasts/docker-flightradar24:latest
    container_name: fr24feed
    restart: always
    ports:
      - 8754:8754
    environment:
      - BEASTHOST=ultrafeeder
      - FR24KEY={your flight radar 24 key}
    dns_search: . # prevents rare connection issues related to a bug in docker and fr24feed
```

6. Validate that you are receiving data correctly by running `nc localhost 30003` on your Pi, you should see messages like:

```
MSG,8,1,1,40756A,1,2025/06/01,17:42:30.733,2025/06/01,17:42:30.776,,,,,,,,,,,,0
MSG,8,1,1,40756A,1,2025/06/01,17:42:33.003,2025/06/01,17:42:33.015,,,,,,,,,,,,0
```

If your antenna has a good view of the sky you can expect around 100-2000 messages/second (depending on your location) with CPU usage sitting comfortably under <20% on a Pi 3.

### Quick Troubleshooting

No aircraft? Check your antenna USB connection with `lsusb | grep RTL` you should see something like `Bus 001 Device 033: ID 0bda:2838 Realtek Semiconductor Corp. RTL2838 DVB-T`, if not your antenna may not be connected correctly. Verify your antenna connection is secure or try different USB port (preferably USB 2.0+) and try restarting ultrafeeder with `docker-compose down && docker-compose up -d`

Tracking very few aircraft? Try placing your antenna higher and away from electronics, for best results try and get an unobstructed view of the sky.

## Kafka Integration

## Conclusion and Next Steps

## Further Reading

[The 1090 Megahertz Riddle (second edition)](https://mode-s.org/1090mhz/content/ads-b/1-basics.html) A Guide to Decoding Mode S and ADS-B Signals by [Junzi Sun](junzis.com)

Install raspbian 64 bit lite

Install docker

sudo apt update
sudo apt install -y docker.io

# Install Docker Compose
sudo apt install -y docker-compose

# Add your user to the docker group to run docker without sudo
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect, or run:
newgrp docker

FEEDER_TZ=Europe/London

FR24_KEY=85fe761bbec41b2e

# SDR device settings
ADSB_SDR_SERIAL=00000001
ADSB_SDR_PPM=0    # PPM correction for your SDR

# Location information (required)
FEEDER_LAT=51.41596
FEEDER_LONG=-0.02855
FEEDER_ALT_M=40

# Identity settings
MULTIFEEDER_UUID=7055a2f4-954d-4807-88ee-25e306ea1bea
FEEDER_NAME=huev

# HeyWhatsThat.com settings (for range visualization)
FEEDER_HEYWHATSTHAT_ID=BDJQNXK1
FEEDER_HEYWHATSTHAT_ALTS=3048,9144,12192

# # InfluxDB settings
# INFLUX_URL=http://influxdb:8086
# INFLUX_TOKEN=your_token_here
# INFLUX_BUCKET=adsb

https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/#scenario-4

docker exec -it broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic connect-configs --partitions 1 --replication-factor 1 --config cleanup.policy=compact

docker exec -it broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic connect-offsets --partitions 1 --replication-factor 1 --config cleanup.policy=compact

docker exec -it broker /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic connect-status --partitions 1 --replication-factor 1 --config cleanup.policy=compact

curl "http://localhost:8123/?user=default&password=ClickHousePassword" --data-binary "CREATE TABLE IF NOT EXISTS adsb_data (
    raw_message String,
    timestamp DateTime64(3, 'UTC'),
    event_time DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (timestamp);"

---

CREATE TABLE adsb_messages (
    value String
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka.hughevans.dev:9092',
    kafka_topic_list = 'adsb-raw',
    kafka_group_name = 'clickhouse-consumer-group-new',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 1;

CREATE TABLE adsb_data (
    raw_message String,
    timestamp DateTime64(3, 'UTC'),
    event_time DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (timestamp);

CREATE MATERIALIZED VIEW adsb_mv TO adsb_data AS
SELECT
    value AS raw_message,
    toDateTime64(JSONExtractInt(value, 'timestamp') / 1000, 3, 'UTC') AS timestamp,
    now() AS event_time
FROM adsb_messages;