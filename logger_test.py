from logger import Logger
from person import Person
import os
import pytest

def test_constructor():
    log = Logger('test1.txt')
    assert log.file_name == 'test1.txt'

def test_write_meta_data():
    log = Logger('test2.txt')
    log.write_metadata(100000, 0.90, "Ebola", 0.70, 0.25)

    #Read test file
    with open('test2.txt', 'r') as f:
        test_data = f.read()

    assert test_data == f"100000\t0.9\tEbola\t0.7\t0.25\n"

    os.remove('test2.txt')


def test_log_interaction():
    log = Logger('test3.txt')

    person = Person(1, True)
    random_person = Person(2, False)
    #Person not sick and not vaccinated but infected
    log.log_interaction(person, random_person, random_person_sick=False, random_person_vacc=False, did_infect=True)
    #Person is vaccinated and did infect
    log.log_interaction(person, random_person, random_person_sick=False, random_person_vacc=True, did_infect=True)
    #Person is not vaccinated but is not infected
    log.log_interaction(person, random_person, random_person_sick=False, random_person_vacc=False, did_infect=False)
    #Person is sick and did get infected
    log.log_interaction(person, random_person, random_person_sick=True, random_person_vacc=False, did_infect=True)

    with open('test3.txt', 'r') as f:
        test_data = f.read()

    assert test_data == ("1 infects 2 \n" +
                        "1 didn't infect 2 because already vaccinated \n" +
                        "1 didn't infect 2 \n" +
                        "1 didn't infect 2 because already sick \n")

    os.remove('test3.txt')

def test_log_infection_survival():
    log = Logger('test4.txt')
    person = Person(1, True)
    person2 = Person(2, False)

    log.log_infection_survival(person, True)
    log.log_infection_survival(person, False)
    log.log_infection_survival(person2, True)
    log.log_infection_survival(person2, False)

    with open('test4.txt', 'r') as f:
        test_data = f.read()
    
    assert test_data == ("1 died from infection\n" +
                        "1 survived infection\n" +
                        "2 died from infection\n" +
                        "2 survived infection\n")

    os.remove('test4.txt')



    