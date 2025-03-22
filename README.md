# URL Monitoring Service

This service checks the status of external URLs and exposes metrics in Prometheus format. It's designed to be deployed in a Kubernetes cluster using Helm.

## Features

- Monitors HTTP endpoints for availability (based on HTTP 200 status code)
- Measures response time in milliseconds
- Exposes metrics in Prometheus format
- Packaged as a Docker container
- Deployable to Kubernetes via Helm chart

## Metrics

The service exposes the following metrics:

- `sample_external_url_up{url="..."}`: 1 if the URL returns a 200 status code, 0 otherwise
- `sample_external_url_response_ms{url="..."}`: Response time in milliseconds
- `sample_external_url_request_count_total{url="..."}`: Counter of URL check attempts

Example output:
```
# HELP sample_external_url_up URL status (1 = up, 0 = down)
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0.0
sample_external_url_up{url="https://httpstat.us/200"} 1.0

# HELP sample_external_url_response_ms URL response time in milliseconds
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 633.38
sample_external_url_response_ms{url="https://httpstat.us/200"} 634.89

# HELP sample_external_url_request_count_total Counter of URL checks
# TYPE sample_external_url_request_count_total counter
sample_external_url_request_count_total{url="https://httpstat.us/503"} 1.0
sample_external_url_request_count_total{url="https://httpstat.us/200"} 1.0
```

## Local Development

### Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster for deployment
- Helm

### Running locally

1. Clone the repository:
   ```
   git clone https://github.com/GeorgiDimv/techhub.git
   cd url-monitor
   ```

2. Install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

3. Run the service:
   ```
   python3 app.py
   ```

4. Check metrics:
   ```
   curl http://localhost:8000
   ```

## Docker Setup

### Building Docker Image

Build the Docker image:

```
docker build -t url-monitor:latest .
```

Test the container:

```
docker run -p 8000:8000 url-monitor:latest
```

### Using Docker Compose

For easier local development, you can use Docker Compose:

1. Start the service:
   ```
   docker compose up
   ```

2. Run in the background:
   ```
   docker compose up -d
   ```

3. Check logs:
   ```
   docker compose logs -f
   ```

4. Stop the service:
   ```
   docker compose down
   ```

## Deploying to Kubernetes

### Step-by-Step Guide to Deploy with Helm

1. Make sure your kubectl is configured to interact with your cluster:
   ```
   kubectl cluster-info
   ```


2. Install the Helm chart:
   ```
   # For a local image or if your cluster can pull from your registry
   helm install url-monitor ./url-monitor-chart
   
   # Or, with custom values
   helm install url-monitor ./url-monitor-chart --set image.repository=registry/url-monitor
   ```

3. Check the status of your deployment:
   ```
   # Check the release status
   helm list
   
   # Check the pods are running
   kubectl get pods
   
   # Check the service is created
   kubectl get svc
   ```

## Viewing Metrics

### Basic Method
To view the raw metrics in Prometheus format:

```bash
# Port-forward the service
kubectl port-forward service/url-monitor 8000:8000

# View metrics in another terminal
curl http://localhost:8000
```

### Cleaning Up

To remove the deployment:

```
helm uninstall url-monitor
```


## Project Structure

- `app.py`: The main Python service code
- `requirements.txt`: Python dependencies
- `Dockerfile`: Instructions for building the Docker image
- `docker-compose.yml`: For local development/testing
- `url-monitor-chart/`: Helm chart for Kubernetes deployment
  - `values.yaml`: Configuration values for the Helm chart
  - `templates/`: Kubernetes manifest templates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a new Pull Request