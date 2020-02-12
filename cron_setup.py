from crontab import CronTab 

cron = CronTab(user=True)

job = cron.new(command='cd sgvheadlines && python3 scraper.py', comment='schedule daily execution of script')
job.hour.on(12)

cron.write()
