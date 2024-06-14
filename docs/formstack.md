## Formstack

### Required Environment Variables

To use the FormstackSSO class and its methods, you need to set up the following environment variables in your `.env` file:

- `FORMSTACK_CLIENT_ID`: Your Formstack OAuth client ID
- `FORMSTACK_CLIENT_SECRET`: Your Formstack OAuth client secret

You can get these credentials by following these steps:

1. **Create a Formstack Application**: 
    - Log in to your Formstack account.
    - Navigate to the "Account" section and select "API" from the sidebar menu.
    - Click on "Add Application" to create a new app.
    - Fill in the necessary details such as the app name and description.
    - Make sure to note down the generated `Client ID` and `Client Secret` as you will need them to set up the environment variables.

2. **Add Environment Variables**:
    - Open your `.env` file.
    - Add the following lines, replacing the placeholder values with your actual Formstack credentials:

    ```plaintext
    FORMSTACK_CLIENT_ID=your_formstack_client_id
    FORMSTACK_CLIENT_SECRET=your_formstack_client_secret
    ```

### Required APIs

Ensure that the necessary APIs are enabled in your Formstack account:

- **User API**: This API allows you to access user information such as first name, last name, and email address.
- **Form API**: This API allows you to manage forms, including sending form submissions.

### Required Scopes for Formstack OAuth

When setting up OAuth for Formstack, make sure you request the following scopes:

- `formstack:read`: Allows you to read data from Formstack, such as user information.
- `formstack:write`: Allows you to write data to Formstack, such as submitting form data.

### Example Usage

Here is an example of how you can use the provided class `FormstackSSO`:

1. **Create an Instance of FormstackSSO**:

    ```python
    from sso.formstack import FormstackSSO

    formstack_sso_instance = FormstackSSO(access_token='your_access_token', refresh_token='your_refresh_token')
    ```

2. **Retrieve User Information**:

    ```python
    user_info = formstack_sso_instance.user_info
    print(user_info)  # Output: {'email': 'user@example.com', 'first_name': 'John', 'last_name': 'Doe'}
    ```

3. **Send Form Submission**:

    ```python
    form_id = 'your_formstack_form_id'
    submission_data = {
        'field_1': 'value_1',
        'field_2': 'value_2',
        # Add other form fields and values as required
    }
    response = formstack_sso_instance.send_form_submission(form_id, submission_data)
    print(response)
    ```

### OAuth Flow

The `formstack_sso` function facilitates the OAuth flow:

1. **Get Authorization Code**:
    - Direct the user to the Formstack authorization URL to get an authorization code.

2. **Exchange Authorization Code for Tokens**:

    ```python
    from sso.formstack import formstack_sso
    
    code = 'authorization_code_received_from_formstack'
    redirect_uri = 'your_redirect_uri'  # Optional
    formstack_sso_instance = formstack_sso(code, redirect_uri)
    ```

3. **Use the FormstackSSO Instance**:
    - Once you have the instance, you can use it to manage user info and form submissions as shown in the examples above.

By following these steps, you should be able to set up and use the Formstack SSO integration in your application seamlessly.