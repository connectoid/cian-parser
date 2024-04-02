import environs

from services.parsing import get_offers
from database.orm import check_database

def parse():
    new_offers = []
    flats_count, offers_json = get_offers(
        city='Kostroma',
        beds_count=3,
        rooms_count=1,
        date_gte='01.06.2024',
        date_lt='08.06.2024',
        pages=1)

    for item in offers_json:
        if check_database(item):
            new_offers.append(item)
    
    return new_offers


if __name__ == '__main__':
    parse()