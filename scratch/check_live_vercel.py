import urllib.request

req = urllib.request.Request(
    'https://b-iiiiii-1wkb.vercel.app/',
    headers={'User-Agent': 'Mozilla/5.0'}
)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8')

# Search for view-step-4 in the live html
idx = html.find('id="view-step-4"')
print("Found view-step-4 at:", idx)
if idx != -1:
    print(html[idx:idx+1200])
