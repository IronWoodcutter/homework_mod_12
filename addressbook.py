'''
У цьому домашньому завданні ми:

Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне.
Додамо функціонал роботи з Birthday у клас Record, а саме функцію days_to_birthday, 
яка повертає кількість днів до наступного дня народження.
Додамо функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
Додамо пагінацію (посторінковий висновок) для AddressBook для ситуацій, 
коли книга дуже велика і треба показати вміст частинами, а не все одразу. 
Реалізуємо це через створення ітератора за записами.
'''

from collections import UserDict
from datetime import datetime, timedelta
import re


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return self.iterator()

    def iterator(self, number_records=None):
        keys = list(self.data.keys())
        current_index = 0

        while current_index < len(keys):
            list_to_show = keys[current_index: current_index + number_records]
            yield [(self.data[key]) for key in list_to_show]
            current_index += number_records


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return 'New phone number added successfully'

    def del_phone(self, phone):
        self.phones.remove(Phone(phone))
        return 'Phone number deleted successfully'

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return 'Phone number changed successfully'
        return 'Phone number not found'

    def days_to_birthday(self):
        if self.birthday:
            current_datetime = datetime.now()
            birthday_in_this_year = datetime(year=datetime.now().year, month=self.birthday.value.month, day=self.birthday.value.day)                      
            if birthday_in_this_year >= current_datetime:
                days_left = birthday_in_this_year - current_datetime
                return f"{self.name}'s birthday {days_left.days} days away"
            else:
                birthday_in_next_year = birthday_in_this_year + \
                    timedelta(year=1)
                days_left = birthday_in_next_year - current_datetime
                return f"{self.name}'s birthday {days_left.days} days away"

    def __repr__(self):
        if isinstance(self.birthday, Birthday):
            return f'{self.name}, phones: {self.phones}, birthday: {self.birthday}'
        else:
            return f'{self.name}, phones: {self.phones}'
        



class Field:
    def __init__(self, value):
        self.__value = None  # спочатку це поле None, його заповнимо в сеттері
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __repr__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):

    # звертаємось до батьковського сеттера і перевизначаємо його в цьому классі
    @Field.value.setter
    def value(self, value):
        valid_value = self.validate_phone_number(value)
        if valid_value:
            self._Field__value = valid_value

    def validate_phone_number(self, phone):
        addon = {9: '+380', 10: '+38', 11: '+3', 12: '+'}
        sanitize_number = re.sub('["(",")","\-", "+", " "]', '', phone)

        if sanitize_number.isdigit():
            digit_count = len(sanitize_number)
            if digit_count >= 9 and digit_count <= 12:
                valid_value = addon.get(digit_count) + sanitize_number
                return valid_value
            else:
                raise ValueError('Wrong number of digits')
        else:
            raise ValueError('Phone number must be numeric!')


class Birthday(Field):
    # 25-07-2023
    @Field.value.setter
    def value(self, value):
        valid_value = self.validate_birthday(value)
        if valid_value:
            self._Field__value = valid_value

    def validate_birthday(self, birthday):
        current_date = datetime.now()
        try:
            birthday = datetime.strptime(birthday, "%d-%m-%Y")
            if birthday > current_date:
                raise ValueError("Date of birth cannot be greater than the current date")
            return birthday       
        except ValueError: 'Wrong date'


    def __repr__(self):
        if self._Field__value:
            return datetime.strftime(self._Field__value, "%d.%m.%Y")


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    birthday = Birthday('25-07-2023')
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)

    name1 = Name('Gorg')
    phone1 = Phone('5864259781')
    birthday1 = Birthday('10-10-2015')
    rec1 = Record(name1, phone1, birthday1)
    ab.add_record(rec1)

    rec2 = Record(Name('Olga'), Phone('026856241'))
    ab.add_record(rec2)

    rec3 = Record(Name('Semen'), Phone('586640298'))
    ab.add_record(rec3)

    name4 = Name('Mykola')
    phone4 = Phone('386425987')
    birthday4 = Birthday('10-11-1901')
    rec4 = Record(name4, phone4, birthday4)
    ab.add_record(rec4)

    print(ab['Bill'].phones[0].value)
    print(next(ab.iterator(5)))
    print(rec1.add_phone('356640298'))
    print(next(ab.iterator(2)))
    print(rec1.change_phone('+385864259781', '0265840278'))
    print(next(ab.iterator(8)))
    print(rec1.days_to_birthday())
