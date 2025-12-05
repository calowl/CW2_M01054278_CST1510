Data Intelligence Platform
A secure web application for managing and visualizing IT tickets, cyber incidents, and datasets with user authentication.

🚀 Features
Secure Authentication - User registration and login with bcrypt password hashing

Dashboard Navigation - Clean interface with sidebar navigation

Data Management - View and analyze multiple datasets:

IT Tickets dataset

Cyber Incidents dataset

Datasets metadata

Responsive Design - Wide layout optimized for data visualization

Session Management - Secure user sessions with logout functionality

📁 Project Structure
text
data-intelligence-platform/
├── home.py                    # Main entry point - Login/Home page
├── main.py                    # Authentication functions
├── tables.py                  # Database table creation and CSV loading
├── config.py                  # Configuration paths and constants
├── pages/
│   └── dashboard.py           # Main dashboard with data tables
├── DATA/                      # Data directory
│   ├── it_tickets.csv
│   ├── cyber_incidents.csv
│   └── datasets_metadata.csv
└── README.md                  # This file
🛠️ Installation
Prerequisites
Python 3.8 or higher

pip package manager

Step 1: Clone and Setup
bash
# Clone the repository
git clone <your-repository-url>
cd data-intelligence-platform

# Create a virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Step 2: Install Dependencies
bash
pip install -r requirements.txt
If requirements.txt doesn't exist, install manually:

bash
pip install streamlit pandas bcrypt sqlite3
🚦 Quick Start
1. Initialize Database
bash
# Run tables.py to create database tables
python tables.py
2. Start the Application
bash
streamlit run home.py
3. Access the Application
Open your browser and go to: http://localhost:8501

🔐 User Authentication
Registration
Click "Register" on the login page

Enter a unique username

Create a password (minimum 4 characters)

Confirm password

Click "Register"

Login
Enter your username and password

Click "Login"

You'll be redirected to the home page

Click "Go to Dashboard" to access data

📊 Dashboard Features
Navigation
Home - Welcome page with dashboard overview

IT - View IT tickets dataset with filtering options

Cyber - View cyber incidents dataset

Metadata - View datasets metadata information

Data Tables
Interactive pandas DataFrames

Search and filter capabilities

Responsive design for all screen sizes

🗄️ Database
The application uses SQLite with the following tables:

Users Table
sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user'
)
Data Tables
cyber_incidents - Cyber security incident records

datasets_metadata - Metadata about available datasets

it_tickets - IT support ticket records

🔧 Configuration
Edit config.py to modify:

Database path

Data directory location

Application settings

🧪 Testing the Authentication System
You can also run the authentication system from command line:

bash
python main.py
This provides a CLI interface with:

User registration

User login

Database management

📈 Adding Visualizations (Future Enhancement)
To add charts and graphs to the dashboard:

Install visualization libraries:

bash
pip install plotly matplotlib seaborn
Modify pages/dashboard.py to include:

Bar charts for ticket status distribution

Line charts for incident trends over time

Pie charts for priority breakdowns

🔒 Security Features
Password Hashing: All passwords are hashed using bcrypt

SQL Injection Protection: Parameterized queries prevent SQL injection

Session Management: Streamlit session state handles user sessions

Input Validation: All user inputs are validated before processing

🐛 Troubleshooting
Common Issues:
"Module not found" error

bash
pip install <missing-module>
Database connection issues

Ensure DATA/ directory exists

Check file permissions

Run python tables.py to initialize database

Streamlit not starting

bash
# Check if port 8501 is in use
streamlit run home.py --server.port 8502
Reset Database:
bash
# Delete the database file
rm DATA/intelligence_platform.db

# Recreate tables
python tables.py
📝 Usage Notes
First-time users must register before logging in

Usernames must be unique

Passwords are minimum 4 characters

All data is stored locally in SQLite database

CSV files in DATA/ directory are loaded into the database

🤝 Contributing
Fork the repository

Create a feature branch

Make your changes

Test thoroughly

Submit a pull request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Built with Streamlit

Authentication with bcrypt

Data handling with pandas

Note: This is a demo application for educational purposes. For production use, consider additional security measures and deployment configurations.

📞 Support
For issues or questions:

Check the troubleshooting section

Review the code comments

Open an issue in the repository