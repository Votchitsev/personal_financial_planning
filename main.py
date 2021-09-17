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
        if self.information == 'exit':
            return self.information
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
    def __init__(self, information, current_date):
        self.data = information
        self.income = (self.data['total_income'])
        self.daily_exp_list = {}
        self.current_date = current_date

    def count_days(self):
        start = datetime.datetime.strptime(self.data['start_date'], '%Y-%m-%d')
        finish = datetime.datetime.strptime(self.data['next_income_date'], '%Y-%m-%d')
        days_between = start - finish
        days_between_int = int(str(days_between).split()[0])
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
            return False
        quest_continue = input('Хотите ли вы ввести данные?: ')
        quest_continue_error_msg = 'Ошибка. Неверный формат данных'
        quest_continue_obj = InputDevise(quest_continue, quest_continue_error_msg)
        answer_continue = quest_continue_obj.in_agreement()
        if answer_continue == 'yes':
            initialization()
            return True
        else:
            return False

    def show(self):
        print(f"Текущая дата: {self.current_date}")
        print(f"Дата следующего поступления денег: {self.data['next_income_date']}")
        if len(self.data['constant_spending']['spending']) == 0:
            print('Постоянных расходов нет.')
        else:
            print('Список расходов: ')
            for spend in self.data['constant_spending']['spending']:
                print(f"{spend['category']} {spend['spend_of_money']}")
            print(f"ИТОГО: {self.count_total_sum()}")
        days = self.count_days()
        date = str(self.current_date.date())
        print(f"Остаток на {days} дней: {self.data['total_income'] - self.count_total_sum()}")
        print(f"Можно тратить в день {round(self.data['daily_exp']['total_daily_exp'], 2)} рублей")
        balance = self.data['daily_exp']['daily_exp_list'][date]['in_balance']
        exp = self.data['daily_exp']['daily_exp_list'][date]['exp_sum']
        today_limit = balance - exp
        print(f"СЕГОДНЯ можно тратить {round(today_limit, 2)} рублей")
        return True

    def add_exp(self, category, spend_of_money):
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
        self.data['constant_spending']['total_const_spend'] = self.count_total_sum()
        with open('data.json', 'w', encoding='utf-8') as save_file:
            json.dump(self.data, save_file, indent=4)
        print(f'Трата категории "{category.strip().capitalize()}" на сумму {exp_sum} рублей добавлена.')
        return True

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
        return True

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
        return True

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
        return True

    def add_daily_exp(self, exp_date, exp_sum):
        balance = self.data['daily_exp']['total_daily_exp']
        exp_date_error_msg = 'Ошибка: Неверный формат даты.'
        exp_date_obj = InputDevise(exp_date, exp_date_error_msg)
        date = exp_date_obj.in_date()
        exp_sum_error_msg = 'Ошибка: Неверное значение.'
        exp_sum_obj = InputDevise(exp_sum, exp_sum_error_msg)
        sum_ = exp_sum_obj.in_float()
        self.data['daily_exp']['daily_exp_list'][date] = {
            'in_balance': balance,
            'exp_sum': sum_,
            'out_balance': balance - sum_}
        with open('data.json', 'w', encoding='utf-8') as exp_file:
            json.dump(self.data, exp_file, indent=4)
        return True

    def del_daily_exp(self, exp_date):
        exp_date_obj_error_msg = 'Ошибка: Неверный формат даты.'
        exp_date_obj = InputDevise(exp_date, exp_date_obj_error_msg)
        date = exp_date_obj.in_date()

        del self.data['daily_exp']['daily_exp_list'][date]
        with open('data.json', 'w', encoding='utf-8') as del_exp_file:
            json.dump(self.data, del_exp_file, indent=4)
        print(f"Расход за {date} удален.")
        return True

    def refresh(self):
        self.count_daily_exp()
        balance = self.data['daily_exp']['total_daily_exp']
        for exp in self.data['daily_exp']['daily_exp_list'].values():
            exp['in_balance'] = balance
            balance -= exp['exp_sum']
            balance += self.data['daily_exp']['total_daily_exp']
            exp['out_balance'] = balance

        with open('data.json', 'w', encoding='utf-8') as exp_file:
            json.dump(self.data, exp_file, indent=4)
        return True

    def show_daily_exp(self):
        daily_exp_list = self.data['daily_exp']['daily_exp_list']
        for exp in daily_exp_list.items():
            if exp[0] != str(self.current_date)[0:10]:
                print(f"{exp[0]} израсходовано {exp[1]['exp_sum']} рублей.")
            else:
                print(f"СЕГОДНЯ израсходовано {exp[1]['exp_sum']} рублей.")
                break
        current_in_balance = daily_exp_list[str(self.current_date)[0:10]]['in_balance']
        current_exp = daily_exp_list[str(self.current_date)[0:10]]['exp_sum']
        allow_sum = round((current_in_balance - current_exp), 2)
        print(f"Можно тратить {allow_sum} рублей")


class Interpreter:
    def __init__(self):
        self.first_value_of_command = {
            'add': expenses.add_exp,    'show': expenses.show,          'exit': exit,
            'del': expenses.delete,     'delete': expenses.delete_all,  'a': expenses.add_daily_exp,
            'reset': expenses.reset,    'd': expenses.del_daily_exp,    's': expenses.show_daily_exp
        }

    def select_command(self):
        expenses.refresh()
        command = list(map(str, input('--> ').split()))
        try:
            if len(command) == 1:
                return self.first_value_of_command[command[0]]()
            elif len(command) == 2:
                val_1 = command[1]
                return self.first_value_of_command[command[0]](val_1)
            elif len(command) == 3:
                val_1 = command[1]
                val_2 = command[2]
                return self.first_value_of_command[command[0]](val_1, val_2)
        except TypeError:
            print('TypeError: Неизвестная команда.')
            return True
        except KeyError:
            print('KeyError: Неизвестная команда.')
            return True


def initialization():
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)
        if data == "empty":
            date_zero = input('Введите дату начала отчетного периода ДД ММ ГГГГ: ')
            date_zero_err_msg = 'Ошибка: Неверный формат даты'
            date_zero_obj = InputDevise(date_zero, date_zero_err_msg)
            zero_date = date_zero_obj.in_date()
            if not zero_date:
                return False
            elif zero_date == 'exit':
                return 'exit'
            date_one = input('Введите дату следующего поступления денег в формате ДД ММ ГГГГ: ')
            date_one_err_msg = 'Ошибка: Неверный формат даты'
            date_one_obj = InputDevise(date_one, date_one_err_msg)
            next_income_date = date_one_obj.in_date()
            if not next_income_date:
                return False

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
                start = datetime.datetime.strptime(inf['next_income_date'], '%Y-%m-%d')
                finish = datetime.datetime.strptime(inf['start_date'], '%Y-%m-%d')
                days_between = start - finish
                days_between_int = int(str(days_between).split()[0])
                if days_between_int <= 0:
                    print('Ошибка. Начальная дата больше конечной.')
                    return False
                else:
                    return days_between_int + 1

            def check_today(current_date, inf):
                if current_date > datetime.datetime.strptime(inf['start_date'], '%Y-%m-%d'):
                    print('Ошибка. Текущая дата больше даты окончания отчетного периода.')
                    return False
                else:
                    return True

            if not count_days(data):
                return False
            elif not check_today(TODAY, data):
                return False
            else:
                date_list = [f"{data['start_date'][0:7]}-{int(data['start_date'][8:]) + i}" for i in
                             range(count_days(data) + 1)]

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
        expenses = Expenses(init_info, TODAY)
        inter = Interpreter()
        sel = inter.select_command()
