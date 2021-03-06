"""
Script that creates the Cronjob for scrapping every 30min
"""

from crontab import CronTab
import os

cron = CronTab(user=True)

# CREATE COMMAND
python_path = os.path.join(
    os.getcwd(),
    'venv',
    'bin',
    'python'
)
script_path = os.path.join(
    os.getcwd(),
    'housing',
    'Scrapper',
    'ScrapperRunner.py'
)
command = f'cd "{os.getcwd()}" && "{python_path}" "{script_path}"'
print(f"COMMAND : {command}")

job = cron.new(command=command, comment='housing_scrap')

# SET RESTRICTIONS
job.minute.on(10)
job.hour.every(1)

for item in cron:
    print(item)

cron.write()
