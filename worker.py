import logging
import requests
from celery import Celery

app = Celery('worker', 
    broker='amqp://{user}:{pw}@{host}//'.format(
        host='localhost',
        user='',
        pw='',
        ), )


print(app)

# adding tasks
@app.task
def load(*args, **kwargs):
    # logging.debug(args)
    print('==============================')
    str_integer = str(args[0])
    print(str_integer)
    url = 'https://admissions.drexel.edu/refer/?' + str_integer.zfill(16)
    print(url)
    r = requests.get(url)
    if 'We were unable to locate a letter of recommendation for this secure link.' in r.text:
        return False
    with open(str_integer + '.htm', 'w') as in_file:
        in_file.write(r.text)
    logging.debug('response written to file:' + str_integer + '.txt')
    return True