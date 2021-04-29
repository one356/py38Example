# 导入模块
from student import *
# 定义管理学员信息类

class StudentManager(object):
    def __init__(self):
        # 存储数据所用的列表
        self.student_list = []
    # 程序入口函数，启动程序后执行的函数：
    def run(self):
        self.load_student()
        while True:
            # 显示功能菜单
            self.show_menu()
            # 用户输入功能序号
            menu_num = int(input('请输入需要的功能序号：'))
            # 根据用户输入的序号执行功能
            if menu_num == 1:
                # 添加学员
                self.add_student()                
            elif menu_num == 2:
                # 删除学员
                self.del_student()
            elif menu_num == 3:
                # 修改学员
                self.modify_student()
            elif menu_num == 4:
                # 查询学员信息
                self.search_student()
            elif menu_num == 5:
                # 显示所有学员信息
                self.show_student()
            elif menu_num == 6:
                # 保存学员信息
                self.save_student()
            elif menu_num == 7:
                # 退出
                break
    # 程序功能函数
    # 显示菜单
    @staticmethod
    def show_menu():
        print('请选择功能')
        print('1:添加学员')
        print('2:删除学员')
        print('3:修改学员')
        print('4:查询学员信息')
        print('5:显示所有学员信息')
        print('6:保存学员信息')
        print('7:退出')
    # 添加学员
    def add_student(self):
        # 用户输入学员信息
        name = input('输入学员姓名：')
        gender = input('输入学员性别：')
        tel = input('输入学员电话：')
        # 创建学员对象
        student = Student(name,gender,tel)
        # 将学员添加到学员列表
        self.student_list.append(student)
        # 打印验证信息
        print(self.student_list)   
        print(student) 
                
    # 删除学员
    def del_student(self):
        del_name = input('输入想要删除的学员姓名：')
        for i in self.student_list:
            if i.name == del_name:
                self.student_list.remove(i)
                print('{}已经删除'.format(del_name))
                break
        else:
            print('没有找到{}'.format(del_name))
        print(self.student_list)  

                

    # 修改学员
    def modify_student(self):
        modify_name = input('输入想要修改的学员姓名：')
        for i in self.student_list:
            if i.name == modify_name:
                print('输入{}新信息'.format(modify_name))
                i.name = input('新姓名：')
                i.gender = input('新性别：')
                i.tel = input('新电话：') 
                print('{}已经修改信息为{}'.format(modify_name,i.name))
                break
        else:
            print('没有找到{}'.format(modify_name))
        print(self.student_list)         

    # 查询学员信息
    def search_student(self):
        search_name = input('输入想要修改的学员姓名：')
        for i in self.student_list:
            if i.name == search_name:
                print('姓名：{}性别：{}电话：{}'.format(i.name,i.gender,i.tel))
                break
        else:
            print('没有找到{}'.format(search_name))  

    # 显示所有学员信息
    def show_student(self):
        print('姓名\t性别\t电话')
        for i in self.student_list:
            print('{}\t{}\t{}'.format(i.name,i.gender,i.tel))

    # 保存学员信息
    def save_student(self):
        
    #加载学员信息
    def load_student(self):
        print('')