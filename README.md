Ballers' Hospital App
A command-line interface (CLI) for a hospital management system built with Python and SQLite. This application allows users to manage patient details, book appointments, and interact with doctor and payment data.

Table of Contents
Features

Getting Started

Prerequisites

Installation

Usage

Project Structure

License

Features
User Authentication: Log in and create new user accounts by providing personal details.

Appointment Booking: Choose a consultation with either a General Practitioner or a Specialist.

Flexible Payments: Select from various payment options, including Cash or a list of Insurance providers.

Doctor Management: An admin panel allows you to view existing doctors and add new ones.

Medical Reports: Users can easily view their medical reports provided by a doctor.

Getting Started
Follow these steps to set up and run the application on your local machine.

Prerequisites
You will need Python 3.x and pip installed.

Installation
Clone the repository:

git clone [https://github.com/allan6757/Hospitali.git](https://github.com/allan6757/Hospitali.git)
cd Hospitali

Set up a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate

Run the seeding script to create the database and populate it with sample data:

python3 seed.py

Usage
To start the application, make sure your virtual environment is active and execute the main CLI script as a module:

python3 -m lib.cli

Follow the on-screen prompts to navigate the menu and use the application's features.

Project Structure
lib/cli.py: The main command-line interface file.

lib/models.py: The Object-Relational Mapping (ORM) and database models.

seed.py: A script to seed the database with initial data.

README.md: Project documentation.

LICENSE.md: The MIT License for this project.

License
This project is licensed under the MIT License. See the LICENSE.md file for more details.
