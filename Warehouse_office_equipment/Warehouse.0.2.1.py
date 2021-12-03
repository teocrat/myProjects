import json

from tabulate import tabulate

import os


class Warehouse:
    with open('printers.csv', 'r', encoding='utf-8') as f:
        shelf_printers = json.load(f)

    with open('scanners.csv', 'r', encoding='utf-8') as f:
        shelf_scanners = json.load(f)

    with open('copiers.csv', 'r', encoding='utf-8') as f:
        shelf_copiers = json.load(f)

    with open('inv_num.csv', 'r', encoding='utf-8') as f:
        inv_num = json.load(f)
    inv_num.sort()
    with open('accounts_department.csv', 'r', encoding='utf-8') as f:
        accounts_department = json.load(f)

    with open('management.csv', 'r', encoding='utf-8') as f:
        management = json.load(f)

    with open('administration.csv', 'r', encoding='utf-8') as f:
        administration = json.load(f)


class OfficeEquipment:

    def __init__(self):
        n = 0
        while n >= 0:
            self.type = input('Введите  тип оргтехники\n принтер - 1, сканер - 2, копир - 3: ')
            if self.type != "1" and self.type != "2" and self.type != "3":
                print('Введен неверный номер меню')
            else:
                break

        self.name = input('Введите модель  оргтехники: ')

        print(f'Существующие инв. номера: {Warehouse.inv_num}')
        try:
            self.num = input('Введите инвентарный номер оргтехники: ')
        except ValueError:
            print('Введена буква вместо цифры')

    # Добавление оргтехники на склад
    def move_warehouse(self):
        if self.num not in Warehouse.inv_num:
            Warehouse.inv_num.append(self.num)

            if self.type == '1':
                Warehouse.shelf_printers.setdefault(self.num, self.name)
                with open('printers.csv', 'r+', encoding='utf-8') as f:
                    json.dump(Warehouse.shelf_printers, f, ensure_ascii=False, indent=4)

                with open('inv_num.csv', 'w', encoding='utf-8') as f:
                    json.dump(Warehouse.inv_num, f, ensure_ascii=False, indent=4)

            elif self.type == '2':
                Warehouse.shelf_scanners.setdefault(self.num, self.name)
                with open('scanners.csv', 'r+', encoding='utf-8') as f:
                    json.dump(Warehouse.shelf_scanners, f, ensure_ascii=False, indent=4)

                with open('inv_num.csv', 'w', encoding='utf-8') as f:
                    json.dump(Warehouse.inv_num, f, ensure_ascii=False, indent=4)

            elif self.type == '3':
                Warehouse.shelf_copiers.setdefault(self.num, self.name)
                with open('copiers.csv.', 'r+', encoding='utf-8') as f:
                    json.dump(Warehouse.shelf_copiers, f, ensure_ascii=False, indent=4)

                with open('inv_num.csv', 'w', encoding='utf-8') as f:
                    json.dump(Warehouse.inv_num, f, ensure_ascii=False, indent=4)

        else:
            print(f'Такой инвентарный номер уже существует: {Warehouse.inv_num}')


# Перемещение оргтехники в подразделения
def move_division():
    i = 0
    while i >= 0:
        Warehouse()
        n = input('Переместить выбранную оргтехнику в подразделение(y/n): ')
        if n == 'y':
            k = input('Выбирите подразделение (бухгалтерия - 1, управление - 2, администрация - 3): ')
            print('На складе:')
            print('Принтеры')
            print(tabulate(Warehouse.shelf_printers.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print('Сканеры')
            print(tabulate(Warehouse.shelf_scanners.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print('Копиры')
            print(tabulate(Warehouse.shelf_copiers.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))

            v = input('Укажите инв. номер перемещаемого аппарата: ')
            try:
                if v in Warehouse.shelf_printers:
                    d = Warehouse.shelf_printers[v]
                    Warehouse.shelf_printers.pop(v)
                    with open('printers.csv', 'w', encoding='utf-8') as f:
                        json.dump(Warehouse.shelf_printers, f, ensure_ascii=False, indent=4)

                elif v in Warehouse.shelf_scanners:
                    d = Warehouse.shelf_scanners[v]
                    Warehouse.shelf_scanners.pop(v)
                    with open('scanners.csv', 'w', encoding='utf-8') as f:
                        json.dump(Warehouse.shelf_scanners, f, ensure_ascii=False, indent=4)

                elif v in Warehouse.shelf_copiers:
                    d = Warehouse.shelf_copiers[v]
                    Warehouse.shelf_copiers.pop(v)
                    with open('copiers.csv', 'w', encoding='utf-8') as f:
                        json.dump(Warehouse.shelf_copiers, f, ensure_ascii=False, indent=4)
                Warehouse()
                if k == '1':
                    Warehouse.accounts_department.setdefault(v, d)
                    with open('accounts_department.csv', 'r+', encoding='utf-8') as f:
                        json.dump(Warehouse.accounts_department, f, ensure_ascii=False, indent=4)
                elif k == '2':
                    Warehouse.management.setdefault(v, d)
                    with open('management.csv', 'r+', encoding='utf-8') as f:
                        json.dump(Warehouse.management, f, ensure_ascii=False, indent=4)
                elif k == '3':
                    Warehouse.administration.setdefault(v, d)
                    with open('administration.csv', 'r+', encoding='utf-8') as f:
                        json.dump(Warehouse.administration, f, ensure_ascii=False, indent=4)
                Warehouse()
            except UnboundLocalError:
                print('Нет такой оргтехники на складе')

        else:
            break


# Возврат оргтехники на склад
def return_warehouse():
    n = 0
    while n >= 0:
        Warehouse()
        i = input('Вернуть выбранную оргтехнику на склад:(y/n) ')
        if i == 'y':
            k = input('Выбирите подразделение (бухгалтерия - 1, управление - 2, администрация - 3): ')
            if k == '1':
                print('В бухгалтерии находяться следующие аппараты: ')
                print(tabulate(Warehouse.accounts_department.items(), headers=['Инв.номер', 'Аппарат'], tablefmt="grid"))
            elif k == '2':
                print('В управлении находяться следующие аппараты:')
                print(tabulate(Warehouse.management.items(), headers=['Инв.номер', 'Аппарат'], tablefmt="grid"))
            elif k == '3':
                print('В администрации находяться следующие аппараты:')
                print(tabulate(Warehouse.administration.items(), headers=['Инв.номер', 'Аппарат'], tablefmt="grid"))
            v = input('Укажите инв. номер перемещаемого аппарата: ')
            t = input('Укажите тип оборудования (принтер - 1, сканер - 2, копир - 3: ')
            try:
                if v in Warehouse.accounts_department:
                    d = Warehouse.accounts_department[v]
                    Warehouse.accounts_department.pop(v)
                    with open('accounts_department.csv', 'w', encoding='utf-8') as f:
                        json.dump(Warehouse.accounts_department, f, ensure_ascii=False, indent=4)
                elif v in Warehouse.management:
                    d = Warehouse.management[v]
                    Warehouse.management.pop(v)
                    with open('management.csv', 'w', encoding='utf-8') as f:
                        json.dump(Warehouse.management, f, ensure_ascii=False, indent=4)
                elif v in Warehouse.administration:
                    d = Warehouse.administration[v]
                    Warehouse.administration.pop(v)
                    with open('administration.csv', 'w', encoding='utf-8') as f:
                        json.dump(Warehouse.administration, f, ensure_ascii=False, indent=4)
                if t == '1':
                    Warehouse.shelf_printers.setdefault(v, d)
                    with open('printers.csv', 'r+', encoding='utf-8') as f:
                        json.dump(Warehouse.shelf_printers, f, ensure_ascii=False, indent=4)
                elif t == '2':
                    Warehouse.shelf_scanners.setdefault(v, d)
                    with open('scanners.csv', 'r+', encoding='utf-8') as f:
                        json.dump(Warehouse.shelf_scanners, f, ensure_ascii=False, indent=4)
                elif t == '3':
                    Warehouse.shelf_copiers.setdefault(v, d)
                    with open('copiers.csv', 'r+', encoding='utf-8') as f:
                        json.dump(Warehouse.shelf_copiers, f, ensure_ascii=False, indent=4)
            except UnboundLocalError:
                print('Нет такой оргтехники в подразделении')

        else:
            break


# Списание оргтехники
def decommissioning():
    i = 0
    while i >= 0:
        Warehouse()
        v = input('Списать оргтехнику? (y/n): ')
        if v == 'y':
            print('На складе:')
            print('Принтеры')
            print(tabulate(Warehouse.shelf_printers.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print('Сканеры')
            print(tabulate(Warehouse.shelf_scanners.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print('Копиры')
            print(tabulate(Warehouse.shelf_copiers.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            n = input('Введите инв. номер аппарата: ')
            if n in Warehouse.shelf_printers:
                del Warehouse.shelf_printers[n]
                with open('printers.csv', 'w', encoding='utf-8') as f:
                    json.dump(Warehouse.shelf_printers, f, ensure_ascii=False, indent=4)
            elif n in Warehouse.shelf_scanners:
                del Warehouse.shelf_scanners[n]
                with open('scanners.csv', 'w', encoding='utf-8') as f:
                    json.dump(Warehouse.shelf_scanners, f, ensure_ascii=False, indent=4)
            elif n in Warehouse.shelf_copiers:
                del Warehouse.shelf_copiers[n]
                with open('copiers.csv', 'w', encoding='utf-8') as f:
                    json.dump(Warehouse.shelf_copiers, f, ensure_ascii=False, indent=4)

            else:
                print('Указанный инв. номер отсутствует на складе,\n'
                      ' переместите аппарат с таким инв. номером из подразделения на склад\n'
                      ' или выбирете другой инв. номер ')

            Warehouse.inv_num.remove(n)
            with open('inv_num.csv', 'w', encoding='utf-8') as f:
                json.dump(Warehouse.inv_num, f, ensure_ascii=False, indent=4)

        else:
            break


# Поиск по инвентарному номеру

def find_inv_num():
    Warehouse()
    n = 0
    while n >= 0:
        b = input('Найти технику по инв. номеру? (y/n): ')
        if b == 'y':
            a = input('Введите инв. номер: ')
            if a in Warehouse.shelf_printers:
                print('Аппарат находится на складе на полке принтеров')
            elif a in Warehouse.shelf_scanners:
                print('Аппарат находится на складе на полке сканеров')
            elif a in Warehouse.shelf_copiers:
                print('Аппарат находится на складе на полке копиров')
            elif a in Warehouse.accounts_department:
                print('Аппарат находится в бухгалтерии')
            elif a in Warehouse.management:
                print('Аппарат находится в управлении')
            elif a in Warehouse.administration:
                print('Аппарат находится в администрации')
            else:
                print('Такой инв. номер отсутствует')
        else:
            break


# Поиск по модели

def find_equipment():
    Warehouse()
    n = 0

    while n >= 0:
        b = input('Найти оргтехнику по модели? (y/n): ')
        list_model_p = []
        list_model_s = []
        list_model_c = []
        list_model_a_d = []
        list_model_m = []
        list_model_a = []

        if b == 'y':
            m = input('Введите модель оргтехники: ')
            for key, value in Warehouse.shelf_printers.items():
                if value == m:
                    list_model_p.append(m)
            if len(list_model_p) != 0:
                print(f'{len(list_model_p)} {m}  на складе на полке принтеров')
            for key, value in Warehouse.shelf_scanners.items():
                if value == m:
                    list_model_s.append(m)
            if len(list_model_s) != 0:
                print(f'{len(list_model_s)} {m} на складе на полке сканеров')
            for key, value in Warehouse.shelf_copiers.items():
                if value == m:
                    list_model_c.append(m)
            if len(list_model_c) != 0:
                print(f'{len(list_model_c)} {m} на складе на полке копиров')
            for key, value in Warehouse.accounts_department.items():
                if value == m:
                    list_model_a_d.append(m)
            if len(list_model_a_d) != 0:
                print(f'{len(list_model_a_d)} {m} в бухгалтерии')
            for key, value in Warehouse.management.items():
                if value == m:
                    list_model_m.append(m)
            if len(list_model_m) != 0:
                print(f'{len(list_model_m)} {m} в управлении')
            for key, value in Warehouse.administration.items():
                if value == m:
                    list_model_a.append(m)
            if len(list_model_a) != 0:
                print(f'{len(list_model_a)} {m} в администрации')

            count_model = len(list_model_p) + len(list_model_s) + len(list_model_c) + len(list_model_a_d) + len(
                list_model_m) + len(list_model_a)
            if count_model == 0:
                print('Нет такой модели в организации')
            else:
                print(f'Количество аппаратов модели {m}: {count_model} шт.')

        else:
            break


class Printer(OfficeEquipment):
    @staticmethod
    def count_printers():
        return len(Warehouse.shelf_printers)


class Scanner(OfficeEquipment):
    @staticmethod
    def count_scanners():
        return len(Warehouse.shelf_scanners)


class Copier(OfficeEquipment):
    @staticmethod
    def count_copiers():
        return len(Warehouse.shelf_copiers)


print('Добро пожаловать на склад оргтехники!')
x = 0
while x >= 0:
    print('Выбирете пункт меню:')
    try:
        i = int(input('1 - Добавить оргтехнику на склад \n'
                      '2 - Перемещение оргтехники в подразделения \n'
                      '3 - Возврат оргтехники на склад из подразделений \n'
                      '4 - Списание оргтехники \n'
                      '5 - Поиск по инвентарному номеру \n'
                      '6 - Поиск по модели \n'
                      '7 - Количество принтеров на складе \n'
                      '8 - Количество сканеров на складе \n'
                      '9 - Количество копиров на складе \n'
                      '10 - Оборудование на складе: \n'
                      '11 - Оборудование в подразделениях: \n'
                      '12 - Общее количество оборудования: \n'
                      'Ваш выбор: '))

        if i == 1:
            n = 0
            while n >= 0:
                s = input('Вы хотите добавить оргтехнику на склад? y/n:  ')
                if s == 'y':
                    a = Printer()
                    a.move_warehouse()
                    Warehouse.inv_num.sort()
                    s = input('Продолжить? y/n: ')
                    if s == 'y':
                        b = Scanner()
                        b.move_warehouse()
                        Warehouse.inv_num.sort()
                    else:
                        break

                    s = input('Продолжить? y/n: ')
                    if s == 'y':
                        c = Copier()
                        c.move_warehouse()
                        Warehouse.inv_num.sort()
                    else:
                        break
                else:
                    break
        if i == 2:
            move_division()
        if i == 3:
            return_warehouse()
        if i == 4:
            decommissioning()
        if i == 5:
            find_inv_num()
        if i == 6:
            find_equipment()
        if i == 7:
            print(f'Количество принтеров на складе: {Printer.count_printers()} шт.')
        if i == 8:
            print(f'Количество сканеров на складе: {Scanner.count_scanners()} шт.')
        if i == 9:
            print(f'Количество копиров на складе: {Copier.count_copiers()} шт.')
        if i == 10:
            print(f'Принтеры: ')
            print(tabulate(Warehouse.shelf_printers.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print(f'Сканеры:')
            print(tabulate(Warehouse.shelf_scanners.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print(f'Копиры:')
            print(tabulate(Warehouse.shelf_copiers.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
        if i == 11:
            print(f'Оборудование в бухгалтерии:')
            print(tabulate(Warehouse.accounts_department.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print(f'Оборудование в управлении: ')
            print(tabulate(Warehouse.management.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
            print(f'Оборудование в администрации:')
            print(tabulate(Warehouse.administration.items(), headers=['Инв.№', 'Аппарат'], tablefmt="grid"))
        count = Printer.count_printers() + Scanner.count_scanners() + Copier.count_copiers()
        count_1 = len(Warehouse.administration) + len(Warehouse.management) + len(Warehouse.accounts_department)
        if i == 12:
            print(f'Общее количество оборудования на складе: {count} шт.')
            print(f'Общее количество оборудования в подразделениях: {count_1}')
            print(f'Всего оборудования в организации: {count + count_1}')
        if int(i) < 1 or int(i) > 12:
            print('Неправильно выбран пункт меню')
    except ValueError:
        print('Вы ввели буквенное значение меню')
    b = input('Вернуться в основное меню? (y/n) ')
    os.system('cls||clear')
    if b != 'y':
        break

input("press Enter")
