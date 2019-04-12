import csv
import re
from urllib.parse import urlparse, urlunsplit

from django.http import HttpResponse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from LottoWebCore.models import Department, Teacher, University, Lecture

DepObj = Department.objects

browser = univ_obj = None
xpath_department = '//*[@id="form:departamento"]'
xpath_department_option = '//*[@id="form:departamento"]/option[@value="{}"]'
xpath_teachers_number = '//*[@id="corpo"]/table/caption'
xpath_teachers_name = '//*[@id="corpo"]/table/tbody/tr[{}]/td[2]/span[1]'
xpath_teachers_link = '//*[@id="corpo"]/table/tbody/tr[{}]/td[2]/span[3]/a'
xpath_lattes_link = '//*[@id="endereco-lattes"]'
xpath_address = '//*[@id="contato"]/dl[1]/dd'
xpath_room = '//*[@id="contato"]/dl[2]/dd'
xpath_phone = '//*[@id="contato"]/dl[3]/dd'
xpath_email = '//*[@id="contato"]/dl[4]/dd'
xpath_interest = '//*[@id="perfil-docente"]/dl[3]/dd'
xpath_description = '//*[@id="perfil-docente"]/dl[1]/dd'
xpath_lectures = '//*[@id="turmas-graduacao"]/table'
link_teachers = '/sigaa/public/docente/portal.jsf?siape={}'
# link_teachers = 'https://www.sigaa.ufs.br/sigaa/public/docente/portal.jsf?siape={}'
link_lectures = '/sigaa/public/docente/disciplinas.jsf?siape={}'
# link_lectures = 'https://www.sigaa.ufs.br/sigaa/public/docente/disciplinas.jsf?siape={}'
xpath_button_search = '//*[@id="form:buscar"]'


def clean_data(data):
    items = ['\n', '\t', '<br>', ' <i> não informado </i> ', ' <i> não informados </i> ', '<i> não informada </i> ',
             ' <i> não informadas </i> ', ' <i> não informado </i><br> ', ' &amp;', '                ', '       ']
    for i in items:
        data = data.replace(i, ' ')
    return data


def get_departments(url):
    department_dict = {}
    #
    browser = webdriver.PhantomJS(executable_path='E:\\Projetos\\GitHub\WrkAgg\\venv\Scripts\\phantomjs.exe')
    browser.maximize_window()
    #
    browser.get(url)
    try:
        select_box = browser.find_element_by_xpath(xpath_department)
        options = [x for x in select_box.find_elements_by_tag_name("option")]  # this part is cool, because it searches
        # the elements contained inside of select_box and then adds them to the list options if they have the tag name
        # "options"
        for element in options:
            try:
                temp_code = element.get_attribute("value")
                if temp_code in [0, "0"]:
                    continue
                elif " - " in element.get_attribute("text"):
                    temp_element = element.get_attribute("text").split(' - ')
                else:
                    temp_element = (element.get_attribute("text"), element.get_attribute("text"))
                #
                department_dict[temp_code] = {'name': temp_element[0], 'city': temp_element[1]}
                # print(temp_code, temp_element[0], temp_element[1])  # or append to list or whatever you want here
            except IndexError:
                print('IndexError on: {} : {}'.format(element.get_attribute("value"), element.get_attribute("text")))
    except NoSuchElementException as E:
        print('NoSuchElementException: {}'.format(E))
    #
    browser.close()
    #
    return department_dict


def get_teachers(pk):
    univ_obj = University.objects.get(pk=pk)
    #
    browser = webdriver.PhantomJS(executable_path='E:\\Projetos\\GitHub\WrkAgg\\venv\Scripts\\phantomjs.exe')
    # browser = webdriver.Edge(executable_path='E:\\Projetos\\GitHub\WrkAgg\\venv\Scripts\\MicrosoftWebDriver.exe')
    # browser.implicitly_wait(15)
    # browser.manage().timeouts().pageLoadTimeout(10, TimeUnit.SECONDS);
    # browser.maximize_window()
    #
    browser.get(univ_obj.sigaa_home)
    browser.get(univ_obj.teachers_search)
    departments = Department.objects.filter(university=univ_obj)
    for dpt_obj in departments:
        try:
            browser.find_element_by_xpath(xpath_department_option.format(dpt_obj.select_value)).click()
            browser.find_element_by_xpath(xpath_button_search).click()
            teachers_number_string = browser.find_element_by_xpath(xpath_teachers_number).get_attribute('innerHTML')
            teachers_number = int(re.findall('(?<=\()\d*(?=\))', teachers_number_string)[0]) + 1
            for teacher in range(1, teachers_number):
                try:
                    t_name = browser.find_element_by_xpath(xpath_teachers_name.format(teacher)).get_attribute(
                        'innerHTML')
                    link = browser.find_element_by_xpath(xpath_teachers_link.format(teacher)).get_attribute("href")
                    teachers_registry = int(re.findall('(?<=siape=)\d*', link)[0])
                    t_obj = Teacher(name=t_name, registry=teachers_registry, department=dpt_obj)
                    t_obj.save()
                except Exception as E:
                    pass
        except NoSuchElementException as E:
            print(dpt_obj.name)
            print(E)
    #
    browser.close()


def get_teachers_data():
    global browser
    browser = webdriver.PhantomJS(executable_path='E:\\Projetos\\GitHub\WrkAgg\\venv\Scripts\\phantomjs.exe')
    teachers = Teacher.objects.filter(analysed=False)
    for teacher_obj in teachers:
        try:
            print(teacher_obj.name)
            url_parsed = urlparse(teacher_obj.department.university.teachers_search)
            url = urlunsplit((url_parsed.scheme, url_parsed.netloc, link_teachers.format(teacher_obj.registry), '', ''))
            browser.get(url)
            try:
                cv_obj = browser.find_element_by_xpath(xpath_lattes_link).get_attribute("href")
                teacher_obj.cv = clean_data(cv_obj)
            except:
                pass
            try:
                room_value = browser.find_element_by_xpath(xpath_room).get_attribute("innerHTML")
                teacher_obj.room = clean_data(room_value)
            except:
                pass
            try:
                phone_value = browser.find_element_by_xpath(xpath_phone).get_attribute("innerHTML")
                teacher_obj.phone = clean_data(phone_value)
            except:
                pass
            try:
                interest_value = browser.find_element_by_xpath(xpath_interest).get_attribute("innerHTML")
                teacher_obj.interest = clean_data(interest_value)
            except:
                pass
            try:
                description_value = browser.find_element_by_xpath(xpath_description).get_attribute("innerHTML")
                teacher_obj.description = clean_data(description_value)
            except:
                pass
            try:
                email_value = browser.find_element_by_xpath(xpath_email).get_attribute("innerHTML")
                teacher_obj.email = clean_data(email_value).lower()
            except:
                pass
            try:
                address_value = browser.find_element_by_xpath(xpath_address).get_attribute("innerHTML")
                teacher_obj.address = clean_data(address_value)
            except:
                pass
            teacher_obj.analysed = True
            teacher_obj.save()
        except:
            pass
    browser.close()


def get_lectures():
    term = None
    #
    browser = webdriver.PhantomJS(executable_path='E:\\Projetos\\GitHub\WrkAgg\\venv\Scripts\\phantomjs.exe')
    existent = list(Lecture.objects.all().values_list('teacher', flat=True).distinct())
    teachers = Teacher.objects.all().exclude(id__in=existent)
    #
    for teacher_obj in teachers:
        try:
            url_parsed = urlparse(teacher_obj.department.university.teachers_search)
            url = urlunsplit((url_parsed.scheme, url_parsed.netloc, link_lectures.format(teacher_obj.registry), '', ''))
            browser.get(url)

            lectures_tr = browser.find_element_by_xpath(xpath_lectures).find_elements_by_tag_name("tr")
            print(teacher_obj.name)

            for tr in lectures_tr:
                td = tr.find_elements_by_tag_name("td")
                if len(td) > 0:
                    if len(td) == 1:
                        for element in td:
                            if len(element.get_attribute("innerHTML")) > 1:
                                term = element.get_attribute("innerHTML")
                    elif len(td) == 5:
                        code = td[0].get_attribute("innerHTML")
                        tid_string = td[1].find_elements_by_tag_name("a")[0].get_attribute("href")
                        tid = int(re.findall('(?<=tid=)\d*', tid_string)[0])
                        name = td[1].find_elements_by_tag_name("a")[0].get_attribute("text")
                        timetable = td[3].get_attribute("innerHTML")
                        workload_string = td[2].get_attribute("innerHTML")
                        workload = int(re.findall('\d+(?=h)', workload_string)[0])
                        #
                        entry = Lecture(code=code, teacher=teacher_obj, term=term, tid=tid, name=name,
                                        workload=workload,
                                        timetable=timetable)
                        entry.save()
        except NoSuchElementException:
            pass
    #
    browser.close()


def get_university(university):
    global univ_obj
    univ_obj = university
    print("*** " + university.name + " ***")
    departments = get_departments(univ_obj.teachers_search)
    #
    r_departments = DepObj.filter(select_value__in=list(departments.keys()), university=univ_obj).values_list(
        "select_value", flat=True)
    #
    list(map(departments.__delitem__, filter(departments.__contains__, r_departments)))
    print("{} new departments".format(len(departments.keys())))
    #
    if len(departments.keys()) > 0:
        for department in departments.keys():
            try:
                entry = Department(name=departments[department]['name'], city=departments[department]['city'],
                                   select_value=department, university=univ_obj)
                entry.save()
            except:
                pass


def reset_analysed():
    Ts = Teacher.objects.filter(analysed=True, cv='', room='', phone='', interest='', description='', address='',
                                email='')
    for e in Ts:
        print(e.name)
        e.analysed = False
        e.save()
        '''
         fields = [e.cv == '', e.room == '', e.phone == '', e.interest == '', e.description == '', e.address == '', e.email == '']
    
        if all(fields):
            e.analysed = False
            e.save()
        '''


def main():
    Us = University.objects.all()
    for u in Us:
        get_university(u)
        get_teachers(u.pk)
        get_teachers_data()
