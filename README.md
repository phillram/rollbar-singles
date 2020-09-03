# Rollbar Singles

This is a collection of scripts to be used with [Rollbar's](http://rollbar.com/) service.
They are meant to be individual and singular scripts. The scripts themselves are titled and annotated to be as user friendly as possible.

## Installing Python requirements
You may not need all the packages in the requirements file, but you can install them to your Python instance:

```
pip install -r requirements.txt
```

## Finding access tokens
These scripts use either the account or project access tokens.  Just  copy and paste your own in the appropriate `token` variable. I've denoted them with  either a `project` or `account` prefix to let you know which ones you'd need.

To find `account` tokens go to the Rollbar dashboard. Click on your icon in the bottom left -> `Manage Account Settings` -> `Account Access Tokens`. This will contain your read and write tokens. You'll use these values to fill in the values for:

- `account_read_token`
- `account_write_token`.

To find your `project` tokens go to the Rollbar dashboard. Click on Settings -> Select a project -> `Project Access Tokens`. These will contain the various tokens associated with this specific project.  You'll use these values to fill in the values for:
- `project_post_client_item_token`
- `project_post_server_item_token`
- `project_read_token`
- `project_write_token`

