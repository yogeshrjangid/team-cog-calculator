# Team COG Calculator

## Overview

Team COG Calculator is a Streamlit-based web application that calculates the geographical Center of Gravity (COG) of a team based on the locations of its members.

The application allows users to add team members, automatically determine their geographic coordinates from city names, visualize member locations on an interactive India map, and calculate the team's overall Center of Gravity.

---

## Features

### Member Management

* Add team members
* Edit existing members
* Delete members
* Store data in a SQLite database

### Geographic Processing

* Automatic city-to-latitude/longitude conversion
* Handles common city name misspellings
* Reverse geocoding to identify the nearest city to the calculated COG

### Visualization

* Interactive India map
* Team member markers
* Permanent member name labels
* Center of Gravity marker
* Nearest city to COG display

### Statistics

* Total number of members
* Average age
* Average domain experience
* Number of unique cities

---

## Technology Stack

### Frontend

* Streamlit

### Database

* SQLite

### Mapping

* Folium
* Streamlit-Folium

### Geocoding

* Geopy
* OpenStreetMap Nominatim

### Fuzzy Matching

* RapidFuzz

### Data Processing

* Pandas

---

## Project Structure

COG_PROJECT/

├── app.py

├── database.py

├── team.db

├── requirements.txt

├── README.md

└── venv/

---

## Installation

### Step 1: Clone or Download the Project

Copy the project folder to your local machine.

### Step 2: Create Virtual Environment

Windows:

```cmd
python -m venv venv
```

### Step 3: Activate Virtual Environment

Windows:

```cmd
venv\Scripts\activate
```

You should see:

```cmd
(venv)
```

at the beginning of the command prompt.

### Step 4: Install Required Packages

```cmd
pip install -r requirements.txt
```

---

## Running the Application

Navigate to the project directory:

```cmd
cd "C:\User\COG_PROJECT"
```

Activate the virtual environment:

```cmd
venv\Scripts\activate
```

Run the application:

```cmd
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

---

## Using the Application

### Add Member

Enter:

* Name
* Age
* Domain Experience
* City

Click:

```text
Add Member
```

The application automatically finds the city coordinates and stores the member.

### Edit Member

Select an existing member and update:

* Name
* Experience
* City
* State

Click:

```text
Update Member
```

### Delete Member

Select a member and click:

```text
Delete Selected Member
```

---

## Center of Gravity Calculation

The current implementation uses a simple arithmetic average of all member locations.

Latitude COG:

COG Latitude = Sum of Member Latitudes / Number of Members

Longitude COG:

COG Longitude = Sum of Member Longitudes / Number of Members

Each team member contributes equally to the calculation.

If multiple members belong to the same city, each member is counted separately.

---

## Example

Members:

| Name   | City   |
| ------ | ------ |
| Yog    | Pune   |
| Amit   | Mumbai |
| Priya  | Delhi  |

The application:

1. Converts cities to coordinates.
2. Computes average latitude and longitude.
3. Determines the nearest city to the COG.
4. Displays the result on the map.

---

## Future Enhancements

Potential future improvements:

* World map support
* Excel export
* PDF reports
* Bulk member upload with city database (latitude and longitude) removing dependency on libraries
* Experience-weighted COG
* Age-weighted COG
* Authentication and user management
* Cloud deployment

---

## Author

Developed as a learning and visualization tool for geographical Center of Gravity analysis of distributed teams.
By Yog
