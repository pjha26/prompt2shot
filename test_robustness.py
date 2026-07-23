import urllib.request
import urllib.error
import json
import time

def submit_job(product_name, description):
    data = json.dumps({
        "product_name": product_name,
        "description": description
    }).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/generate', data=data, headers={'Content-Type': 'application/json'})
    try:
        res = urllib.request.urlopen(req)
        response_data = json.loads(res.read().decode())
        return response_data.get('job_id')
    except urllib.error.HTTPError as e:
        return f"HTTPError {e.code}: {e.read().decode()}"
    except Exception as e:
        return f"Error: {e}"

def poll_job(job_id):
    if not job_id or "Error" in str(job_id):
        return None
    
    print(f"Polling job {job_id}...")
    while True:
        try:
            res = urllib.request.urlopen(f'http://127.0.0.1:8000/jobs/{job_id}')
            job_data = json.loads(res.read().decode())
            if job_data['status'] in ['completed', 'failed']:
                return job_data
            time.sleep(1.5)
        except Exception as e:
            print(f"Poll Error: {e}")
            break

print("--- Test 1: Empty Product Name ---")
res = submit_job("   ", "Valid description")
print(res)

print("\n--- Test 2: Very Long Description ---")
res = submit_job("Cool Product", "A" * 2500)
print(res)

print("\n--- Test 3: Tech Gadget ---")
job1 = submit_job("Cyberpunk Smartwatch", "A futuristic smartwatch with neon glowing edges and a holographic display. Cyberpunk aesthetic, dark background.")
print(f"Submitted Tech Gadget: {job1}")

print("\n--- Test 4: Vintage Furniture ---")
job2 = submit_job("Mid-Century Modern Armchair", "A stylish mid-century modern armchair with mustard yellow upholstery and wooden legs, placed in a well-lit living room.")
print(f"Submitted Furniture: {job2}")

print("\n--- Awaiting Results ---")
for job_id in [job1, job2]:
    result = poll_job(job_id)
    if result:
        print(f"Result for {result['product_name']}: Status={result['status']}, URL={result.get('image_url')}")
