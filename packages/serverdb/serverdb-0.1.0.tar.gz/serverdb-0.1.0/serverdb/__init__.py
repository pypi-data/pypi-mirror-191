from requests import get
from orjson import loads


class ServerDB():

    api = "https://api.countapi.xyz/"
    error = ""

    def __init__(self, user: str, project: str):
        self.data = f"{user}.{project}.com"
        self.user = user
        self.project = project

    def create(self, key: str, value: int = 0) -> bool:
        return get(self.api+"create", params={
            "key": self.apik(key),
            "namespace": self.data,
            "value": value,
            "enable_reset": 1,
        }).status_code == 200
    
    def set(self, key: str, value: int) -> int:
        return value if get(f"{self.api}set/{self.data}/{self.apik(key)}", params={"value": value}).status_code == 200 else -1
    
    def get(self, key: str) -> int:
        return loads(get(f"{self.api}get/{self.data}/{self.apik(key)}").text)["value"]
    
    def apik(self, key: str) -> str: return f"{self.project}{self.user}-{key}{len(self.data)}"