import sqlite3

def check_database(offer):
    offer_id = offer['offer_id']
    connection = sqlite3.connect('./database/realty.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT offer_id FROM offers WHERE offer_id = (?)
    """, (offer_id, ))
    result = cursor.fetchone()
    if result is None:
        #sent_to_TG(item)
        cursor.execute("""
            INSERT INTO offers
            VALUES (NULL, :offer_id, :title, :url, :added_datetime, :description, :address,
                    :phone, :price, :area, :rooms_count, :floor, :floor_count)
        """, offer)
        connection.commit()
        print(f'Объявление {offer_id} добавлено в БД')

    connection.close()