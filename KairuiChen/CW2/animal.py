SPECIES = ['cat', 'dog']
import datetime

class Animal:
    def __init__(self, name: str, species: str, dob: datetime.datetime, arrival_date: datetime.datetime,
                 live_with_cats: bool, live_with_dogs: bool, live_with_children: bool, adopted: bool):
        self.name = name
        self.species = species
        self.dob = dob
        self.arrival_date = arrival_date
        self.live_with_cats = live_with_cats
        self.live_with_dogs = live_with_dogs
        self.live_with_children = live_with_children
        self.adopted = adopted

    def __str__(self) -> str:
        age_string = self.get_age()
        return f'{self.name}, {self.species}, {age_string}'

    def get_age(self) -> str:
        age = datetime.datetime.today() - self.dob
        years = int(age.days / 365)
        months = int((age.days - years * 365) / 30)
        if years == 0:
            return f'{months} months'
        elif years == 1:
            return f'{years} year, {months} months'
        else:
            return f'{years} years, {months} months'

    def get_adopted(self) -> str:
        if self.adopted:
            return 'yes'
        return 'no'
