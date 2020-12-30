import praw
import smtplib, ssl
import os

from email.message import EmailMessage

# ENV Variables
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_msg(msg_text):

    port = 465
    password = PASSWORD

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(FROM_EMAIL, PASSWORD)

        msg = EmailMessage()
        msg.set_content(msg_text)

        msg['Subject'] = ""
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL

        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

def main():
    # Reddit instance
    reddit = praw.Reddit("redditbot", user_agent="python:redditbot:v1.0 (by /u/Seanp50)")

    subreddit = reddit.subreddit("buildapcsales")

    for submission in subreddit.stream.submissions():
        if "3080" in submission.title:
            link = "https://www.reddit.com" + submission.permalink
            category = submission.title.split()[0]
            msg_text = f"{category} {link}"
            if len(msg_text) > 160:
                msg_text = link

            send_msg(msg_text)


if __name__ == '__main__':
    main()