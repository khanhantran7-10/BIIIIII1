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
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(body)
        except:
            return e.code, body
    except Exception as e:
        return 0, str(e)

# 1. Test status
code, res = post("/api/status", {})
print("1. /api/status:", code, res.get('status') if isinstance(res, dict) else res)

# 2. Test step1-analyze
code, res = post("/api/step1-analyze", {
    "raw_text": "Doanh nghiệp bán lẻ đa kênh thời trang và phụ kiện",
    "business_profile": {
        "company_overview": "Doanh nghiệp bán lẻ đa kênh",
        "primary_goal": "Tối ưu lợi nhuận ròng",
        "key_questions": ["Kênh nào sinh lời cao nhất?"]
    }
})
print("2. /api/step1-analyze:", code, res.get('status') if isinstance(res, dict) else res)

# 3. Test step1-confirm
code, res = post("/api/step1-confirm", {})
print("3. /api/step1-confirm:", code, res.get('status') if isinstance(res, dict) else res)

# 4. Test upload with dummy rows
dummy_rows = [
    {"Ngày": "2026-01-01", "Kênh": "Shopee", "Sản phẩm": "Áo sơ mi", "Doanh thu": 500000, "Giá vốn": 200000, "Chi phí Ads": 50000, "Số lượng": 2},
    {"Ngày": "2026-01-02", "Kênh": "TikTok", "Sản phẩm": "Quần jean", "Doanh thu": 800000, "Giá vốn": 350000, "Chi phí Ads": 150000, "Số lượng": 2},
    {"Ngày": "2026-01-03", "Kênh": "Lazada", "Sản phẩm": "Váy đầm", "Doanh thu": 600000, "Giá vốn": 250000, "Chi phí Ads": 80000, "Số lượng": 1},
]
code, res = post("/api/step2-upload", {"filename": "test.xlsx", "rows": dummy_rows})
print("4. /api/step2-upload:", code, res.get('status') if isinstance(res, dict) else res)

# 5. Test step2-confirm
code, res = post("/api/step2-confirm", {})
print("5. /api/step2-confirm:", code, res.get('status') if isinstance(res, dict) else res)

# 6. Test step3-clean
code, res = post("/api/step3-clean", {"options": {}})
print("6. /api/step3-clean:", code, res.get('status') if isinstance(res, dict) else res)

# 7. Test step3-confirm
code, res = post("/api/step3-confirm", {})
print("7. /api/step3-confirm:", code)
if isinstance(res, dict):
    print("   status:", res.get('status'))
    data = res.get('data', {})
    step5 = data.get('step5', {})
    print("   step5 has_dashboard:", step5.get('has_dashboard'))
    print("   step5 kpis:", step5.get('kpis'))
    print("   step5 quadrant_counts:", step5.get('quadrant_counts'))
    print("   step5 time_trend:", bool(step5.get('time_trend')))
else:
    print("   res:", res)
