from datetime import datetime, timedelta


# today = date.today()


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
                print('Saving')
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
            date = input('When would you like to make a reservation {DD.MM.YYY HH:MM}\n')
            date_format = '%d.%m.%Y %H:%M'
            date = datetime.strptime(date, date_format)
            is_possible = self.check_if_possible(date)
            if is_possible:
                duration = input('How long would you like to book?\na) 30 minutes\nb) 60 minutes\nc) 90 minutes\n')
                match duration:
                    case 'a':
                        duration = 30
                    case 'b':
                        duration = 60
                    case 'c':
                        duration = 90
                    case _:
                        print('you chose nothing')
                is_available = self.check_if_available(date, duration)
            elif not is_possible:
                print('The date you have choosen is either in the past or in less than two hours.')
            if is_available:
                self.stored_reservations(full_name, date, duration)
                answer_1 = int(input(
                    'Reservation completed. What would you like to do now?\n1.Make another reservation\n2.Go to the main menu\n3.Exit'))
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
        b = False
        full_name = input('Please provide the name that you have made the reservation with\n')
        for i in Reservations.list_of_reservations:
            if i.get('full name') == full_name:
                date = input('Please provide the date with and hour that you have booked {DD.MM.YYY HH:MM}\n')
                if i.get('date') == date:
                    Reservations.list_of_reservations.remove(i)
                    b = True
                else:
                    print('You have no reservation in that time\n')
            else:
                print('You dont have any reservations under your name\n')
                self.open_menu()
        if b:
            print('We succesfully cancelled your reservation')
            self.open_menu()

    def save_to_file(self):
        # save dict of reservations to file
        pass

    def open_menu(self):
        menu.display_menu()
        answer = int(input())
        menu.match_answer(answer)

menu = Menu()
menu.display_menu()
answer = int(input())
menu.match_answer(answer)
