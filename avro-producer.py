from confluent_kafka.schema_registry import SchemaRegistryClient
from configparser import ConfigParser
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
from email.message import Message


key_schema = """ 
    {"type": "string"}
    """
#/Users/thejasreedasari/Applications/Kafka-Python-Docker/avro
with open('avro/Message.avsc') as f:
  value_schema = f.read()


topic = 'avro_python_test'
schemaurl = "https://psrc-o2wjx.us-east-2.aws.confluent.cloud"
schema_key = "EDKNVGDYYFEEKUOR"
schema_secret = "eoDP7BoVlKCxLye+c5Ip5FuXXjLtUe3Rt57nfPBeYUKWdI73v2VYwPHlvscYfi/j"

registry = SchemaRegistryClient({
  "url": schemaurl,
  "basic.auth.user.info": f'{schema_key}:{schema_secret}'
})

key_serializer = AvroSerializer(registry, key_schema)
value_serializer = AvroSerializer(registry, value_schema)
# Parse the configuration.
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
config_parser = ConfigParser()
with open('client.ini') as f:
  config_parser.read_file(f)
  config = dict(config_parser['default'])


config['key.serializer'] = key_serializer
config['value.serializer'] = value_serializer
producer = SerializingProducer(config)

for i in range(10):
  value = {'my_field1': i, 'my_field2': f'{i}'}
  try:
    producer.produce(topic=topic, key=f'{i}', value=value)
  except Exception as e:
    print(f"Exception while producing record value - {value} to topic - {topic}: {e}")
  else:
      print(f"Successfully producing record value - {value} to topic - {topic}")

producer.flush()
