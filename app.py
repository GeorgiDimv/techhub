import time
import requests
from prometheus_client import start_http_server, Gauge, Counter
import logging
import schedule
import threading
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the URLs to monitor
URLS = [
    "https://httpstat.us/503",
    "https://httpstat.us/200"
]

# Define Prometheus metrics
url_up = Gauge('sample_external_url_up', 'URL status (1 = up, 0 = down)', ['url'])
response_time = Gauge('sample_external_url_response_ms', 'URL response time in milliseconds', ['url'])
request_count = Counter('sample_external_url_request_count', 'Counter of URL checks', ['url'])

def check_url(url):
    """
    Check if the URL is up and measure response time
    """
    logger.info(f"Checking URL: {url}")
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        status = 1 if response.status_code == 200 else 0
        
        # Update Prometheus metrics
        url_up.labels(url=url).set(status)
        response_time.labels(url=url).set(duration_ms)
        request_count.labels(url=url).inc()
        
        logger.info(f"URL: {url}, Status: {status}, Response time: {duration_ms:.2f}ms")
    except requests.RequestException as e:
        logger.error(f"Error checking URL {url}: {e}")
        url_up.labels(url=url).set(0)
        response_time.labels(url=url).set(0)
        request_count.labels(url=url).inc()

def check_all_urls():
    """
    Check all defined URLs
    """
    for url in URLS:
        check_url(url)

def run_scheduler():
    """
    Run the URL checks on a schedule
    """
    schedule.every(30).seconds.do(check_all_urls)
    
    # Run once immediately
    check_all_urls()
    
    # Keep running the scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('METRICS_PORT', 8000))
    
    # Start Prometheus HTTP server
    start_http_server(port)
    logger.info(f"Prometheus metrics server started on port {port}")
    
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Service stopped")