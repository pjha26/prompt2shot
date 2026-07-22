import time
import urllib.request
import urllib.error
import json

data = json.dumps({
    "product_name": "Florentine Wooden Salad Bowl",
    "description": "A match made in summer - salads and wooden bowls. Handpainted on mango wood, this compact salad bowl serves a supper for two."
}).encode('utf-8')

req = urllib.request.Request('http://127.0.0.1:8000/generate', data=data, headers={'Content-Type': 'application/json'})

try:
    res = urllib.request.urlopen(req)
    response_data = json.loads(res.read().decode())
    job_id = response_data['job_id']
    print(f"Created job: {job_id}")
    
    while True:
        res = urllib.request.urlopen(f'http://127.0.0.1:8000/jobs/{job_id}')
        job_data = json.loads(res.read().decode())
        print(f"Status: {job_data['status']}")
        if job_data['status'] in ['completed', 'failed']:
            print(json.dumps(job_data, indent=2))
            break
        time.sleep(1)
except urllib.error.URLError as e:
    print(f"Error fetching API: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode())
except Exception as e:
    print(f"Error: {e}")
