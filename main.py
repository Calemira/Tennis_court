from datetime import datetime, timedelta
import json
import csv


class Menu:
    def __init__(self):
        self.reservation = Reservations(self)

    def display_menu(self):
        print('Welcome to your favourite tennis court site')
        print('What would you like to do today?')
        print('1. Make a reservation')
        print('2. Cancel a reservation')
        print('3. Print schedule')
        print('4. Save your schedule')
        print('5. Exit')

    def match_answer(self):
        while True:
            answer = input()
            match answer:
                case '1':
                    self.reservation.making_reservation()
                case '2':
                    self.reservation.cancel_reservation()
                case '3':
                    self.reservation.print_schedule()
                case '4':
                    self.reservation.save_to_file()
                case '5':
                    exit()
                case _:
                    print('Choose one of the options above')
                    continue
            break


class Reservations:
    def __init__(self, menu):
        self.now = datetime.now()
        self.list_of_reservations = []
        self.menu = menu

    def making_reservation(self):
        i = 0
        j = 0
        while i == 0:
            while True:
                full_name = input("What's your name?\n")
                if ' ' in full_name:
                    break
                else:
                    print('Please provide your full name (name and surname)\n')
            if not self.check_if_can(full_name):
                self.open_menu()
            while True:
                date = input('When would you like to make a reservation for the court? {DD.MM.YYY HH:MM}\n')
                date_format = '%d.%m.%Y %H:%M'
                try:
                    start_time = datetime.strptime(date, date_format)
                    if self.check_if_possible(start_time):
                        break
                    else:
                        print('The date that you have chosen is either in the past or in less than two hours.')
                except (ValueError, TypeError):
                    print('Please provide the date in given format\n')
            while True:
                duration = input('How long would you like to book?\na) 30 minutes\nb) 60 minutes\nc) 90 minutes\n')
                match duration:
                    case 'a':
                        duration = 30
                    case 'b':
                        duration = 60
                    case 'c':
                        duration = 90
                    case _:
                        print('Please choose one of given options\n')
                        continue
                break
            end_time = start_time + timedelta(minutes=duration)
            is_available, new_starting_time = self.check_if_available(date, end_time)
            end_time = datetime.strftime(end_time, '%d.%m.%Y %H:%M')
            if is_available:
                self.stored_reservations(full_name, start_time, end_time)
                self.answer()
            elif not is_available:
                print('The date you choose is already taken. The closest one to the one you choose is',
                      new_starting_time)
                while j == 0:
                    ans = int(
                        input('Is that time ok or do you want to choose a different one?\n 1) its ok\n 1) its not\n'))
                    if ans == 1:
                        new_ending_time = new_starting_time + timedelta(minutes=duration)
                        self.stored_reservations(full_name, new_starting_time, new_ending_time)
                        self.answer()
                    elif ans == 2:
                        j = 1
                        continue
                    else:
                        print('Please choose either 1 or 2')

    def stored_reservations(self, full_name, start_time, end_time):
        start_time = start_time.strftime('%d.%m.%Y %H:%M')
        reservations = {'full name': full_name, 'start_time': start_time, 'end_time': end_time}
        self.list_of_reservations.append(reservations)

    def get_start_time(self, my_list):
        return my_list['start_time']

    def sorting(self, my_list):
        sorted_reservations = sorted(my_list, key=self.get_start_time)
        return sorted_reservations

    def check_if_can(self, full_name):
        num = 0
        for i in self.list_of_reservations:
            if i.get('full name') == full_name:
                num += 1
                if num >= 2:
                    print('You already have 2 or more reservations')
                    return False
        return True

    def start_end_date(self):
        my_list = []
        while True:
            start_date = input('Please enter starting date {dd.mm.YY}\n')
            end_date = input('Please enter ending date {dd.mm.YY}\n')
            date_format = '%d.%m.%Y'
            try:
                start_date_output = start_date
                end_date_output = end_date
                start_date = self.change_to_date(start_date, date_format)
                end_date = self.change_to_date(end_date, date_format)
                delta = timedelta(days=1)
                while start_date <= end_date:
                    for i in self.list_of_reservations:
                        date_format = '%d.%m.%Y'
                        data = i.get('start_time')[:-6]
                        data = self.change_to_date(data, date_format)
                        if start_date == data:
                            my_list.append(i)
                    start_date += delta
                my_list = self.sorting(my_list)
                print('\n')
                return my_list, start_date_output, end_date_output
            except (ValueError, TypeError):
                print('Please provide date in given format')

    def print_schedule(self):
        my_list, start_date, end_date = self.start_end_date()
        date_format = '%d.%m.%Y'
        start_date_i = self.change_to_date(start_date, date_format)
        end_date_i = self.change_to_date(end_date, date_format)
        delta = timedelta(days=1)
        while start_date_i <= end_date_i:
            day_of_week = start_date_i.strftime('%A')
            print(day_of_week, ':')
            found_reservation = False
            for reservation in my_list:
                date = self.date_without_hours(reservation.get('start_time'), 6)
                if date == start_date_i:
                    found_reservation = True
                    print('Name:', reservation.get('full name'), reservation.get('start_time'),
                          '-', reservation.get('end_time'))
            if not found_reservation:
                print('No Reservations')
            start_date_i += delta

    def check_if_possible(self, ext_day):
        while True:
            if self.now + timedelta(hours=2) <= ext_day:
                return True
            else:
                return False

    def date_without_hours(self, date, number):
        date_format = '%d.%m.%Y'
        data = date[:-number]
        data = datetime.strptime(data, date_format).date()
        return data

    def change_to_date(self, string, format):
        date = datetime.strptime(string, format).date()
        return date

    def change_to_string(self, date, format):
        time = date.strftime(format)
        return time

    def check_if_available(self, starting_time, ending_time):
        if len(self.list_of_reservations) == 0:
            return True, None
        else:
            for i in self.list_of_reservations:
                starting_time = datetime.strptime(starting_time, '%d.%m.%Y %H:%M')
                i_start = datetime.strptime(i['start_time'], '%d.%m.%Y %H:%M')
                i_end = datetime.strptime(i['end_time'], '%d.%m.%Y %H:%M')
                if i_end > starting_time and ending_time > i_start:
                    return False, i_end
                else:
                    return True, None

    def cancel_reservation(self):
        is_name_found = False
        full_name = input('Please provide the name that you have made the reservation with\n')
        for i in self.list_of_reservations:
            if i.get('full name') == full_name:
                is_name_found = True
                date = input('Please provide the date with and hour that you have booked {DD.MM.YYY HH:MM}\n')
                date = datetime.strptime(date, '%d.%m.%Y %H:%M')
                act_date = datetime.strptime(i.get('start_time'), '%d.%m.%Y %H:%M')
                if act_date == date:
                    if act_date - timedelta(hours=1) >= self.now:
                        self.list_of_reservations.remove(i)
                        print('We successfully cancelled your reservation\n')
                        self.open_menu()
                        return
                    else:
                        print("You cannot cancel a reservation that is in less than 1 hour\n")
                        self.open_menu()
                else:
                    print('You have no reservation in that time\n')
                    self.open_menu()
        if not is_name_found:
            print('No reservation was found under this name\n')
            self.answer()
            return

    def answer(self):
        k = 0
        while k == 0:
            print('Action completed. What would you like to do now?\n1.Make another reservation'
                  '\n2.Go to the main menu\n3.Exit\n', flush=True)
            answer_1 = input()
            if answer_1 == '1':
                k = 1
                break
            if answer_1 == '2':
                i = 1
                self.open_menu()
            if answer_1 == '3':
                i = 1
                exit()
            else:
                print('Choose one of given answers')
                continue

    def save_to_file(self):
        my_list, start_date, end_date = self.start_end_date()
        while True:
            ans = int(input('How would you like to save? 1. Json 2. CVS\n'))
            if ans == 1:
                json_file = json.dumps(my_list, separators=(',', ':'))
                with open("reservations_file.json", "w") as f:
                    f.write(json_file)
                self.answer()
                return
            elif ans == 2:
                with open('reservations_file.csv', 'w', newline='') as f:
                    fieldnames = list(self.list_of_reservations[0].keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in self.list_of_reservations:
                        writer.writerow(row)
                self.answer()
                return
            else:
                print('Please choose one of two options')
                continue

    def open_menu(self):
        self.menu.display_menu()
        self.menu.match_answer()


menu1 = Menu()
menu1.display_menu()
menu1.match_answer()
