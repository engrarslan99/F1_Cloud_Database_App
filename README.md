# F1 Database App 🏎️

A full-stack **PaaS web application** built on **Google App Engine** that stores and manages **Formula 1 driver and team data**. It functions similarly to Wikipedia. Authenticated users can create, edit, and delete records, while public users can browse and query freely. Built with **Python** and **Firebase** as part of **MSc Computer Science at Griffith College Dublin**.

---

## Features

### 🔐 Authentication
- **Firebase-based** login and logout system
- **Role-based access** logged-in users can modify data, logged-out users can only view and query

### 🏁 Driver Management
- **Add, edit, and delete** F1 drivers
- Each driver stores:
  - **Age**
  - **Total Pole Positions**
  - **Total Race Wins**
  - **Total Points Scored**
  - **Total World Titles**
  - **Total Fastest Laps**
  - **Current Team**
- **Duplicate driver names are prevented**
- Each driver displayed as a **clickable link** leading to their individual profile page

### 🏢 Team Management
- **Add, edit, and delete** F1 teams
- Each team stores:
  - **Year Founded**
  - **Total Pole Positions**
  - **Total Race Wins**
  - **Total Constructor Titles**
  - **Finishing Position in Previous Season**
- **Duplicate team names are prevented**
- Each team displayed as a **clickable link** leading to their individual profile page

### 🔍 Query & Filtering
- Filter drivers or teams by **any single attribute**
- Supports three comparison types: **greater than**, **less than**, and **equal to**
- Query forms accessible to **both logged-in and logged-out users**

### ⚖️ Comparison Tool
- Compare **any two drivers** side by side in a 2-column stats table
  - Better stat highlighted in **green**
  - For all stats except Age: **higher number wins**
  - For Age: **lower number wins**
- Compare **any two teams** side by side in a 2-column stats table
  - Better stat highlighted in **green**
  - For Finishing Position and Year Founded: **lower number wins**
  - For all other stats: **higher number wins**
- Comparison **cannot be triggered** with 0 or 1 selections

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python (Google App Engine) |
| **Authentication** | Firebase Authentication |
| **Database** | Cloud Firestore (NoSQL) |
| **Frontend** | HTML, CSS, JavaScript |
| **Auth Library** | firebase-login.js |

---

## 🗄️ Data Model

```
Firestore
 ├── drivers (collection)
 │     └── driver document
 │           ├── name
 │           ├── age
 │           ├── pole_positions
 │           ├── race_wins
 │           ├── points_scored
 │           ├── world_titles
 │           ├── fastest_laps
 │           └── team
 │
 └── teams (collection)
       └── team document
             ├── name
             ├── year_founded
             ├── pole_positions
             ├── race_wins
             ├── constructor_titles
             └── previous_season_position
```

> **Note:** No Firestore indexes are used in this project.

---

## 🚀 How to Run

### Prerequisites
- **Python 3.x**
- **Google Cloud SDK** installed
- **Firebase project** set up

### Steps

1. **Clone the repository**

2. **Set up Firebase**
   - Go to [Firebase Console](https://console.firebase.google.com)
   - Create a new project
   - Enable **Authentication** (Email/Password)
   - Enable **Firestore Database**
   - Copy your Firebase config into the project

3. **Run locally**
   ```bash
   dev_appserver.py app.yaml
   ```

4. **Deploy to Google App Engine**
   ```bash
   gcloud app deploy
   ```


---

## 🎓 Academic Context

| Detail | Info |
|--------|------|
| **Institution** | Griffith College Dublin |
| **Programme** | MSc Computer Science |
| **Module** | Cloud Platforms & Applications |
| **Year** | 2025 |

---

## 👨‍💻 Author

**Arslan Ashfaq**  
[LinkedIn](https://www.linkedin.com/in/arslanashfaq99) · [GitHub](https://github.com/engrarslan99)
