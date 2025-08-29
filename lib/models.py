import sqlite3

# Global variables for database connection
CONN = sqlite3.connect('hospital_app.db')
CURSOR = CONN.cursor()

def create_tables():
    """
    Creates all necessary tables for the hospital application.
    This function should be called once at the start of the application.
    """
    # Create the users table
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            phone_number TEXT,
            age INTEGER,
            gender TEXT
        )
    ''')

    # Create the doctors table
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL
        )
    ''')

    # Create the medical_reports table, with foreign keys linking to users and doctors
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS medical_reports (
            report_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            doctor_id INTEGER,
            report_content TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE SET NULL
        )
    ''')

    CONN.commit()
    print("Database tables created successfully.")

class User:
    """
    Represents a user in the hospital application.
    This class provides methods for creating, retrieving, and deleting user records.
    """
    def __init__(self, username, phone_number, age, gender, user_id=None):
        self.username = username
        self.phone_number = phone_number
        self.age = age
        self.gender = gender
        self.user_id = user_id

    @staticmethod
    def create(username, phone_number, age, gender):
        """Creates a new user record in the database."""
        CURSOR.execute(
            "INSERT INTO users (username, phone_number, age, gender) VALUES (?, ?, ?, ?)",
            (username, phone_number, age, gender)
        )
        CONN.commit()
        print(f"User '{username}' created successfully.")

    @staticmethod
    def get_all():
        """Fetches all users from the database."""
        CURSOR.execute("SELECT * FROM users")
        rows = CURSOR.fetchall()
        return [User(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    @staticmethod
    def find_by_id(user_id):
        """Finds a user by their unique ID."""
        CURSOR.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = CURSOR.fetchone()
        if row:
            return User(row[1], row[2], row[3], row[4], row[0])
        return None

    def delete(self):
        """Deletes the user and all their associated medical reports."""
        # Use a transaction to ensure both deletions happen or none at all
        try:
            CURSOR.execute("DELETE FROM users WHERE user_id = ?", (self.user_id,))
            CONN.commit()
            print(f"User '{self.username}' and their reports deleted successfully.")
        except sqlite3.Error as e:
            CONN.rollback()
            print(f"Failed to delete user: {e}")

class Doctor:
    """
    Represents a doctor in the hospital system.
    Provides methods for managing doctor records.
    """
    def __init__(self, name, specialty, doctor_id=None):
        self.name = name
        self.specialty = specialty
        self.doctor_id = doctor_id

    @staticmethod
    def create(name, specialty):
        """Creates a new doctor record in the database."""
        CURSOR.execute(
            "INSERT INTO doctors (name, specialty) VALUES (?, ?)",
            (name, specialty)
        )
        CONN.commit()
        print(f"Doctor '{name}' created successfully.")

    @staticmethod
    def get_all():
        """Fetches all doctors from the database."""
        CURSOR.execute("SELECT * FROM doctors")
        rows = CURSOR.fetchall()
        return [Doctor(row[1], row[2], row[0]) for row in rows]

    @staticmethod
    def find_by_id(doctor_id):
        """Finds a doctor by their unique ID."""
        CURSOR.execute("SELECT * FROM doctors WHERE doctor_id = ?", (doctor_id,))
        row = CURSOR.fetchone()
        if row:
            return Doctor(row[1], row[2], row[0])
        return None

    @staticmethod
    def get_by_specialty(specialty):
        """Fetches all doctors with a specific specialty."""
        CURSOR.execute("SELECT * FROM doctors WHERE specialty = ?", (specialty,))
        rows = CURSOR.fetchall()
        return [Doctor(row[1], row[2], row[0]) for row in rows]

class MedicalReport:
    """
    Represents a medical report linking a user to a doctor.
    """
    def __init__(self, user_id, doctor_id, report_content, report_id=None):
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.report_content = report_content
        self.report_id = report_id

    @staticmethod
    def create(user_id, doctor_id, report_content):
        """Creates a new medical report record."""
        CURSOR.execute(
            "INSERT INTO medical_reports (user_id, doctor_id, report_content) VALUES (?, ?, ?)",
            (user_id, doctor_id, report_content)
        )
        CONN.commit()
        print("Medical report created.")

    @staticmethod
    def get_user_reports(user_id):
        """
        Fetches all medical reports for a specific user, including doctor details.
        Uses an INNER JOIN to combine data from both tables.
        """
        CURSOR.execute(
            """SELECT mr.report_id, d.name, d.specialty, mr.report_content
            FROM medical_reports mr
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.user_id = ?""",
            (user_id,)
        )
        return CURSOR.fetchall()

def close_connection():
    """Closes the database connection."""
    CONN.close()
    print("Database connection closed.")
