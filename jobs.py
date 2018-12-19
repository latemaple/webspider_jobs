import urllib.request
from bs4 import BeautifulSoup
import re
import time
import random
import xlwt  # ��������excel�ĵ���д������
m=0 # ���
def getHtml(url):
    head = {}
    # д��User Agent��Ϣ
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # ����Request����
    req = urllib.request.Request(url, headers=head)
    # ���봴���õ�Request����
    page = urllib.request.urlopen(req)
  #  page=urllib.request.urlopen(url,headers=head)
    html=page.read()
    html=html.decode('utf-8')
    return html
def choice(html):
    soup=BeautifulSoup(html,"lxml")
    divs=soup.find_all('div',class_='jobList')
   # print(divs)
    area=soup.find('span',class_='loc f16')#�������ڵ�
    area=area.em.text
    #print(area)
    global m  # global��������˼��˵global����������һ����������Ϊȫ�ֱ��������������ڵ�ǰ���������Ч������֮�⣬û�취����ȫ�ֱ�����
    for div in divs:
        time.sleep(random.randint(0,1))## ��ͣ0~3��������룬ʱ�����䣺[1,3]
        m = m + 1

        names = div.span.a.get_text()  # ��λ��λ
        salary_time = div.find_all("span", {"class": "e2"})  # ���ʺ͸���ʱ��

        salary = salary_time[1].text
        update =salary_time[0].text
        company = div.find("span", {"class": "e3 cutWord"})  # ��˾����
        company = company.a.text
        scales = div.find_all('em')  # ��˾��ģ
        scales2=scales[2].text
        scales1=scales[1].text
        classes = div.em.get_text() #�������

        link = div.a.get('href')  # �ҵ�����,������һ��ҳ��
        a = getHtml(link)
        a_soup = BeautifulSoup(a, "lxml")
        a_div = a_soup.find_all("div", {"class": "job_require"})
        a_all = a_div[0].find_all('span')
        a_all_number=len(a_all)
        if a_all_number>=4:
            education = a_all[3].text
        else:
            education="����"
        if a_all_number>=5:
            year = a_all[4].text
        else:
            year = "����Ӧ����"
      #  results={names,salary,update,company,scales2,scales1,area,classes,education,year}
       # print(results)
        results=[names,update,salary,company,scales2,scales1,area,classes,education,year]

        for i in range(0,10):
            print(results[i])
            ws.write(m,i,results[i])
            wb.save(newTable)
        print("����ɹ�",m)
        print("-------------")
     #   ws.write(m,0,names)
     #   wb.save(newTable)
newTable="city3_day30.xls"#�������
wb = xlwt.Workbook(encoding='utf-8')#����excel�ļ�����������
ws = wb.add_sheet('sheet1')#�������
headData = ['������λ','����ʱ��','����','��˾����','��˾��ģ','��˾����','���ڵ�','�������','ѧ��Ҫ��','����Ҫ��']#��ͷ����Ϣ
for colnum in range(0, 10):
    ws.write(0, colnum, headData[colnum], xlwt.easyxf('font: bold on'))  # �У��� #�ѱ�ͷд�ڵ�0�У����У�������������Ϊ�Ӵ�


def main(jobs):
	html = getHtml("http://www.chinahr.com/beijing/jobs/57552/"+str(jobs))#����

    choice(html)
for i in range(1,91):
    main(i)
