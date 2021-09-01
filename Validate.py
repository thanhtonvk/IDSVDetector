from Student import Student
def Refactor(s):
    s = s.lower()
    s = s.replace('mã sv', '').replace('khóa học', '').replace('lớp', '').replace('ngành học', '').replace('ngày sinh', '').replace('họ và tên', '').replace(':', '')
    return s.strip()
def Definition(sv,list):
    for s in list:
        s = s.lower()
        if s.find('mã sv') != -1 and Refactor(s) != '':
            sv.id = Refactor(s).title()
        if s.find('khóa học') != -1 and Refactor(s) != '':
            sv.khoahoc = Refactor(s).title()
        if s.find('lớp') != -1 and Refactor(s) != '':
            sv.lop = Refactor(s).upper()
        if s.find('ngành học') != -1 and Refactor(s) != '':
            sv.nganhhoc = Refactor(s).title()
        if s.find('ngày sinh') != -1 and Refactor(s) != '':
            sv.ngaysinh = Refactor(s).title()
        if s.find('họ và tên') != -1 and Refactor(s) != '':
            sv.hovaten = Refactor(s).title()
def StudentInfo(list):
    sv  = Student()
    Definition(sv,list)
    return sv
