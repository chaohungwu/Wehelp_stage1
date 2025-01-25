# -*- coding: utf-8 -*-

# In[2] Task2

"""
邏輯：
樂透版的文章標題、推/噓、日期
文章標題：str
文章標題：int
文章標題：Fri Jul 14 23:34:43 2023
逐步地去尋找相同的內容
"""

#抓取網頁html function
import urllib
import urllib.request as req
import bs4

def getdata(url):
    #url="https://www.ptt.cc/bbs/Lottery/index.html"
    
    #這邊要輸入一些你的請求辨識資訊
    #建立一個request物件，附加Request hraders 的資訊
    request = req.Request(url, headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        })
    
    
    #這邊用request物件來打開網址
    #with req.urlopen(url) as response:
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
        #print(data)
    return data

# In[] 
"""
整體做題邏輯：
進網頁取得標題，在取得標題時同時紀錄該標題的連結，執行3頁的文章抓取
然後再根據抓取的標題url取得html原始碼

"""
all_article_title_list=[]
all_article_url_list=[]
all_article_like_list=[]
all_article_publish_time_list=[]

for i in range(3): #往前翻3頁
    print("第{}頁文章".format(i))
    if i ==0: #第1頁的，因為第一頁的url後綴是index
        data = getdata("https://www.ptt.cc/bbs/Lottery/index.html")
        root = bs4.BeautifulSoup(data, "html.parser")
        article_titles_all = root.find_all("div", class_="title")#尋找所有<div class="title">的標題 取得所有文章標題
        article_like = root.find_all("div", class_="nrec")#尋找所有<div class="nrec">的標題 取得所有文章推數
        
        for i in range(len(article_titles_all)):#逐個文章取出標題、推數
            if article_titles_all[i].a != None: #不是已經刪文
            
                try:
                    article_data = getdata("https://www.ptt.cc{}".format(article_titles_all[i].a["href"]))#文章內的html
                    article_data_root = bs4.BeautifulSoup(article_data, "html.parser")
                    article_time_all = article_data_root.find_all("span", class_="article-meta-value")
                    
                    if article_time_all != []:
                    
                        all_article_publish_time_list.append(article_time_all[3].string)
                        all_article_title_list.append(article_titles_all[i].a.string) #加入文章title的list
                        
                        if article_like[i].span!=None:#加入文章堆文數的list
                            all_article_like_list.append(article_like[i].span.string) 
                        else:#如果那個文的推文數為0
                            all_article_like_list.append(0)                
                        
                        all_article_url_list.append(article_titles_all[i].a["href"])
                        
                    else:
                        pass
                                
                        
                except urllib.error.HTTPError:
                    pass
                
                
            else:
                pass
                
        lastpage_link = root.find("a", string="‹ 上頁")#取得上一頁的url
                
    else:
        data = getdata("https://www.ptt.cc{}".format(lastpage_link["href"]))
        root = bs4.BeautifulSoup(data, "html.parser")
        article_titles_all = root.find_all("div", class_="title")#尋找所有<div class="title">的標題
        article_like = root.find_all("div", class_="nrec")
        
        
        for i in range(len(article_titles_all)):#逐個文章取出標題、推數
            if article_titles_all[i].a != None: #如果沒刪文了的話
                
                #抓取推文數
                try:
                    article_data = getdata("https://www.ptt.cc{}".format(article_titles_all[i].a["href"]))#文章內的html
                    article_data_root = bs4.BeautifulSoup(article_data, "html.parser")
                    article_time_all = article_data_root.find_all("span", class_="article-meta-value")
                    
                    if article_time_all != []:
                    
                        all_article_publish_time_list.append(article_time_all[3].string)
                        all_article_title_list.append(article_titles_all[i].a.string) #加入文章title的list
                        
                        if article_like[i].span!=None:#加入文章堆文數的list
                            all_article_like_list.append(article_like[i].span.string) 
                        else:#如果那個文的推文數為0
                            all_article_like_list.append(0)                
                        
                        all_article_url_list.append(article_titles_all[i].a["href"])
                        
                    else:
                        pass
                            
                    
                except urllib.error.HTTPError:
                    pass
        

            else:
                pass
                
        lastpage_link = root.find("a", string="‹ 上頁")#取得上一頁的url


# In[] 
#import pandas as pd

def save_lists_to_csv(list1, list2, list3, filename):
    """
    將三個 list 的資料存成 CSV 文件
    """

    with open(filename, 'w') as csvfile:
        for row in zip(list1, list2, list3): #將3個csv合併成一個tuple，並對應3個list中每個index的值
            line = ','.join(map(str, row)) + '\n'
            csvfile.write(line)


save_lists_to_csv(all_article_title_list,
                  all_article_like_list,
                  all_article_publish_time_list,
                  r"G:\05_wehelp\03_week_work\01_stage1\week3\article.csv")






