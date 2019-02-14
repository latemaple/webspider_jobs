import urllib.request
from bs4 import BeautifulSoup
import re
import time
import random
import xlwt  # 用来创建excel文档并写入数据
m=0 # 序号
def getHtml(url):
    head = {}
    # 写入User Agent信息
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # 创建Request对象
    req = urllib.request.Request(url, headers=head)
    # 传入创建好的Request对象
    page = urllib.request.urlopen(req)
  #  page=urllib.request.urlopen(url,headers=head)
    html=page.read()
    html=html.decode('utf-8')
    return html
def choice(html):
    soup=BeautifulSoup(html,"lxml")
    divs=soup.find_all('div',class_='jobList')
   # print(divs)
    area=soup.find('span',class_='loc f16')#工作所在地
    area=area.em.text
    #print(area)
    global m  # global声明，意思是说global语句可以声明一个或多个变量为全局变量。该声明仅在当前代码块中有效。除此之外，没办法访问全局变量。
    for div in divs:
        time.sleep(random.randint(0,1))## 暂停0~3秒的整数秒，时间区间：[1,3]
        m = m + 1

        names = div.span.a.get_text()  # 工位岗位
        salary_time = div.find_all("span", {"class": "e2"})  # 工资和更新时间

        salary = salary_time[1].text
        update =salary_time[0].text
        company = div.find("span", {"class": "e3 cutWord"})  # 公司名称
        company = company.a.text
        scales = div.find_all('em')  # 公司规模
        scales2=scales[2].text
        scales1=scales[1].text
        classes = div.em.get_text() #工作类别

        link = div.a.get('href')  # 找到链接,进入下一个页面
        a = getHtml(link)
        a_soup = BeautifulSoup(a, "lxml")
        a_div = a_soup.find_all("div", {"class": "job_require"})
        a_all = a_div[0].find_all('span')
        a_all_number=len(a_all)
        if a_all_number>=4:
            education = a_all[3].text
        else:
            education="不限"
        if a_all_number>=5:
            year = a_all[4].text
        else:
            year = "经验应届生"
      #  results={names,salary,update,company,scales2,scales1,area,classes,education,year}
       # print(results)
        results=[names,update,salary,company,scales2,scales1,area,classes,education,year]

        for i in range(0,10):
            print(results[i])
            ws.write(m,i,results[i])
            wb.save(newTable)
        print("保存成功",m)
        print("-------------")
     #   ws.write(m,0,names)
     #   wb.save(newTable)
newTable="beijing_job.xls"#表格名称
wb = xlwt.Workbook(encoding='utf-8')#创建excel文件，声明编码
ws = wb.add_sheet('sheet1')#创建表格
headData = ['工作岗位','更新时间','工资','公司名称','公司规模','公司性质','所在地','工作类别','学历要求','经验要求']#表头部信息
for colnum in range(0, 10):
    ws.write(0, colnum, headData[colnum], xlwt.easyxf('font: bold on'))  # 行，列 #把表头写在第0行，各列，并把字体设置为加粗


def main(jobs):
    html = getHtml("http://www.chinahr.com/beijing/jobs/57552/"+str(jobs))#北京

    choice(html)
for i in range(1,91):
    main(i)
