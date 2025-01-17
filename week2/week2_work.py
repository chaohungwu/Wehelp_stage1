#week2 work


# In[1]task1


#task1 邏輯紀錄：
#將每個站設定一個值，然後用彼此兩個值的差絕對值去比大小，找出最小的那一個

"""
messages:(str) 回傳的json

"""


def find_and_print(messages, current_station):
    #my code
    #各站點值
    station_value1 = {"Songshan":0, 
                     "Nanjing Sanmin":1,
                     "Taipei Arena":2,
                     "Nanjing Fuxing":3,
                     "Songjiang Nanjing":4,
                     "Zhongshan":5,
                     "Beimen":6,
                     "Ximen":7,
                     "Xiaonanmen":8,
                     "Chiang Kai-Shek Memorial Hall":9,
                     "Guting":10,
                     "Taipower Building":11,
                     "Gongguan":12,
                     "Wanlong":13,
                     "Jingmei":14,
                     "Dapinglin":15,
                     "Qizhang":16,
                     "Xiaobitan":17,
                     "Xindian City Hall":18,
                     "Xindian":19,
                     }


    #取得現有捷運站的站點值
    now_station_value = station_value1[current_station]
    mes_name= list(messages.keys())
    mes_station=[]
    station_distance = []

    ##校正值(因為有人在捷運站，有人在捷運站附近，在站點的為0，在附近的為0.5)
    fix_value=[0.5,0,0.5,0.5,0]

    #取得朋友訊息中站點的資訊，並獲取站點值
    for i in range(len(mes_name)):
        #現在查詢的名子 mes_name[i]        
        
        #從所有站點值dic中找出訊息中站點的值,這邊的st是站名
        for st in station_value1.keys():
            if st in messages[mes_name[i]]:
                mes_station.append(station_value1[st])
                station_distance.append(abs(now_station_value - station_value1[st])+ fix_value[i])##差值絕對值
                
            else:
                pass
    
    return mes_name[station_distance.index(min(station_distance))]



messages={"Leslie":"I'm at home near Xiaobitan station.", 
          "Bob":"I'm at Ximen MRT station.", 
          "Mary":"I have a drink near Jingmei MRT station.", 
          "Copper":"I just saw a concert at Taipei Arena.", 
          "Vivian":"I'm at Xindian station waiting for you." }



find_and_print(messages, "Wanlong") # print Mary 
find_and_print(messages, "Songshan") # print Copper 
find_and_print(messages, "Qizhang") # print Leslie 
find_and_print(messages, "Ximen") # print Bob 
find_and_print(messages, "Xindian City Hall") # print Vivian

# In[2] task2

"""
邏輯紀錄：
consultants：(list)預約內容
hour：(int)預約時間
duration：(int)預約時長
criteria：(str)預約標準依據price or rate

建立一個dict去做那個時間的查詢，先依據標準做查詢，然後依序查詢三個顧問可不可以
"""

global John_book_db
global Bob_book_db
global Jenny_book_db
global answer

John_book_db = []
Bob_book_db=[]
Jenny_book_db=[]
answer=""

##可預訂為1
for i in range(24):
    John_book_db.append(1)
    Bob_book_db.append(1)
    Jenny_book_db.append(1)



# your code here, maybe
def book(consultants, hour, duration, criteria):
    # your code here
    answer=""
    #1.先做檢視評判標準的價格順序表
    price_select={} #放價格
    
    for i in range(len(consultants)):
        #price_select.append(consultants[i]["price"])
        price_select[consultants[i]["price"]] = consultants[i]["name"]
        price_select_sort = sorted(price_select.keys()) #價格順序，用這個去找price_select裡的名子
    
    
    #2.先做檢視評判標準評分的順序表
    rate_select={} #放評分
    
    for i in range(len(consultants)):
        #price_select.append(consultants[i]["price"])
        rate_select[consultants[i]["rate"]] = consultants[i]["name"]
        rate_select_sort = sorted(rate_select.keys(),reverse = True) #價格順序，用這個去找price_select裡的名子

    
    #先做檢視評判標準(價格)
    if criteria =="price":
        for p1 in range(len(price_select_sort)):
            #依照標準選出顧問
            price_select[price_select_sort[p1]]


            #看要選哪個顧問的時間點
            if price_select[price_select_sort[p1]] == "John":
                #看這個顧問這個時間有沒有空
                if 0 not in John_book_db[hour:(hour+duration)]:
                #if John_book_db[hour]==1:
                    John_book_db[hour]=0 #變成無法預定
                    for t in range(1,duration+1):#把預訂時長內的時間變為無法預定
                        John_book_db[hour+t]=0 #變成無法預定
                        
                    answer = price_select[price_select_sort[p1]]
                    break #跳出迴圈
                
                #這個顧問沒時間
                else:
                    pass
            
            
            elif price_select[price_select_sort[p1]] == "Bob":
                #看這個顧問這個時間有沒有空
                if 0 not in Bob_book_db[hour:(hour+duration)]:
                #if Bob_book_db[hour]==1:
                    Bob_book_db[hour]=0 #變成無法預定
                    for t in range(1,duration+1):#把預訂時長內的時間變為無法預定
                        Bob_book_db[hour+t]=0 #變成無法預定

                    answer = price_select[price_select_sort[p1]]
                    break #跳出迴圈
                #這個顧問沒時間
                else:
                    pass
                
            
            elif price_select[price_select_sort[p1]] == "Jenny":
                #看這個顧問這個時間有沒有空
                if 0 not in Jenny_book_db[hour:(hour+duration)]:

                #if Jenny_book_db[hour]==1:
                    Jenny_book_db[hour]=0 #變成無法預定
                    for t in range(1,duration+1):#把預訂時長內的時間變為無法預定
                        Jenny_book_db[hour+t]=0 #變成無法預定

                    answer = price_select[price_select_sort[p1]]
                    break #跳出迴圈
                #這個顧問沒時間
                else:
                    pass
        
        
          
    #先做檢視評判標準(評分)
    if criteria =="rate":
        for p1 in range(len(rate_select_sort)):
            #依照標準選出顧問
            rate_select[rate_select_sort[p1]]


            #看要選哪個顧問的時間點
            if rate_select[rate_select_sort[p1]] == "John":
                #看這個顧問這個時間有沒有空
                if 0 not in John_book_db[hour:(hour+duration)]:
                #if John_book_db[hour]==1:
                    John_book_db[hour]=0 #變成無法預定
                    for t in range(1,duration+1):#把預訂時長內的時間變為無法預定
                        John_book_db[hour+t]=0 #變成無法預定
                        
                    answer = rate_select[rate_select_sort[p1]]
                    break #跳出迴圈
                
                #這個顧問沒時間
                else:
                    pass
            
            
            elif rate_select[rate_select_sort[p1]] == "Bob":
                #看這個顧問這個時間有沒有空
                if 0 not in Bob_book_db[hour:(hour+duration)]:
                #if Bob_book_db[hour]==1:
                    Bob_book_db[hour]=0 #變成無法預定
                    for t in range(1,duration+1):#把預訂時長內的時間變為無法預定
                        Bob_book_db[hour+t]=0 #變成無法預定

                    answer = rate_select[rate_select_sort[p1]]
                    break #跳出迴圈
                #這個顧問沒時間
                else:
                    pass
                
            
            elif rate_select[rate_select_sort[p1]] == "Jenny":
                #看這個顧問這個時間有沒有空
                if 0 not in Jenny_book_db[hour:(hour+duration)]:

                #if Jenny_book_db[hour]==1:
                    Jenny_book_db[hour]=0 #變成無法預定
                    for t in range(1,duration+1):#把預訂時長內的時間變為無法預定
                        Jenny_book_db[hour+t]=0 #變成無法預定

                    answer = rate_select[rate_select_sort[p1]]
                    break #跳出迴圈
                #這個顧問沒時間
                else:
                    pass  
        
        
        
        if answer=="":
            answer="No Service "
        
        else:
            pass
            
    return answer







consultants = [{"name":"John", "rate":4.5, "price":1000},
               {"name":"Bob", "rate":3, "price":1200},
               {"name":"Jenny", "rate":3.8, "price":800}]

book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate") # Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John




# In[3] task3
"""
邏輯紀錄：

"""

def func(*data): 
    # your code here 
    
    #所有輸入的名子
    name_tumple = data
    center_word_list = []
    center_word_count = []
    uniqul_name=""
    
    #每個名子做處理取中間名
    for i in range(len(name_tumple)):
        #判斷裡面有幾個字
        #字數為兩個字
        if len(name_tumple[i])/2 == 1:
            center_word_list.append(name_tumple[i][1])
        
        #字數為其他數字
        else:
            num = len(name_tumple[i])/2 
            if num!=int:#字數為奇數
                center_word_list.append(name_tumple[i][int(num)])
            else:#字數為偶數
                center_word_list.append(name_tumple[i][int(num)+1])
        

   #檢視名子有沒有重複，計算中間名的次數
    for i in range(len(center_word_list)):
        count = center_word_list.count(center_word_list[i])
        center_word_count.append(count)
        
    #只有出現一次的中間名
    if 1 in center_word_count:    
        uniqul_name = data[center_word_count.index(1)]
        
    else:
        uniqul_name="沒有"
    

    return uniqul_name
    
    
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆 
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安


# In[4] task4
"""
0, 4, 8, 7, 11, 15, 14, 18, 22, 21, 25, …
數列邏輯是+4 +4 -1，所以這邊用/3來計算，
"""

def get_number(index): 
    # your code here
    
    if index==1:
        number=4
        
    elif index==2:
        number=8
    
    else:
        #for i in range(index):
        a1 = int(index/3) #除3之後的商數
        a2 = index%3
        number = (8*a1)-a1+(4*a2)

    
    return number
    
get_number(1) # print 4 
get_number(5) # print 15 
get_number(10) # print 25 
get_number(30) # print 70

# In[5] task5

def find(spaces, stat, n): # your code here
    """
    spaces: 剩下的位置(list)
    stat: 可不可以進入該車廂(list)
    n: 有幾個客人(int)
    """   
    carriage = ""
    pool = []#候選池(index)
    
    for i in range(len(stat)):
        
        if stat[i]==1:#該車廂可以進入
            #看該車廂剩下的座位夠不夠坐
            if spaces[i]>=n:
                pool.append(i)
            else:
                pass
        else:
            pass
    
    
    if pool != []:
        compare = [] #用來比較選出最小值(剩餘車位數)
        for i2 in range(len(pool)):
            compare.append(spaces[pool[i2]])
        
        carriage = pool[compare.index(min(compare))]
        
    #如果車廂都沒有座位
    else:
        carriage = -1
    

    return carriage



find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5 
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1 
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2





