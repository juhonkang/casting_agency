# Auth0 Setup Guide

This guide walks you through setting up Auth0 authentication for the Trivia API with Role-Based Access Control (RBAC).

## Table of Contents

- [Overview](#overview)
- [Step 1: Create Auth0 Account](#step-1-create-auth0-account)
- [Step 2: Create API](#step-2-create-api)
- [Step 3: Define Permissions](#step-3-define-permissions)
- [Step 4: Create Roles](#step-4-create-roles)
- [Step 5: Create Test Users](#step-5-create-test-users)
- [Step 6: Get JWT Tokens](#step-6-get-jwt-tokens)
- [Step 7: Configure Application](#step-7-configure-application)
- [Testing Authentication](#testing-authentication)
- [Troubleshooting](#troubleshooting)

## Overview

Our Trivia API implements RBAC with two roles:

| Role | Permissions | Description |
|------|-------------|-------------|
| **Trivia User** | `get:questions`, `get:categories` | Can view questions and categories |
| **Trivia Manager** | All permissions | Can create, view, and delete questions |

## Step 1: Create Auth0 Account

1. Go to [https://auth0.com](https://auth0.com)
2. Click "Sign Up"
3. Choose "Sign up with GitHub" (recommended) or email
4. Select **Region**: Choose US or EU based on your location
5. Complete account setup
6. Verify your email address

## Step 2: Create API

An API in Auth0 represents your backend application.

### Create the API

1. Log in to [Auth0 Dashboard](https://manage.auth0.com)
2. Navigate to **Applications → APIs**
3. Click **+ Create API**
4. Configure:
   - **Name**: `Trivia API`
   - **Identifier**: `trivia-api` (This is your `API_AUDIENCE`)
   - **Signing Algorithm**: `RS256`
5. Click **Create**

### Important: Save These Values

You'll need these for your application:

```bash
AUTH0_DOMAIN=your-tenant.us.auth0.com
API_AUDIENCE=trivia-api
ALGORITHMS=["RS256"]
```

**How to find your AUTH0_DOMAIN:**
1. Dashboard → Applications → APIs → Trivia API
2. Look at **Test** tab
3. Copy the domain from the curl example (without `https://`)

Example: `dev-abc123.us.auth0.com`

## Step 3: Define Permissions

Permissions define what actions users can perform.

### Add Permissions to Your API

1. Go to **Applications → APIs → Trivia API**
2. Click **Permissions** tab
3. Add these permissions:

| Permission | Description |
|------------|-------------|
| `get:questions` | View trivia questions |
| `get:categories` | View question categories |
| `post:questions` | Create new questions |
| `delete:questions` | Delete existing questions |

**For each permission:**
1. Enter permission name in **Permission** field (e.g., `get:questions`)
2. Enter description (e.g., "View trivia questions")
3. Click **Add**

### Enable RBAC

1. Still in **Trivia API** settings
2. Click **Settings** tab
3. Scroll to **RBAC Settings**
4. Enable:
   - ✅ **Enable RBAC**
   - ✅ **Add Permissions in the Access Token**
5. Click **Save**

## Step 4: Create Roles

Roles group permissions for easier user management.

### Create Trivia User Role

1. Navigate to **User Management → Roles**
2. Click **+ Create Role**
3. Configure:
   - **Name**: `Trivia User`
   - **Description**: `Basic user who can view questions and categories`
4. Click **Create**
5. Click the **Permissions** tab
6. Click **Add Permissions**
7. Select **Trivia API** from dropdown
8. Check these permissions:
   - ✅ `get:questions`
   - ✅ `get:categories`
9. Click **Add Permissions**

### Create Trivia Manager Role

1. Click **+ Create Role** again
2. Configure:
   - **Name**: `Trivia Manager`
   - **Description**: `Manager who can create, view, and delete questions`
3. Click **Create**
4. Click the **Permissions** tab
5. Click **Add Permissions**
6. Select **Trivia API** from dropdown
7. Check ALL permissions:
   - ✅ `get:questions`
   - ✅ `get:categories`
   - ✅ `post:questions`
   - ✅ `delete:questions`
8. Click **Add Permissions**

## Step 5: Create Test Users

Create test accounts for each role.

### Create Trivia User Account

1. Navigate to **User Management → Users**
2. Click **+ Create User**
3. Configure:
   - **Email**: `trivia-user@test.com` (or your preferred email)
   - **Password**: Create a strong password (save it!)
   - **Connection**: `Username-Password-Authentication`
4. Click **Create**
5. Click on the newly created user
6. Click **Roles** tab
7. Click **Assign Roles**
8. Select **Trivia User**
9. Click **Assign**

### Create Trivia Manager Account

1. Click **+ Create User** again
2. Configure:
   - **Email**: `trivia-manager@test.com`
   - **Password**: Create a strong password (save it!)
   - **Connection**: `Username-Password-Authentication`
3. Click **Create**
4. Click on the newly created user
5. Click **Roles** tab
6. Click **Assign Roles**
7. Select **Trivia Manager**
8. Click **Assign**

## Step 6: Get JWT Tokens

You need valid JWT tokens for testing. There are two methods:

### Method 1: Using Auth0 Test Tool (Easiest)

1. Go to **Applications → APIs → Trivia API**
2. Click **Test** tab
3. Scroll to **Sending the token to the API**
4. You'll see a sample token
5. **However**, this token has ALL permissions, not role-specific

### Method 2: Using Authentication Flow (Recommended)

This generates role-specific tokens for testing.

#### A. Create Application for Token Generation

1. Navigate to **Applications → Applications**
2. Click **+ Create Application**
3. Configure:
   - **Name**: `Trivia Test Client`
   - **Application Type**: Select **Single Page Web Applications**
4. Click **Create**
5. Go to **Settings** tab
6. Configure URLs:
   - **Allowed Callback URLs**: `http://localhost:3000/callback`
   - **Allowed Logout URLs**: `http://localhost:3000`
   - **Allowed Web Origins**: `http://localhost:3000`
7. Scroll down and click **Save Changes**
8. Copy the **Domain** and **Client ID** (you'll need these)

#### B. Generate Tokens Using Auth0 Debugger

1. Go to [https://jwt.io](https://jwt.io)
2. OR use this direct link:

```
https://YOUR_AUTH0_DOMAIN/authorize?
  audience=trivia-api&
  response_type=token&
  client_id=YOUR_CLIENT_ID&
  redirect_uri=https://jwt.io
```

Replace:
- `YOUR_AUTH0_DOMAIN` with your domain (e.g., `dev-abc123.us.auth0.com`)
- `YOUR_CLIENT_ID` with your Client ID from step A

3. Login as `trivia-user@test.com`
4. After authorization, you'll be redirected to jwt.io
5. Copy the `access_token` from the URL
6. This is your **TRIVIA_USER_TOKEN**
7. Logout and repeat for `trivia-manager@test.com` to get **TRIVIA_MANAGER_TOKEN**

#### C. Generate Tokens Using curl (Advanced)

```bash
# Get token for Trivia User
curl --request POST \
  --url https://YOUR_AUTH0_DOMAIN/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"YOUR_CLIENT_ID","client_secret":"YOUR_CLIENT_SECRET","audience":"trivia-api","grant_type":"client_credentials"}'
```

**Note**: This requires Client Secret, which is available in Application Settings.

### Save Your Tokens

Once you have tokens, save them in `backend/setup.sh`:

```bash
export TRIVIA_USER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZC...'
export TRIVIA_MANAGER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZC...'
```

## Step 7: Configure Application

### Update setup.sh

Edit `backend/setup.sh` with your Auth0 credentials:

```bash
#!/bin/bash

# Auth0 Configuration
export AUTH0_DOMAIN='dev-abc123.us.auth0.com'  # Replace with your domain
export ALGORITHMS='["RS256"]'
export API_AUDIENCE='trivia-api'

# JWT Tokens for Testing
export TRIVIA_USER_TOKEN='your-actual-token-here'
export TRIVIA_MANAGER_TOKEN='your-actual-token-here'

# Database Configuration
export database_username='your_username'
export database_password='your_password'
export database_name='trivia'

# Test Database
export test_database_username='your_username'
export test_database_password='your_password'
export test_database_name='trivia_test'

# Flask Configuration
export FLASK_APP=flaskr
export FLASK_ENV=development
```

### Load Environment Variables

**macOS/Linux:**
```bash
cd backend
source setup.sh
```

**Windows (Git Bash):**
```bash
cd backend
source setup.sh
```

**Windows (PowerShell):**
```powershell
cd backend
$env:AUTH0_DOMAIN="dev-abc123.us.auth0.com"
$env:API_AUDIENCE="trivia-api"
$env:ALGORITHMS='["RS256"]'
# ... set other variables
```

## Testing Authentication

### Test with curl

**1. Test without token (should fail):**
```bash
curl http://localhost:5000/questions
```

Expected response:
```json
{
  "code": "authorization_header_missing",
  "description": "Authorization header is expected."
}
```

**2. Test Trivia User (can GET, cannot POST/DELETE):**
```bash
# This should work
curl http://localhost:5000/questions \
  -H "Authorization: Bearer $TRIVIA_USER_TOKEN"

# This should fail with 403
curl -X POST http://localhost:5000/questions \
  -H "Authorization: Bearer $TRIVIA_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Test","answer":"Test","category":1,"difficulty":1}'
```

**3. Test Trivia Manager (should have all permissions):**
```bash
# Should work
curl -X POST http://localhost:5000/questions \
  -H "Authorization: Bearer $TRIVIA_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Manager Test","answer":"Success","category":1,"difficulty":2}'
```

### Run RBAC Tests

```bash
cd backend
source setup.sh
python test_rbac.py
```

Expected output:
```
..........
----------------------------------------------------------------------
Ran 10 tests in 2.456s

OK
```

### Verify Token Contents

Use [jwt.io](https://jwt.io) to decode and inspect your tokens:

1. Go to https://jwt.io
2. Paste your token in the **Encoded** section
3. Check the **Decoded** payload:

```json
{
  "iss": "https://dev-abc123.us.auth0.com/",
  "sub": "auth0|123456789",
  "aud": "trivia-api",
  "iat": 1630000000,
  "exp": 1630086400,
  "azp": "your-client-id",
  "scope": "",
  "permissions": [
    "get:questions",
    "get:categories"
  ]
}
```

Verify:
- ✅ `aud` matches your `API_AUDIENCE`
- ✅ `iss` matches your `AUTH0_DOMAIN`
- ✅ `permissions` array contains expected permissions
- ✅ `exp` (expiration) is in the future

## Troubleshooting

### Issue: "Invalid header" Error

**Cause**: Token format is incorrect

**Solution**:
```bash
# Correct format
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...

# Wrong format
Authorization: eyJhbGciOiJSUzI1NiIs...  # Missing "Bearer "
```

### Issue: "Token expired" Error

**Cause**: JWT tokens expire after 24 hours by default

**Solution**: Generate a new token using Step 6

### Issue: "Permission not found" (403 Error)

**Cause**: User's role doesn't include the required permission

**Solution**:
1. Go to Auth0 Dashboard → Users
2. Click on the test user
3. Verify assigned role under **Roles** tab
4. Check role permissions under User Management → Roles → [Role Name] → Permissions

### Issue: "Incorrect claims" Error

**Cause**: API audience doesn't match

**Solution**:
1. Verify `API_AUDIENCE` in `setup.sh` matches Auth0 API Identifier
2. Regenerate token with correct audience

### Issue: Import Error for `auth`

**Cause**: `auth.py` file not found or has syntax errors

**Solution**:
```bash
# Verify file exists
ls -la backend/auth.py

# Test imports
python
>>> from auth import AuthError, requires_auth
>>> exit()
```

### Issue: "Unable to find appropriate key"

**Cause**: Auth0 domain mismatch or network issue

**Solution**:
1. Verify `AUTH0_DOMAIN` has no `https://` prefix
2. Test connection:
```bash
curl https://YOUR_AUTH0_DOMAIN/.well-known/jwks.json
```

## Token Expiration and Renewal

### Default Expiration

Auth0 tokens expire after:
- **Access Tokens**: 24 hours (default)
- **Refresh Tokens**: Can be configured for longer periods

### Extend Token Lifetime

1. Go to **Applications → APIs → Trivia API → Settings**
2. Scroll to **Token Settings**
3. Configure **Token Expiration (Seconds)**
4. Maximum: 2592000 (30 days)
5. Click **Save**

### Automatic Token Refresh (Future Enhancement)

For production, implement token refresh:

```python
# Example: Token refresh logic
def refresh_token(refresh_token):
    response = requests.post(
        f'https://{AUTH0_DOMAIN}/oauth/token',
        json={
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'refresh_token': refresh_token
        }
    )
    return response.json()['access_token']
```

## Security Best Practices

1. **Never commit tokens to Git**
   - Add `setup.sh` to `.gitignore`
   - Use environment variables in production

2. **Use short-lived tokens in production**
   - Keep default 24-hour expiration
   - Implement refresh token flow

3. **Restrict allowed origins**
   - Update Auth0 Application URLs for production domains
   - Remove localhost URLs in production

4. **Monitor Auth0 logs**
   - Dashboard → Monitoring → Logs
   - Set up alerts for suspicious activity

5. **Rotate secrets regularly**
   - Rotate Client Secrets every 90 days
   - Update tokens when users change roles

## Next Steps

After completing Auth0 setup:

1. ✅ Run `python test_rbac.py` to verify RBAC works
2. ✅ Deploy to production (see DEPLOYMENT.md)
3. ✅ Update Auth0 URLs for production domain
4. ✅ Test with Postman collection
5. ✅ Document for project reviewers

## Additional Resources

- [Auth0 Python Quick Start](https://auth0.com/docs/quickstart/backend/python)
- [Auth0 RBAC Documentation](https://auth0.com/docs/manage-users/access-control/rbac)
- [JWT.io Debugger](https://jwt.io)
- [Auth0 Community Forum](https://community.auth0.com)

---

**Questions?** Check the [README.md](README.md) or refer to Auth0's excellent documentation.
