# WSO2 Identity Single Sign-On (SSO) Documentation

This guide provides detailed instructions on how to set up and configure WSO2 Identity Server for Single Sign-On (SSO) in your application. The provided `wso2_identity.py` script allows you to authenticate users and send emails via WSO2 Identity Server.

## Required Environment Variables

To use the provided script, you need to set up the following environment variables:

- `WSO2_CLIENT_ID`: The OAuth client ID obtained from WSO2 Identity Server
- `WSO2_CLIENT_SECRET`: The OAuth client secret obtained from WSO2 Identity Server

## Required APIs

Make sure you have the necessary APIs enabled within your WSO2 Identity Server. Add the `WSO2_CLIENT_ID` and `WSO2_CLIENT_SECRET` environment variables to your `.env` file.

## Required Scopes for WSO2 SSO

- `openid`
- `profile`
- `email`
- `wso2.send_email` (assuming WSO2 has a custom scope for sending emails)

The permissions granted by these scopes will allow your application to access basic user profile information and send emails on behalf of the user.
