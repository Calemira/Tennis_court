from datetime import datetime, timedelta
import json


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
        print('5. Exit\n')

    def match_answer(self, answer):
        while True:
            match answer:
                case 1:
                    self.reservation.making_reservation()
                case 2:
                    self.reservation.cancel_reservation()
                case 3:
                    self.reservation.start_end_date()
                case 4:
                    self.reservation.save_to_file()
                case 5:
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
        while i == 0:
            full_name = input('What is your full name\n')
            if not self.check_if_can(full_name):
                self.open_menu()
            while True:
                date = input('When would you like to make a reservation {DD.MM.YYY HH:MM}\n')
                date_format = '%d.%m.%Y %H:%M'
                try:
                    date = datetime.strptime(date, date_format)
                    if self.check_if_possible(date):
                        break
                    else:
                        print('The date you have choosen is either in the past or in less than two hours.')
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
            end_date = date + timedelta(minutes=duration)
            is_available = self.check_if_available(date, end_date)
            end_date = datetime.strftime(end_date, '%d.%m.%Y %H:%M')
            if is_available:
                self.stored_reservations(full_name, date, end_date)
                answer_1 = int(input('Reservation completed. What would you like to do now?\n1.Make another reservation\n2.Go to the main menu\n3.Exit\n'))
                if answer_1 == 1:
                    pass
                if answer_1 == 2:
                    i = 1
                    self.open_menu()
                if answer_1 == 3:
                    i = 1
                    exit()
            elif not is_available:
                print('The date you choose is already taken.')
                i = 1

    def stored_reservations(self, full_name, date, end_date):
        date = date.strftime('%d.%m.%Y %H:%M')
        reservations = {'full name': full_name, 'date': date, 'end_date': end_date}
        self.list_of_reservations.append(reservations)

    def check_if_can(self, full_name):
        num = 0
        for i in self.list_of_reservations:
            if i.get('full name') == full_name:
                num += 1
                if num >= 2:
                    print('You already have 2 or more reservations')
                    return False
        return True

    def print_schedule(self):
        my_list = self.start_end_date()
        print(my_list)

    def check_if_possible(self, ext_day):
        while True:
            if self.now + timedelta(hours=2) <= ext_day:
                return True
            else:
                return False

    def check_if_available(self, starting_time, ending_time):
        if len(self.list_of_reservations) == 0:
            return True
        else:
            for i in self.list_of_reservations:
                i_start = datetime.strptime(i['date'], '%d.%m.%Y %H:%M')
                i_end = datetime.strptime(i['end_date'], '%d.%m.%Y %H:%M')
                if i_end > starting_time and ending_time > i_start:
                    return False
                else:
                    return True

    def cancel_reservation(self):
        is_name_found = False
        full_name = input('Please provide the name that you have made the reservation with\n')
        for i in self.list_of_reservations:
            if i.get('full name') == full_name:
                is_name_found = True
                date = input('Please provide the date with and hour that you have booked {DD.MM.YYY HH:MM}\n')
                date = datetime.strptime(date, '%d.%m.%Y %H:%M')
                act_date = datetime.strptime(i.get('date'), '%d.%m.%Y %H:%M')
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
            return

    def start_end_date(self):
        my_list = []
        start_date = input('Please enter starting date {dd.mm.YY}')
        end_date = input('Please enter ending date {dd.mm.YY}')
        date_format = '%d.%m.%Y'
        start_date = datetime.strptime(start_date, date_format).date()
        end_date = datetime.strptime(end_date, date_format).date()
        delta = timedelta(days=1)
        while start_date <= end_date:
            for i in self.list_of_reservations:
                date_format = '%d.%m.%Y'
                data = i.get('date')[:-6]
                data = datetime.strptime(data, date_format)
                data = data.date()
                if start_date == data:
                    my_list.append(i)
            start_date += delta
        return my_list

    def save_to_file(self):
        my_list = self.start_end_date()
        while True:
            ans = int(input('How would you like to save? 1. Json 2. CVS\n'))
            if ans == 1:
                json_file = json.dumps(my_list, separators=(',', ':'))
                with open("reservations_file.json", "w") as f:
                    f.write(json_file)
                return
            elif ans == 2:
                pass
            else:
                print('Please choose one of two options')
                continue

    def open_menu(self):
        self.menu.display_menu()
        answer = int(input())
        self.menu.match_answer(answer)

menu1 = Menu()
menu1.display_menu()
answer1 = int(input())
menu1.match_answer(answer1)
