from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()

posts = requests.get(os.getenv("API_ENDPOINT")).json()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
ADDR_EMAIL = os.getenv("ADDR_EMAIL")

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template('index.html', all_posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=ADDR_EMAIL,
                msg=f"{data['message']}"
            )
        return render_template("contact.html", ack="Successfully sent your message!")
    return render_template("contact.html")


@app.route("/post/<int:index>")
def post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
