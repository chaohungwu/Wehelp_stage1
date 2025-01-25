# -*- coding: utf-8 -*-

# In[] Task1

"""
邏輯：
樂透版的文章標題、推/噓、日期
文章標題：str
文章標題：int
文章標題：Fri Jul 14 23:34:43 2023
逐步地去尋找相同的內容
"""

#抓取網頁html
import urllib.request as req
import json

def getdata(url):    
    #這邊要輸入一些你的請求辨識資訊
    #建立一個request物件，附加Request hraders 的資訊
    request = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        })
    
    
    #這邊用request物件來打開網址
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
        json_data =json.loads(data)
    return json_data


#站點的json資料
spot_json_data = getdata("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1")

print(spot_json_data["data"]["results"][0]["info"])

#捷運站點的json資料
mrt_json_data = getdata("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2")
print(mrt_json_data["data"][0]["MRT"])


spot_name_list = []
spot_info_list = []
spot_lon_list=[]
spot_lat_list=[]
spot_image_list=[]
spot_xbody_list=[]
spot_serial_list=[]

spot_area_list=[]
the_closest_mrt_list=[]

mrt_name_list = []
mrt_area_list = []
mrt_serial_list = []


#逐個摘出景點的資料，然後對應捷運站的行政區
for i in range(len(spot_json_data["data"]["results"])):
    #print(spot_json_data["data"]["results"][i]["info"])
    spot_name_list.append(spot_json_data["data"]["results"][i]["stitle"])
    spot_info_list.append(spot_json_data["data"]["results"][i]["info"])
    spot_lon_list.append(spot_json_data["data"]["results"][i]["longitude"])
    spot_lat_list.append(spot_json_data["data"]["results"][i]["latitude"])
    spot_image_list.append(spot_json_data["data"]["results"][i]["filelist"])
    spot_xbody_list.append(spot_json_data["data"]["results"][i]["xbody"])
    spot_serial_list.append(spot_json_data["data"]["results"][i]["SERIAL_NO"])

# 逐個摘出捷運站的資料
for i in range(len(mrt_json_data["data"])):
    #print(spot_json_data["data"]["results"][i]["info"])
    mrt_name_list.append(mrt_json_data["data"][i]["MRT"])
    mrt_area_list.append(mrt_json_data["data"][i]["address"])
    mrt_serial_list.append(mrt_json_data["data"][i]["SERIAL_NO"])


#重新開始用serial number針對剩下的沒對應的做辨識
for i in range(len(spot_serial_list)):
    for i2 in range(len(mrt_serial_list)):
        if spot_serial_list[i] == mrt_serial_list[i2]:
            spot_area_list.append(mrt_area_list[i2][5:8])
            the_closest_mrt_list.append(mrt_name_list[i2])
        else:
            pass
        
#只取第一個圖片
for i in range(len(spot_image_list)):
    #print(spot_image_list[i])
    index = spot_image_list[i].find(".jpg")
    if index != -1:
        spot_image_list[i] = spot_image_list[i][:index+4]
    
    else:
        index = spot_image_list[i].find(".JPG")
        spot_image_list[i] = spot_image_list[i][:index+4]


#捷運統計
#the_closest_mrt_list=[]

#the_closest_mrt_list
mrt_spot_list=[]
for i in range(len(mrt_name_list)):
    pre_mrt_spot_list = []
    for i2 in range(len(spot_name_list)):
        if the_closest_mrt_list[i2] == mrt_name_list[i]:
            pre_mrt_spot_list.append(spot_name_list[i2])
    
    mrt_spot_list.append(pre_mrt_spot_list)
    



def save_lists_to_csv(list1, list2, list3, list4, list5, filename):
    """
    list 的資料存成 CSV 文件
    """

    with open(filename, 'w') as csvfile:
        for row in zip(list1, list2, list3, list4, list5): #將4個csv合併成一個tuple，並對應4個list中每個index的值
            line = ','.join(map(str, row)) + '\n'
            csvfile.write(line)
            



save_lists_to_csv(spot_name_list,
                  spot_area_list,
                  spot_lon_list,
                  spot_lat_list,
                  spot_image_list,
                  r"G:\05_wehelp\03_week_work\01_stage1\week3\spot.csv")        
        

mrt_spot_list_str=[]
for i in range(len(mrt_spot_list)):
    list_to_text=""
    for i2 in range(len(mrt_spot_list[i])):
        if i2==0:
            list_to_text= "{}{}".format(list_to_text,mrt_spot_list[i][i2])
        else:
            list_to_text= "{},{}".format(list_to_text,mrt_spot_list[i][i2])
        
    mrt_spot_list_str.append(list_to_text)



def save_lists_to_csv2(list1, list2, filename):
    """
    list 的資料存成 CSV 文件
    """
    
    
    with open(filename, 'w') as csvfile:
        for row in zip(list1, list2): #將4個csv合併成一個tuple，並對應4個list中每個index的值
            line = ','.join(map(str, row)) + '\n'
            csvfile.write(line)

save_lists_to_csv2(mrt_name_list,
                   mrt_spot_list_str,

                  r"G:\05_wehelp\03_week_work\01_stage1\week3\mrt.csv")         
        
        
        
        
        
