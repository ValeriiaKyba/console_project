import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE photos
                       (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title text,
                        field_id char(23),
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
                            val integer,
                            frequency integer
                           )
                       """)
    conn.commit()
