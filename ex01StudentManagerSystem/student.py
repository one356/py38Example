
# 学员角色类创建
class Student(object):
    def __init__(self, name, gender, tel):
        # 定义姓名，性别，手机号
        self.name = name
        self.gender = gender
        self.tel = tel

    def __str__(self):
        # 定义魔法方法，返回类信息
        return f'{self.name},{self.gender},{self.tel}'
        # return format(self.name,self.gender,self.tel)



