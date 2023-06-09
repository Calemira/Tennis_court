from datetime import datetime, timedelta
import json
import csv
import re


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
        self.list_of_reservations = []
        self.menu = menu

    def making_reservation(self):
        i = 0
        j = 0
        while i == 0:
            full_name = self.get_name()
            start_time = self.get_date()
            duration = self.get_duration()
            end_time = start_time + timedelta(minutes=duration)
            # checking if the date user choose is not taken
            is_available, new_starting_time = self.check_if_available(start_time, end_time)
            end_time = datetime.strftime(end_time, '%d.%m.%Y %H:%M')
            if is_available:
                self.stored_reservations(full_name, start_time, end_time)
                self.answer()
            # if the date is taken the user gets a chance to choose the first closest time
            else:
                print('The date you choose is already taken. The closest one to the one you choose is',
                      new_starting_time)
                while j == 0:
                    ans = input('Does this date fit or do you want to pick another one?\n '
                                '1)It fits \n 2)It does not fit\n')
                    if ans == '1':
                        new_ending_time = new_starting_time + timedelta(minutes=duration)
                        self.stored_reservations(full_name, new_starting_time, new_ending_time)
                        self.answer()
                    elif ans == '2':
                        ans_1 = input('What do you want to do next: \n1)Make a reservation for a different time'
                                      '\n2)Exit the page\n')
                        if ans_1 == '1':
                            j = 1
                            continue
                        elif ans_1 == '2':
                            exit()
                        else:
                            print('Please choose either option 1 or 2')
                    else:
                        print('Please choose either option 1 or 2')

    def get_name(self):
        while True:
            # checking if the name is a full name
            full_name = input("What's your name?\n")
            if ' ' in full_name and self.contains_only_letters_and_spaces(full_name):
                break
            print('Please provide your full name (name and surname)\n')
        if not self.check_reservations_number(full_name):
            self.open_menu()
        return full_name

    def contains_only_letters_and_spaces(self, string_input):
        pattern = "^[a-zA-Z ]*$"  # matches only letters and spaces
        return bool(re.match(pattern, string_input))

    def get_date(self):
        while True:
            date = input('When would you like to make a reservation for the court? {DD.MM.YYY HH:MM}\n')
            date_format = '%d.%m.%Y %H:%M'
            # checking if the date is not in the past or in less than 2 hours and if it is given in
            # right format
            try:
                start_time = datetime.strptime(date, date_format)
                if self.check_if_possible(start_time):
                    break
                else:
                    print('The date that you have chosen is either in the past or in less than two hours.')
            except (ValueError, TypeError):
                print('Please provide the date in given format\n')
        return start_time

    def get_duration(self):
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
        return duration

    def stored_reservations(self, full_name, start_time, end_time):
        start_time = start_time.strftime('%d.%m.%Y %H:%M')
        reservations = {'full name': full_name, 'start_time': start_time, 'end_time': end_time}
        self.list_of_reservations.append(reservations)

    def get_start_time(self, my_list):
        return my_list['start_time']

    def sorting(self, my_list):
        # sorting reservations making the earliest first
        sorted_reservations = sorted(my_list, key=self.get_start_time)
        return sorted_reservations

    def check_reservations_number(self, full_name):
        # checking if the person doesn't have
        num = 0
        for i in self.list_of_reservations:
            if i.get('full name') == full_name:
                num += 1
                if num >= 2:
                    print('You already have 2 or more reservations')
                    return False
        return True

    def time_frame(self):
        # sorting trough reservations to pick only those that are in given time frame
        my_list = []

        while True:
            start_date = input('Please enter starting date, from which you want to start the search {dd.mm.YY}\n')
            end_date = input('Please enter ending date, from which you want to end the search  {dd.mm.YY}\n')
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
        date_format = '%d.%m.%Y'
        my_list, start_date, end_date = self.time_frame()
        start_date_i = self.change_to_date(start_date, date_format).date()
        end_date_i = self.change_to_date(end_date, date_format).date()
        delta = timedelta(days=1)

        while start_date_i <= end_date_i:
            day_of_week = start_date_i.strftime('%A')
            print(day_of_week, ':')
            found_reservation = False
            for reservation in my_list:
                date = self.change_to_date(reservation.get('start_time'), date_format).date()
                if date == start_date_i:
                    found_reservation = True
                    print('Name:', reservation.get('full name'), reservation.get('start_time'),
                          '-', reservation.get('end_time'))
            if not found_reservation:
                print('No Reservations')
            start_date_i += delta

    def check_if_possible(self, ext_day):
        # Checking if the time given by user is not in less than 2 hours or in the past
        now = datetime.now()
        if now + timedelta(hours=2) <= ext_day:
            return True
        else:
            return False

    def change_to_date(self, string, date_format):
        date = datetime.strptime(string, date_format)
        return date

    def check_if_available(self, starting_time, ending_time):
        if len(self.list_of_reservations) == 0:
            return True, None
        else:
            date_format = '%d.%m.%Y %H:%M'
            for reservation in self.list_of_reservations:
                i_start = self.change_to_date(reservation['start_time'], date_format)
                i_end = self.change_to_date(reservation['end_time'], date_format)
                if i_end > starting_time and ending_time > i_start:
                    return False, i_end
            return True, None

    def cancel_reservation(self):
        is_name_found = False
        now = datetime.now()
        full_name = input('Please provide the name that you have made the reservation with\n')

        # This method checks if there is a reservation under given name
        # Then it checks if there is a reservation under given time
        for reservation in self.list_of_reservations:
            if reservation.get('full name') == full_name:
                is_name_found = True
                date = input('Please provide the date with and hour that you have booked {DD.MM.YYY HH:MM}\n')
                date = datetime.strptime(date, '%d.%m.%Y %H:%M')
                act_date = datetime.strptime(reservation.get('start_time'), '%d.%m.%Y %H:%M')
                # Checking if the reservation is in over an hour in order to cancell it
                if act_date == date:
                    if act_date - timedelta(hours=1) >= now:
                        self.list_of_reservations.remove(reservation)
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
        while True:
            print("Action completed successfully. What would you like to do now?\n1.Make another reservation"
                  "\n2.Go to the main menu\n3.Exit\n", flush=True)
            answer_1 = input()
            if answer_1 == '1':
                break
            elif answer_1 == '2':
                self.open_menu()
            elif answer_1 == '3':
                exit()
            else:
                print('Choose one of given answers')
                continue

    def save_to_file(self):
        my_list, start_date, end_date = self.time_frame()
        while True:
            ans = input('How would you like to save the schedule? 1. Json 2. CSV\n')
            if ans == '1':
                json_filename = input("Enter the name of the JSON file to create: ")
                if not json_filename.endswith('.json'):
                    json_filename += '.json'
                with open(json_filename, "w") as f:
                    json.dump(my_list, f, indent=2)
                self.answer()
                return
            elif ans == '2':
                csv_filename = input("Enter the name of the CSV file to create: ")
                if not csv_filename.endswith('.csv'):
                    csv_filename += '.csv'
                with open(csv_filename, 'w', newline='') as f:
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


if __name__ == "__main__":
    menu1 = Menu()
    menu1.display_menu()
    menu1.match_answer()
