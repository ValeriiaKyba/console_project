import datetime
import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()


def create_photo(filename, calc):
    """
    :param filename: ddMMyyyy_(FIELD_ID)_NDVI_P...17_S2B.PNG
    :return:
    """
    date_raw = filename[0:8]
    field_id = filename[10:15]
    date = datetime.datetime.strptime(date_raw, '%d%m%Y').date()
    cursor.execute("INSERT INTO photos(title, field_id, date_of_photo, weighted_average,"
                   " root_mean_square, min_confidence_interval, max_confidence_interval, cloudiness) values (?, ?, ?, ?, ?, ?, ?, ?)",
                   (filename, field_id, date, calc.weighted_average,
                    calc.root_mean_square, calc.min_confidence_interval, calc.max_confidence_interval,
                    calc.cloudiness))
    res = cursor.execute("SELECT last_insert_rowid();")
    conn.commit()
    return res.lastrowid


def create_frequencies(f_id, counter):
    for key, val in counter.items():
        cursor.execute("INSERT INTO frequencies(photo_id, val, frequency) values (?, ?, ?)",
                       (f_id, key, val))
    conn.commit()


def get_fields_list():
    sql = "SELECT distinct field_id FROM photos where cloudiness < 0.5"
    cursor.execute(sql)
    res = cursor.fetchall()
    return [{'name': i[0]} for i in res]


def get_stats_by_field(field_id, period):
    sql = 'select weighted_average, min_confidence_interval,' \
          ' max_confidence_interval, date_of_photo from photos where field_id = ? and cloudiness < 0.5 ' \
          ' order by date_of_photo desc'
    params = [field_id]
    if period != 'all':
        sql = 'select weighted_average, min_confidence_interval,' \
              ' max_confidence_interval, date_of_photo from photos where field_id = ? ' \
              'and date_of_photo > ? and date_of_photo < ? and cloudiness < 0.5 ' \
              'order by date_of_photo desc'
        params = [field_id, period[0], period[1]]
    cursor.execute(sql, params)
    res = cursor.fetchall()
    return res

def get_count_by_cloudiness(field_id):
    sql = "select distinct strftime('%m', q.date_of_photo) as mth, " \
          "(select count(1) from photos as sq1 " \
          "where sq1.cloudiness = 0 and sq1.field_id = q.field_id " \
          "and strftime('%m', sq1.date_of_photo) = strftime('%m', q.date_of_photo)) as cl_0, " \
          '(select count(1) from photos as sq2 ' \
          'where sq2.cloudiness = 1 and sq2.field_id = q.field_id ' \
          "and strftime('%m', sq2.date_of_photo) = strftime('%m', q.date_of_photo)) as cl_1, " \
          '(select count(1) from photos as sq3 ' \
          'where sq3.cloudiness > 0 and sq3.cloudiness < 1 and sq3.field_id = q.field_id ' \
          "and strftime('%m', sq3.date_of_photo) = strftime('%m', q.date_of_photo)) as cl_other " \
          'from photos as q where q.field_id = ?'
    cursor.execute(sql, [field_id])
    res = cursor.fetchall()
    return res

def get_freq(field_id, date):
    sql = "select f.val, sum(f.frequency) " \
          "from frequencies as f join photos as p on f.photo_id = p.id " \
          "where p.field_id = ? and f.val != 0 and f.val != 254 and f.val != 255 and p.date_of_photo = ?" \
          "group by f.val"
    cursor.execute(sql, [field_id, date])
    res = cursor.fetchall()
    return res

