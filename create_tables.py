import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE photos
                       (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title text,
                        field_code char(23),
                        revision char(23),
                        satellite char(23),
                        smth char(23),
                        date_of_photo DATE,
                        weighted_average decimal, 
                        root_mean_square decimal, 
                        min_confidence_interval decimal, 
                        max_confidence_interval decimal, 
                        cloudiness decimal
                       )
                   """)

    cursor.execute("""CREATE TABLE frequencies
                           (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            photo_id INTEGER,
                            val char(23),
                            frequency INTEGER
                           )
                       """)
    conn.commit()
