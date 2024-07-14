from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json

# Creating a Flask app instance
app = Flask(__name__)

@app.route("/createJIRA", methods=["POST"])
def createJIRA():
    # Get the incoming JSON payload
    payload = request.json

    # Check if the comment body contains '/jira'
    if payload.get("comment", {}).get("body", "") == "/jira":
        url = "https://abdbeast69.atlassian.net/rest/api/3/issue"
        auth = HTTPBasicAuth("abdbeast69@gmail.com", "<api-token>")  # Replace with your API token

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        jira_payload = json.dumps({
            "fields": {
                "issuetype": {
                    "id": "10003"
                },
                "project": {
                    "key": "SCRUM"
                },
                "summary": "My first JIRA ticket",
            }
        })

        # Make the POST request to create an issue
        response = requests.post(
            url,
            data=jira_payload,
            headers=headers,
            auth=auth
        )

        # Check response status
        if response.status_code == 201:  # 201 Created
            success_message = "Issue created successfully!"
            json_response = json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": "))
            return f"{success_message}\n{json_response}"
        else:
            error_message = f"Request failed with status code: {response.status_code}"
            response_content = response.text
            return f"{error_message}\nResponse content: {response_content}"
    else:
        return "Comment does not contain /jira. No action taken."

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)
