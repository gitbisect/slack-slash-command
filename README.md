# slack-slash-command
This is a simple experiment to show how to create a slash command in slack. In this example the slash command will invoke a wordpress CLI command. Thats it.

## secure.json
You need to have a secure.json file in your current directory. I have git-ignored it for security. The format of the contents of that file is in secure.json.example.

## How it works
The wordpress CLI command will work with either the username or the email id. In this case we have decided to use the email ID. This will make it easier when you have used Single-Sign-On, as we have done, to login to WP. 

But Slack does not use email IDs or usernames. It uses its own internal UserID. So we have to translate from slack's UserID to our email. This is what the script `slack_users.py` will help us do. It will generate `slack_user_list.json` when run. You might want to run the script once a day.

*Troubleshooting tip:* If you are using a slack sandbox account, remember that your id in your production account will differ from that in your sandbox account.

