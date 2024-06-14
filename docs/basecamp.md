# Basecamp SSO Integration Guide

This guide provides detailed instructions on setting up Basecamp Single Sign-On (SSO) in your application. By following this guide, you'll be able to seamlessly authenticate users using their Basecamp account.

## Prerequisites

Before you begin, ensure you have the following:

1. A [Basecamp](https://basecamp.com/) account.
2. The required environment variables:
   - `BASECAMP_CLIENT_ID`
   - `BASECAMP_CLIENT_SECRET`

## Setting Up Basecamp OAuth

1. **Register an OAuth Application**:
   - Go to the [Basecamp Developer Portal](https://integrate.37signals.com/) and create a new application.
   - Fill in the required details such as application name and redirect URI. The redirect URI will be used later in the integration process.
   - Upon creation, you will receive your `BASECAMP_CLIENT_ID` and `BASECAMP_CLIENT_SECRET`.

2. **Enable Required APIs**:
   - **Auth Code API**: This endpoint is used to obtain the authorization code.
     - URL: `https://launchpad.37signals.com/authorization/new`
   - **Token API**: This endpoint is used to exchange the authorization code for an access token.
     - URL: `https://launchpad.37signals.com/authorization/token`
   - **Users API**: This endpoint retrieves the authenticated user's information.
     - URL: `https://3.basecampapi.com/{account_id}/people/me.json`

3. **Add Environment Variables**:
   - Create a `.env` file in your project's root directory if it does not exist.
   - Add the following entries to the `.env` file:

     ```env
     BASECAMP_CLIENT_ID=your_basecamp_client_id
     BASECAMP_CLIENT_SECRET=your_basecamp_client_secret
     ```
