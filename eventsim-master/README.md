# Streaming Simulator

This streaming simulator uses [Eventsim](./Eventsim.md) as data simulator with [Fluentd](https://www.fluentd.org/) as data collector that sends a small stream of data to [Minio](https://min.io/).

The data is generated inside a while loop, creating a continuous flow of logs in the ``/opt/eventsim/output`` folder. The fluentd agent is tailing the logs from this folder and sending these as packages of JSON files to S3 (or a compatible s3 storage like Minio). A sample of these files is located in [2023061719_20.json](samples/2023061719_20.json).

Each record contains the following information: 

```json
{
  "artist": "Daryl Hall & John Oates",
  "song": "Don't Hold Back Your Love",
  "duration": 313.8869,
  "ts": 1661129304330,
  "sessionId": 20857,
  "auth": "Logged In",
  "level": "paid",
  "itemInSession": 20,
  "city": "Memphis",
  "zip": "38135",
  "state": "TN",
  "userAgent": "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
  "lon": -89.848559,
  "lat": 35.238925,
  "userId": 212,
  "lastName": "Morgan",
  "firstName": "Tenli",
  "gender": "F",
  "registration": 1655316754330
}
```

The max size of each JSON file is 3MB, this can be modified in the [fluent.conf](fluent.conf). 

<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

- Docker
- Docker compose plugin


<!-- USAGE EXAMPLES -->
### Usage

This streaming simulator uses two services with docker-compose:

1) [Minio](https://min.io/): It is an open source S3 compatible object storage. This service help us emulate the S3 behavior locally. This can be replaced for real S3 in AWS or another object storage. 
2) Eventsim: This service is the one in charge to generate the simulated events and forward them to Minio as a Streaming Sink.
 
To run the streaming simulator just run:

```sh
docker compose up
```

The [entrypoint.sh](entrypoint.sh) will initialize the Minio Bucket and start sinking all the data in the bucket ``de-streaming-test`` and the path ``Raw/listen_events/``. The credentials to access the bucket are defined in [minio.env](minio.env), and it is possible to access via UI the bucket in http://localhost:9001 with the same credentials.

<!-- ADVANCE CONFIGURATIONS -->
## Advance Configurations

### Kafka

Kafka can be configured as sink, adding the [output plugging](https://github.com/fluent/fluent-plugin-kafka) configuration in [fluent.conf](fluent.conf)

### S3

In the case that the preferred sink is the real S3 instead the compatible solution (Minio), the following parameters needs to be updated in [fluent.conf](fluent.conf) with the proper credentials, bucket, and removing the s3_endpoint parameter.

```pycon
  aws_key_id minio_ak         # The access key for Minio
  aws_sec_key minio_sk        # The secret key for Minio
  s3_bucket de-streaming-test         # The bucket to store the log data
  s3_endpoint http://minio:9000/          # The endpoint URL (like "http://localhost:9000/")
```

### Other sinks

Refer to the Fluentd [documentation](https://www.fluentd.org/dataoutputs) to configure additional sinks. 