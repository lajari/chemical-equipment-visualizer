# Chemical Equipment Parameter Visualizer  
(Hybrid Web + Desktop Application)

This project is developed as part of the FOSSEE Internship Screening Task.  
It is a hybrid application that runs as both a Web Application (React) and a Desktop Application (PyQt5) using a common Django REST backend.

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

## How to Run

### Backend
```bash
cd backend
venv\Scripts\activate
python manage.py migrate
python manage.py runserver

##  Web App
cd web
npm install
npm start

## Desktop App
python desktop_app.py

##Sample CSV
Use the provided sample_equipment_data.csv file for testing.

