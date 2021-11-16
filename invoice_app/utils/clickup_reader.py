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
    base_url = "https://api.clickup.com/api/v2/"
    team_id = 2443740
    dev_space_id = 4730256

    def __init__(self):
        request = Request(
            url="https://api.clickup.com/api/v2/space/4730256/folder?archived=false",
            headers=self.header,
        )
        response = urlopen(request, timeout=10).read()
        response = json.loads(response)

        self.folder_dict = {
            int(item["id"]): {
                "name": item["name"],
                "billable": 0,
                "non_billable": 0,
                "tasks": [],
            }
            for item in response["folders"]
        }
        self.backlog_lists = []
        for folder in response["folders"]:
            for task_list in folder["lists"]:
                if re.search("[bB]acklog", task_list["name"]):
                    self.backlog_lists.append(task_list["id"])
        
        url = f"https://api.clickup.com/api/v2/team"
        request = Request(
            url=url,
            headers=self.header,
        )
        response = urlopen(request).read()
        response = json.loads(response)
        self.assignees = [member["user"]["id"] for member in response["teams"][0]["members"]]

    def get_billed_tasks(self, start_date=None, end_date=None):
        if not end_date:
            end_date = datetime.now().timestamp()
        if not start_date:
            start_date = (datetime.today() - relativedelta(months=1)).timestamp()
            
        url = f"https://api.clickup.com/api/v2/team/2443740/time_entries?start_date={int(start_date)}000&end_date={int(end_date)}000&assignee={','.join([str(assignee) for assignee in self.assignees])}"
        request = Request(
            url=url,
            headers=self.header,
        )

        response = urlopen(request).read()
        response = json.loads(response)
        response = list(
            filter(
                lambda task: str(task["task_location"]["subcategory_id"]) in self.backlog_lists
                if isinstance(task["task"], dict)
                else False,
                response["data"],
            )
        )
        response = [
        {
            "task": {"id": timer["task"]["id"], "name": timer["task"]["name"]},
            "user": {"id": timer["user"]["id"], "name": timer["user"]["username"]},
            "billable": timer["billable"],
            "start": timer["start"],
            "end": timer["end"],
            "duration": timer["duration"],
            "folder": timer["task_location"]["category_id"],
        }
        for timer in response
        ]
        response = sorted(
            response, key=lambda timer: (timer["task"]["id"], timer["user"]["id"], timer["billable"])
        )

        def timer_reduce(timer1, timer2):
            new_timer = timer1
            new_timer["duration"] = str(int(new_timer["duration"]) + int(timer2["duration"]))
            return new_timer

        response = [
            reduce(timer_reduce, list(group))
            for _, group in groupby(
                response, key=lambda timer: (timer["task"]["id"], timer["user"]["id"], timer["billable"])
            )
        ]
        for _, group in groupby(response, key=lambda timer: str(timer["folder"])):
            group_tasks = list(group)
            folder_id = 0
            for task in group_tasks:
                folder_id = task["folder"]
                if task["billable"]:
                    self.folder_dict[folder_id]["billable"] += int(task["duration"] )
                else:
                    self.folder_dict[folder_id]["non_billable"] += int(task["duration"] )
            self.folder_dict[group_tasks[0]["folder"]]["tasks"] += group_tasks

        return self.folder_dict