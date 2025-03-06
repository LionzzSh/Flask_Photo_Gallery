# Flask Photo Gallery

![GitHub License](https://img.shields.io/github/license/LionzzSh/Flask_Photo_Gallery)  
![Python Version](https://img.shields.io/badge/Python-3.10-blue)  
![Deployed](https://img.shields.io/website?down_color=red&down_message=Down&up_color=green&up_message=Up&url=https%3A%2F%2Flionzz.pythonanywhere.com%2F)

Welcome to **Flask Photo Gallery**, a modern web application built with Flask for managing photo galleries. This project allows users to authenticate, upload photos, organize them into folders, and share with others, with all images stored securely on AWS S3. The app is deployed and live at [https://lionzz.pythonanywhere.com/](https://lionzz.pythonanywhere.com/).

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **User Authentication**: Register and log in with secure password hashing using Flask-Bcrypt.
- **Photo Management**: Upload, view, edit, and delete photos.
- **Folder Organization**: Create and manage folders to categorize your photos.
- **AWS S3 Integration**: Store photos securely in Amazon S3 with boto3.
- **Sharing**: Generate shareable links for photos or folders.
- **Responsive Design**: Basic HTML/CSS templates for a user-friendly interface.

## Screenshots
![Login Page](insert-screenshot-login.jpg)  
*Login Page: User authentication interface.*  

![Gallery View](insert-screenshot-gallery.jpg)  
*Gallery View: Display of photos in a grid layout.*  

![Folder Management](insert-screenshot-folders.jpg)  
*Folder Management: Creating and organizing photo folders.*  

![Upload Photo](insert-screenshot-upload.jpg)  
*Upload Photo: Interface for uploading images to AWS S3.*  

*(Insert your screenshots here. Replace `insert-screenshot-login.jpg`, etc., with the actual file names of the images you provide. Upload them to the repo and link them accordingly.)*

## Tech Stack
- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, boto3
- **Storage**: AWS S3
- **Database**: MySQL (or SQLite for local testing)
- **Hosting**: PythonAnywhere
- **Version Control**: Git, GitHub
- **Python Version**: 3.10

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/LionzzSh/Flask_Photo_Gallery.git
   cd Flask_Photo_Gallery
