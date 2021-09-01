import datetime
import json
from pprint import pprint

TODAY = datetime.datetime.today()


class ConstantSpending:
    def __init__(self, plan):
        self.spending_plan = plan

    def show(self):
        pprint(self.spending_plan)

    def add_exp(self):
        category = input('Введите категорию: ')
        spend_of_money = float(input('Введите сумму: '))
        d, m, y = map(int, input('Введите дату: ').split())
        spend_inf = {
            'category': category,
            'spend_of_money': spend_of_money,
            'date': str(datetime.date(y, m, d))
        }
        self.spending_plan['spending'].append(spend_inf)
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.spending_plan, save_file, indent=4)

    def delete(self):
        print('\nКакую трату вы хотите удалить?\n')
        select_spend = {}
        num = 0
        for item in self.spending_plan['spending']:
            num += 1
            select_spend[num] = item
            print(f"{num} - {item['category']} {item['spend_of_money']} {item['date']}")
        select_num = int(input('Введите номер: '))
        remove_element = select_spend[select_num]
        self.spending_plan['spending'].remove(remove_element)
        print('Трата удалена.')
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.spending_plan, save_file, indent=4)


def menu(command):
    if command == 'add':
        const.add_exp()
    elif command == 'show':
        const.show()
    elif command == 'del':
        const.delete()


with open('data.json', 'r') as data_file:
    data = json.load(data_file)
    if data == "empty":
        day, month, year = map(int, input('Введите дату следующего поступления денег в формате ДД ММ ГГГГ').split())
        next_income_date = datetime.date(year, month, day)
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
