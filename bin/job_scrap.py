"""
Script that creates the Cronjob for scrapping every 30min
"""

from crontab import CronTab
import os


cron = CronTab(user=True)

# CREATE COMMAND
python_path = os.path.join(
    os.getcwd(),
    os.pardir,
    'venv',
    'bin',
    'python'
)
script_path = os.path.join(
    os.getcwd(),
    'Scrapper',
    'ScrapperRunner.py'
)
command = f'"{python_path}" "{script_path}""'

job = cron(command=command, comment='housing_scrap')

# SET RESTRICTIONS
job.minute.on(10)
job.hour.every(1)

for item in cron:
    print(item)

cron.write()
