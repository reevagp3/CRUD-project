# CRUD Dashboard - Flask + Supabase

A production-ready full-stack CRUD web application built with Flask backend and vanilla JavaScript frontend. Data is persisted in Supabase PostgreSQL.

## 🚀 Features

- **Full CRUD Operations**: Create, Read, Update, Delete items
- **Real-time Updates**: Instant UI updates without page reload
- **Dark/Light Theme**: Toggle between themes (persisted in localStorage)
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Production Ready**: Error handling, logging, security best practices
- **Database Pooling**: Connection pooling for optimal performance
- **Input Validation**: Server-side and client-side validation
- **Secure**: XSS protection, SQL injection prevention via parameterized queries

## 📋 Tech Stack

- **Backend**: Python Flask with Gunicorn
- **Database**: Supabase PostgreSQL
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Deployment**: Render, Heroku, or any platform supporting WSGI

## 🛠️ Project Structure

```
CRUD proj/
├── app.py                 # Flask application entry point
├── config/
│   ├── __init__.py
│   └── config.py         # Environment configuration
├── routes/
│   ├── __init__.py
│   ├── home.py           # Home and UI routes
│   └── items.py          # CRUD API routes
├── services/
│   ├── __init__.py
│   └── db_service.py     # Database operations and item service
├── utils/
│   ├── __init__.py
│   └── validators.py     # Input validation functions
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Stylesheet
│   └── script.js         # Frontend JavaScript
├── .env                  # Environment variables (not committed)
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── Procfile              # Render/Heroku deployment config
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 📦 Installation

### Prerequisites

- Python 3.8+
- Git
- Supabase account and PostgreSQL database

### Local Development Setup

1. **Clone the repository** (if applicable):
```bash
git clone <repository-url>
cd "CRUD proj"
```

2. **Create a virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your Supabase credentials
# SUPABASE_DB_URL=postgresql://user:password@host:6543/database
```

5. **Set up database** (in Supabase):
```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

6. **Run the application**:
```bash
# Development with auto-reload
FLASK_ENV=development python app.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

7. **Access the application**:
```
http://localhost:5000/ui
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Flask Configuration
FLASK_ENV=development        # development, production, testing
FLASK_APP=app.py
SECRET_KEY=your-secure-random-key-change-this

# Database
SUPABASE_DB_URL=postgresql://user:password@host:6543/database

# Server
PORT=5000
HOST=0.0.0.0
LOG_LEVEL=INFO
```

**Important**: Never commit `.env` file to version control!

## 📚 API Endpoints

### Home Routes
- `GET /` - API status message
- `GET /ui` - Main CRUD dashboard

### CRUD API Routes (prefix: `/api`)

#### Get All Items
```http
GET /api/items
```
**Response**:
```json
[
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]
```

#### Create Item
```http
POST /api/add
Content-Type: application/json

{"name": "New Item"}
```
**Response** (201):
```json
{
    "id": 3,
    "name": "New Item",
    "message": "Item added successfully ✅"
}
```

#### Update Item
```http
PUT /api/update/<id>
Content-Type: application/json

{"name": "Updated Item"}
```
**Response** (200):
```json
{
    "id": 3,
    "name": "Updated Item",
    "message": "Item updated successfully ✏️"
}
```

#### Delete Item
```http
DELETE /api/delete/<id>
```
**Response** (200):
```json
{
    "id": 3,
    "message": "Item deleted successfully 🗑"
}
```

#### Health Check
```http
GET /api/health
```
**Response** (200):
```json
{
    "status": "ok",
    "database": "connected"
}
```

## 🚀 Deployment

### Deploy to Render

1. **Push your code to GitHub**:
```bash
git add .
git commit -m "Production-ready Flask CRUD app"
git push origin main
```

2. **Create a new Web Service on Render**:
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Set the following:
     - **Name**: my-crud-app
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

3. **Add Environment Variables**:
   - Add `SUPABASE_DB_URL` with your database URL
   - Add `SECRET_KEY` with a secure random value
   - Set `FLASK_ENV=production`

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your app will be available at `https://my-crud-app.onrender.com`

### Deploy to Heroku

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create Heroku app**:
```bash
heroku create my-crud-app
```

3. **Set environment variables**:
```bash
heroku config:set SUPABASE_DB_URL="postgresql://..."
heroku config:set SECRET_KEY="your-secure-key"
heroku config:set FLASK_ENV=production
```

4. **Deploy**:
```bash
git push heroku main
```

## 🔐 Security Considerations

- ✅ **SQL Injection Protection**: Uses parameterized queries
- ✅ **XSS Protection**: HTML escaping on frontend
- ✅ **Environment Variables**: Sensitive data in .env (not committed)
- ✅ **HTTPS Only**: Enforced in production (Render/Heroku)
- ✅ **Connection Pooling**: Prevents connection exhaustion
- ✅ **Input Validation**: Server-side validation for all inputs
- ✅ **Error Handling**: Generic error messages in production

## 📊 Performance Optimizations

- **Connection Pooling**: 5-connection pool for optimal database performance
- **JSON Parsing**: Efficient client-side rendering
- **Caching**: Theme preference cached in localStorage
- **Compression**: GZIP compression on production servers

## 🧪 Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test get items
curl http://localhost:5000/api/items

# Test create item
curl -X POST http://localhost:5000/api/add \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item"}'

# Test update item
curl -X PUT http://localhost:5000/api/update/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Test"}'

# Test delete item
curl -X DELETE http://localhost:5000/api/delete/1
```

## 🐛 Troubleshooting

### Database Connection Issues
- Verify `SUPABASE_DB_URL` is correct in `.env`
- Check SSL mode is set to `require` in connection string
- Ensure Supabase database is running and accessible

### Port Already in Use
```bash
# Change PORT in .env or run with different port
PORT=5001 python app.py
```

### Module Not Found
```bash
# Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Theme Not Persisting
- Check browser localStorage is enabled
- Try clearing browser cache and localStorage

## 📝 Logging

Logs are written to `app.log` and console. Configure log level in `.env`:
```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 📄 License

This project is provided as-is for educational and production use.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements.

## 📧 Support

For issues or questions, create an issue in the repository or contact the development team.

---

**Last Updated**: April 2026  
**Version**: 1.0.0  
**Production Ready**: ✅ Yes
