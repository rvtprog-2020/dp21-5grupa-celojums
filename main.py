# Project "Celojums" DP2-1

from flask import Flask, flash, render_template, url_for, request, redirect, session
from pymongo import MongoClient
from bson.json_util import dumps
from random import randint

app = Flask(__name__)
app.secret_key = "hkIbg#45f1_"



# -- PyMongoDB/start -- #

# Login: oleg
# Password: A6muTqLJ1cCEFaOK

client = MongoClient("mongodb+srv://oleg:A6muTqLJ1cCEFaOK@posts-db.gzxb0.mongodb.net/posts?retryWrites=true&w=majority")

db = client.client
client_db = db.client_info

db = client.posts
posts_db = db.posts_info

# -- PyMongoDB/end -- #



@app.route('/', methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route('/home', methods=["GET","POST"])
def home():
    return render_template("home.html")

@app.route('/about-us', methods=["GET","POST"])
def about():
    return render_template("about-us.html")

@app.route('/search-flight', methods=["GET","POST"])
def search():
    return render_template("search-flight.html")

@app.route('/book-flight/<int:id>', methods=["GET","POST"])
def book(id):
    posts_to_book = posts_db.find_one({"id":id})
    l = posts_to_book['seats']
    l = int(l)

    if l <= 0:
        return redirect(url_for("home"))
    
    if "auth" in session:
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
                return render_template("book-flight.html", id=id, from_c=from_c, to_c=to_c, start=start, end=end, price=price)
            else:
                email = session["auth"]

                travels_id = client_db.find_one({"email":email})
                post_db = posts_db.find_one({"id":id})
                
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
                client_db.update_one({"email":email}, {"$set": {"booked":boo}})
                return render_template("successful-payment.html")

        else:
            posts_to_book = posts_db.find_one({"id":id})

            from_c = posts_to_book['from_c']
            to_c = posts_to_book['to_c']
            start = posts_to_book['start']
            end = posts_to_book['end']
            price = posts_to_book['price']
            return render_template("book-flight.html", id=id, from_c=from_c, to_c=to_c, start=start, end=end, price=price)
    else:
        return redirect(url_for("login"))

@app.route('/register', methods=["GET","POST"])
def register():
    if "auth" in session:
        return redirect(url_for("home"))
    else:
        if request.method == 'POST':

            with open('last-id.txt', 'r') as file:
                data = file.read().replace('\n', '')
                id_ = int(data)

            id_ += 1

            with open('last-id.txt', 'a') as file:
                file.truncate(0)
                file.write(str(id_))
                file.close()

            email = request.form['email']
            name = request.form['name']
            last_name = request.form['last-name']
            password = request.form['password']
            email = email.lower()

            a = client_db.find_one({"email":email})
            if a != None:
                a = a['email']

            if a == email:
                flash("This email has already in base")
                return render_template("register.html")

            session["auth"] = email

            client_db.insert_one({"id":id_,"booked":[],"email":email,"name":name,"last-name":last_name,"password":password})
            return render_template("successful-registration.html")
        else:
            return render_template("register.html")

@app.route('/login', methods=["GET","POST"])
def login():
    if "auth" in session:
        return redirect(url_for("home"))
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            email = email.lower()

            a = client_db.find_one({"email":email})
            b = client_db.find_one({"email":email},{"password":password})

            if a != None or b != None:
                a = a['email']
                b = b['password']

            if a != email or b != password:
                flash("User is not found")
                return render_template("login.html")

            session["auth"] = email

            return redirect(url_for("home"))

        else:
            return render_template("login.html")

@app.route('/logout', methods=["GET","POST"])
def logout():
    session.pop("auth", None)
    return redirect(url_for("home"))

@app.route('/control-panel', methods=["GET","POST"])
def panel():
    if "auth" in session:
        if session["auth"] == "admin":
            if request.method == 'POST':

                with open('last-id.txt', 'r') as file:
                    data = file.read().replace('\n', '')
                    id_ = int(data)

                id_ += 1

                with open('last-id.txt', 'a') as file:
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
                return render_template("control-panel.html")
            else:
                return render_template("control-panel.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route('/control-panel/edit/<int:id>', methods=["GET","POST"])
def edit(id):
    if "auth" in session:
        if session["auth"] == "admin":

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

                return redirect(url_for("panel"))
            else:

                posts_to_update = posts_db.find_one({"id":id})

                from_c = posts_to_update['from_c']
                to_c = posts_to_update['to_c']
                agency = posts_to_update['agency']
                start = posts_to_update['start']
                end = posts_to_update['end']
                price = posts_to_update['price']
                seats = posts_to_update['seats']
                return render_template("control-panel-edit.html", id=id, from_c=from_c, to_c=to_c, agency=agency, start=start, end=end, price=price, seats=seats)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route('/control-panel/delete/<int:id>', methods=["GET","POST"])
def delete(id):
    if "auth" in session:
        if session["auth"] == "admin":
            posts_db.delete_one({"id":id})
            return redirect(url_for("panel"))
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route('/data', methods=["GET","POST"])
def data():
    data_flight = posts_db.find()
    data = list(data_flight)
    return dumps(data)

@app.route('/control-panel/books/<int:id>', methods=["GET","POST"])
def books(id):
    if "auth" in session:
        if session["auth"] == "admin":
            post_to_view = posts_db.find_one({"id":id})
            view = post_to_view['booked']
            if view == []:
                view = "Nothing..."
            return render_template("books.html",view=view)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



# -- Start 'main.py' -- #

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)