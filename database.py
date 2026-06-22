import sqlite3

DB_NAME = "team.db"


def create_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        experience INTEGER,

        work_location TEXT,

        district TEXT,

        state TEXT,

        country TEXT,

        latitude REAL,

        longitude REAL

    )
    """)

    conn.commit()
    conn.close()


def add_member(
        name,
        experience,
        work_location,
        district,
        state,
        country,
        latitude,
        longitude):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO members
    (
        name,
        experience,
        work_location,
        district,
        state,
        country,
        latitude,
        longitude
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        name,
        experience,
        work_location,
        district,
        state,
        country,
        latitude,
        longitude
    ))

    conn.commit()
    conn.close()


def get_all_members():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM members
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_member(member_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM members
    WHERE id = ?
    """, (member_id,))

    conn.commit()
    conn.close()


def update_member(
        member_id,
        name,
        experience,
        work_location,
        district,
        state,
        country,
        latitude,
        longitude):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE members
    SET
        name = ?,
        experience = ?,
        work_location = ?,
        district = ?,
        state = ?,
        country = ?,
        latitude = ?,
        longitude = ?
    WHERE id = ?
    """,
    (
        name,
        experience,
        work_location,
        district,
        state,
        country,
        latitude,
        longitude,
        member_id
    ))

    conn.commit()
    conn.close()


create_table()
