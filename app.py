from flask import Flask, request, Response
import requests

app = Flask(__name__)

IBKR_GATEWAY = "http://100.85.23.15:5000"  # vervang met Tailscale IP van je Hetzner-server

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{IBKR_GATEWAY}/{path}"
    headers = {'Content-Type': 'application/json'}
    try:
        if request.method == 'GET':
            resp = requests.get(url, headers=headers, verify=False)
        else:
            resp = requests.post(url, headers=headers, json=request.json, verify=False)

        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type', 'application/json'))
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
