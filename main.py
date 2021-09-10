import datetime
import json

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


class Expenses:
    def __init__(self, information):
        self.data = information
        self.income = (self.data['total_income'])
        self.daily_exp_list = {}

    def count_days(self):
        days_between = datetime.datetime.strptime(self.data['start_date'], '%Y-%m-%d') - \
                       datetime.datetime.strptime(self.data['next_income_date'], '%Y-%m-%d')
        days_between_int = int(str(abs(days_between)).split()[0])
        return days_between_int + 1

    def reset(self):
        quest = input('Вы уверены, что хотите очистить библиотеку?: ')
        quest_error_msg = 'Ошибка. Неверный формат данных'
        quest_reset_obj = InputDevise(quest, quest_error_msg)
        answer = quest_reset_obj.in_agreement()
        if answer == 'yes':
            self.data = "empty"
            with open('data.json', 'w', encoding='utf-8') as reset_file:
                json.dump(self.data, reset_file, indent=4)
            print('Библиотека трат очищена')
        else:
            pass
        quest_continue = input('Хотите ли вы ввести данные?: ')
        quest_continue_error_msg = 'Ошибка. Неверный формат данных'
        quest_continue_obj = InputDevise(quest_continue, quest_continue_error_msg)
        answer_continue = quest_continue_obj.in_agreement()
        if answer_continue == 'yes':
            initialization()
        else:
            return False

    def show(self, current_date):
        expenses.count_daily_exp()
        print(f"Текущая дата: {current_date}")
        print(f"Дата следующего поступления денег: {self.data['next_income_date']}")
        if len(self.data['constant_spending']['spending']) == 0:
            print('Постоянных расходов нет.')
        else:
            print('Список расходов: ')
            for spend in self.data['constant_spending']['spending']:
                print(f"{spend['category']} {spend['spend_of_money']}")
            print(f"ИТОГО: {self.count_total_sum()}")
        days = self.count_days()
        date = str(current_date.date())
        print(f"Остаток на {days} дней: {self.data['total_income'] - self.count_total_sum()}")
        print(f"Можно тратить в день {round(self.data['daily_exp']['total_daily_exp'], 2)} рублей")
        balance = self.data['daily_exp']['daily_exp_list'][date]['in_balance']
        exp = self.data['daily_exp']['daily_exp_list'][date]['exp_sum']
        today_limit = balance - exp
        print(f"СЕГОДНЯ можно тратить {round(today_limit, 2)} рублей")

    def add_exp(self):
        category = input('Введите категорию: ')
        if category == 'exit':
            return 'exit'
        spend_of_money = input('Введите сумму: ')
        coast_error_msg = 'Ошибка: Неверный формат данных.'
        exp = InputDevise(spend_of_money, coast_error_msg)
        exp_sum = exp.in_float()
        if not exp_sum:
            return False
        spend_inf = {
            'category': category,
            'spend_of_money': exp_sum
        }
        self.data['constant_spending']['spending'].append(spend_inf)
        self.data['total_const_spend'] = self.count_total_sum()
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.data, save_file, indent=4)
        print(f'Трата категории "{category.strip().capitalize()}" на сумму {exp_sum} рублей добавлена.')
        expenses.count_daily_exp()

    def delete(self):
        print('\nКакую трату вы хотите удалить?\n')
        select_spend = {}
        num = 0
        for item in self.data['constant_spending']['spending']:
            num += 1
            select_spend[num] = item
            print(f"{num} - {item['category']} {item['spend_of_money']}")
        print(f"ИТОГО: {self.count_total_sum()}")
        err_msg = 'Ошибка: Неверный формат.'
        select_num = InputDevise(input('Введите номер: '), err_msg)
        select = select_num.in_integer()
        if not select:
            return False
        remove_element = select_spend[select]
        self.data['constant_spending']['spending'].remove(remove_element)
        print('Трата удалена.')
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.data, save_file, indent=4)
        expenses.count_daily_exp()

    def delete_all(self):
        agreement = input('Вы уверены, что хотите удалить все траты? (Y/N)')
        agr_del_class = InputDevise(agreement, "")
        agr = agr_del_class.in_agreement()
        if agr == 'yes':
            self.data['spending'] = []
            with open('data.json', 'w') as data_del:
                json.dump(self.data, data_del, indent=4)
        else:
            pass

    def count_total_sum(self):
        total_sum = 0
        for num in self.data['constant_spending']['spending']:
            total_sum += num['spend_of_money']
        return total_sum

    def count_daily_exp(self):
        balance = self.income - self.count_total_sum()
        days_between_int = self.count_days()
        day_exp = balance / days_between_int
        self.data['daily_exp']['total_daily_exp'] = day_exp
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.data, save_file, indent=4)

    def add_daily_exp(self):
        balance = self.data['daily_exp']['total_daily_exp']
        exp_date = input('Введите дату: ')
        exp_date_error_msg = 'Ошибка: Неверный формат даты.'
        exp_date_obj = InputDevise(exp_date, exp_date_error_msg)
        date = exp_date_obj.in_date()
        exp_sum = input('Введите сумму потраченных денег: ')
        exp_sum_error_msg = 'Ошибка: Неверное значение.'
        exp_sum_obj = InputDevise(exp_sum, exp_sum_error_msg)
        sum_ = exp_sum_obj.in_float()
        self.data['daily_exp']['daily_exp_list'][date] = {
            'in_balance': balance,
            'exp_sum': sum_,
            'out_balance': balance - sum_}
        with open('data.json', 'w', encoding='utf-8') as exp_file:
            json.dump(self.data, exp_file, indent=4)

    def refresh(self):
        balance = self.data['daily_exp']['total_daily_exp']
        for exp in self.data['daily_exp']['daily_exp_list'].values():
            exp['in_balance'] = balance
            balance -= exp['exp_sum']
            balance += self.data['daily_exp']['total_daily_exp']
            exp['out_balance'] = balance

        with open('data.json', 'w', encoding='utf-8') as exp_file:
            json.dump(self.data, exp_file, indent=4)


def menu(command):
    if command == 'add':
        result = expenses.add_exp()
        if not result:
            expenses.add_exp()
        elif result == 'exit':
            return False
    elif command == 'a':
        expenses.add_daily_exp()
        expenses.refresh()
    elif command == 'show':
        expenses.show(TODAY)
    elif command == 'del':
        expenses.delete()
    elif command == 'del_all':
        expenses.delete_all()
    elif command == 'reset':
        expenses.reset()
    elif command == 'refresh':
        expenses.refresh()
    else:
        print('Неизвестная команда.')


def initialization():
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)
        if data == "empty":
            date_zero = input('Введите дату начала отчетного периода ДД ММ ГГГГ: ')
            date_zero_err_msg = 'Ошибка: Неверный формат даты'
            date_zero_obj = InputDevise(date_zero, date_zero_err_msg)
            zero_date = date_zero_obj.in_date()
            date_one = input('Введите дату следующего поступления денег в формате ДД ММ ГГГГ: ')
            date_one_err_msg = 'Ошибка: Неверный формат даты'
            date_one_obj = InputDevise(date_one, date_one_err_msg)
            next_income_date = date_one_obj.in_date()

            data = {
                "total_income": 0,
                "start_date": zero_date,
                "next_income_date": next_income_date,
                "constant_spending": {
                    "spending": [],
                    "total_const_spend": 0
                },
                "daily_exp": {
                    "total_daily_exp": 0,
                    "daily_exp_list": {}
                }
            }

            def count_days(inf):
                days_between = datetime.datetime.strptime(inf['start_date'], '%Y-%m-%d') - \
                               datetime.datetime.strptime(inf['next_income_date'], '%Y-%m-%d')
                days_between_int = int(str(abs(days_between)).split()[0])
                return days_between_int + 1

            date_list = [f"{data['start_date'][0:7]}-{int(data['start_date'][8:]) + i}" for i in range(count_days(data)
                                                                                                       + 1)]
            date_list_format = []
            for i in date_list:
                if len(i) == 9:
                    i = f"{i[0:8]}{0}{i[8]}"
                    date_list_format.append(i)
                else:
                    date_list_format.append(i)
            date_dict = {x: {'in_balance': 0, 'exp_sum': 0, 'out_balance': 0} for x in date_list_format}
            data['daily_exp']['daily_exp_list'] = date_dict
        else:
            pass
        if data['total_income'] == 0:
            in_total_income = input('Введите планируемый доход: ')
            in_total_income_err_msg = 'Ошибка: Неверный формат.'
            in_total_income_obj = InputDevise(in_total_income, in_total_income_err_msg)
            total_income = in_total_income_obj.in_float()
            data['total_income'] = total_income
        else:
            pass

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    return data


if __name__ == "__main__":
    while True:
        init_info = initialization()
        expenses = Expenses(init_info)
        mes = input('Введите команду: ')
        if mes == 'exit':
            print('Работа завершена.')
            break
        menu(mes)
        expenses.refresh()
