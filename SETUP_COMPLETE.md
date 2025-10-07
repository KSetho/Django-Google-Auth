# Django Google Authentication Backend - Complete Setup

## 🚀 Project Overview

This is a complete Django REST Framework backend system with Google OAuth2 authentication using JWT tokens. The system provides secure user authentication and authorization.

## 📁 Project Structure

```
google_auth/
├── auth/                           # Django project settings
│   ├── settings.py                # Main configuration
│   ├── urls.py                    # Main URL routing
│   └── ...
├── accounts/                      # Authentication app
│   ├── views.py                   # API endpoints
│   ├── urls.py                    # App URL routing
│   ├── serializers.py             # API serializers
│   ├── management/commands/       # Custom management commands
│   └── ...
├── env/                           # Virtual environment
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── README.md                     # API documentation
├── test.html                     # Frontend test page
└── manage.py                     # Django management script
```

## ✅ What's Included

### Backend Features
- ✅ Google OAuth2 authentication
- ✅ JWT token-based authorization
- ✅ User registration and login
- ✅ Token refresh mechanism
- ✅ Secure logout with token blacklisting
- ✅ User profile management
- ✅ CORS configuration for frontend integration
- ✅ Comprehensive error handling

### API Endpoints
- `POST /api/auth/google/` - Google authentication
- `POST /api/auth/refresh/` - Refresh JWT tokens
- `POST /api/auth/logout/` - Logout user
- `GET /api/auth/profile/` - Get user profile
- `GET /api/auth/test/` - Test API connectivity

### Security Features
- JWT tokens with configurable expiration
- Refresh token rotation
- Token blacklisting on logout
- CORS protection
- Environment-based configuration

## 🔧 Quick Setup

1. **Activate Virtual Environment**
   ```bash
   source env/bin/activate
   ```

2. **Install Dependencies** (Already done)
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Update `.env` file with your Google OAuth credentials:
   ```env
   GOOGLE_CLIENT_ID="your_actual_client_id"
   GOOGLE_CLIENT_SECRET="your_actual_secret"
   SECRET_KEY="your_secure_django_secret_key"
   ```

4. **Run Migrations** (Already done)
   ```bash
   python manage.py migrate
   ```

5. **Setup Google OAuth** (Optional)
   ```bash
   python manage.py setup_google_oauth
   ```

6. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## 🧪 Testing

### API Test
The server is currently running at `http://localhost:8000`

Test the API:
```bash
curl http://localhost:8000/api/auth/test/
```

Expected response:
```json
{
    "message": "API is working!",
    "allauth_available": true,
    "endpoints": {
        "google_auth": "/api/auth/google/",
        "logout": "/api/auth/logout/",
        "profile": "/api/auth/profile/",
        "refresh": "/api/auth/refresh/",
        "test": "/api/auth/test/"
    }
}
```

### Frontend Test
Open `test.html` in your browser to test the complete authentication flow.

## 📝 Next Steps

1. **Get Google OAuth Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Google+ API
   - Create OAuth 2.0 credentials
   - Add `http://localhost:8000` to authorized origins
   - Update `.env` with real credentials

2. **Update Test Page**
   - Update the `data-client_id` in `test.html` with your Google Client ID

3. **Frontend Integration**
   - Use the provided JavaScript/React examples in `README.md`
   - Configure CORS for your frontend domain

4. **Production Deployment**
   - Use HTTPS
   - Set `DEBUG=False`
   - Configure secure CORS settings
   - Use a production database (PostgreSQL)
   - Set up proper secret key management

## 🔐 Admin Access

- **Username:** admin
- **Email:** admin@example.com  
- **Password:** admin123
- **Admin URL:** http://localhost:8000/admin/

## 📚 Documentation

- Complete API documentation: `README.md`
- Frontend integration examples included
- Error handling and security notes provided

## 🛠 Technology Stack

- **Backend:** Django 5.2.7 + Django REST Framework 3.16.1
- **Authentication:** django-allauth 65.3.0 + JWT
- **Database:** SQLite (development)
- **CORS:** django-cors-headers 4.9.0
- **Environment:** python-decouple 3.8

## 🔍 Current Status

✅ **Server Running:** http://localhost:8000  
✅ **Database:** Migrated and ready  
✅ **API:** All endpoints functional  
✅ **Admin:** Superuser created  
✅ **Documentation:** Complete  
✅ **Test Page:** Ready for use  

The backend is fully functional and ready for Google OAuth integration!
