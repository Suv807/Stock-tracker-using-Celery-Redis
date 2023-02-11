from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue
from channels.layers import get_channel_layer
import asyncio
import simplejson as json
@shared_task(bind=True)

def update_stock(self,stockpicker):# we want to update the data at regular interval from yahoo fin .after user have selected the stock it will update at the task of celery if the second user comes and select some stocks so instead of creating one seperate tasks in celery we will add 5 stocks in celeryif both user have some common stocks so it will reduce no of api calls

    data = {}
    available_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            stockpicker.remove(i)

    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put(
            {stockpicker[i]: json.loads(json.dumps(get_quote_table(arg1), ignore_nan=True))}),
                        args=(que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)

    # send data to group
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type': 'send_stock_update',
        'message': data,
    }))

    return 'Done'