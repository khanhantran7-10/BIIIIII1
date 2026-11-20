import urllib.request
import json

base_url = "https://b-iiiiii-1wkb.vercel.app"

def post(endpoint, data):
    url = base_url + endpoint
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

post("/api/step1-analyze", {"raw_text": "Test"})
post("/api/step1-confirm", {})
post("/api/step2-upload", {"filename": "test.xlsx", "rows": [{"Doanh thu": 500, "Chi phí": 200, "Đơn hàng": 2}]})
post("/api/step2-confirm", {})
post("/api/step3-clean", {"options": {}})
post("/api/step3-confirm", {})
code, res = post("/api/step4-confirm", {})
print("Step4-confirm code:", code)
print("Step4-confirm message:", res.get("message"))
s5 = res.get("data", {}).get("step5", {})
print("Step5 has_dashboard:", s5.get("has_dashboard"))
print("Step5 kpis:", s5.get("kpis"))
print("Step5 quadrant_counts:", s5.get("quadrant_counts"))
