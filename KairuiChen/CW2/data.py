from animal import Animal
import pandas as pd

_date_format = '%d/%m/%Y'
_name_col = 'name'
_dob_col = 'dob'
_arrival_col = 'arrival'
_species_col = 'species'
_live_with_cats_col = 'live_with_cats'
_live_with_dogs_col = 'live_with_dogs'
_live_with_children_col = 'live_with_children'
_adopted_col = 'adopted'
_cols = [_name_col, _species_col, _dob_col, _arrival_col, _live_with_cats_col, _live_with_dogs_col,
         _live_with_children_col, _adopted_col]

class AnimalData:
    def __init__(self, animals: pd.DataFrame):
        self._animals = animals
        self._displayed_animals = []

    def get_animals_list(self) -> list[Animal]:
        return df_to_animal_list(self._animals)

    def get_longest_resident(self, count=5) -> list[Animal]:
        ordered = self._animals.sort_values(_arrival_col).iloc[0:5]
        return df_to_animal_list(ordered)

    def get_displayed_animal_list(self) -> list[Animal]:
        return self._displayed_animals

    def reset_displayed_animals(self):
        not_adopted_animales = self._animals[self._animals[_adopted_col] == False]
        self._displayed_animals = df_to_animal_list(not_adopted_animales)

    def apply_filter(self, species: list[str], dog_friendly, cat_friendly, child_friendly):
        # create empty filter
        animal_filter = pd.Series([False] * len(self._animals))

        for s in species:
            animal_filter = animal_filter | (self._animals[_species_col] == s)

        if dog_friendly == 1:
            animal_filter = animal_filter & self._animals[_live_with_dogs_col]
        if cat_friendly == 1:
            animal_filter = animal_filter & self._animals[_live_with_cats_col]
        if child_friendly == 1:
            animal_filter = animal_filter & self._animals[_live_with_children_col]

        filtered_animals = self._animals[animal_filter]
        self._displayed_animals = df_to_animal_list(filtered_animals)

    def search_animal_name(self, search_text: str):
        search_filter = self._animals[_name_col].str.contains(search_text)
        self._displayed_animals = df_to_animal_list(self._animals[search_filter])

    def mark_adopted(self, animal: Animal):
        """
        Mark the specified animal as adopted.
        :param animal: The animal to mark as adopted.
        :return:
        """
        animal.adopted = True
        animal_filter = self.find_animal_filter(animal)
        self._animals.loc[animal_filter, _adopted_col] = True

    def save_animals(self, filename):
        self._animals.to_csv(filename, index=False, date_format=_date_format)

    def add_animal(self, animal: Animal):
        #  avoid adding duplicate animals, same name , same date of birth
        duplicate_filter = (self._animals[_name_col] == animal.name) & (self._animals[_dob_col] == animal.dob)
        if duplicate_filter.any():
            raise ValueError(f'Animal with name {animal.name} and date of birth {animal.dob} already exists.')
        new_animal = list_to_df([animal])
        self._animals = pd.concat([self._animals, new_animal], ignore_index=True)

    def delete_animal(self, animal: Animal):
        """
        Delete the specified animal.
        :param animal: The animal to delete
        :return:
        """
        animal_filter = self.find_animal_filter(animal)
        self._animals = self._animals[~animal_filter]

    def find_animal_filter(self, animal: Animal) -> bool:
        """
        Create filter to find unique animal based on name and date of birth.
        Assumption is that combination name and dob uniquely identify an animal
        :param animal: The animal to select
        :return: A filter matching the row for that animal
        """
        return (self._animals[_name_col] == animal.name) & (self._animals[_dob_col] == animal.dob)

def df_to_animal_list(df: pd.DataFrame) -> list[Animal]:
    animals = []
    for i in range(len(df)):
        row = df.iloc[i]
        animals.append(Animal(row[_name_col], row[_species_col], row[_dob_col], row[_arrival_col],
                              row[_live_with_cats_col], row[_live_with_dogs_col], row[_live_with_children_col],
                              row[_adopted_col]))
    return animals

def list_to_df(animals: list[Animal]) -> pd.DataFrame:
    rows = []
    for a in animals:
        rows.append([a.name, a.species, a.dob, a.arrival_date, a.live_with_cats, a.live_with_dogs, a.live_with_children,
                     a.adopted])
    df = pd.DataFrame(rows, columns=_cols)
    return df

def load_animals(filename: str) -> AnimalData:
    """
    Load the list of animals from the specified csv file.
    :param filename: Path to specified csv file
    :return: AnimalData representing the animals in the selected csv file
    """
    df = pd.read_csv(filename, skipinitialspace=True, usecols=_cols)
    df[_dob_col] = pd.to_datetime(df[_dob_col], format=_date_format)
    df[_arrival_col] = pd.to_datetime(df[_arrival_col], format=_date_format)
    return AnimalData(df)
