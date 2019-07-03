import requests
import json


# Call deploy instructions endpoint to access deploy command
def deploy_app(app_name: str) -> str:
    try:
        response = requests.get("https://api.kscout.io/apps/id/" + app_name + "/deployment-instructions", verify=False)
        if response.status_code != 200:
            status = dict()
            status["error connecting to kscout"] = "kscout api not reachable"
            raise Exception(status)
        resp = {"text": response.json()["instructions"]}
        return json.dumps(resp)

    except ConnectionRefusedError:
        status = dict()
        status["error connecting to kscout"] = "Connection Refused"
        raise Exception(status)
    except Exception as e:
        status = dict()
        status["error connecting to kscout"] = str(e)
        raise Exception(status)
