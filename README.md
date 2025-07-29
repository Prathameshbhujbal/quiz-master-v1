# Quiz Master - Flask Quiz Application

A comprehensive web-based quiz application built with Flask that allows administrators to create and manage quizzes while users can take quizzes and track their scores.

## 🚀 Features

### For Administrators
- **User Management**: View all registered users
- **Subject Management**: Create, edit, and delete subjects
- **Chapter Management**: Organize content by chapters within subjects
- **Quiz Management**: Create quizzes with custom time durations and remarks
- **Question Management**: Add multiple-choice questions with 4 options
- **Score Tracking**: Monitor user performance across all quizzes

### For Users
- **User Registration & Authentication**: Secure signup and login system
- **Quiz Dashboard**: Browse available quizzes by subject and chapter
- **Interactive Quiz Taking**: Real-time quiz interface with timer
- **Score Tracking**: View personal quiz scores and performance history
- **Performance Summary**: Detailed analysis of quiz attempts

## 🛠️ Technology Stack

- **Backend**: Flask 3.1.0
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Session-based with password hashing
- **Template Engine**: Jinja2
- **Additional Libraries**: 
  - Flask-RESTful for API endpoints
  - python-dotenv for environment management
  - matplotlib for data visualization
  - numpy for numerical operations

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mad-1-quiz-master-v1
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp sample_dotenv .env
   ```
   
   Edit the `.env` file with your configuration:
   ```
   FLASK_DEBUG=true
   FLASK_APP=app.py
   SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
   SQLALCHEMY_TRACK_MODIFICATIONS=False
   SECRET_KEY=your_secret_key_here
   ```

5. **Initialize the database**
   ```bash
   python app.py
   ```
   This will create the database and set up an admin user with credentials:
   - Username: `admin`
   - Password: `admin`

## 🎯 Usage

### Starting the Application
```bash
python app.py
```
The application will be available at `http://localhost:5000`

### Default Admin Account
- **Username**: admin
- **Password**: admin

### User Roles

#### Administrator
1. Login with admin credentials
2. Access admin dashboard at `/admin`
3. Manage subjects, chapters, quizzes, and questions
4. View user list and performance metrics

#### Regular User
1. Register a new account or login
2. Browse available quizzes by subject and chapter
3. Take quizzes and view scores
4. Track performance history

## 📁 Project Structure

```
mad-1-quiz-master-v1/
├── app.py                 # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── sample_dotenv         # Environment variables template
├── application/
│   ├── config.py         # Application configuration
│   ├── database.py       # Database setup
│   ├── models.py         # SQLAlchemy models
│   └── routes.py         # Flask routes and views
├── templates/            # HTML templates
│   ├── admin.html        # Admin dashboard
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── user_dashboard.html # User dashboard
│   ├── quiz/            # Quiz-related templates
│   ├── question/        # Question management templates
│   ├── chapter/         # Chapter management templates
│   └── subject/         # Subject management templates
└── instance/
    └── db.sqlite3       # SQLite database file
```

## 🗄️ Database Schema

### Core Models
- **User**: User accounts with authentication
- **Subject**: Quiz subjects/categories
- **Chapter**: Chapters within subjects
- **Quiz**: Quiz instances with time limits
- **Question**: Multiple-choice questions
- **Score**: User quiz scores and timestamps

## 🔐 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control (Admin/User)
- Input validation and sanitization
- CSRF protection through Flask-SQLAlchemy

## 🎨 Features in Detail

### Quiz Management
- Create quizzes with custom time durations
- Add multiple-choice questions with 4 options
- Set correct answers for automatic scoring
- Organize quizzes by subjects and chapters

### User Experience
- Responsive web interface
- Real-time quiz timer
- Immediate score calculation
- Performance tracking and analytics
- User-friendly navigation

### Admin Features
- Comprehensive CRUD operations for all entities
- User management and monitoring
- Quiz and question management
- Performance analytics and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the GPL License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please refer to the project documentation or create an issue in the repository.

## 📊 Demo

A demo of this application is available at:
https://drive.google.com/drive/folders/1pOgDTKzU0hSsGeeVWu0n1Kze8diau4pR?usp=sharing

---

**Note**: This is a Flask-based quiz application developed for educational purposes. Make sure to change the default admin password in production environments.
