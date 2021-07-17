import celery
import os
                
celeryApp = celery.Celery('example')
celeryApp.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@celeryApp.task
def add(x, y):
    return x+y