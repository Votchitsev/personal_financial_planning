import datetime
import json
from pprint import pprint

TODAY = datetime.datetime.today()


class InputDevise:
    def __init__(self, input_information, error_message: str):
        self.information = input_information
        self.error_message = error_message

    def in_integer(self):
        if self.information.isdigit():
            output_information = int(self.information)
            return output_information
        elif self.information == 'exit':
            return False
        else:
            print(self.error_message)
            return False 


class ConstantSpending:
    def __init__(self, plan):
        self.spending_plan = plan

    def show(self):
        pprint(self.spending_plan)

    def add_exp(self):
        category = input('Введите категорию: ')
        spend_of_money = input('Введите сумму: ')
        try:
            format_spend_of_money = round(float(spend_of_money.replace(',', '.')), 2)
        except ValueError:
            print('Ошибка: неверное значение суммы')
            return False
        date_add = input('Введите дату: ')
        format_date = date_add.replace('/', '.')
        date_list = format_date.split('.')
        if date_list[0].isdigit() and len(date_list[0]) == 2 and date_list[1].isdigit() \
                and len(date_list[1]) == 2 and date_list[2].isdigit() and len(date_list[2]) == 4:
            day = int(date_list[0])
            month = int(date_list[1])
            year = int(date_list[2])
        else:
            print('Ошибка: неверный формат даты')
            return False

        spend_inf = {
            'category': category,
            'spend_of_money': format_spend_of_money,
            'date': str(datetime.date(year, month, day))
        }
        self.spending_plan['spending'].append(spend_inf)
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.spending_plan, save_file, indent=4)
        print(f'Трата категории "{category.strip().capitalize()}" на сумму {format_spend_of_money} рублей добавлена.')

    def delete(self):
        print('\nКакую трату вы хотите удалить?\n')
        select_spend = {}
        num = 0
        for item in self.spending_plan['spending']:
            num += 1
            select_spend[num] = item
            print(f"{num} - {item['category']} {item['spend_of_money']} {item['date']}")
        err_msg = 'Ошибка: Неверный формат.'
        select_num = InputDevise(input('Введите номер: '), err_msg)
        select = select_num.in_integer()
        if not select:
            return False
        remove_element = select_spend[select]
        self.spending_plan['spending'].remove(remove_element)
        print('Трата удалена.')
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.spending_plan, save_file, indent=4)

    def delete_all(self):
        agreement = input('Вы уверены, что хотите удалить все траты? (Y/N)').lower()
        if agreement == 'y':
            self.spending_plan['spending'] = []
            with open('data.json', 'w') as data_del:
                json.dump(self.spending_plan, data_del, indent=4)
        else:
            pass


def menu(command):
    if command == 'add':
        const.add_exp()
    elif command == 'show':
        const.show()
    elif command == 'del':
        const.delete()
    elif command == 'del_all':
        const.delete_all()
    else:
        print('Неизвестная команда.')


with open('data.json', 'r') as data_file:
    data = json.load(data_file)
    if data == "empty":
        date_one = input('Введите дату следующего поступления денег в формате ДД ММ ГГГГ: ')
        date_inc = date_one.split('.' or '/')
        d = int(date_inc[0])
        m = int(date_inc[1])
        y = int(date_inc[2])
        next_income_date = datetime.date(d, m, y)
        data = {
            "current_date": str(TODAY),
            "next_income_date": str(next_income_date),
            "spending": []
        }
    else:
        pass

const = ConstantSpending(data)

while True:
    mes = input('Введите команду: ')
    if mes == 'exit':
        print('Работа завершена.')
        break
    menu(mes)
