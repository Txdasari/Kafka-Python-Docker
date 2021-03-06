# Schemaful Kafka streaming with Python and AVRO

Basic Python AVRO consumer and producer implementation.

This repository accompanies
[Schemafull streaming data processing in ML pipelines](https://towardsdatascience.com/using-kafka-with-avro-in-python-da85b3e0f966) article.

## Running

Running all the services:
`docker-compose -f docker-compose.yaml up --build -d`

Attaching to the app's logs:
`docker-compose logs worker -f`

## Compiling AVRO into Python classes

Compiling AVRO schema `./avro/Messgae.avsc` into Python classes
is done during building docker image, that is why some imports
in the `__main__.py` can be unreachable. However, it is possible to
generate those classes with the [`avro-to-python`](https://pypi.org/project/avro-to-python/)
tool:
```shell
pip install avro_to_python==0.3.2

avro_to_python ./avro . 
# alternative command: `python -m avro_to_python.cli ./avro .`
```
This will result in the `protocol` Python package generated which will contain
the `Message` and `Data` classes.

# Docker commands for reference
docker build -t python-imdb .
docker run python-imdb

docker build -t kafka-imdb . 
docker buildx build --platform=linux/amd64 -t kafka-test-imdb .
docker tag kafka-test-imdb  783819836456.dkr.ecr.us-east-1.amazonaws.com/fargate
