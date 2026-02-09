# Chemical Equipment Parameter Visualizer  
(Hybrid Web + Desktop Application)

This project is developed as part of the FOSSEE Internship Screening Task.  
It is a hybrid application that runs as both a Web Application (React) and a Desktop Application (PyQt5) using a common Django REST backend.

The application allows users to upload a CSV file containing chemical equipment parameters and visualizes useful summary statistics and charts.

## Features
- Upload CSV file containing chemical equipment data  
- Backend parses CSV and calculates:
  - Total equipment count  
  - Average flowrate, pressure, temperature  
  - Equipment type distribution  
- Visualization:
  - Web: React + Chart.js  
  - Desktop: PyQt5 + Matplotlib  
- Stores last 5 upload summaries in SQLite  
- Generate PDF report from backend  

## Tech Stack
- Backend: Django + Django REST Framework  
- Web Frontend: React.js + Chart.js  
- Desktop App: PyQt5 + Matplotlib  
- Database: SQLite  
- Data Processing: Pandas  

## Project Structure
chemical-equipment-visualizer/
│
├── backend/ # Django REST API
├── web/ # React frontend
├── desktop/ # PyQt5 desktop application
├── sample_equipment_data.csv
├── .gitignore
└── README.md

## Setup Instructions

### 1 . Backend(Django)
cd backend
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Backend will run at:
http://127.0.0.1:8000/

### 2. Web App(React)
cd web
npm install
npm start

Web app will run at:
http://localhost:3000/

### 3. Desktop App(PyQt5)
python desktop_app.py

##Sample CSV
Use the provided sample_equipment_data.csv file for testing.
Demo

A short demo video (2–3 minutes) is recorded to show:

Backend API running
Web app uploading CSV and showing chart
Desktop app displaying same analytics

## Future Enhancements
User authentication and role-based access
Advanced filtering and search on equipment data
Export charts and summaries as PDF from frontend
Deployment of web version on cloud platform

Author
Developed by Lajari Shinde as part of the FOSSEE Internship Screening Task.
 




