import sqlite3


def create_database():
    conn = sqlite3.connect("./database/student.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                        id TEXT PRIMARY KEY CHECK(length(id) = 10),
                        name TEXT NOT NULL,
                        class TEXT NOT NULL)''')

    # Insert data into the table
    cursor.execute("INSERT INTO student (id, name, class) VALUES (?, ?, ?)",
                   ("1120201524", "fys", "07112003"))
    cursor.execute("INSERT INTO student (id, name, class) VALUES (?, ?, ?)",
                   ("1122112211", "Jane", "07112004"))
    cursor.execute("INSERT INTO student (id, name, class) VALUES (?, ?, ?)",
                   ("2211221122", "Bob", "07112001"))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
