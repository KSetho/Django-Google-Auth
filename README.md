# Google Authentication Backend API

This Django REST Framework backend provides Google OAuth2 authentication with JWT tokens.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   
   Create a `.env` file with the following variables:
   ```env
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   GOOGLE_CALLBACK_URL=http://localhost:8000/accounts/google/login/callback/
   SECRET_KEY=your_django_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. **Google OAuth Setup**
   
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add authorized origins: `http://localhost:8000`
   - Add authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`

4. **Database Migration**
   ```bash
   python manage.py migrate
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

#### 1. Google Authentication
**POST** `/api/auth/google/`

Authenticate user with Google ID token.

**Request Body:**
```json
{
    "id_token": "google_id_token_here"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_new_user": false
    },
    "tokens": {
        "access": "jwt_access_token",
        "refresh": "jwt_refresh_token"
    }
}
```

#### 2. Refresh Token
**POST** `/api/auth/refresh/`

Refresh JWT access token.

**Request Body:**
```json
{
    "refresh": "refresh_token_here"
}
```

**Response:**
```json
{
    "access": "new_access_token"
}
```

#### 3. Logout
**POST** `/api/auth/logout/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh_token": "refresh_token_here"
}
```

**Response:**
```json
{
    "message": "Logout successful"
}
```

### User Profile

#### 4. Get User Profile
**GET** `/api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2025-10-02T10:30:00Z",
        "last_login": "2025-10-02T11:00:00Z"
    },
    "social_account": {
        "provider": "google",
        "uid": "google_user_id"
    }
}
```

## Frontend Integration

### JavaScript Example

```javascript
// 1. Initialize Google Sign-In (in your HTML)
<script src="https://accounts.google.com/gsi/client" async defer></script>

// 2. Handle Google Sign-In Response
function handleCredentialResponse(response) {
    const idToken = response.credential;
    
    // Send to your backend
    fetch('http://localhost:8000/api/auth/google/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            id_token: idToken
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.tokens) {
            // Store tokens
            localStorage.setItem('access_token', data.tokens.access);
            localStorage.setItem('refresh_token', data.tokens.refresh);
            
            // Redirect or update UI
            console.log('Login successful:', data.user);
        }
    })
    .catch(error => {
        console.error('Authentication failed:', error);
    });
}

// 3. Make authenticated requests
function makeAuthenticatedRequest(url) {
    const token = localStorage.getItem('access_token');
    
    return fetch(url, {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
}

// 4. Refresh token when needed
function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    return fetch('http://localhost:8000/api/auth/refresh/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            refresh: refreshToken
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            return data.access;
        }
    });
}
```

### React Example

```jsx
import { GoogleLogin } from '@react-oauth/google';

function LoginComponent() {
    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            const response = await fetch('http://localhost:8000/api/auth/google/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id_token: credentialResponse.credential
                })
            });
            
            const data = await response.json();
            
            if (data.tokens) {
                // Store tokens
                localStorage.setItem('access_token', data.tokens.access);
                localStorage.setItem('refresh_token', data.tokens.refresh);
                
                // Handle successful login
                console.log('Login successful:', data.user);
            }
        } catch (error) {
            console.error('Authentication failed:', error);
        }
    };

    return (
        <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => console.log('Login Failed')}
        />
    );
}
```

## CORS Configuration

The backend is configured to allow requests from:
- `http://localhost:3000` (React dev server)
- `http://127.0.0.1:3000`
- `http://localhost:8080` (Vue/other dev servers)
- `http://127.0.0.1:8080`

## Security Notes

1. **Environment Variables**: Never commit real credentials to version control
2. **HTTPS**: Use HTTPS in production
3. **Token Storage**: Store tokens securely (consider HttpOnly cookies for refresh tokens)
4. **Token Expiration**: Access tokens expire in 60 minutes, refresh tokens in 7 days
5. **CORS**: Configure CORS properly for your frontend domain

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing/invalid data)
- `401`: Unauthorized (invalid/expired token)
- `500`: Internal Server Error

Error responses include a descriptive message:
```json
{
    "error": "Error description here"
}
```
