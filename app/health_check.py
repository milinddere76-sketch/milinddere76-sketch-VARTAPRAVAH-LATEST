import requests
import time
import sys

def check_stream(url="http://localhost:8000/health"):
    """
    Checks the health of the VARTAPRAVAH service.
    Returns True if the service is online (200 OK).
    """
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🏥 [HEALTH] Monitoring VARTAPRAVAH Node...")
    while True:
        if check_stream():
            print("✅ Service is Healthy")
        else:
            print("⚠️ Service is DOWN or UNRESPONSIVE!")
            # In an enterprise flow, this could trigger a server restart
        
        time.sleep(30)
