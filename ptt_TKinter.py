# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 22:38:09 2019

@author: Xiang
"""

import tkinter as tk
from tkinter.ttk import Combobox
from bs4 import BeautifulSoup
from tkinter import messagebox #如果要用messagebox要額外加這一行
import requests
import time
import webbrowser #產生url
import re
window = tk.Tk()
window.title("PTT爬蟲")
window.geometry("1000x600")
labelTop = tk.Label(window, text = "PTT熱門版爬蟲－－PTT熱門版爬蟲", bg = "pink", font = ("Arial", 18),
             width = 30, height = 2).pack(side = "top")
###
#爬取ptt熱門版
req = requests.get("https://www.ptt.cc/bbs/hotboards.html")
soup = BeautifulSoup(req.text, "lxml")
board = []
for item in soup.find_all("div", {"class": "board-name"}):
    board.append(item.get_text().strip())

board_name = []
for item in soup.find_all("div", {"class": "board-title"}):
    board_name.append(item.get_text().strip())
###    
cb1 = Combobox(window, values = board)
cb1.place(x = 130, y = 80)
tk.Label(window, text = "爬取的版： ", font = ("Arial", 12)).place(x = 40, y = 75)
tk.Label(window, text = "爬取頁數： ", font = ("Arial", 12)).place(x = 40, y = 105)
e = tk.Entry(window, font = ("Arial", 12))
e.place(x = 130, y =110)
###
#對應字串相加
def list_add(a, b):
    c = [a1+"："+b1 for a1, b1 in zip(a, b)]
    return c
###
def is_int(value):
  try:
    int(value)
    return True
  except:
    return False
###
def printProgress(iteration, total, prefix='', suffix='', decimals=1, barLength=100):
    """
    Call in a loop to create a terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    result = (('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)) + '\n')
    return result
###
# Make a list
items = list(range(0, 100))
i = 0
l = len(items)
# Initial call to print 0% progress
printProgress(i, l, prefix='Progress:', suffix='Complete',decimals=1, barLength=50)
###
timecost = []
timecost_2 = []
def catch():
    global html
    var.set("")
    page = e.get()
    if cb1.get() == "" and is_int(page) == False:
        tk.messagebox.showerror(title = "貼心小提醒", message= "請選擇要爬取的版以及頁數(必須為整數)")
    elif cb1.get() == "":
        tk.messagebox.showerror(title = "貼心小提醒", message= "請選擇要爬取的版")
    else:
        if is_int(page) == False:
            tk.messagebox.showerror(title = "貼心小提醒", message= "請輸入頁數(必須為整數)")
        else:
            page = int(e.get())
            r = requests.Session() #儲存自身的cookie
        #爬取資料
        if "Gossiping" in cb1.get() :
            start = time.time()
            payload = {"from": "/bbs/Gossiping/index.html", "yes": "yes"} #參數設定(字典)
            r.post("https://www.ptt.cc/ask/over18", data = payload) #模仿已滿18歲，並送出確認按鈕
            r2 = r.get("https://www.ptt.cc/bbs/Gossiping/index.html") #爬主頁面
            soup = BeautifulSoup(r2.text, "lxml")
            url = "https://www.ptt.cc/bbs/Gossiping/index.html"
            url_append = "https://www.ptt.cc"
            page = int(e.get())
        elif "sex" in cb1.get() :
            start = time.time()
            payload = {"from": "/bbs/sex/index.html", "yes": "yes"} #參數設定(字典)
            r.post("https://www.ptt.cc/ask/over18", data = payload) #模仿已滿18歲，並送出確認按鈕
            r2 = r.get("https://www.ptt.cc/bbs/sex/index.html") #爬主頁面
            soup = BeautifulSoup(r2.text, "lxml")
            url = "https://www.ptt.cc/bbs/sex/index.html"
            url_append = "https://www.ptt.cc"
            page = int(e.get())
        else:
            start = time.time()
            u1 = "https://www.ptt.cc/bbs/"
            u2 = cb1.get()
            u3 = "/index.html"
            r2 = r.get(u1 + u2 + u3) #爬主頁面
            soup = BeautifulSoup(r2.text, "lxml")
            url = u1 + u2 + u3
            url_append = "https://www.ptt.cc"
            page = int(e.get())
        array = 0
        #爬取標題 日期
        html = []      
        for i in range(page):
            r2 = r.get(url) #爬主頁面
            soup = BeautifulSoup(r2.text, "lxml")
            uppage = soup.findAll("a", class_="btn wide")
            title = soup.select(".r-ent")
            url = url_append + uppage[1]["href"]
            for item in title:
                if (item.a != None):
                    lb.insert("end", item.select('.date')[0].text.strip() + "　" + item.select('a')[0].text.strip())
                    array +=1
            time.sleep(0.1)
            i += 1
            k = printProgress(i*100/page, l, prefix='Progress:', suffix='Complete', barLength=50)
            Label = tk.Label(window, text = k)
            Label.place(x = 170, y = 400)
        #爬取內文網址
            for item in soup.find_all("a", {"href": re.compile("/bbs/" + cb1.get() + "/M")}):
                html.append(url_append + item["href"])
        end = time.time()
        tk.messagebox.showinfo(title = "貼心小提醒", message= "花費了" + str(round((end - start), 3)) + "秒" + "\n共爬取了" + str(array) + "篇文章")

b = tk.Button(window, text = "確認", command = catch)
b.place(x = 120, y = 140)
var = tk.StringVar()
##設置listbox跟捲動條##
frm = tk.Frame(window) #大框架
frm.place(x = 30, y = 190)
scrollbary = tk.Scrollbar(frm)
scrollbarx = tk.Scrollbar(frm, orient = tk.HORIZONTAL)#orient=tk.HORIZONTAL表示為橫向滾動
lb = tk.Listbox(frm, list = var, font = ("Arial", 10), width = 130,#設置橫向、豎向捲動軸
                yscrollcommand = scrollbary.set, xscrollcommand = scrollbarx.set, selectmode = "EXTENDED")
scrollbary.pack(side = "right", fill = "y") #擺在右邊#fill 向Y軸填滿滾動條
scrollbarx.pack(side = "bottom", fill = "x")
scrollbary.config(command = lb.yview)#設置config才能有效滾動
scrollbarx.config(command = lb.xview)#設置config才能有效滾動
lb.pack(expand = "yes", fill = "both")
##
def clear():
    var.set("")
    
b2 = tk.Button(window, text = "清除", command = clear)
b2.place(x = 170, y = 140)


def clear_search():
    var_null.set("")
    
def callback(url):
    webbrowser.open_new(url)
    
var_null = tk.StringVar()
short = tk.Label(window, textvariable = var_null,
                 font = ("Arial", 20), fg="blue", cursor="hand2")
short.place(x = 133, y = 520)
def print_selection():
    index = lb.curselection()#拿出滑鼠選定的項目的index
    var_null.set(html[index[0]])
    short.bind("<Button-1>", lambda e: callback(html[index[0]]))#繫結事件,(label被放置時，繫結callback函式)  
b3 = tk.Button(window, text = "產生網址", command = print_selection)
b3.place(x = 420, y = 480)
b4 = tk.Button(window, text = "清除", command = clear_search)
b4.place(x = 500, y = 480)

window.mainloop()