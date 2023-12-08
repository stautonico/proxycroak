from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

from proxycroak.models import SharedDecklist

scheduler = APScheduler()
