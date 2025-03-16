# PS_06 Работа с данными и сохранение результатов
Когда мы парсим данные с различных веб-страниц, мы часто получаем сырые данные, которые неудобно (или вообще нельзя) использовать и которые нуждаются в обработке.
## В обработку входят:
очистка данных — удаление лишних пробелов, специальных символов, лишней информации, исправление некорректных, повреждённых данных и т.д. Когда мы регулируем парсинг, лишней информации может почти не быть;
преобразование данных — перевод строк в числа и т.п.;
фильтрация данных — отбор только нужный случай.

Проделываем очистку данных:
Пишем простой парсер. В итоге мы получим коллекцию со всеми рядами таблицы.
import requests
from bs4 import BeautifulSoup
url = "https://"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
rows = soup.find_all("tr")
# tr - каждый ряд таблицы
# td - каждая ячейка внутри ряда таблицы
data = []
2. Теперь нам нужно перебрать коллекцию. Используем цикл “for”.
for row in rows:
    cols = row.find_all("td")
    # Используем укороченный вариант цикла for
    # Для удаления пробелов и других лишних символов используем функцию strip
    cleaned_cols = [col.text.strip() for col in cols]
    # Чтобы удалить пробелы, оставляем ()
    # Чтобы удалить какие-то символы из начала и конца, пишем ('то-что-надо-удалить')
    data.append(cleaned_cols)
    # Функция append добавляет в список.
print(data)
____________________________________________________________________
Также можно удалять символы из списка при помощи метода pop и других.
Преобразуем данные (цены)
Представим, что мы уже достали информацию из списков, и теперь у нас два списка, которые находятся внутри друг друга (вложенные списки, двумерные массивы).
data = [
    ['100', '200', '300']
    ['400', '500', '600']
    ]
# С сайта мы получаем именно списки.
    numbers = []
2. Используем функции float или int, чтобы преобразовать данные.

for row in data:
    for text in row:
        number = int(text)
        numbers.append(number)
print(numbers)
Чаще всего преобразования — это просто преобразование одного типа данных в другой.
Отфильтруем данные — это можно делать через обычные условия.
У нас также есть двумерный список, содержащий другие списки.
data = [
    [100, 110, 120]
    [400, 500, 600]
    [150, 130, 140]
    ]
    list = []
2. Используем цикл for и условие:

for row in data:
    for item in row:
        if item > 190:
            list.append(item)
print(list)
_______________________________________________________________________
##Существует множество методов и форматов для сохранения данных, каждый из которых имеет свои преимущества и недостатки.
Форматы:

txt — текстовый формат;

csv (Comma-Separated Values) — также текстовый формат; один из наиболее простых и распространённых форматов для хранения табличных данных. 
В нём мы можем сохранить самые простые структуры (например, таблицу из двух столбцов: имя пользователя, телефон пользователя). 
Нельзя загрузить большие объёмы данных. Можем легко читать этот формат. Формат совместим, открывается через текстовые редакторы или Excel.

json (JavaScript Object Notation) — формат, удобный для передачи данных между сервером и клиентом. 
Формат похож на словари в Python, удобен для работы со сложными структурами (вложенные объекты, вложенные массивы). Также удобен для чтения человеком.

База данных SQLite — легковесная база данных, удобно для небольших объёмов данных, можно посылать такой базе запросы, базу можно масштабировать;
электронные таблицы (например, гугл таблицы) — удобны для визуализации данных и выполнения расчётов. 
Основное удобство в том, что мы можем иметь доступ к этим таблицам с различных устройств.
_________________________________________________________________________
###Разрабатываем программу
Мы будем парсить данные с сайта https://tomsk.hh.ru/vacancies/programmist и сохранять их в csv-файл.
###Тут селекторы я менял на обновленные с сайта!!!
#Код, написанный с использованием новых селекторов.
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Firefox()
url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)
time.sleep(3)
vacancies = driver.find_elements(By.CSS_SELECTOR, 'div.vacancy-info--umZA61PpMY07JVJtomBA')
parsed_data = []
for vacancy in vacancies:
    try:
        title_element = vacancy.find_element(By.CSS_SELECTOR, 'a.magritte-link___b4rEM_4-3-2')
        title = title_element.text
        link = title_element.get_attribute('href')
        company = vacancy.find_element(By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-employer-text"]').text
        try:
            salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-labels--cR9OD8ZegWd3f7Mzxe6z').text
        except:
            salary = "Не указана"
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue
    parsed_data.append([title, company, salary, link])

driver.quit()

with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Название компании', 'Зарплата', 'Ссылка на вакансию'])
    writer.writerows(parsed_data)
    ______________________________________________________________________________________
    ###Пошаговое объяснение написания кода:
#Код, написанный экспертом в уроке.
# Импортируем модуль со временем
import time
# Импортируем модуль csv
import csv
# Импортируем Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# Инициализируем браузер
driver = webdriver.Firefox()
# Если мы используем Chrome, пишем
# driver = webdriver.Chrome()

# В отдельной переменной указываем сайт, который будем просматривать
url = "https://tomsk.hh.ru/vacancies/programmist"

# Открываем веб-страницу
driver.get(url)

# Задаём 3 секунды ожидания, чтобы веб-страница успела прогрузиться
time.sleep(3)

# Находим все карточки с вакансиями с помощью названия класса
# Названия классов берём с кода сайта
vacancies = driver.find_elements(By.CLASS_NAME, 'vacancy-card--H8LvOiOGPll0jZvYpxIF')

# Выводим вакансии на экран
print(vacancies)
# Создаём список, в который потом всё будет сохраняться
parsed_data = []

# Перебираем коллекцию вакансий
# Используем конструкцию try-except, чтобы "ловить" ошибки, как только они появляются
for vacancy in vacancies:
   try:
   # Находим элементы внутри вакансий по значению
       # Находим названия вакансии  
     title = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-name--SYbxrgpHgHedVTkgI_cA').text
     # Находим названия компаний
     company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text--O32pGCRW0YDmp3BHuNOP').text
     # Находим зарплаты
     salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text--cCPBXayRjn5GuLFWhGTJ').text
     # Находим ссылку с помощью атрибута 'href'
     link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')
   # Вставляем блок except на случай ошибки - в случае ошибки программа попытается продолжать
   except:
     print("произошла ошибка при парсинге")
         continue

    # Вносим найденную информацию в список
    parsed_data.append([title, company, salary, link])

# Закрываем подключение браузер
driver.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
# 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("hh.csv", 'w',newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    # Создаём объект
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название вакансии', 'название компании', 'зарплата', 'ссылка на вакансию'])
    # Прописываем использование списка как источника для рядов таблицы
    writer.writerows(parsed_data)
