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

    def in_float(self):
        try:
            format_spend_of_money = round(float(self.information.replace(',', '.')), 2)
            return format_spend_of_money
        except ValueError:
            print('Ошибка: неверное значение суммы')
            return False

    def in_date(self):
        try:
            format_date = self.information.replace('/', '.')
            date_list = format_date.split('.')
            day = int(date_list[0])
            month = int(date_list[1])
            year = int(date_list[2])
            date = str(datetime.date(year, month, day))
            return date
        except ValueError:
            print('Ошибка: неверный формат даты')
            return False

    def in_agreement(self):
        if self.information.lower() == 'y':
            return 'yes'
        else:
            return 'no'


class ConstantSpending:
    def __init__(self, plan):
        self.spending_plan = plan

    def show(self):
        print(f"Текущая дата: {self.spending_plan['current_date']}")
        print(f"Дата следующего поступления денег: {self.spending_plan['next_income_date']}")
        print()
        for spend in self.spending_plan['spending']:
            print(f"{spend['category']} {spend['spend_of_money']}")
        print(f"ИТОГО: {self.count_total_sum()}")

    def add_exp(self):
        category = input('Введите категорию: ')
        spend_of_money = input('Введите сумму: ')
        coast_error_msg = 'Ошибка: Неверный формат данных.'
        exp = InputDevise(spend_of_money, coast_error_msg)
        exp_sum = exp.in_float()
        if not exp_sum:
            return False
        date_add = input('Введите дату: ')
        exp_error_msg = 'Ошибка: Неверный формат даты'
        exp_date_class = InputDevise(date_add, exp_error_msg)
        exp_date = exp_date_class.in_date()
        if not exp_date:
            return False

        spend_inf = {
            'category': category,
            'spend_of_money': exp_sum,
            'date': exp_date
        }
        self.spending_plan['spending'].append(spend_inf)
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.spending_plan, save_file, indent=4)
        print(f'Трата категории "{category.strip().capitalize()}" на сумму {exp_sum} рублей добавлена.')

    def delete(self):
        print('\nКакую трату вы хотите удалить?\n')
        select_spend = {}
        num = 0
        for item in self.spending_plan['spending']:
            num += 1
            select_spend[num] = item
            print(f"{num} - {item['category']} {item['spend_of_money']} {item['date']}")
        print(f"ИТОГО: {self.count_total_sum()}")
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
        agreement = input('Вы уверены, что хотите удалить все траты? (Y/N)')
        agr_del_class = InputDevise(agreement, "")
        agr = agr_del_class.in_agreement()
        if agr == 'yes':
            self.spending_plan['spending'] = []
            with open('data.json', 'w') as data_del:
                json.dump(self.spending_plan, data_del, indent=4)
        else:
            pass

    def count_total_sum(self):
        total_sum = 0
        for num in self.spending_plan['spending']:
            total_sum += num['spend_of_money']
        return total_sum


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
