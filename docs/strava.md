## Strava

### Required environment variables

To use the Strava SSO and activity creation functionality, you need to set the following environment variables in your `.env` file:

- `STRAVA_CLIENT_ID`: Strava OAuth client ID
- `STRAVA_CLIENT_SECRET`: Strava OAuth client secret

### How to Acquire Strava Client ID and Client Secret

1. **Create a Strava Developer Account**:
   - If you don’t already have a Strava account, you need to sign up for one at [Strava](https://www.strava.com/).

2. **Register Your Application**:
   - Go to [Strava Developers](https://developers.strava.com/).
   - Sign in with your Strava account if needed.
   - Navigate to the “Create & Manage Your App” section.
   - Click on "Create New App."
   - Fill in the required details such as Application Name, Category, Club, Website, Authorization Callback Domain, and Scope.
   - After creating the app, you will be provided with a `Client ID` and `Client Secret`.

3. **Set Environment Variables**:
   - Add the `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET` to your `.env` file:
     ```dotenv
     STRAVA_CLIENT_ID=your_strava_client_id
     STRAVA_CLIENT_SECRET=your_strava_client_secret
     ```

### Required APIs

No additional APIs need to be enabled beyond the standard Strava API settings.

### Required scopes for Strava OAuth

When setting up OAuth for your Strava application, ensure that the following scopes are enabled:

- `read`
- `activity:write`

### Example Code for Strava Integration

The following code demonstrates integrating Strava SSO and activity creation functionalities into your application.

```python
from fastapi import FastAPI
from sso.strava import strava_sso, StravaSSO

app = FastAPI()

# OAuth callback endpoint
@app.get("/auth/strava/callback")
async def strava_callback(code: str):
    strava_sso_instance = strava_sso(code)
    if not strava_sso_instance:
        raise HTTPException(status_code=400, detail="Authentication failed")
    user_info = strava_sso_instance.user_info
    return {"user_info": user_info}

# Endpoint to create a new Strava activity
@app.post("/create/strava/activity")
async def create_activity(
    name: str, 
    activity_type: str, 
    start_date: str, 
    elapsed_time: int, 
    description: str = None
):
    strava_sso_instance = StravaSSO()
    activity_response = strava_sso_instance.create_activity(
        name=name, 
        activity_type=activity_type, 
        start_date=start_date, 
        elapsed_time=elapsed_time, 
        description=description
    )
    return {"activity_response": activity_response}
```

### Strava SSO Usage

1. **Authentication**:
   - When a user is redirected back to your application from Strava after OAuth authentication, you’ll receive a `code` parameter.
   - Use this `code` to create an `StravaSSO` instance:
     ```python
     strava_sso_instance = strava_sso(code)
     if not strava_sso_instance:
         raise HTTPException(status_code=400, detail="Authentication failed")
     ```
   - Retrieve user information:
     ```python
     user_info = strava_sso_instance.user_info
     ```

2. **Creating Activities**:
   - With a valid `StravaSSO` instance, you can create activities:
     ```python
     response = strava_sso_instance.create_activity(
         name="Morning Run", 
         activity_type="Run", 
         start_date="2023-10-01T07:00:00Z", 
         elapsed_time=3600, 
         description="Morning run in the park"
     )
     ```