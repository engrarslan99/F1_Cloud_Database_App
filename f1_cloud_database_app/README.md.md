**F1 Cloud Database Application**



**Overview**

This project was developed as part of my Master’s in Computer Science for the Cloud Platforms \& Applications module.



It is a cloud-based web application that stores and manages Formula 1 drivers and teams using Google App Engine and Google Firestore.



**## Features**

\- User authentication using Firebase login

\- Add, edit, delete F1 drivers and teams

\- Query drivers and teams using comparison filters

\- Compare two drivers or two teams with visual highlights

\- Role-based access (logged-in vs logged-out users)



**## Technologies Used**

\- Backend: Python

\- Frontend: HTML, CSS, JavaScript

\- Cloud Platform: Google App Engine

\- Database: Google Firestore

\- Authentication: Firebase Authentication



**## Application Structure**

\- Backend handles data storage and business logic

\- Firestore collections for drivers and teams

\- Separate pages for create, edit, view, query, and compare operations



\## Security \& Credentials

This project uses Google Cloud service accounts and Firebase configuration files.

**⚠️ For security reasons:**

* Service account credentials
* API keys
* Secret configuration files

are NOT included in this repository.



**To run this project locally or deploy it:**



1. Create a Google Cloud service account
2. Download the credentials JSON file
3. Set the GOOGLE\_APPLICATION\_CREDENTIALS environment variable
4. Configure Firebase Authentication in your Google Cloud project



This follows industry best practices for cloud security.



**How to Run (High-Level)**

Clone the repository

Install required dependencies using requirements.txt

Configure Google Cloud and Firebase credentials

Deploy the application using Google App Engine



Note: This project was originally deployed on Google Cloud as part of academic coursework.



**Key Learning Outcomes:**

* Deploying applications using a Platform as a Service (PaaS)
* Designing and querying NoSQL databases
* Implementing authentication and access control
* Structuring scalable cloud-based web applications
* Applying secure credential management practices



**Author:**



Muhammad Arslan Ashfaq

Master’s in Computer Science

Software Developer | Cybersecurity Enthusiast

