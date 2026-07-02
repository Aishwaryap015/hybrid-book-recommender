# BookAI – Hybrid Book Recommendation System
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-Framework-green)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-success)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-orange)
![License](https://img.shields.io/badge/License-Academic-lightgrey)

A full-stack machine learning web application that provides personalized book recommendations using a hybrid recommendation approach combining **Collaborative Filtering** and **Content-Based Filtering**.

BookAI was developed as the **Final Year B.Tech Project** for the **Department of Computer Science & Engineering (Data Science)** at **Government Engineering College, Arwal**, affiliated with **Bihar Engineering University, Patna**, during the academic session **2022–2026**.

The application integrates Django, MongoDB, and machine learning techniques to deliver personalized recommendations based on user behavior and book metadata.

---

## Overview

BookAI addresses the challenges of discovering relevant books from large digital libraries and online book collections. The recommendation engine combines collaborative filtering with content-based filtering to improve recommendation quality while minimizing cold-start and sparsity issues.

The system is designed to provide an intuitive user experience with personalized recommendations, user authentication, book search, wishlist management, and responsive web interfaces.

---

## Features

- Hybrid recommendation engine
- Personalized book recommendations
- Collaborative Filtering using Pearson Correlation
- Content-Based Filtering using TF-IDF and Cosine Similarity
- User authentication
- Guest login
- Book search
- Wishlist and favorites
- Recently viewed books
- Popular and top-rated books
- Responsive user interface
- MongoDB database integration

---

## Recommendation Algorithms

### Content-Based Filtering

- TF-IDF Vectorization
- Cosine Similarity
- Metadata-based similarity computation

### Collaborative Filtering

- User-Item Interaction Matrix
- Pearson Correlation
- K-Nearest Neighbors (KNN)

### Hybrid Recommendation

The recommendation engine combines collaborative filtering and content-based filtering to generate accurate and personalized recommendations while reducing the cold-start problem.

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Django

### Database

- MongoDB

### Machine Learning

- Scikit-learn
- Pandas
- NumPy

### Development Tools

- Git
- GitHub
- Visual Studio Code

---

## Project Structure

```text
BookAI/

├── core/
├── data/
├── ml_models/
│   ├── train_content.py
│   ├── train_collaborative.py
│   ├── recommender.py
│   └── saved_models/
│
├── templates/
├── static/
├── notebooks/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Aishwaryap015/hybrid-book-recommender.git
```

### Navigate to the Project

```bash
cd hybrid-book-recommender
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure MongoDB

Install MongoDB and update the database configuration in:

```
settings.py
```

---

## Training the Machine Learning Models

The trained machine learning models are not included in this repository because they exceed GitHub's file size limits.

Generate the required models locally by running:

```bash
python ml_models/train_content.py
python ml_models/train_collaborative.py
```

The generated model files will be stored in:

```
ml_models/saved_models/
```

---

## Running the Application

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Screenshots

Screenshots of the application interface will be added in a future update.

---

## Future Enhancements

- Deep learning-based recommendation models
- Large Language Model (LLM) assisted recommendations
- REST API integration
- Docker containerization
- Cloud deployment
- Book review and rating system
- Recommendation explainability

---

## Academic Information

**Project Title**

Book Recommendation System Using Collaborative and Content-Based Filtering

**Project Type**

Final Year B.Tech Project

**Department**

Computer Science & Engineering (Data Science)

**Institution**

Government Engineering College, Arwal

**Affiliated University**

Bihar Engineering University, Patna

**Academic Session**

2022–2026

---

## Author

**Aishwarya Priydarshni**

B.Tech – Computer Science & Engineering (Data Science)

Government Engineering College, Arwal

GitHub: https://github.com/Aishwaryap015

---

## License

This project is developed for academic and educational purposes.

If you find this project useful, consider giving it a ⭐ on GitHub.
