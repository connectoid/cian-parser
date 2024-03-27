from services.parsing import get_offers
from database.orm import check_database

def main():
    flats_count, offers_json = get_offers(
        city='Kostroma',
        beds_count=3,
        rooms_count=1,
        date_gte='01.06.2024',
        date_lt='08.06.2024',
        pages=1)
    print(f'По запросу найдено {flats_count} квартир')

    for item in offers_json:
        check_database(item)



if __name__ == '__main__':
    main()