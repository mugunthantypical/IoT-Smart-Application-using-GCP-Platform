# IoT Weather Monitoring Station using Google Cloud Platform

Welcome to the repository for **IoT Weather Monitoring Station using Google Cloud Platform**. This project showcases an end-to-end IoT solution to monitor environmental conditions using Google Cloud Platform (GCP).

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [System Architecture](#system-architecture)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Security](#security)
* [Contributing](#contributing)
* [License](#license)

## Overview

This project presents a weather monitoring station that collects **temperature**, **humidity**, and **rainfall** data using a microcontroller and sensors, transmitting the data securely to GCP for processing, storage, and visualization.

The system combines:

* **DHT11** sensor (temperature & humidity)
* **Rain sensor**
* **Cytron Maker Feather S3**
* **Mosquitto MQTT broker**
* **MongoDB + BigQuery**
* **Looker Studio dashboard**

## Features

* Real-time environmental monitoring
* MQTT over TLS communication
* Sensor data storage in MongoDB and BigQuery
* Interactive dashboards using Looker Studio
* Scalable and secure GCP-based cloud architecture

## System Architecture

The solution is designed in five layers:

1. **Hardware Layer**: DHT11, Rain sensor, and Maker Feather S3.
2. **Communication Layer**: MQTT over TLS (Mosquitto broker on GCP VM).
3. **Cloud Infrastructure**: GCP Compute Engine, VPC firewall, IAM, and Service Account.
4. **Data Management Layer**: MongoDB for real-time ingestion; BigQuery for long-term storage and analysis.
5. **Visualization Layer**: Looker Studio dashboards connected to BigQuery.

## Getting Started

### Prerequisites

* [Arduino IDE](https://www.arduino.cc/en/software) (with PubSubClient library)
* [Python 3](https://www.python.org/)
* Google Cloud Platform account with billing enabled
* JSON service account key for BigQuery access

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mugunthantypical/IoT-Smart-Application-using-GCP-Platform.git
   cd IoT-Smart-Application-using-GCP-Platform
   ```

2. **Set up your Arduino hardware:**

   * Load `arduino-code.ino` to your Maker Feather S3 via Arduino IDE.
   * Install **PubSubClient** from Arduino Library Manager.

3. **Install VM dependencies:**

   ```bash
   sudo apt-get update && sudo apt-get install mosquitto mosquitto-clients mongodb python3-pip
   pip3 install pymongo google-cloud-bigquery paho-mqtt
   ```

4. **Upload the service account key:**

   ```bash
   nano service-account-key.json
   # Paste your JSON key content and save
   ```

## Usage

1. **Run Python MQTT listener** on your GCP VM:

   ```bash
   python3 mongo-bq.py
   ```

2. **Dashboard Visualization:**

   * Go to BigQuery > your dataset > table
   * Click `Explore with Looker Studio`
   * Create your own charts using real-time sensor data

## Project Structure

```
IoT-Smart-Application-using-GCP-Platform/
├── IoT-SmartApp-Report.pdf   # Project report and Guidelines
├── arduino-code.ino          # Microcontroller sensor script
├── mongo-bq.py               # Python script to ingest MQTT data and upload to BigQuery
├── README.md                 # Project documentation
```

## Security

The system enforces multiple layers of security:

* TLS encryption (port 8883) for MQTT communication
* GCP IAM roles with principle of least privilege
* VPC firewall with port-level access control
* OAuth tokens and session expiration for service access
* MongoDB and BigQuery data encryption (at-rest and in-transit)

## Contributing

Contributions are welcome via pull requests or issues.

## License

This repository is created for academic purposes for **CPC357 – IoT Architecture and Smart Applications**, Universiti Sains Malaysia.
