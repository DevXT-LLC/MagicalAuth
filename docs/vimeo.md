## Vimeo

### Required Environment Variables

To use Vimeo's OAuth system, you need to set up the following environment variables in your `.env` file:

- `VIMEO_CLIENT_ID`: Vimeo OAuth client ID
- `VIMEO_CLIENT_SECRET`: Vimeo OAuth client secret

### Required APIs

Ensure you have the necessary APIs enabled in Vimeo's developer platform. Follow these steps to obtain your `VIMEO_CLIENT_ID` and `VIMEO_CLIENT_SECRET`:

1. **Create a Vimeo Developer Account**: If you don't have one, you'll need to create a Vimeo developer account at [Vimeo Developer](https://developer.vimeo.com/).
2. **Create an App**: Go to your [My Apps](https://developer.vimeo.com/apps) page and create a new app. You will be given a `Client ID` and `Client Secret` which you need to copy and save.
3. **Set Up Scopes**: Ensure that your app has the following scopes enabled:
    - `public`: Access public videos and account details.
    - `private`: Access private videos.
    - `video_files`: Access video files.

4. **Add Environment Variables**: Copy your `VIMEO_CLIENT_ID` and `VIMEO_CLIENT_SECRET` into your `.env` file.

### Required Scopes for Vimeo OAuth

To ensure that your application can access the necessary Vimeo resources, the following scopes must be enabled:

- `public`
- `private`
- `video_files`

### Example Usage

Here is an example of how to use the `VimeoSSO` class to upload a video, fetch user info, and handle OAuth tokens.

#### Step 1: Add Environment Variables

Ensure the `.env` file contains the following lines:

```plaintext
VIMEO_CLIENT_ID=your_client_id_here
VIMEO_CLIENT_SECRET=your_client_secret_here
```

#### Step 2: Implement VimeoSSO in Your Code

Use the `VimeoSSO` class from `vimeo.py` in your project to handle various Vimeo operations.

```python
from vimeo import VimeoSSO, vimeo_sso

# Example of how to retrieve VimeoSSO instance using authorization code
code = 'authorization_code_received_from_vimeo'
redirect_uri = 'your_redirect_uri_here'

vimeo_instance, _ = vimeo_sso(code, redirect_uri)

if vimeo_instance:
    print("Fetched user info:", vimeo_instance.user_info)

    # Example of how to upload a video
    video_file_path = 'path_to_your_video.mp4'
    video_title = 'My Video Title'
    video_description = 'A description of my video.'

    upload_response = vimeo_instance.upload_video(video_file_path, video_title, video_description)
    print("Video uploaded successfully. Response:", upload_response)
else:
    print("Failed to get VimeoSSO instance.")
```

### Notes

- If you encounter any errors, ensure that your `VIMEO_CLIENT_ID` and `VIMEO_CLIENT_SECRET` are set correctly in your environment.
- Ensure the correct scopes are enabled for your application in the Vimeo Developer portal.
- You might need to handle different HTTP response statuses carefully, especially the 401 status which indicates that the access token might need to be refreshed.

By following these steps, you should be able to use Vimeo's OAuth system to authenticate users, fetch user information, and upload videos to Vimeo using the provided `VimeoSSO` class.