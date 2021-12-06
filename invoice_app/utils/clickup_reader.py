from urllib.request import Request, urlopen
from itertools import groupby
from functools import reduce
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json, re, os


class ClickupReader:
    header = {
        "Authorization": os.environ.get("CLICKUP_ACCESS_TOKEN"),
        "content-type": "application/json",
    }
    base_url = "https://api.clickup.com/api/v2"
    team_id = 2443740
    spaces = {
        "IN PROGRESS - DEV": 4730256,
        "SERVICE": 4730259,
        "DONE": 4730258,
        "IN PROGRESS - DESIGN/CONSULTING": 4730469,
    }
    
    def _get_folder_list(self):
        folders = []
        for space in self.spaces.values():
            request = Request(
                url=f"{self.base_url}/space/{space}/folder?archived=false",
                headers=self.header,
            )
            response = urlopen(request, timeout=10).read()
            response = json.loads(response)
            folders += response["folders"]
        
        return folders

    def __init__(self):
        folder_list = self._get_folder_list()
        self.folder_dict = {
            int(item["id"]): {
                "name": item["name"],
                "billable": 0,
                "non_billable": 0,
                "tasks": [],
            }
            for item in folder_list
        }
        self.backlog_lists = []
        for folder in folder_list:
            for task_list in folder["lists"]:
                if re.search("[bB]acklog", task_list["name"]):
                    self.backlog_lists.append(task_list["id"])
                    
        url = f"{self.base_url}/team"
        request = Request(
            url=url,
            headers=self.header,
        )
        response = urlopen(request).read()
        response = json.loads(response)
        self.assignees = [
            member["user"]["id"] for member in response["teams"][0]["members"]
        ]

    def get_billed_tasks(self, start_date=None, end_date=None):
        if not end_date:
            # ms
            end_date = datetime.now().timestamp() * 1000
        if not start_date:
            # ms
            start_date = (datetime.today() - relativedelta(months=1)).timestamp() * 1000

        url = f"https://api.clickup.com/api/v2/team/2443740/time_entries?start_date={int(start_date)}&end_date={int(end_date)}&assignee={','.join([str(assignee) for assignee in self.assignees])}"

        request = Request(
            url=url,
            headers=self.header,
        )
        response = urlopen(request).read()
        response = json.loads(response)

        response = list(
            filter(
                lambda task: str(task["task_location"]["list_id"]) in self.backlog_lists
                if "task" in task.keys() and isinstance(task["task"], dict)
                else False,
                response["data"],
            )
        )
        response = [
            {
                "task": {"id": timer["task"]["id"], "name": timer["task"]["name"]},
                "user": {"id": timer["user"]["id"], "name": timer["user"]["username"]},
                "billable": timer["billable"],
                "start": int(timer["start"][:-3]),  # ms
                "end": int(timer["end"][:-3]),  # ms
                "duration": int(timer["duration"][:-3])
                if len(timer["duration"]) > 3
                else 1,  # ms
                "folder": timer["task_location"]["folder_id"],
            }
            for timer in response
        ]
        response = sorted(
            response,
            key=lambda timer: (
                timer["task"]["id"],
                timer["user"]["id"],
                timer["billable"],
            ),
        )

        def timer_reduce(timer1, timer2):
            new_timer = timer1
            new_timer["duration"] = new_timer["duration"] + timer2["duration"]
            return new_timer

        response = [
            reduce(timer_reduce, list(group))
            for _, group in groupby(
                response,
                key=lambda timer: (
                    timer["task"]["id"],
                    timer["user"]["id"],
                    timer["billable"],
                ),
            )
        ]
        for _, group in groupby(response, key=lambda timer: str(timer["folder"])):
            group_tasks = list(group)
            folder_id = 0
            for task in group_tasks:
                folder_id = int(task["folder"])
                if task["billable"]:
                    # ms
                    self.folder_dict[folder_id]["billable"] += task["duration"]
                else:
                    # ms
                    self.folder_dict[folder_id]["non_billable"] += task["duration"]
            self.folder_dict[folder_id]["tasks"] += group_tasks
        return self.folder_dict
