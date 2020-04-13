import requests
from bs4 import BeautifulSoup
import xlsxwriter
import time
import threading

num_chexing=[]


#第一级得到所需车辆名称信息及网址
def getHtml(first_url,down_cheming):
    url='https://www.autohome.com.cn/nanjing/'
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
               'Referer': 'https://www.autohome.com.cn/nanjing/',
             'get':'https://www.autohome.com.cn/aspx/GetDealerInfoByCityIdNew.aspx?cityid=320100 ',
               }
    request_html=requests.get(url=url,headers=headers)
    html=request_html.text
    #print(html)
    soup=BeautifulSoup(html,'lxml')
    mingzi=soup.find_all('p')
    #print(mingzi)
    #得到车辆具体url和名字
    for index in range(0,30):
        index2=index*2
        first_url.append(mingzi[index2].find('a').get('href'))
        down_cheming.append(mingzi[index2].text)#得到车名
    print(first_url)

#第二级得到单个车辆的具体信息和价格

def getOnecar(first_url,down_chexing,down_guideprice,down_pingce,k):
    #flag=1
   # for i1 in range(0,3):
    url2='https://www.autohome.com.cn'+first_url[k]
    headers2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'Referer': 'https://www.autohome.com.cn/4851/',
            'get': 'https://www.autohome.com.cn/4851/ ',
            }
    request_html2=requests.get(url=url2,headers=headers2)
    html2=request_html2.text
    soup=BeautifulSoup(html2,'lxml')

    #################提取车型ok
    neirong=soup.find_all('div',class_='name-param')
    #print(neirong)
    for index in range(0,len(neirong)):
        down_chexing.append(neirong[index].text)#得到车型
    num_chexing.append(len(neirong))#得到每个车名对应车型的数量
    #print(num_chexing)
    #print(down_cheming)

    ##############提取参考价ok
    guideprice=soup.find_all('p',class_='guidance-price')
    down_guideprice.append('   ')
    for i in range(0,len(guideprice)):
        down_guideprice.append(guideprice[i].text)
    #print(down_guideprice)


    #############提取评测ok
    pingce=soup.find_all('p',class_='editor-con')
    #print(pingce)
    if len(pingce)==0:
        for i in range(0,len(neirong)+2):
            down_pingce.append('  ')
    else:
        for i in range(0,3):
            down_pingce.append(pingce[i].text)
        for i in range(4,len(neirong)+2):
            down_pingce.append(" ")
    #s='第'++'辆完成'
    print(first_url[k])
    time.sleep(0.5)
    #print(down_pingce)


#第三级将车辆信息整合到excel

def Write(down_cheming,down_guideprice,down_pingce,down_chexing):
    flag=1
    flag2=1
    k=0
    for i in range(0,len(down_chexing)):
        down_cheming.insert(flag,down_chexing[i])
        flag=flag+1
        if(k<len(num_chexing)):
            if(flag2==num_chexing[k]):
                flag=flag+1
                k=k+1
                flag2=1
            else:
                flag2=flag2+1


    workbook = xlsxwriter.Workbook('d:\jieguo.xlsx')  # 创建一个Excel文件
    worksheet = workbook.add_worksheet()  # 创建一个sheet
    title = [U'车名', U'参考价格',U'评价']  # 表格title
    worksheet.write_row('A1', title)  # title 写入Excel
    worksheet.write_column('A2',down_cheming)
    worksheet.write_column('B2', down_guideprice)
    worksheet.write_column('C2',down_pingce)
    workbook.close()



def main():
    first_url=[]
    down_cheming=[]
    down_chexing=[]
    getHtml(first_url,down_cheming)
    down_guideprice=[]
    down_pingce=[]

    #多线程
    threadl = []  # 线程列表，用例存放线程
    # 产生线程的实例
    lenght=int(len(first_url))
    for k in range(0,lenght,2):
        t1 = threading.Thread(target=getOnecar, args=(first_url,down_chexing,down_guideprice,down_pingce,k))  # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式；
        t2 = threading.Thread(target=getOnecar, args=(first_url,down_chexing,down_guideprice,down_pingce,k+1))
        threadl.append(t1)
        threadl.append(t2)
    # 循环列表，依次执行各个子线程
    for x in threadl:
        x.start()
    # 将最后一个子线程阻塞主线程，只有当该子线程完成后主线程才能往下执行
        x.join()
    Write(down_cheming, down_guideprice, down_pingce,down_chexing)


if __name__=='__main__':
    main()
