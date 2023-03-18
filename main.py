from datetime import date
from datetime import datetime
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
    now_with_sec = datetime.now()
    now = now_with_sec.strftime('%d.%m.%Y %H:%M')
    list_of_reservations = []


    def making_reservation(self):
        i = 0
        while i == 0:
            full_name = input('What is your full name\n')
            date = input('When would you like to make a reservation {DD.MM.YYY HH:MM}\n')
            date_format = '%d.%m.%Y %H:%M'
            date = datetime.strptime(date, date_format)
            is_it = self.check_if_available(date)
            if is_it == True:
                duration = input('How long would you like to book?\na) 30 minutes\nb) 60 minutes\nc) 90 minutes')
                match duration:
                    case 'a':
                        duration = 30
                    case 'b':
                        duration = 60
                    case 'c':
                        duration = 90
            elif is_it == False:
                say = input('The time you choose is unavailable. Would you like to choose a different time?')
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
        reservations = {'full name': full_name, 'date': date, 'duration': duration}
        Reservations.list_of_reservations.append(reservations)

    def print_schedule(self):
        print(Reservations.list_of_reservations)

    def check_if_available(self, ext_day):
        # i should check if the date that user is choosing is in over 2hrs
        return True

    def cancel_reservation(self, full_name, date):
        # here i have to search trough my dict to look for persons reservation having provided their
        # name and date and delete it
        # i also have to check if the reservation is in less then an hour or if it even exists,
        # if not cancel the process
        pass

    def save_to_file(self):
        #save dict of reservations to file
        pass


menu = Menu()
menu.display_menu()
answer = int(input())
menu.match_answer(answer)