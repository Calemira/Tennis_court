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
                print('Cancel')
            case 3:
                reservation.print_schedule()
            case 4:
                print('Saving')
            case 5:
                exit


class Reservations:

    now = datetime.now()
    list_of_reservations = []

    def making_reservation(self):
        i = 0
        while i == 0:
            full_name = input('What is your full name\n')
            date = input('When would you like to make a reservation {DD.MM.YYY HH:MM}\n')
            date_format = '%d.%m.%Y %H:%M'
            date = datetime.strptime(date, date_format)
            self.check_if_possible(date)
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
            self.check_if_available(date, duration)
            self.stored_reservations(full_name, date, duration)
            answer_1 = int(input('Reservation completed. What would you like to do now?\n1.Make another reservation\n2.Go to the main menu\n3.Exit'))
            if answer_1 == 1:
                pass
            if answer_1 == 2:
                i = 1
                menu = Menu()
                menu.display_menu()
                answer = int(input())
                menu.match_answer(answer)
            if answer_1 == 3:
                i =1
                exit

    def stored_reservations(self, full_name, date, duration):
        date = date.strftime('%d.%m.%Y %H:%M')
        reservations = {'full name': full_name, 'date': date, 'duration': duration}
        Reservations.list_of_reservations.append(reservations)

    def print_schedule(self):
        for i in Reservations.list_of_reservations:
            print(i)

    def check_if_possible(self, ext_day):
        i = 0
        while i == 0:
            if Reservations.now + timedelta(hours=2) <= ext_day:
                i = 1
                return True
            else:
                print('The time you choose is in the past or is in less than two hours. please choose a different time\n')

    def check_if_available(self, starting_time, duration):
        while True:
            if len(Reservations.list_of_reservations) == 0:
                return True
            else:
                ending_time = starting_time + timedelta(minutes=int(duration))
                for i in Reservations.list_of_reservations:
                    i_start = datetime.strptime(i['date'], '%d.%m.%Y %H:%M')
                    i_end = i_start + timedelta(minutes=i['duration'])
                    if i_end > starting_time and ending_time > i_start:
                        print('The time you have picked is taken. Please choose a different time\n')
                        return False
                return True


    def cancel_reservation(self, full_name, date):
        # here i have to search trough my dict to look for persons reservation having provided their
        # name and date and delete it
        # i also have to check if the reservation is in less then an hour or if it even exists,
        # if not cancel the process
        pass

    def save_to_file(self):
        # save dict of reservations to file
        pass


menu = Menu()
menu.display_menu()
answer = int(input())
menu.match_answer(answer)