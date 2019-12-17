import logging
import requests
from celery import Celery
from utils import USER_AGENT_LIST
app = Celery('worker', 
    broker='amqp://{user}:{pw}@{host}//'.format(
        host='localhost',
        user='dc_rabbitmq_user',
        pw='zR3gp5zTJwkwA7wA',
        ), )


print(app)

# adding tasks
@app.task
def load(*args, **kwargs):
    # logging.debug(args)
    print('==============================')
    str_integer = str(args[0])
    print(str_integer)
    return True
    url = 'https://admissions.drexel.edu/refer/?' + str_integer.zfill(16)
    print(url)
    
    session = requests.session()
    session.proxies = {
        'https': 'socks5h://localhost:9050',
        'http': 'socks5h://localhost:9050'
        }
    
    headers = {
        'User-agent': USER_AGENT_LIST[int(str_integer[-1])]
    }
    try:
        r = session.get(url)
    except Exception as e:
        logging.error(e)
        logging.info('adding integer back to q: {}'.format(str_integer))
        load.delay(args[0])
        return False
    if 'We were unable to locate a letter of recommendation for this secure link.' in r.text:
        return False
    with open(str_integer + '.htm', 'w') as in_file:
        in_file.write(r.text)
    logging.debug('response written to file:' + str_integer + '.txt')
    return True