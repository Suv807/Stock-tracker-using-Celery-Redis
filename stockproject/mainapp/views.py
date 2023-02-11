from django.shortcuts import render
from django.http.response import HttpResponse
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread
from asgiref.sync import sync_to_async
# Create your views here.

def stockPicker(request):
    stock_picker=tickers_nifty50()
    print(stock_picker)
    return render(request,'mainapp/stockpicker.html',{'stockpicker':stock_picker})


@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True

async def stockTraker(request):
    is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
    stockpicker = request.GET.getlist('stockpicker')
    stockshare = str(stockpicker)[1:-1]

    print(stockpicker)
    data={}
    available_stocks=tickers_nifty50()#we want user to pick the available stocks from nifty 50
    for i in stockpicker:
        if i in available_stocks:

            pass
        else:
            return HttpResponse("Error")
    n_threads=len(stockpicker)# We have use multithreading to increase the efficiency it will take less time to update the data
    thread_list = []
    que=queue.Queue()
    start=time.time()
    print(start)
    # for i in stockPicker:
    #     result = get_quote_table(i)  # get the real time data of the stock. web scrape the yahoo data
    #     data.update({i:result})# append in inside our data
    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}),
                        args=(que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    for thread in thread_list:
        thread.join()

    while not que.empty():
        result=que.get()
        data.update(result)
    end=time.time()
    time_taken=end-start
    print(time_taken)
    print(data)
    return render(request,'mainapp/stocktracker.html',{'data':data,'room_name':'track','selectedstock':stockshare})
