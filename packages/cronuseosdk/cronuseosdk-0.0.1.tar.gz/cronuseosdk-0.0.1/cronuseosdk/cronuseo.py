import json
import requests

class Cronuseo:

    def __init__(self, endpoint, organization, token):
        
        self.__endpoint = endpoint
        self.__organization = organization
        self.__token = token

    def checkPermission(self,username, permission, resource):

        url = f"{self.__endpoint}/{self.__organization}/permission/check/username"
        data = json.dumps({"username": username, "permission": permission, "resource": resource})
        try: 
            response = requests.post(url, 
                                data= data, 
                                headers={"API_KEY": f"{self.__token}",
                                        "Content-Type": "application/json"}
                            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def checkPermissions(self,username, permissions, resource):

        url = f"{self.__endpoint}/{self.__organization}/permission/check/multi_actions"

        permissions = [{"permission": permission} for permission in permissions]

        data = json.dumps({"username": username, "permissions": permissions, "resource": resource})
        try: 
            response = requests.post(url, 
                                data= data, 
                                headers={"API_KEY": f"{self.__token}",
                                        "Content-Type": "application/json"}
                            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)