__author__ = 'odmen'

# Python3
# 1. Ищет одинаковые файлы в каталоге
# 2. Создает каталог для уникальных файлов
# 3. Копирует в этот каталог файлы без повторений

import glob
import os
import sys
import re
import hashlib
import shutil
import string
import random
from functools import partial

for arg in sys.argv:
# перебираем аргументы, переданные скрипту
    currindex = sys.argv.index(arg)
# запоминаем индекс текущего выбранного аргумента
    if arg == "-p":
# если текущий элемент - "-p"
        work_dir = sys.argv[currindex+1]
# то запоминаем текст следующего (по индексу) элемента как "рабочий каталог"

copied = []
# будет хранить хеши скопированных файлов
img_regex = re.compile("\.(jpg|jpeg|png)$")
# регулярка выборки файлов определенного разрешения

def md5file(filename):
# эта функция считает md5 сумму файла
# на вход принимает полный путь до файла
# возвращает строку
# код фунции сопирован из интернета, как работает пока не смотрел
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
# функция берет последовательность букв и цифр
# берет из этой последовательности случайные символы
# последовательность длинной 6 символов
# возвращает эту последовательность
    return ''.join(random.choice(chars) for _ in range(size))

def create_folder():
# функция герерирует имя папки для уникальных файлов,
# проверяя нет ли случайно такой папки уже
    interest_folder = "ufiles_"+id_generator()
# составляем имя папки для уникальных файлов
    if not os.path.exists(interest_folder):
# проверяем нет ли такой папки в рабочем каталоге
        os.makedirs(interest_folder)
# если нету создаем папку
        return interest_folder
# и возвращаем имя
    else:
        create_folder()
# если такая папка уже есть запускаем функцию заново

out_folder = create_folder()
# получаем имя папки для уникальных фалов
os.chdir(work_dir)
# переходим в рабочий каталог
for filename in glob.glob("*.*"):
# перебираем имена файлов в этом каталоге
    if img_regex.search(filename):
# если текущий выбранный файл нам подходит по регулярке
        filemd5 = md5file(work_dir+filename)
# передаем путь до файла в функцию вычисления md5 и в ответ получаем хеш файла
        if filemd5 not in copied:
# если такого хеша нет в списке скопированных файлов, то
            print("Copy "+work_dir+filename+" to "+work_dir+out_folder+'/'+filename)
            shutil.copy2(work_dir+filename, work_dir+out_folder+'/'+filename)
# копируем файл в
# копируем файл
            copied.append(filemd5)
# добавляем его хеш в список