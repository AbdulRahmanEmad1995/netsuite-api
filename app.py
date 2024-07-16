import requests
from requests_oauthlib import OAuth1
from flask import Flask, request, Response
from flask_cors import CORS
import json

# Initialize flask instance of our application
app = Flask(__name__)
CORS(app)

@app.route("/api/v1/netsuite", methods=["POST"])
def perform_oauth_request() -> Response | tuple[Response, int] | str:
    
    body = json.loads(request.data)
    # check ig we have authorization error
    
    response = {}
    if "error code" in body or "error message" in body:
        message, code = body.split("error message:")[1], body.split("error code:")[1]
        response["error code"] = code
        response["error message"] = message
        return Response(response)

    try:
        req_url = body["url"] 
        req_headers = body["headers"]
        req_data = body["data"]
        req_auth = body["auth"]
        req_method = body["method"]

        # extract authorization data
        consumer_key = req_auth["consumer_key"]
        consumer_secret = req_auth["consumer_secret"]
        access_token = req_auth["access_token"]
        secret_token = req_auth["secret_token"]
        signature_method = req_auth["signature_method"]
        realm = req_auth["realm"]
        _force_flag = True
        force_include_body = req_auth["force_include_body"]
        if(force_include_body.lower() == "false"):
           _force_flag = False
        
        # Create an OAuth1 session
        oauth = OAuth1(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=secret_token,
            signature_method= signature_method,
            realm=realm,
            force_include_body=_force_flag,
        )
        
        # Make the POST request
        if req_method.lower() == "post":
            response = requests.post(req_url, headers=req_headers, json=req_data, auth=oauth)
        elif req_method.lower() == "get":
            response = requests.get(req_url, headers=req_headers, json=req_data, auth=oauth)
        elif req_method.lower() == "delete":
            response = requests.delete(req_url, headers=req_headers, json=req_data, auth=oauth)
        elif req_method.lower() == "put":
            response = requests.put(req_url, headers=req_headers, json=req_data, auth=oauth)
        elif req_method.lower() == "patch":
            response = requests.patch(req_url, headers=req_headers, json=req_data, auth=oauth)
    except Exception as e:
        return str(e), 500    
    return {"response": json.loads(response.text), "code": response.status_code}

# if __name__ == "__main__":
#     app.run(debug=True, threaded=True)
