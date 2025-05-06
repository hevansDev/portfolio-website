---
title: What do community organisers need? Not another pizza.
tags: [Community, Events, Organising, Article]
layout: post
image: /assets/images/pizza_stack.jpg
---

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