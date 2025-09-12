# SERCONN - IntegratedProject1

**SERCONN** is a platform designed to connect service seekers with service providers. It offers a comprehensive solution for searching, booking, and managing various professional services. The platform ensures a secure and efficient process through a robust backend developed with Django and a real-time communication system.

---

## 🏗 Architectural Overview

The project is built on a modular architecture, with a clear separation of concerns to ensure scalability and maintainability.

---

## 🚀 Deployment Architecture

The application is currently configured for local development. The client-side, accessible from both web and mobile browsers, communicates with the local server via HTTP.

- **Backend:** Python + Django  
- **Database:** SQLite3 (default for local development)  
- **External Integrations (planned):**
  - Google Calendar API
  - Gemini API

---

## 🧩 Component Architecture

The core of the application is divided into four main components:

- **`accounts`**  
  Manages user registration, login, profile editing, and the rating system.

- **`searching`**  
  Handles all service search functionalities, including category, location, and keyword-based filters.

- **`payments`**  
  Processes all financial transactions securely and manages payment history.

- **`interactions`**  
  Facilitates real-time communication between users and manages the booking lifecycle.

---

## 🗃 Database Schema

The schema supports all functionalities of the application with key tables for:

- Users  
- Services  
- Bookings  
- Payments  

Relational integrity ensures smooth flow of information and data consistency.

---

## 🚧 Getting Started

Follow these steps to set up and run the project locally.

### ✅ Prerequisites

Make sure you have the following installed:

- Python 3.8 or higher  
- `pip` (Python package manager)  
- Git

### 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/Jarax26/Serconn-IntegratedProject1.git
cd Serconn-IntegratedProject1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```
4. Database setup:
The project is configured to use SQLite3 by default for local development. No additional setup is required.

### ▶️ Running the Application

1. Apply database migrations:
```bash
python manage.py migrate
```

2. Run the development server:
```bash
python manage.py runserver
```
>The application will be accessible at http://127.0.0.1:8000
