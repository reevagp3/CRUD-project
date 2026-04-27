# Quick Start Guide

Get your production-ready Flask CRUD app running in minutes!

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd "CRUD proj"
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Supabase credentials
# On Windows: Open .env with your editor and add:
# SUPABASE_DB_URL=postgresql://user:password@host:6543/database
```

### Step 3: Setup Database
```bash
python setup_db.py
```
This creates the `items` table in your Supabase database.

### Step 4: Run Locally
```bash
# Development mode (with auto-reload)
python app.py
```

### Step 5: Open in Browser
```
http://localhost:5000/ui
```

That's it! 🎉

## 📖 Common Commands

### Development
```bash
# Run with auto-reload
python app.py

# Or with FLASK_ENV
FLASK_ENV=development python app.py
```

### Production Simulation
```bash
# Test production setup locally
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Test API
```bash
# Get all items
curl http://localhost:5000/api/items

# Check health
curl http://localhost:5000/api/health

# Add item
curl -X POST http://localhost:5000/api/add \
  -H "Content-Type: application/json" \
  -d '{"name":"My Item"}'
```

## 🚀 Deploy to Render (3 Steps)

1. **Push to GitHub**
```bash
git push origin main
```

2. **On Render.com:**
   - New Web Service
   - Connect your GitHub repo
   - Set environment variables (`.env` values)
   - Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📚 Documentation

- **[README.md](README.md)** - Full documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - What changed

## ⚠️ Important Notes

- ✅ Never commit `.env` file to Git
- ✅ Use `.env.example` as template
- ✅ Change `SECRET_KEY` in production
- ✅ Database table created automatically
- ✅ All CRUD operations working

## 🆘 Troubleshooting

### Database Connection Error
```
Make sure SUPABASE_DB_URL is correct in .env
Format: postgresql://user:password@host:6543/database
```

### Port Already in Use
```bash
# Use different port
PORT=5001 python app.py
```

### Module Not Found
```bash
# Make sure dependencies installed
pip install -r requirements.txt
```

### Table Already Exists
The setup script handles this automatically - just run `python setup_db.py`

## ✨ Features

- ✅ Full CRUD operations
- ✅ Dark/Light theme toggle
- ✅ Real-time updates
- ✅ Mobile responsive
- ✅ Error handling
- ✅ Logging
- ✅ Connection pooling
- ✅ Security best practices

## 📞 Need Help?

1. Check [README.md](README.md) - Common questions
2. Check [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment issues
3. Review logs: `app.log` file
4. Check Flask docs: https://flask.palletsprojects.com

---

**Ready?** Run `python app.py` and enjoy! 🚀
