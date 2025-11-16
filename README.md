# SERCONN - IntegratedProject1

**SERCONN** is a platform designed to connect service seekers with service providers. It offers a complete solution for searching, booking, and managing professional services. The platform ensures an efficient and structured process through a Django backend and a responsive interface styled with Tailwind CSS.

---

## 🏗 Architectural Overview

The project is built on a modular architecture, with a clear separation of concerns to ensure scalability and maintainability.

---

## 🚀 Deployment Architecture

The application is currently configured for local development. The client-side, accessible from both web and mobile browsers, communicates with the local server via HTTP.

- **Backend:** Python + Django  
- **Database:** SQLite3 (default for local development)  
- **Styling:** TailwindCSS (requires Node.js for building styles)

---

## 🧩 Component Architecture

The core of the application is divided into three main components:

- **`accounts`**  
  Manages user registration, login, profile editing, and the rating system.

- **`searching`**  
  Handles all service search functionalities, including category, location, and keyword-based filters.

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

---

### ✅ Prerequisites

Make sure you have the following installed:

- Python 3.8 or higher  
- `pip` (Python package manager)  
- Git  
- **Node.js 18+** (required for TailwindCSS)  
- **npm** (comes with Node)  

---

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

3. Install the python required dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node/Tailwind dependencies (inside the project root):
```bash
npm install
```

5. Build Tailwind styles (required before running the app):
```bash
npm run build:css
```

6. Database setup:
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
