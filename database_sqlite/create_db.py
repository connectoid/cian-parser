import sqlite3


def main():
    connection = sqlite3.connect('realty.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE offers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_id INTEGER,
            title TEXT,
            url TEXT,
            date TEXT,
            description TEXT,
            address TEXT,
            phone TEXT,
            price INTEGER,
            area INTEGER,
            rooms_count INTEGER,
            floor INTEGER,
            fllor_count INTEGER,
            photo_mini TEXT,
            photos TEXT
        )
    """)
    connection.close()


if __name__ == '__main__':
    main()