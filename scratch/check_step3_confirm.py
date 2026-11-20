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

post("/api/step1-analyze", {
    "raw_text": "Doanh nghiệp",
    "business_profile": {"company_overview": "test"}
})
post("/api/step1-confirm", {})
post("/api/step2-upload", {"filename": "test.xlsx", "rows": [{"a": 1, "b": 2}]})
post("/api/step2-confirm", {})
post("/api/step3-clean", {"options": {}})
code, res = post("/api/step3-confirm", {})
print("Message:", res.get("message"))
print("Current unlocked step:", res.get("data", {}).get("current_unlocked_step"))
print("step4:", res.get("data", {}).get("step4"))
print("step5 keys:", list(res.get("data", {}).get("step5", {}).keys()))
print("step5 has_dashboard:", res.get("data", {}).get("step5", {}).get("has_dashboard"))
