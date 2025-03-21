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
- `sample_external_url_request_count{url="..."}`: Counter of URL check attempts

## Local Development

### Prerequisites

- Python 3.9+
- Docker
- Kubernetes cluster for deployment
- Helm

### Running locally

1. Clone the repository:
   ```
   git clone <repository-url>
   cd url-monitor
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the service:
   ```
   python app.py
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
   docker-compose up
   ```

2. Run in the background:
   ```
   docker-compose up -d
   ```

3. Check logs:
   ```
   docker-compose logs -f
   ```

4. Stop the service:
   ```
   docker-compose down
   ```

## Deploying to Kubernetes

### Using Helm

1. Make sure your kubectl is configured to interact with your cluster

2. Create a new Helm chart using the helm create command:
   ```
   helm create url-monitor
   ```

3. Replace the generated template files with the custom ones from this repository:
   - Replace `url-monitor/values.yaml` with our customized values.yaml
   - Replace `url-monitor/templates/deployment.yaml` with our deployment template
   - Replace `url-monitor/templates/service.yaml` with our service template
   
   Note: Keep other generated files (like _helpers.tpl, NOTES.txt, etc.) as they are.

3. Install the chart:
   ```
   helm install url-monitor ./url-monitor
   ```

4. Verify deployment:
   ```
   kubectl get pods
   kubectl get services
   ```

5. Check metrics from inside the cluster:
   ```
   kubectl port-forward service/url-monitor 8000:8000
   curl http://localhost:8000
   ```

### Updating the Deployment

To update the deployment after making changes:

```
helm upgrade url-monitor ./url-monitor
```

### Cleaning Up

To remove the deployment:

```
helm uninstall url-monitor
```

## Configuring Prometheus to Scrape Metrics

The Helm chart includes annotations to enable Prometheus scraping. If you have Prometheus installed in your cluster, it should automatically discover and scrape the service metrics.

If you're using the Prometheus Operator, you may need to create a ServiceMonitor:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: url-monitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: url-monitor
  endpoints:
  - port: metrics
    interval: 15s
```

## Project Structure

- `app.py`: The main Python service code
- `requirements.txt`: Python dependencies
- `Dockerfile`: Instructions for building the Docker image
- `url-monitor/`: Helm chart for Kubernetes deployment
  - `values.yaml`: Configuration values for the Helm chart
  - `templates/`: Kubernetes manifest templates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a new Pull Request