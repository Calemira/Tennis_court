from datetime import datetime, timedelta
import json


class Menu:

    def display_menu(self):
        print('Welcome to your favourite tennis court site')
        print('What would you like to do today?')
        print('1. Make a reservation')
        print('2. Cancel a reservation')
        print('3. Print schedule')
        print('4. Save your schedule')
        print('5. Exit')

    def match_answer(self, answer):
        reservation = Reservations()
        match answer:
            case 1:
                reservation.making_reservation()
            case 2:
                reservation.cancel_reservation()
            case 3:
                reservation.print_schedule()
            case 4:
                reservation.save_to_file()
            case 5:
                exit


class Reservations:
    now = datetime.now()
    list_of_reservations = []
    menu = Menu()

    def making_reservation(self):
        i = 0
        while i == 0:
            full_name = input('What is your full name\n')
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
            is_available = self.check_if_available(date, duration)
            if is_available:
                self.stored_reservations(full_name, date, duration)
                answer_1 = int(input('Reservation completed. What would you like to do now?\n1.Make another reservation\n2.Go to the main menu\n3.Exit'))
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

    def stored_reservations(self, full_name, date, duration):
        date = date.strftime('%d.%m.%Y %H:%M')
        reservations = {'full name': full_name, 'date': date, 'duration': duration}
        Reservations.list_of_reservations.append(reservations)

    def print_schedule(self):
        for i in Reservations.list_of_reservations:
            print(i)

    def check_if_possible(self, ext_day):
        while True:
            if Reservations.now + timedelta(hours=2) <= ext_day:
                return True
            else:
                return False

    def check_if_available(self, starting_time, duration):
        if len(Reservations.list_of_reservations) == 0:
            return True
        else:
            ending_time = starting_time + timedelta(minutes=int(duration))
            for i in Reservations.list_of_reservations:
                i_start = datetime.strptime(i['date'], '%d.%m.%Y %H:%M')
                i_end = i_start + timedelta(minutes=i['duration'])
                if i_end > starting_time and ending_time > i_start:
                    return False
                else:
                    return True

    def cancel_reservation(self):
        is_reserved = False
        is_name_found = False
        full_name = input('Please provide the name that you have made the reservation with\n')
        for i in Reservations.list_of_reservations:
            if i.get('full name') == full_name:
                is_name_found = True
                date = input('Please provide the date with and hour that you have booked {DD.MM.YYY HH:MM}\n')
                if i.get('date') == date:
                    if i.get('date') - datetime.timedelta(hours=1) >= Reservations.now:
                        # needs checking
                        Reservations.list_of_reservations.remove(i)
                        is_reserved = True
                        print('We succesfully cancelled your reservation')
                        self.open_menu()
                        return
                else:
                    print('You have no reservation in that time\n')
                    return
        if not is_name_found:
            print('No reservation was found under this name\n')
            return

    def save_to_file(self):
        start_date = input('Please enter the start date')
        end_date = input('Please enter the end date')
        while True:
            ans = int(input('How would you like to save? 1. Json 2. CVS'))
            if ans == 1:
                with open("reservations_file.json", "w") as f:
                    json.dump(Reservations.list_of_reservations, f)
                return
            elif ans == 2:
                pass
            else:
                print('Please choose one of two options')
                continue

    def open_menu(self):
        menu.display_menu()
        answer = int(input())
        menu.match_answer(answer)

menu = Menu()
menu.display_menu()
answer = int(input())
menu.match_answer(answer)
# plan for tomorrow:
# make it so that when user want to print schedule it asks for start date and end date
# then depending on if he wanted to just print it or save it we have 2 options following
# saving to json and cvs file
# printing in right format
