import os
import pickle
import re
from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, data):
        self.data = data
        self.__data = None

    def __str__(self):
        return str(self.data)


class Name(Field):
    pass


class Birthday(Field):
    def __str__(self):
        return datetime.strftime(self.data, "%d/%m/%Y")

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = datetime.strptime(data, "%d/%m/%Y")


class Phone(Field):
    def __str__(self):
        return str(self.__data)


    def __repr__(self):
        return f"{self.data}"
    @property
    def data(self):
        return str(self.__data)

    @data.setter
    def data(self, data):
        pattern = re.compile("^\+[0-9]{3}\([0-9]{2}\)[0-9]{3}-[0-9]-[0-9]{3}$", re.IGNORECASE)
        if not pattern.match(data):
            raise ValueError
        self.__data = data


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phone = []
        self.birthday = birthday
        if phone:
            self.phone.append(phone)

    def days_to_birthday(self):
        check = self.birthday.data.replace(year=datetime.now().year)
        check1 = check - datetime.now()
        if check1.days < 0:
            check = check.replace(year=datetime.now().year + 1)
        return check - datetime.now()

    def add_value(self, phone: Phone):
        self.phone.append(phone)
        return "was add"

    def delite(self, delete: Phone):
        for i in self.phone:
            print(i)
            print(delete)
            if str(i) == delete:
                self.phone.remove(i)
                return f" was deleete from adressbook"
        return f"number not in adres"

    def update(self, changewhat: Phone, changeto: Phone):
        for i in range(len(self.phone)):
            if self.phone[i].data == changewhat:
                self.phone[i].data = changeto
                return f"{changewhat} data was change to {changeto}"
        return f"{changewhat} data was not change to {changeto}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.data] = record
        return f"enter next command"

    def find_value(self, what_to_find):
        for j in self.values():
            if str(j.name).find(what_to_find) > -1:
                print(f"{j.name}|{j.phone}|{j.birthday}")
            for i in j.phone:
                if str(i).find(what_to_find) >-1:
                    print(f"{j.name}|{j.phone}|{j.birthday}")
        return "enter next command"

    def paginator(self, page=2):
        start = 0
        iter_obj2 = []
        for j in self.values():
            i = [m.data for m in j.phone]
            iter_obj2.append(f"{j.name} {i} {j.birthday}")
        while True:
            result = iter_obj2[start:start + page]
            if not result:
                break
            yield result
            start += page



with open("data.bin", "a") as fh:
    pass

if not os.stat("data.bin").st_size == 0:
    with open("data.bin", "rb") as fh:
        ad = pickle.load(fh)
else:
    ad = AddressBook()
def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (IndexError, ValueError, KeyError):
            return "wrong data. for help input 'help'"
        except AttributeError:
            return "you dont have such name in dict"

    return inner


@input_error
def days_to_birth(*args):
    data = args[0].split()
    r = ad.get(data[0])
    return r.days_to_birthday()


def to_exit(args):
    if not args:
        return "bye"
    else:
        return "you entered an additional data. Maybe you wanted to enter a different command ?"


def to_help(*args):
    return "phone name number birthday- to add number\nchange name number number - to change number" \
           "\ndell name number - to delete number \nadd name number -to add number to name" \
           "\nnext birth name\nfind data - to search data \nshow all - to see dict" \
           "\nexit - to exit\nformats is dd/mm/yyyy and +***(**)***-*-***"


@input_error
def change(*args):
    data = args[0].split()
    r = ad.get(data[0])
    return r.update(data[1], data[2])


@input_error
def phone(*args):
    data = args[0].split()
    if len(data) == 3:
        r = Record(Name(data[0]), Phone(data[1]), Birthday(data[2]))
    elif len(data) == 2:
        r = Record(Name(data[0]), Phone(data[1]))
    else:
        r = Record(Name(data[0]))
    return ad.add_record(r)


def show_all(*args):
    data = args[0].split()
    if data:
        gen_obj = ad.paginator(int(data[0]))
    else:
        gen_obj = ad.paginator()
    for i in gen_obj:
        print(i)
        input("press any key")
    return "enter next command"


def hello(*args):
    return "How can I help you?"


@input_error
def dell(*args):
    data = args[0].split()
    r = ad.get(data[0])
    return r.delite(data[1])


@input_error
def add(*args):
    data = args[0].split()
    r = ad.get(data[0])
    return r.add_value(Phone(data[1]))


def find_v(*args):
    data = args[0].split()
    return ad.find_value(data[0])


def undefinde_command(*args):
    return "I don`t know this command"


COMANDS = {to_exit: (" exit ", " close ", " good bye "),
           to_help: (" help ",),
           change: (" change ",),
           show_all: (" show all ",),
           phone: (" phone ",),
           hello: (" hello ",),
           dell: (" dell ",),
           add: (" add ",),
           days_to_birth: (" next birth ",),
           find_v: (" find ",)}


def normilize(data: str):
    data = " " + data.strip() + " "
    for key, value in COMANDS.items():
        for i in value:
            if data.find(i, 0, 12) > -1:
                return key, data.replace(str(i), '').strip()
    return undefinde_command, None


def dumpp_dict(ad: AddressBook, file_name):
    with open(file_name, "wb") as fh:
        pickle.dump(ad, fh)


def load_dict(file_name):
    if not os.stat(file_name).st_size == 0:
        with open(file_name, "rb") as fh:
            return pickle.load(fh)
    else:
        return AddressBook()


def main():
    while True:
        user_input = input(">>>")
        command, data = normilize(user_input)
        print(command(data))
        if command == to_exit and not data:
            break
    dumpp_dict(ad, "data.bin")


if __name__ == "__main__":
    main()
