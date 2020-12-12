from flask import Flask, flash, render_template, url_for, request, redirect, session
from pymongo import MongoClient
from bson.json_util import dumps
from random import randint

app = Flask(__name__)
app.secret_key = "hkIbg#45f1_"

client = MongoClient("mongodb+srv://oleg:A6muTqLJ1cCEFaOK@posts-db.gzxb0.mongodb.net/posts?retryWrites=true&w=majority")

db = client.posts
posts_db = db.posts_info

db = client.users
users_db = db.users_info

@app.route('/data')
def posts():
    data_posts = posts_db.find()
    data = list(data_posts)
    return dumps(data)

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")



@app.route("/home", methods=["GET","POST"])
def home():
    if "username_user" in session or "password_user" in session:
        return render_template("home-user.html")
    else:
        return render_template("home.html")



@app.route("/about", methods=["GET","POST"])
def about():
    if "username_user" in session or "password_user" in session:
        return render_template("about-user.html")
    else:
        return render_template("about.html")



@app.route("/search", methods=["GET","POST"])
def search():
    if "username_user" in session or "password_user" in session:
        return render_template("search-user.html")
    else:
        return render_template("search.html")



@app.route("/successful", methods=["GET","POST"])
def successful():
    if "username_user" in session or "password_user" in session:
            return render_template("successful-payment.html")
    else:
        return redirect(url_for("home"))



@app.route("/login-user", methods=["GET","POST"])
def login_user():
    if "username_user" in session or "password_user" in session:
        return redirect(url_for("home"))
    else:
        if request.method == 'POST':
            username_user = request.form['username_user']

            username_lower_user = username_user.lower()
            password_user = request.form['password_user']

            a = users_db.find_one({"username_lower":username_lower_user})
            b = users_db.find_one({"username_lower":username_lower_user},{"password":password_user})

            if a != None or b != None:
                a = a['username_lower']
                b = b['password']

            if a != username_lower_user or b != password_user:
                flash("User is not found")
                return render_template("login-user.html")

            session["username_user"] = username_user
            session["password_user"] = password_user

            return redirect(url_for("home"))

        else:
            return render_template("login-user.html")



@app.route("/register", methods=["GET","POST"])
def register():
    if "username_user" in session or "password_user" in session:
        return redirect(url_for("home"))
    else:
        if request.method == 'POST':

            with open('last_id.txt', 'r') as file:
                data = file.read().replace('\n', '')
                id_ = int(data)

            id_ += 1

            with open('last_id.txt', 'a') as file:
                file.truncate(0)
                file.write(str(id_))
                file.close()

            username_user = request.form['username']
            name_user = request.form['name']
            last_name_user = request.form['last-name']
            password_user = request.form['password']
            username_lower_user = username_user
            username_lower_user = username_lower_user.lower()

            a = users_db.find_one({"username_lower":username_lower_user})
            if a != None:
                a = a['username_lower']

            if a == username_lower_user:
                flash("This username has already been taken")
                return render_template("register.html")

            session["username_user"] = username_user
            session["password_user"] = password_user

            users_db.insert_one({"id":id_, "booked":[], "travels_id":[],"username":username_user, "username_lower":username_lower_user, "name":name_user,"last-name":last_name_user,"password":password_user})
            return render_template("successful.html")
        else:
            return render_template("register.html")



@app.route("/login", methods=["GET","POST"])
def login():
    if "name" in session and "password" in session:
        if session["name"] == "root" and session["password"] == "sb3125":
            return redirect(url_for("panel"))

    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        session["name"] = name
        session["password"] = password
        return redirect(url_for("panel"))
    else:
        return render_template("login.html")



@app.route("/panel", methods=["GET","POST"])
def panel():
    if "name" in session and "password" in session:
        if session["name"] == "root" and session["password"] == "sb3125":
            if request.method == 'POST':

                with open('last_id.txt', 'r') as file:
                    data = file.read().replace('\n', '')
                    id_ = int(data)

                id_ += 1

                with open('last_id.txt', 'a') as file:
                    file.truncate(0)
                    file.write(str(id_))
                    file.close()

                from_c = request.form['from_c']
                to_c = request.form['to_c']
                agency = request.form['agency']
                start = request.form['start']
                end = request.form['end']
                price = request.form['price']
                seats = request.form['seats']

                posts_db.insert_one({"id":id_, "booked":[], "from_c":from_c, "to_c":to_c,"agency":agency,"start":start,"end":end,"price":price,"seats":seats})
                return render_template("panel.html")
            else:
                return render_template("panel.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



@app.route("/logout", methods=["GET","POST"])
def logout():
    session.pop("name", None)
    session.pop("password", None)
    session.pop("username_user", None)
    session.pop("password_user", None)
    return redirect(url_for("home"))



@app.route("/view", methods=["GET","POST"])
def view():
    if "name" in session and "password" in session:
        if session["name"] == "root" and session["password"] == "sb3125":
            return render_template("view.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



@app.route("/book/<int:id>", methods=["GET","POST"])
def book(id):

    posts_to_book = posts_db.find_one({"id":id})
    l = posts_to_book['seats']
    l = int(l)

    if l <= 0:
        return redirect(url_for("home"))
    
    if "username_user" in session or "password_user" in session:
        if request.method == 'POST':

            card_number = request.form['card_number']
            date_1 = request.form['date_1']
            date_2 = request.form['date_2']
            name_lastname = request.form['name_lastname']
            cvv = request.form['cvv']

            if card_number == "" or date_1 == "" or date_2 == "" or name_lastname == "" or cvv == "":
                flash("fail")

                from_c = posts_to_book['from_c']
                to_c = posts_to_book['to_c']
                start = posts_to_book['start']
                end = posts_to_book['end']
                price = posts_to_book['price']
                return render_template("book.html", id=id, from_c=from_c, to_c=to_c, start=start, end=end, price=price)
            else:
                name = session["username_user"]
                name = name.lower()

                travels_id = users_db.find_one({"username_lower":name})
                post_db = posts_db.find_one({"id":id})

                travels_id['travels_id'].insert(0,id)
                x = travels_id['travels_id']
                
                booking = randint(100,10000000)

                for i in post_db['booked']:
                    if booking == i:
                        booking = randint(100,10000000)
                
                post_db['booked'].insert(0,booking)
                bo = post_db['booked']

                travels_id['booked'].insert(0,booking)
                boo = post_db['booked']
                
                data = post_db['start']
                data2 = post_db['end']

                flash(f"Your book id is: {booking}")
                flash(f"Flight id is: {id}")
                flash(f"Start date: {data}")
                flash(f"End date: {data2}")


                seats_int = post_db['seats']
                seats_int = int(seats_int)
                seats = seats_int - 1
                
                posts_db.update_one({"id":id}, {"$set": {"booked":bo}})
                posts_db.update_one({"id":id}, {"$set": {"seats":seats}})
                users_db.update_one({"username_lower":name}, {"$set": {"booked":boo}})
                users_db.update_one({"username_lower":name}, {"$set": {"travels_id":x}})
                return redirect(url_for("successful"))

        else:
            posts_to_book = posts_db.find_one({"id":id})

            from_c = posts_to_book['from_c']
            to_c = posts_to_book['to_c']
            start = posts_to_book['start']
            end = posts_to_book['end']
            price = posts_to_book['price']
            return render_template("book.html", id=id, from_c=from_c, to_c=to_c, start=start, end=end, price=price)
    else:
        return redirect(url_for("login_user"))



@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    if "name" in session and "password" in session:
        if session["name"] == "root" and session["password"] == "sb3125":

            if request.method == 'POST':
                form_from_c = request.form['from']
                form_to_c = request.form['to']
                form_agency = request.form['agency']
                form_start = request.form['start']
                form_end = request.form['end']
                form_price = request.form['price']
                form_seats = request.form['seats']

                posts_db.update_one({"id":id}, {"$set": {"from_c":form_from_c}})
                posts_db.update_one({"id":id}, {"$set": {"to_c":form_to_c}})
                posts_db.update_one({"id":id}, {"$set": {"agency":form_agency}})
                posts_db.update_one({"id":id}, {"$set": {"start":form_start}})
                posts_db.update_one({"id":id}, {"$set": {"end":form_end}})
                posts_db.update_one({"id":id}, {"$set": {"price":form_price}})
                posts_db.update_one({"id":id}, {"$set": {"seats":form_seats}})

                return redirect(url_for("view"))
            else:

                posts_to_update = posts_db.find_one({"id":id})

                from_c = posts_to_update['from_c']
                to_c = posts_to_update['to_c']
                agency = posts_to_update['agency']
                start = posts_to_update['start']
                end = posts_to_update['end']
                price = posts_to_update['price']
                seats = posts_to_update['seats']
                return render_template("update.html", id=id, from_c=from_c, to_c=to_c, agency=agency, start=start, end=end, price=price, seats=seats)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



@app.route("/delete/<int:id>", methods=["GET","POST"])
def delete(id):
    if "name" in session and "password" in session:
        if session["name"] == "root" and session["password"] == "sb3125":
            posts_db.delete_one({"id":id})
            return redirect(url_for("view"))
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



@app.route("/view/<int:id>", methods=["GET","POST"])
def view_book(id):
    if "name" in session and "password" in session:
        if session["name"] == "root" and session["password"] == "sb3125":
            post_to_view = posts_db.find_one({"id":id})
            view = post_to_view['booked']
            if view == []:
                view = "Nothing..."
            return render_template("view-book.html",view=view)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)
