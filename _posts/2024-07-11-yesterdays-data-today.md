---
title: Make "today's" data "yesterday's" data 
tags: [How to, Druid, APIs, Testing, Draft]
layout: post
---

## Make "today's" data "yesterday's" data 

### Always "yesterday's" data "today"

```
SELECT "__time", "hex_ident_val", "altitude", "longitude", "latitude" FROM "adsb-json" WHERE "__time" >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS
```

|__time|hex_ident_val|altitude|longitude|latitude|
|--------|---------------|----------|-----------|----------|
|2024-07-11T15:19:12.540Z|4401DC|38025|null|null|
|...|...|...|...|...|

Run the post request below with curl to get the last 24 hours of data from Druid and save it locally as JSON data.

```
curl "http://localhost:8888/druid/v2/sql" \
--header 'Content-Type: application/json' \
--data '{
    "query": "SELECT * FROM \"adsb-json\" WHERE \"__time\" >= CURRENT_TIMESTAMP - INTERVAL 24 HOURS",
    "resultFormat": "objectLines"
}' > sample-data.json
```

Druid has an ~~annoying~~ fun quirk where if you try to ingest data from a record where the time field is in a column called `__time` the ingestion will fail. This is because the SQL for ingestion will contain the line  `SELECT ... "__time" as "__time" ...` because Druid tries to change the name of your time column to `__time`.

This is an issue for use because our time column is called `__time` in sample data as it is directly from an existing Druid table. 

We can use `sed` to replace all of the instances of `__time` in the JSON with some other column name, it doesn't matter what it is as long as it isn't `__time` (here I'm using `time`).

```
sed -i '' 's/__time/time/g' sample-data.json
```

Run a quick `tail` against your file to check for any tailing spaces and remove as appropriate (there should be no tailing spaces, these will cause your ingestion to fail, thanks Druid).

```
tail sample-data.json
```

Druid wants it's data nicely bundled up in a GZIP, so run a GZIP to pack your file up nicely.

```
gzip sample-data.json
```

Stick your file somewhere where Druid can get it for example you could copy it into the filesystem of the running container or  push it to a GitHub repo (just bear in mind if your shiny new zipped file is larger than 100MB GitHub won't let you push it without LFS, _large file havers_ should consider breaking them up across multiple files).

Go to batch ingestion in the Druid web console and add the path/URL (paths/URLs if your data is spread across multiple files) to your GZIPP'ed data.

Now we have 24 hours of data in a file that is ready to be ingested back into Druid for testing or demos etc. How can we change the timestamps on this data to make it appear to be from yesterday (or any other past or future date for that matter)?

**_With this Eldritch terror of a Druid ingestion query!_**

```
REPLACE INTO "sample-data" OVERWRITE WHERE "__time" >= TIMESTAMP '2024-07-10' AND "__time" < TIMESTAMP '2024-07-11'
WITH "ext" AS (
  SELECT *
  FROM TABLE(
    EXTERN(
      '{"type":"http","uris":["https://github.com/hellmarbecker/kfd-demo-stack/raw/oss_flight_data_demo/oss-flight-data-demo/sample-data.json.gz"]}',
      '{"type":"json"}'
    )
  ) EXTEND ("time" VARCHAR, "kafka.header.ReceiverLat" VARCHAR, "date_message_logged" VARCHAR, "altitude" BIGINT, "time_message_generated" VARCHAR, "latitude" DOUBLE, "hex_ident_val" VARCHAR, "emergency" BIGINT, "ground_speed" BIGINT, "kafka.header.ClientTimezone" VARCHAR, "transmission_type" BIGINT, "client_id" VARCHAR, "aircraft_id" BIGINT, "client_lat" VARCHAR, "squawk" VARCHAR, "kafka.header.ReceiverLon" VARCHAR, "alert" BIGINT, "time_message_logged" VARCHAR, "callsign" VARCHAR, "ts_generated" VARCHAR, "track" BIGINT, "longitude" DOUBLE, "kafka.header.ClientID" VARCHAR, "is_on_ground" BIGINT, "session_id" BIGINT, "message_type" VARCHAR, "date_message_generated" VARCHAR, "spi" BIGINT, "client_lon" VARCHAR, "flight_id" BIGINT, "ts_logged" VARCHAR, "kafka.topic" VARCHAR, "kafka.key" VARCHAR, "vertical_rate" BIGINT)
)
SELECT
  TIME_FLOOR(TIME_PARSE(TIME_FORMAT(TIME_SHIFT(CURRENT_TIMESTAMP,'P1D',-1),'yyyy-MM-dd')||'T'||TIME_FORMAT(TIME_PARSE("time"),'HH:mm:ss.SSS')||'Z') , 'PT15S') AS "__time",
  "transmission_type",
  "hex_ident_val",
  "callsign",
  CAST("aircraft_id" AS VARCHAR) AS "aircraft_id",
  COUNT(*) AS "readings",
  MAX("altitude") AS "altitude",
  MAX("latitude") AS "latitude",
  MAX("longitude") AS "longitude",
  MAX("track") AS "track",
  MAX("ground_speed") AS "ground_speed",
  MAX("vertical_rate") AS "vertical_rate"
FROM "ext"
GROUP BY 1,2,3,4
PARTITIONED BY DAY

```

There's a lot going on in the big picture here so let's break it down a bit.

First we're going to make sure we don't accidentally overwrite all of the data in our table by limiting our ingestion to just within the boundaries of "yesterday".

> For the sake of clarity the "yesterday" I'm working with in this particular example is 10/11/2024. The day I collected the data I'm making using (i.e. "today") is 11/11/2024.

```
REPLACE INTO "sample-data" OVERWRITE WHERE "__time" >= TIMESTAMP '2024-07-10' AND "__time" < TIMESTAMP '2024-07-11'
...
```

Now we know where we are putting our data we need to specify where we are getting our data from. This is actually pretty simple, we're just specifying the path/URL to our data and the (very, very many) column names within it.

```
...
WITH "ext" AS (
  SELECT *
  FROM TABLE(
    EXTERN(
      '{"type":"http","uris":["https://github.com/hellmarbecker/kfd-demo-stack/raw/oss_flight_data_demo/oss-flight-data-demo/sample-data.json.gz"]}',
      '{"type":"json"}'
    )
  ) EXTEND ("time" VARCHAR, "kafka.header.ReceiverLat" VARCHAR, "date_message_logged" VARCHAR, "altitude" BIGINT, "time_message_generated" VARCHAR, "latitude" DOUBLE, "hex_ident_val" VARCHAR, "emergency" BIGINT, "ground_speed" BIGINT, "kafka.header.ClientTimezone" VARCHAR, "transmission_type" BIGINT, "client_id" VARCHAR, "aircraft_id" BIGINT, "client_lat" VARCHAR, "squawk" VARCHAR, "kafka.header.ReceiverLon" VARCHAR, "alert" BIGINT, "time_message_logged" VARCHAR, "callsign" VARCHAR, "ts_generated" VARCHAR, "track" BIGINT, "longitude" DOUBLE, "kafka.header.ClientID" VARCHAR, "is_on_ground" BIGINT, "session_id" BIGINT, "message_type" VARCHAR, "date_message_generated" VARCHAR, "spi" BIGINT, "client_lon" VARCHAR, "flight_id" BIGINT, "ts_logged" VARCHAR, "kafka.topic" VARCHAR, "kafka.key" VARCHAR, "vertical_rate" BIGINT)
)
...
```

So far, not so bad! Now for some light time travel via SQL select statement.

```
SELECT
  TIME_PARSE(TIME_FORMAT(TIME_SHIFT(CURRENT_TIMESTAMP,'P1D',-1),'yyyy-MM-dd')||'T'||TIME_FORMAT(TIME_PARSE("time"),'HH:mm:ss.SSS')||'Z') AS "__time",
  "kafka.header.ReceiverLat",
  "kafka.header.ReceiverLon",
  "date_message_logged",
  "time_message_logged",
  "altitude",
  "latitude",
  "longitude",
  "hex_ident_val"
FROM "ext"
PARTITIONED BY DAY
```

Mmmmmmmmm... Don't love that!

Let's build our way up from the core of this `TIME_PARSE` statement to explain what is happening.

`TIME_PARSE("time")` takes the time string from our `time` column and makes it a proper time we can do _fancy stuff_ to like our next step ``TIME_FORMAT(...,'HH:mm:ss.SSS')` which strips out just the hours, minutes, and seconds from the time field.

`CURRENT_TIMESTAMP` gives us the time right now and now comes the (by SQL standards) fun part! We can use `TIME_SHIFT(...,'P1D',-1)` to shift the date back in time by subtracting (`-1`) one day (`P1D`) from the current date.

Now we have "yesterday's" date and the time stamps minus the date for our date we collected "today" we can recombine them with `("Yesterday's" date)||'T'||("Today's" timestamp)||'Z'`. Finally we can parse this conglomeration back into a usable time, again with `TIME_FORMAT(The stuff of nightmares)`.

> **TLDR** This results in us being table to take the timestamp of a record of today's data i.e. `2024-07-11T10:30:24.345` and artificially age it to make it look like it happened at the same time yesterday i.e. `2024-07-10T10:30:24.345`.

This initially seems like a lot of work for a simple change of 1 day to a time string but the value here comes from that every day your sample data will _always look exactly like yesterday's data_. For example if instead of "today" I ran this ingestion a week from now on `2024-07-18` the date in the time column of the ingested data would be `2024-07-17`.

The rest of our `SELECT` statement is just a list of the columns we are interested in.

You can now run your ingestion and watch "yesterday's" data appear in the segments view in the Druid web console.

```
SELECT "__time", "hex_ident_val", "altitude", "longitude", "latitude" FROM "adsb-json" WHERE "__time" >= CURRENT_TIMESTAMP - INTERVAL 48 HOURS
```

|__time|hex_ident_val|altitude|longitude|latitude|
|--------|---------------|----------|-----------|----------|
|2024-07-11T15:19:12.540Z|4401DC|38025|null|null|
|2024-07-10T15:19:12.540Z|4401DC|38025|null|null|
|...|...|...|...|...|


### Transforming 'Yesterday's" data

This is a different concept entirely but I'm going to demonstrate it on the ingestion we did in the previous section because it means I can reuse the same example. **_Fun!_**

Here's the same ingestion as above but now reduced to a granularity of 15 seconds for faster queries and reduced segment sizes.

```
REPLACE INTO "sample-data" OVERWRITE WHERE "__time" >= TIMESTAMP '2024-07-10' AND "__time" < TIMESTAMP '2024-07-11'
WITH "ext" AS (
  SELECT *
  FROM TABLE(
    EXTERN(
      '{"type":"http","uris":["https://github.com/hellmarbecker/kfd-demo-stack/raw/oss_flight_data_demo/oss-flight-data-demo/sample-data.json.gz"]}',
      '{"type":"json"}'
    )
  ) EXTEND ("time" VARCHAR, "kafka.header.ReceiverLat" VARCHAR, "date_message_logged" VARCHAR, "altitude" BIGINT, "time_message_generated" VARCHAR, "latitude" DOUBLE, "hex_ident_val" VARCHAR, "emergency" BIGINT, "ground_speed" BIGINT, "kafka.header.ClientTimezone" VARCHAR, "transmission_type" BIGINT, "client_id" VARCHAR, "aircraft_id" BIGINT, "client_lat" VARCHAR, "squawk" VARCHAR, "kafka.header.ReceiverLon" VARCHAR, "alert" BIGINT, "time_message_logged" VARCHAR, "callsign" VARCHAR, "ts_generated" VARCHAR, "track" BIGINT, "longitude" DOUBLE, "kafka.header.ClientID" VARCHAR, "is_on_ground" BIGINT, "session_id" BIGINT, "message_type" VARCHAR, "date_message_generated" VARCHAR, "spi" BIGINT, "client_lon" VARCHAR, "flight_id" BIGINT, "ts_logged" VARCHAR, "kafka.topic" VARCHAR, "kafka.key" VARCHAR, "vertical_rate" BIGINT)
)
SELECT
  TIME_FLOOR(TIME_PARSE(TIME_FORMAT(TIME_SHIFT(CURRENT_TIMESTAMP,'P1D',-1),'yyyy-MM-dd')||'T'||TIME_FORMAT(TIME_PARSE("time"),'HH:mm:ss.SSS')||'Z') , 'PT15S') AS "__time",
  "transmission_type",
  "hex_ident_val",
  "callsign",
  CAST("aircraft_id" AS VARCHAR) AS "aircraft_id",
  COUNT(*) AS "readings",
  MAX("altitude") AS "altitude",
  MAX("latitude") AS "latitude",
  MAX("longitude") AS "longitude",
  MAX("track") AS "track",
  MAX("ground_speed") AS "ground_speed",
  MAX("vertical_rate") AS "vertical_rate"
FROM "ext"
GROUP BY 1,2,3,4, 5
PARTITIONED BY DAY
```

After running the ingestion below we can run a query to get "yesterday's data"