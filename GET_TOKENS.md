# 🔑 How to Get Auth0 JWT Tokens

## Quick Method (Easiest)

### Step 1: Go to Auth0 Dashboard

1. Visit: https://manage.auth0.com/
2. Login with your Auth0 account
3. Select your tenant (dev-8607typd5q1j6mig)

### Step 2: Get Token via API Test Tab

**Method A: Using API Test Tab**

1. Go to **Applications** → **APIs**
2. Click on **Trivia API** (or your API name)
3. Click the **Test** tab
4. You'll see a section "Sending a Test Request"
5. Click **Copy Token** button
6. This gives you a token with ALL permissions

⚠️ **Issue:** This gives you a Machine-to-Machine token with all permissions, not role-specific tokens.

**Method B: Using Test Application (RECOMMENDED)**

### Step 3: Create Test Application (If Not Created)

1. Go to **Applications** → **Applications**
2. Click **Create Application**
3. Name: `Trivia Test App`
4. Type: **Single Page Application**
5. Click **Create**

### Step 4: Configure Test Application

1. Click on your new application
2. Go to **Settings** tab
3. Set **Allowed Callback URLs**:
   ```
   http://localhost:3000/callback,
   https://jwt.io
   ```
4. Set **Allowed Logout URLs**:
   ```
   http://localhost:3000
   ```
5. Set **Allowed Web Origins**:
   ```
   http://localhost:3000
   ```
6. Scroll down and click **Save Changes**

### Step 5: Enable API for Application

1. Go to **APIs** → **Trivia API**
2. Click **Machine to Machine Applications** tab
3. Find your test application
4. Toggle it ON (authorized)
5. Expand it and select permissions
6. Click **Update**

### Step 6: Create Test Users

1. Go to **User Management** → **Users**
2. Click **Create User**

**User 1: Trivia User (Read-Only)**
- Email: `triviauser@test.com`
- Password: `Test1234!` (or your choice)
- Connection: Username-Password-Authentication
- Click **Create**

**User 2: Trivia Manager (Full Access)**
- Email: `triviamanager@test.com`
- Password: `Test1234!` (or your choice)
- Connection: Username-Password-Authentication
- Click **Create**

### Step 7: Assign Roles to Users

**For Trivia User:**
1. Click on `triviauser@test.com`
2. Go to **Roles** tab
3. Click **Assign Roles**
4. Select **Trivia User**
5. Click **Assign**

**For Trivia Manager:**
1. Click on `triviamanager@test.com`
2. Go to **Roles** tab
3. Click **Assign Roles**
4. Select **Trivia Manager**
5. Click **Assign**

---

## 🎯 Getting Actual Tokens

### Option 1: Using Auth0 Login Page (EASIEST)

1. Open this URL in your browser (replace CLIENT_ID):
   ```
   https://dev-8607typd5q1j6mig.us.auth0.com/authorize?
   audience=trivia-api&
   response_type=token&
   client_id=YOUR_CLIENT_ID&
   redirect_uri=https://jwt.io&
   scope=openid profile email
   ```

2. **Get YOUR_CLIENT_ID**:
   - Go to Applications → Trivia Test App → Settings
   - Copy the **Client ID**

3. **Full URL Example**:
   ```
   https://dev-8607typd5q1j6mig.us.auth0.com/authorize?audience=trivia-api&response_type=token&client_id=YOUR_CLIENT_ID&redirect_uri=https://jwt.io&scope=openid%20profile%20email
   ```

4. **Login as each user**:
   - Login as `triviauser@test.com` → Copy token from URL
   - Logout and login as `triviamanager@test.com` → Copy token from URL

5. **Extract Token**:
   - After login, you'll be redirected to jwt.io
   - The URL will contain `#access_token=eyJhbG...`
   - Copy everything after `access_token=` until `&token_type`

### Option 2: Using Postman

1. Open Postman
2. Create new request
3. Go to **Authorization** tab
4. Type: **OAuth 2.0**
5. Configure:
   - Grant Type: `Authorization Code`
   - Callback URL: `https://jwt.io`
   - Auth URL: `https://dev-8607typd5q1j6mig.us.auth0.com/authorize`
   - Access Token URL: `https://dev-8607typd5q1j6mig.us.auth0.com/oauth/token`
   - Client ID: (from your app settings)
   - Scope: `openid profile email`
   - Audience: `trivia-api`
6. Click **Get New Access Token**
7. Login with test user
8. Copy the token

### Option 3: Using cURL (Command Line)

**For Machine-to-Machine (not role-specific):**

```bash
curl --request POST \
  --url https://dev-8607typd5q1j6mig.us.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{
    "client_id":"YOUR_CLIENT_ID",
    "client_secret":"YOUR_CLIENT_SECRET",
    "audience":"trivia-api",
    "grant_type":"client_credentials"
  }'
```

Get CLIENT_ID and CLIENT_SECRET from your M2M application settings.

---

## 📝 What to Do With Tokens

### 1. Update setup.sh

Once you have the tokens, update `backend/setup.sh`:

```bash
#!/bin/bash

# Auth0 Configuration
export AUTH0_DOMAIN='dev-8607typd5q1j6mig.us.auth0.com'
export ALGORITHMS='["RS256"]'
export API_AUDIENCE='trivia-api'

# JWT Tokens (REPLACE WITH YOUR ACTUAL TOKENS)
export TRIVIA_USER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik...'
export TRIVIA_MANAGER_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik...'
```

### 2. Test Tokens Locally

```bash
cd backend
source setup.sh

# Test User token
curl http://localhost:5000/questions \
  -H "Authorization: Bearer $TRIVIA_USER_TOKEN"

# Test Manager token
curl -X POST http://localhost:5000/questions \
  -H "Authorization: Bearer $TRIVIA_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Test","answer":"Test","category":"1","difficulty":2}'
```

### 3. Test Against Live API

```bash
# Test User token
curl https://trivia-api.onrender.com/questions \
  -H "Authorization: Bearer $TRIVIA_USER_TOKEN"

# Test Manager token (can POST)
curl -X POST https://trivia-api.onrender.com/questions \
  -H "Authorization: Bearer $TRIVIA_MANAGER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Live Test","answer":"Success","category":"1","difficulty":2}'

# Test User token trying to POST (should fail with 403)
curl -X POST https://trivia-api.onrender.com/questions \
  -H "Authorization: Bearer $TRIVIA_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Should Fail","answer":"403","category":"1","difficulty":2}'
```

---

## 🔍 Verify Your Tokens

### Method 1: Using jwt.io

1. Go to https://jwt.io
2. Paste your token in the **Encoded** section
3. Check the **Decoded** section:
   - `iss` should be `https://dev-8607typd5q1j6mig.us.auth0.com/`
   - `aud` should be `trivia-api`
   - `permissions` should list the correct permissions

**Trivia User Token Should Have:**
```json
"permissions": [
  "get:questions",
  "get:categories"
]
```

**Trivia Manager Token Should Have:**
```json
"permissions": [
  "get:questions",
  "get:categories",
  "post:questions",
  "delete:questions"
]
```

### Method 2: Test with API

```bash
# This should succeed (User has get:questions)
curl https://trivia-api.onrender.com/questions \
  -H "Authorization: Bearer $TRIVIA_USER_TOKEN"

# This should FAIL with 403 (User lacks post:questions)
curl -X POST https://trivia-api.onrender.com/questions \
  -H "Authorization: Bearer $TRIVIA_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"Test","answer":"Test","category":"1","difficulty":2}'
```

---

## ⚠️ Token Expiration

**Important Notes:**

1. **Tokens expire after 24 hours** by default
2. You'll need to generate new tokens before Udacity submission
3. Generate tokens RIGHT BEFORE submitting to Udacity
4. Don't commit tokens to GitHub (they're in setup.sh which is gitignored)

---

## 🎯 Quick Summary

**Easiest Way to Get Tokens:**

1. Create a Single Page Application in Auth0
2. Get the Client ID
3. Open this URL (replace YOUR_CLIENT_ID):
   ```
   https://dev-8607typd5q1j6mig.us.auth0.com/authorize?audience=trivia-api&response_type=token&client_id=YOUR_CLIENT_ID&redirect_uri=https://jwt.io
   ```
4. Login as `triviauser@test.com` → Copy token
5. Logout and login as `triviamanager@test.com` → Copy token
6. Update setup.sh with both tokens
7. Test with live API

**Total Time:** 10-15 minutes

---

## 📞 Need Help?

If you have issues:

1. **Check Auth0 Dashboard**:
   - Verify API is created
   - Verify roles have permissions
   - Verify users have roles assigned

2. **Check Token at jwt.io**:
   - Verify `aud` is `trivia-api`
   - Verify `permissions` array is present
   - Verify token hasn't expired (`exp` field)

3. **Test Response**:
   - 401 = No token or invalid token
   - 403 = Valid token but missing permission
   - 200 = Success!

---

**Last Updated:** 2025-10-25
**Auth0 Domain:** dev-8607typd5q1j6mig.us.auth0.com
**API Audience:** trivia-api
