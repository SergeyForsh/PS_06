# преобразовывать данные
data - [
    ['100', '200', '300'],
    ['400', '500', '600']
]
# С сайта мы получаем именно списки
numbers = []
# Используем функции float или int, чтобы преобразовать данные
for row in data:
    for text in row:
        number = int(text)
        numbers.append(number)

print(numbers)
