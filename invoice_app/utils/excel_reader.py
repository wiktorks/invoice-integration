from openpyxl import load_workbook
import datetime as dt


class ExcelReader:
    def __init__(self, path):
        wb = load_workbook(path)
        self.work_book = wb.active

    def add_time(self, time1: str, time2: str):
        # object timedelta z time2
        total = time1
        if time2:
            time_pattern = "%H:%M:%S"
            time_zero = dt.datetime.strptime("00:00:00", time_pattern)
            start_time = dt.datetime.strptime(time1, time_pattern)
            time_to_add = (
                dt.datetime.strptime(time2, time_pattern) if time2 else time_zero
            )
            total = str((start_time - time_zero + time_to_add).time())
            # total = str((start_time + time_to_add).time())

        return total

    def add_hours_to_project(
        self, project_name, total_hours, billable_hours, non_billable_hours
    ):
        if project_name in total_hours:
            total_hours[project_name]["billable"] = self.add_time(
                total_hours[project_name]["billable"], billable_hours
            )
            total_hours[project_name]["non_billable"] = self.add_time(
                total_hours[project_name]["non_billable"], non_billable_hours
            )
        else:
            total_hours[project_name] = {
                "billable": billable_hours if billable_hours else "00:00:00",
                "non_billable": non_billable_hours
                if non_billable_hours
                else "00:00:00",
            }

        return total_hours

    # TODO zoptymalizować algorytm do złożoności O(n)
    #! Użyj pandasa zamiast tego niżej (dask -> do optymalizacji Pandas)
    def get_total_hours_by_project(self):
        total_hours_per_company = {}
        total_hours_per_task = {}
        company_tasks = {}
        row_num = 2
        while self.work_book[f"A{row_num}"].value is not None:
            company = self.work_book[f"B{row_num}"].value
            task = self.work_book[f"D{row_num}"].value

            billable_hours = self.work_book[f"G{row_num}"].value
            non_billable_hours = self.work_book[f"H{row_num}"].value

            total_hours_per_company = self.add_hours_to_project(
                company, total_hours_per_company, billable_hours, non_billable_hours
            )
            total_hours_per_task = self.add_hours_to_project(
                task, total_hours_per_task, billable_hours, non_billable_hours
            )

            if company not in company_tasks:
                company_tasks[company] = set([task])
            else:
                company_tasks[company].add(task)

            row_num += 1

        total_hours = {}
        for company, task_set in company_tasks.items():
            total_hours[company] = {
                "billable": total_hours_per_company[company]["billable"],
                "non_billable": total_hours_per_company[company]["non_billable"],
                "tasks": {
                    task_name: total_hours_per_task[task_name]
                    for task_name in company_tasks[company]
                },
            }

        return total_hours

    def __enter__(self, value):

        return self

    def __exit__(self):
        pass
