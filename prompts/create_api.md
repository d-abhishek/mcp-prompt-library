---
name: create_api
description: "Generate a REST API endpoint"
arguments:
  - name: resource
    description: "Resource name e.g. user"
    required: true
  - name: methods
    description: "HTTP methods, comma-separated"
    required: true
---

Please generate a REST API endpoint for **{{resource}}** supporting **{{methods}}**, including:
- input validation
- error handling
- example request/response
