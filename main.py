import mongo
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "lkjsfdbjgjbs"
db = mongo.DataBase()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.register(username, password):
            session["username"] = username
            return redirect(url_for('index'))
    return render_template("registration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = db.login(username, password)
        if result:
            session["username"] = result["username"]
            return redirect(url_for('index'))
        else:
            return "Invalid username or password"
    return render_template("login.html", username=session.get("username"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        username = session.get("username", False)
        if username:
            title = request.form["title"]
            author = request.form["author"]
            description = request.form["description"]
            link = request.form["link"]
            db.add_book(username, title, author, description, link)
            return redirect(url_for('index'))
        else:
            print("You are not logged in.")
    return render_template("add_book.html")

@app.route("/account")
def account():
    username = session.get("username", False)
    return render_template("account.html", username=username, books=db.get_books(username))

@app.route("/admin", methods=["GET", "POST"])
def adminPanel():
    if db.admin(session["username"]):
        books = db.get_all_books()
        if request.method == "POST":
            book_id = request.form["book_id"]
            action = request.form["action"]
            db.edit_book(book_id, action)
        return render_template("admin.html", books=books)
    else:
        return "404"

@app.route("/about")
def about():
    return render_template("about.html", username=session.get("username"))

@app.route("/rules")
def rules():
    return render_template("rules.html", username=session.get("username"))


if __name__ == "__main__":
    app.run(debug=True)
