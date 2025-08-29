from .models import User, Doctor, MedicalReport, create_tables, close_connection
import sys

def main_menu():
    """Displays the main menu options."""
    print("\nWeLcoME TO tHe BaLLeRs HeAlTh CaRe SyStEm")
    print("1. Log In / Fill Your Details")
    print("2. Book an Appointment")
    print("3. View Medical Reports")
    print("4. Manage Doctors (Admin)")
    print("5. Exit")

def manage_doctors_menu():
    """Menu for doctor management operations."""
    print("\n--- Doctor Management ---")
    print("1. Create new doctor")
    print("2. View all doctors")
    print("3. Add specialists")
    print("4. Back to main menu")

def handle_user_creation():
    """Prompts for user details and creates a user."""
    print("\n--- Log In / Fill Your Details ---")
    print("Please enter your details to create a user account.")
    username = input("Username: ")
    phone_number = input("Phone Number: ")
    age = input("Age: ")
    gender = input("Gender: ")
    
    if not all([username, phone_number, age, gender]):
        print("Error: All fields are required.")
        return
    
    try:
        age = int(age)
        User.create(username, phone_number, age, gender)
    except ValueError:
        print("Error: Age must be a number.")

def handle_view_users():
    """Displays all users."""
    users = User.get_all()
    if not users:
        print("No users found.")
        return
    print("\n--- All Users ---")
    for user in users:
        print(f"ID: {user.user_id}, Name: {user.username}, Phone: {user.phone_number}, Age: {user.age}, Gender: {user.gender}")

def handle_find_user():
    """Finds and displays a user by ID."""
    try:
        user_id = int(input("Enter user ID to find: "))
        user = User.find_by_id(user_id)
        if user:
            print(f"\nUser Found: ID: {user.user_id}, Name: {user.username}, Age: {user.age}")
        else:
            print(f"User with ID {user_id} not found.")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")

def handle_delete_user():
    """Deletes a user by ID."""
    try:
        user_id = int(input("Enter user ID to delete: "))
        user = User.find_by_id(user_id)
        if user:
            user.delete()
        else:
            print(f"User with ID {user_id} not found.")
    except ValueError:
        print("Error: Invalid ID. Please enter a number.")

def handle_doctor_creation():
    """Prompts for doctor details and creates a doctor."""
    print("\nEnter doctor details:")
    name = input("Name: ")
    specialty = input("Specialty (e.g., 'Specialist' or 'General Practitioner'): ")
    
    if not all([name, specialty]):
        print("Error: Name and specialty are required.")
        return

    Doctor.create(name, specialty)

def handle_add_five_specialists():
    """Adds 5 sample specialists to the database."""
    specialists = [
        "Dr. Benz", "Dr. lambo", "Dr. Money", "Dr. Dee", "Dr. Patelo"
    ]
    for name in specialists:
        Doctor.create(name, "Specialist")
    print("5 sample specialists have been added.")

def handle_view_doctors():
    """Displays all doctors."""
    doctors = Doctor.get_all()
    if not doctors:
        print("No doctors found.")
        return
    print("\n--- All Doctors ---")
    for doctor in doctors:
        print(f"ID: {doctor.doctor_id}, Name: {doctor.name}, Specialty: {doctor.specialty}")

def handle_view_reports():
    """Displays medical reports for a user."""
    try:
        user_id = int(input("Enter your user ID to view reports: "))
        user = User.find_by_id(user_id)
        if not user:
            print("User not found.")
            return

        reports = MedicalReport.get_user_reports(user_id)
        if not reports:
            print("You have no medical reports yet.")
            return

        print("\n--- Your Medical Reports ---")
        for report in reports:
            print(f"Report ID: {report[0]}")
            print(f"Doctor: {report[1]} ({report[2]})")
            print(f"Report Content: {report[3]}\n")

    except ValueError:
        print("Error: Invalid user ID. Please enter a number.")

def treatment_and_payment_flow():
    """Handles the doctor and payment selection process."""
    print("\n--- Book an Appointment ---")
    user_id_input = input("Enter your User ID to proceed: ")
    try:
        user_id = int(user_id_input)
        user = User.find_by_id(user_id)
        if not user:
            print("User not found. Please log in first by selecting '1' from the main menu.")
            return
    except ValueError:
        print("Invalid User ID. Please enter a number.")
        return

    print("\nChoose your mode of treatment:")
    print("1. General Doctor")
    print("2. Specialist")
    
    specialty_choice = input("Enter your choice (1 or 2): ")
    if specialty_choice == '1':
        specialty = 'General Practitioner'
    elif specialty_choice == '2':
        specialty = 'Specialist'
    else:
        print("Invalid choice.")
        return

    available_doctors = Doctor.get_by_specialty(specialty)
    if not available_doctors:
        print(f"No {specialty}s available at the moment.")
        return
    
    print(f"\nAvailable {specialty}s:")
    for doc in available_doctors:
        print(f"ID: {doc.doctor_id}, Name: {doc.name}")
    
    try:
        doctor_id = int(input("Enter the ID of the doctor you want to see: "))
        doctor = Doctor.find_by_id(doctor_id)
        if not doctor or doctor.specialty != specialty:
            print("Invalid doctor ID or specialty mismatch.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    print("\nChoose your payment option:")
    print("1. Cash")
    print("2. Insurance")
    
    payment_choice = input("Enter your choice (1 or 2): ")
    if payment_choice == '1':
        print("\nThank you. Please proceed to the cashier.")
    elif payment_choice == '2':
        handle_insurance_payment()
    else:
        print("Invalid payment choice.")
        return
    
    # Simulate a successful appointment
    print(f"\nAppointment with {doctor.name} booked successfully!")

def handle_insurance_payment():
    """Handles the insurance company selection."""
    print("\n--- Insurance Companies ---")
    insurance_companies = ["SHA", "NHIF", "OLD MUTUAL", "BIMA"]
    for i, company in enumerate(insurance_companies, 1):
        print(f"{i}. {company}")
    
    try:
        company_choice = int(input("Enter the number for your insurance provider: "))
        if 1 <= company_choice <= len(insurance_companies):
            selected_company = insurance_companies[company_choice - 1]
            print(f"\nThank you. Your insurance with {selected_company} will be processed.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def run():
    """Main function to run the application loop."""
    create_tables()
    
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            handle_user_creation()
        elif choice == '2':
            treatment_and_payment_flow()
        elif choice == '3':
            handle_view_reports()
        elif choice == '4':
            while True:
                manage_doctors_menu()
                doctor_choice = input("Enter your choice: ")
                if doctor_choice == '1':
                    handle_doctor_creation()
                elif doctor_choice == '2':
                    handle_view_doctors()
                elif doctor_choice == '3':
                    handle_add_five_specialists()
                elif doctor_choice == '4':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '5':
            close_connection()
            print("Exiting application. Goodbye!👋")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    run()