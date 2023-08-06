def api(**kwargs):
    api_title = kwargs.get('api_title', 'My API')
    api_description = kwargs.get('api_description', 'My API Description')
    project = kwargs.get('project')
    region = kwargs.get('region')
    return f"""swagger: '2.0'
info:
  title: {api_title}
  description: {api_description}
  version: 0.0.0
schemes:
  - https
produces:
  - application/json
securityDefinitions:
  api_key:
    type: "apiKey"
    name: "key"
    in: "query"
paths:
  /hello-world:
    get:
      tags:
      - "Main"
      summary: Hello World
      operationId: hello_world
      consumes:
      - "application/json"
      x-google-backend:
        address: https://{region}-{project}.cloudfunctions.net/hello_world
      security:
      - api_key: []
      responses:
        "200":
          description: A successful response
          schema:
            $ref: "#/definitions/HelloWorldResponse"
  /docs:
    get:
      tags:
      - "Documentation"
      summary: Documentation
      operationId: docs
      x-google-backend:
        address: https://{region}-{project}.cloudfunctions.net/docs
      parameters:
      - in: "query"
        type: "string"
        name: "content"
        description: "Specify the content"
        enum: ["docs", "openapi.json"]
        default: "docs"
      responses:
        "200":
          description: A successful response
definitions:
  HelloWorld:
    type: "object"
    required:
      - value
    properties:
      value:
        type: "string"
  HelloWorldResponse:
    type: "object"
    required:
      - value
    properties:
      status:
        type: "string"

"""


def endpoint_main(name: str, **kwargs):
    if name == 'docs':
        return """import yaml
from flask import jsonify


def main(request):
    print(request)
    if request.args.get('content') == 'openapi.json':
        with open("api.yaml") as f:
            data = yaml.safe_load(f.read())
        return jsonify(data)

    return \"""<!DOCTYPE html>
<html>
<head>
<link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css">
<link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
<title>Sage-Gateway - Swagger UI</title>
</head>
<body>
<div id="swagger-ui">
</div>
<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js"></script>
<!-- `SwaggerUIBundle` is now available on the page -->
<script>
const ui = SwaggerUIBundle({
    url: '/docs?content=openapi.json',
"dom_id": "#swagger-ui",
"layout": "BaseLayout",
"deepLinking": true,
"showExtensions": true,
"showCommonExtensions": true,
oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect',
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
    ],
})
</script>
</body>
</html>
    \"""

"""
    return """from flask import jsonify

from .src.services import hello_world


def main(request):
    return jsonify({'status': hello_world.get_hello_world()})
"""


def endpoint_config(name: str, **kwargs):
    return """memory: 128MB
trigger: http
"""


def endpoint_lib(name: str, **kwargs):
    return """def get_hello_world():
    return "Hello World"

    """


def requirements():
    return """functions-framework
pyyaml
"""


def job_main():
    return """from shopcloud_serverless import Environment

if __name__ == "__main__":
    env = Environment()
    print(env.get('ENV'))
    print("Hello World")

"""


def job_procfile():
    return """web: python3 main.py"""
