import urllib.request
import json

req = urllib.request.Request(
    'https://api.github.com/repos/khanhantran2k7-3786/b-iiiiii-1wkb/commits',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    with urllib.request.urlopen(req) as response:
        commits = json.loads(response.read().decode('utf-8'))
        for c in commits[:5]:
            print(c['sha'][:7], c['commit']['committer']['date'], c['commit']['message'])
except Exception as e:
    print("Error:", e)
