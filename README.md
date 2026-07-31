# Healthy Water Pro 💧

## Overview

Healthy Water Pro is a management system designed for water filter service businesses.

The application helps manage customers, maintenance visits, inventory, expenses, profits, and store operations through an easy-to-use dashboard.

Built with Python and Streamlit.

---

# Features

## 👥 Customer Management

- Add new customers
- Store customer information
- Track customer history
- Search and manage customer records

## 🔧 Maintenance Management

- Record maintenance visits
- Track replaced cartridges and parts
- Save service details
- Manage technician information
- View maintenance history

## 📦 Inventory Management

- Manage stock items
- Add and remove inventory quantities
- Track stock levels
- Set minimum stock limits
- Monitor inventory movements

## 💰 Financial Management

- Track expenses
- Calculate profits
- Monitor sales and costs

## 🏪 Store Management

- Manage products
- Track available items
- Organize sales information

---

# Technology Stack

- Python
- Streamlit
- Pandas
- Google Sheets API
- Firebase / Firestore
- GitHub

---

# Project Structure

```text
healthy-water-v2/

│
├── app.py                         # Main application entry point
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
│
├── .devcontainer/
│   └── devcontainer.json           # Development container configuration
│
├── .streamlit/
│   └── secrets.toml               # Streamlit secrets and configuration
│
├── assets/                        # Static project resources
│   │
│   ├── fonts/
│   │   └── arial.ttf              # Application font
│   │
│   └── images/
│       └── logo.png               # Application logo
│
├── components/                    # Reusable UI components
│   └── parts_manager.py           # Parts management component
│
├── modules/                       # Main application modules
│   │
│   ├── customers.py               # Customer management
│   ├── dashboard.py               # Dashboard and statistics
│   ├── expenses.py                # Expense management
│   ├── inventory.py               # Inventory management
│   ├── maintenance.py             # Maintenance records management
│   ├── profits.py                 # Profit calculations and reports
│   └── store.py                   # Store management
│
└── utils/                         # Utility and backend services
    │
    ├── api.py                     # API communication functions
    ├── constants.py               # Global constants
    ├── data_service.py            # Data handling and database services
    ├── helpers.py                 # Helper functions
    ├── i18n.py                    # Language and translation support
    ├── inventory_history_service.py # Inventory movement history
    ├── inventory_service.py       # Inventory business logic
    └── pdf.py                     # PDF generation utilities
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/ibrahimerian28-coder/healthy-water-v2.git
```

## Move into the project folder

```bash
cd healthy-water-v2
```

## Install required packages

```bash
pip install -r requirements.txt
```

---

# Running The Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# Application Architecture

The project follows a modular architecture:

## app.py

Main entry point responsible for launching the Streamlit application.

## modules/

Contains user interface pages and main business features:

- Customer management
- Inventory management
- Maintenance management
- Expenses
- Profits
- Store operations
- Dashboard

## utils/

Contains backend logic, database operations, helpers, and shared services:

- Data management
- API communication
- Inventory services
- PDF generation
- Language support

## components/

Contains reusable interface components.

## assets/

Contains static resources such as:

- Images
- Fonts
- Application branding files

---

# Data Management

The application uses:

- Google Sheets for data storage
- Firestore for cloud database operations

Database connection settings should be configured before running the application.

Sensitive files such as:

```
.streamlit/secrets.toml
```

should not be uploaded publicly because they may contain API keys or credentials.

---

# Future Development

Planned improvements:

- Automatic maintenance reminders
- Customer notification system
- Advanced reports
- Mobile application version
- Multi-technician support
- Smart inventory suggestions
- SaaS version for other businesses

---

# Developer Notes

This project is under continuous development.

Main goal:

Create a complete business management platform for water filter companies and technicians.

---

# Author

Healthy Water Pro Team
