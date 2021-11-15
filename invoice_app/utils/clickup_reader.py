from urllib.request import Request, urlopen
import re, json, os


class ClickupReader:
    header = {
        "Authorization": os.environ.get("CLICKUP_ACCESS_TOKEN"),
        "content-type": "application/json",
    }
    base_url = "https://api.clickup.com/api/v2/"
    team_id = 2443740
    dev_space_id = 4730256

    def __init__(self, json_path):
        self.json_path = json_path
        
    def cache_api_data(self):
        request = Request(
            url="https://api.clickup.com/api/v2/space/4730256/folder?archived=false",
            headers=self.header,
        )
        response = urlopen(request).read()
        response = json.loads(response)