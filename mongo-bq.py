import pymongo
from google.cloud import bigquery
from datetime import datetime
import paho.mqtt.client as mqtt
import os
import json
from google.protobuf.timestamp_pb2 import Timestamp

# Set up Google Cloud credentials 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-key.json'

# MongoDB Configuration
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["weatherstation"]
collection = db["iot"]

# BigQuery Configuration
bigquery_client = bigquery.Client()
dataset_id = 'sensor_data'
table_id = 'environmental_readings'

# Create the BigQuery table schema
schema = [
    bigquery.SchemaField('timestamp', 'TIMESTAMP', mode='REQUIRED'),
    bigquery.SchemaField('temperature', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('humidity', 'FLOAT', mode='NULLABLE'),
    bigquery.SchemaField('rain', 'INTEGER', mode='NULLABLE')
]

# Create or get the table
dataset_ref = bigquery_client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)

try:
    table = bigquery_client.get_table(table_ref)
except Exception:
    table = bigquery.Table(table_ref, schema=schema)
    table = bigquery_client.create_table(table)

# MQTT Configuration
mqtt_broker_address = "34.31.221.19"  # Use the same MQTT server IP as in Arduino code
mqtt_topic = "iot"

def parse_mqtt_payload(payload):
    """
    Parse the MQTT payload into structured data
    Assumes payload format: "Temperature: X.XX °C, Humidity: Y.YY %, Rain: Z"
    """
    try:
        # Split the payload into components
        parts = payload.split(', ')
        
        # Extract temperature
        temp_str = parts[0].split(': ')[1].replace(' °C', '')
        temperature = float(temp_str)
        
        # Extract humidity
        humidity_str = parts[1].split(': ')[1].replace(' %', '')
        humidity = float(humidity_str)
        
        # Extract rain value
        rain_str = parts[2].split(': ')[1]
        rain = int(rain_str)
        
        return temperature, humidity, rain
    except Exception as e:
        print(f"Error parsing payload: {payload}")
        print(f"Error details: {e}")
        return None, None, None

def on_connect(client, userdata, flags, reason_code, properties):
    """MQTT connection callback"""
    if reason_code == 0:
        print("Successfully connected to MQTT broker")
        client.subscribe(mqtt_topic)
    else:
        print(f"Failed to connect, return code {reason_code}")

def on_message(client, userdata, message):
    """
    MQTT message receive callback
    Parses the message and uploads to BigQuery
    """
    payload = message.payload.decode("utf-8")
    print(f"Received message: {payload}")
    
    # Parse payload
    temperature, humidity, rain = parse_mqtt_payload(payload)
    
    # Skip if parsing failed
    if temperature is None:
        return
    
    # Prepare row for BigQuery
    timestamp = Timestamp()
    timestamp.GetCurrentTime()
    
    # Convert Timestamp to a string (ISO 8601 format)
    timestamp_str = timestamp.ToJsonString()

    row = {
        'timestamp': timestamp,
        'temperature': temperature,
        'humidity': humidity,
        'rain': rain
    }
    
    # Insert row into BigQuery
    try:
        errors = bigquery_client.insert_rows_json(table, [json.dumps(row)])
        if errors:
            print(f"Errors inserting row: {errors}")
        else:
            print("Row successfully inserted into BigQuery")
    except Exception as e:
        print(f"Error inserting into BigQuery: {e}")

# Create MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(mqtt_broker_address, 8883, 60)

# Start the MQTT loop
print("Starting MQTT listener and BigQuery uploader...")
client.loop_forever()