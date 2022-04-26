import backend
import webapp
from apscheduler.schedulers.background import BackgroundScheduler


def start_backend():
    backend.everything()


def netz_politik_news_push():
    start_backend()
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(start_backend, 'interval', minutes=20)
    sched.start()
    webapp.webapp()


if __name__ == "__main__":
    netz_politik_news_push()
