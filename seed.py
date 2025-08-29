# seed.py
from lib.models import User, Doctor, MedicalReport, create_tables

def seed_database():
    create_tables()

    print("Seeding users...")
    User.create("Leta Coke", "0700000000", 35, "Male")
    User.create("Ziende Sana", "0768686868", 28, "Female")

    print("Seeding doctors...")
    Doctor.create("Dr. Patelo", "Specialist")
    Doctor.create("Dr. Dee", "General Practitioner")

    print("Creating sample reports...")
    MedicalReport.create(user_id=1, doctor_id=1, report_content="Patient has a rare neurological condition.")
    MedicalReport.create(user_id=2, doctor_id=2, report_content="Patient is recovering well from the flu.")

    print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()