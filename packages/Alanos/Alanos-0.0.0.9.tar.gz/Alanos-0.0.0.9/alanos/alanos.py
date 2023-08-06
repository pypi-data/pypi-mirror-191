import time,os,random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep     
class tool:
    __my_headers__ = [
        # 各种PC端
        # Opera
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Opera/8.0 (Windows NT 5.1; U; en)",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
        # Firefox
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        # Safari
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
        # chrome
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        # 360
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        # 淘宝浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        # 猎豹浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        # QQ浏览器
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        # sogou浏览器
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        # maxthon浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        # UC浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
        # 各种移动端
        # IPhone
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        # IPod
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        # IPAD
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        # Android
        "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        # QQ浏览器 Android版本
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        # Android Opera Mobile
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        # Android Pad Moto Xoom
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        # BlackBerry
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        # WebOS HP Touchpad
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        # Nokia N97
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        # Windows Phone Mango
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        # UC浏览器
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        # UCOpenwave
        "Openwave/ UCWEB7.0.2.37/28/999",
        # UC Opera
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            # 一部分 PC端的
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    ]
    def get_headers():
        return random.choice(self.__my_headers__)
    def get_now_date(self):
        '''
        ===========================
            返回当前日期
        ===========================
        '''
        YY = time.strftime("%Y",time.localtime())
        MM = time.strftime("%m",time.localtime())
        DD = time.strftime("%d",time.localtime())
        return YY+MM+DD

class Stu_Manage:
    __file_name__ = 'student.txt'
    def usr(self):
        while True:
            self.menu()
            choose = int(input('请选择：'))
            if choose in range(8):
                if choose == 0:
                    answer = input('您确定要退出系统吗？(Y/N):')
                    if answer == 'y' or answer == 'Y':
                        print('谢谢您的使用！')
                        break
                    else:
                        continue
                elif choose == 1:
                    self.insert()
                elif choose == 2:
                    self.search()
                elif choose == 3:
                    self.delete()
                elif choose == 4:
                    self.modify()
                elif choose == 5:
                    self.sort()
                elif choose == 6:
                    self.total()
                elif choose == 7:
                    self.show()
    def menu(self):
        print('='*20,'学生信息管理系','='*20)
        print('-'*20,'功能菜单','-'*20)
        print('\t\t1.录入学生成绩')
        print('\t\t2.查找学生成绩')
        print('\t\t3.删除学生成绩')
        print('\t\t4.修改学生成绩')
        print('\t\t5.排序')
        print('\t\t6.统计学生总人数')
        print('\t\t7.显示所有学生信息')
        print('\t\t0.退出')
    def show_student(self,lst):
        if len(lst) == 0:
            print('没有查询到学生，无数据显示！')
            return
        format_title = '{:^6}\t{:^12}\t{:^8}\t{:^10}\t{:^10}\t{:^8}'
        print(format_title.format('ID','姓名','英语成绩','Python成绩','Java成绩','总成绩'))
        format_data = '{:^6}\t{:^12}\t{:^8}\t{:^8}\t{:^8}\t{:^8}'
        for item in lst:
            print(format_data.format(item.get('id'),
                                    item.get('name'),
                                    item.get('english'),
                                    item.get('python'),
                                    item.get('java'),
                                    int(item.get('english'))+int(item.get('python'))+int(item.get('java'))
            ))
    def insert(self):
        student_list = []
        while True:
            id = input('请输入ID:')
            if not id:
                break
            name = input('请输入姓名')
            if not name:
                break
            try:
                english = int(input('请输入英语成绩：'))
                python = int(input('请输入python成绩：'))
                java = int(input('请输入java成绩：'))
            except:
                print('输入成绩无效，不是整数类型，请重新输入')
            student = {'id':id,'name':name,'english':english,'python':python,'java':java}
            student_list.append(student)
            anawer = input('是否继续添加信息（Y/N）：')
            if anawer == 'y' or anawer == 'Y':
                continue
            else:
                break
        self.save(student_list)
        print('学生信息录入完毕!!!')
    def save(self,lst):
        try:
            stu_txt = open(self.__file_name__,'a',encoding='utf-8')
        except:
            stu_txt = open(self.__file_name__,'w',encoding='utf-8')
        for item in lst:
            stu_txt.write(str(item)+'\n')
        stu_txt.close()
    def search(self):
        pass
    def delete(self):
        while True:
            student_id = input('请输入要删除的学生都ID:')
            if student_id != '':
                if os.path.exists(self.__file_name__):
                    with open(self.__file_name__,'r',encoding='utf-8') as file:
                        student_old = file.readlines()
                else:
                    student_old = []
                flag = False
                if student_old:
                    with open(self.__file_name__,'w',encoding='utf-8') as wfile:
                        d={}
                        for item in student_old:
                            d = dict(eval(item))
                            if d['id'] != student_id:
                                wfile.write(str(d)+'\n')
                            else:
                                flag = True
                        if flag:
                            print(f'id为{student_id}的学生信息已被删除')
                        else:
                            print(f'没有找到{student_id}的学生信息')
                else:
                    print('无学生信息')
                    break
                self.show()
                answer = input('是否继续修改其他学生信息?（Y/N):')
                if answer == 'y' or answer == 'Y':
                    continue
                else:
                    break        
    def modify(self):
        self.show()
        if os.path.exists(self.__file_name__):
            with open(self.__file_name__,'r',encoding='utf-8') as rfile:
                student_old = rfile.readlines()
        else:
            return
        student_id = input('请输入要修改的学员ID:')
        with open(self.__file_name__,'w',encoding='utf-8') as wfile:
            for item in student_old:
                d = dict(eval(item))
                if d['id'] == student_id:
                    print('找到学生信息，可以修改他的相关信息了！')
                    while True:
                        try:
                            d['name'] = input('请输入姓名')
                            d['english'] = input('请输入英语成绩')
                            d['python'] = input('请输入python成绩')
                            d['java'] = input('请输入java成绩')
                        except:
                            print('您的输入有误，请重新输入！！！')
                        else:
                            break
                    wfile.write(str(d)+'\n')
                    print('修改成功')
                else:
                    wfile.write(str(d)+'\n')
            answer = input('是否继续修改其他学生信息?（Y/N):')
            if answer == 'y' or answer == 'Y':
                self.modify()

    def sort(self):
        show()
        if os.path.exists(self.__file_name__):
            with open(self.__file_name__,'r',encoding='utf-8') as rfile:
                student_list = rfile.readlines()
            student_new = []
            for item in student_list:
                d = dict(eval(item))
                student_new.append(d)
        else:
            return
        asc_or_desc = input('请选择(0.升,1.降)')
        if asc_or_desc == '0':
            asc_or_desc = False
        elif asc_or_desc == '1':
            asc_or_desc =True
        else:
            print('您到输入有误，请重新输入')
            sort()
        mode = input('请选择排序方式（1.按英语成绩排序，2.按python成绩排序，3.按java成绩排序,0.按总成绩排序）')
        if mode == '1':
            student_new.sort(key = lambda x :int(x['english']),reverse = asc_or_desc )
        elif mode == '2':
            student_new.sort(key = lambda x :int(x['python']),reverse = asc_or_desc )
        elif mode == '3':
            student_new.sort(key = lambda x :int(x['java']),reverse = asc_or_desc )
        elif mode == '0':
            student_new.sort(key = lambda x :int(x['english'])+int(x['python'])+int(x['java']),reverse = asc_or_desc )
        else:
            print('您到输入有误，请重新输入')
            sort()      
        self.show_student(student_new)
    def total(self):
        if os.path.exists(self.__file_name__):
            with open(self.__file_name__,'r',encoding='utf-8') as rfile:
                students = rfile.readlines()
                if students:
                    print(f'一共有{len(students)}名学生')
                else:
                    print('还没有录入学生信息')
    def show(self):
        student_lst = []
        if os.path.exists(self.__file_name__):
            with open(self.__file_name__,'r',encoding='utf-8') as rfile:
                students = rfile.readlines()
                for item in students:
                    student_lst.append(eval(item))
                if student_lst:
                    self.show_student(student_lst)

class WisdomTree:
    __start__ = 0       
    __startclass__ = 0
    __classList_len__ = 0
    __url__ = 'https://passport.zhihuishu.com/login'
    def __init__(self):#,tel,passwd):
        '''初始化'''
        # self.tel = tel
        # self.passwd = passwd
        # 不自动关闭浏览器
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        option.add_argument("--mute-audio")
        # 注意此处添加了chrome_options参数
        self.driver = webdriver.Chrome(chrome_options=option)
        self.driver.implicitly_wait(10)
        
    def tree_login(self):
        '''登陆'''
        self.driver.get(self.__url__)
        sleep(10)
        while True:
            try:
                self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/ul/li[4]/a").click()
            except:
                pass
            else:
                break
        # self.driver.get("http://www.zhihuishu.com/")                                   #打开知到智慧树官网
        # self.driver.find_element(By.ID,"notLogin").click()                             #定位到【登录】
        # while True:                                                         #等待用户登录、进入课程
        #     try:
        #         self.driver.find_element(By.CLASS_NAME,"hint_delete").click()
        #     except:
        #         print("未找到课程")
        #     else:
        #         break
        # sleep(3)

    def get_class(self):
        '''获取课程'''               
        classList = self.driver.find_elements(By.CLASS_NAME,"courseName")   # 存放全部课程，列表
        self.__classList_len__ = len(classList)                                    # 课程总数
        try:
            classList[self.__start__].click()    # 进入未完成的第一个课程
        except:
            return
        
            # classList_len-=1
        #打开对应对应课程
        # classList = self.driver.find_elements(By.XPATH,"//ul[@class='datalist']")
        # for i in classList:
        #     i.click()
            # title = i.find_element(By.XPATH,"./div/dl/dt/div[1]")
            # if title.text == self.classTitle:
            #     i.click()
            #     time.sleep(3)
            #     break
    def close_w(self):
        '''关闭弹窗'''
        try:
            #关闭学前必读
            allClose = self.driver.find_elements(By.XPATH,"//div[@class='el-dialog__header']")
            for i in allClose:
                title = i.find_element(By.XPATH,"./span").text
                if title=="智慧树警告":
                    i.find_element(By.XPATH,"./button").click()
                    sleep(1)
                    break
            self.driver.find_element(By.XPATH,"//div[@class='dialog-read']/div/i").click()
        except:
            try:
                allClose = self.driver.find_elements(By.XPATH,"//div[@class='el-dialog__header']")
                for i in allClose:
                    title = i.find_element(By.XPATH,"./span").text
                    if title=="课程提醒":
                        i.find_element(By.XPATH,"./button").click()
                        sleep(1)
                        break
                self.driver.find_element(By.XPATH,"//*[@id=\"app\"]/div/div[4]/div/div[2]/div/div[2]/div[2]/div/span[1]").click()
            except:
                return
    def CloseTitle(self):
        '''关闭弹出题目'''
        # try:
        #     #选个A并关闭
        #     self.driver.find_element(By.CLASS_NAME,'topic-item').click()
        #     time.sleep(1)
        #     self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div[7]/div/div[1]/button").click()
        #     time.sleep(1)
        #     #继续播放
        #     ac = ActionChains(self.driver)
        #     e = self.driver.find_element(By.CLASS_NAME,'videoArea')
        #     ac.move_to_element_with_offset(e, 100, 100)
        #     ac.click()
        #     ac.perform()
        # except:
        #     return
        try:
            self.driver.find_elements(By.CLASS_NAME,"topic-item")[0].click()       #小弹窗选项，默认选第一个（A）
        except:
            return
        else:
            print("检测到小测验弹窗")
            btn1 = self.driver.find_element(By.CLASS_NAME,"el-dialog__wrapper.dialog-test")
            btn2 = btn1.find_element(By.CLASS_NAME,"el-dialog")
            btn3 = btn2.find_element(By.CLASS_NAME,"el-dialog__headerbtn").click()
            sleep(3)
            videoArea = self.driver.find_element(By.CLASS_NAME,"videoArea")        #视频播放区域
            ActionChains(self.driver).move_to_element(videoArea).perform()         #鼠标悬停
            self.driver.find_element(By.ID,"playButton").click()                   #重新播放视频
    def ViewIsEnd(self):
        '''判断视频是否播放完毕'''
        try:
            # 读取当前进度
            video = self.driver.find_element(By.ID,"vjs_container")
            if "vjs-ended" in video.get_attribute("class"):
                print("播放完毕,切换下一个")
                return True
            return False
        except:
            return False
    def vdeio_play(self):
        '''播放视频'''
        playlist = self.driver.find_elements(By.CLASS_NAME,'lessonName')
        for count, video in enumerate(playlist):
            if (count < self.__startclass__):
                continue
            try:
                video.click()
            except:
                continue
            sleep(3)  # 等待加载出来//*[@id="vjs_container"]/div[10]
            videoArea = self.driver.find_element(By.CLASS_NAME,"videoArea")                #视频播放区域
            ActionChains(self.driver).move_to_element(videoArea).perform()                 #鼠标悬停
            speedBox = self.driver.find_element(By.CLASS_NAME,"speedBox")                  #视频倍速按钮
            ActionChains(self.driver).move_to_element(speedBox).perform()                  #鼠标悬停
            self.driver.find_element(By.CLASS_NAME,"speedTab.speedTab15").click()          #视频1.5倍速
            definiBox = self.driver.find_element(By.CLASS_NAME,"definiBox")                #视频清晰度按钮
            videoArea = self.driver.find_element(By.CLASS_NAME,"videoArea")                #视频播放区域
            ActionChains(self.driver).move_to_element(definiBox).perform()                 #鼠标悬停
            self.driver.find_element(By.CLASS_NAME,"line1gq.switchLine").click()           #视频【流畅】清晰度
            # videoArea = self.driver.find_element(By.CLASS_NAME,"videoArea")                #视频播放区域
            # self.driver.find_element(By.ID,"playButton").click()                           #视频播放按钮
            sleep(5)
            print(f'当前视频: {count + 1:3d} / {len(playlist)}')
            while True:
                # self.CloseTitle()
                if (self.ViewIsEnd()):
                    print("播放完毕,开始播放下一个")
                    break
        self.driver.find_element(By.XPATH,"//*[@id=\"app\"]/div/div[1]/header/div/div[1]").click()
        self.__start__+=1
        if self.__start__ == self.__classList_len__:
            return True
        else:
            return False
    def usr(self):
        tree = WisdomTree()#username, passwd)
        while True:
            tree.tree_login()
            tree.get_class()
            tree.close_w()
            bun = tree.vdeio_play()
            if bun:
                break
        print("全部课程已完成")