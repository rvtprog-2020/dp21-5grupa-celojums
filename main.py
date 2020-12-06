from flask import Flask, render_template, url_for, request, redirect, session
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
app.secret_key = "hkIbg#45f1_"

# A6muTqLJ1cCEFaOK

client = MongoClient("mongodb+srv://oleg:A6muTqLJ1cCEFaOK@posts-db.gzxb0.mongodb.net/posts?retryWrites=true&w=majority")

db = client.posts
posts_db = db.posts_info

#posts = {"from":"Latvia, Riga", "to":"Poland, Varsava","agency":"Novatours","start":"10.01.20 8:30","end":"19.01.20 4:30","price":"869","seats":"144"}
#posts_db.insert_one(posts)

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
    return render_template("home.html")



@app.route("/about", methods=["GET","POST"])
def about():
    return render_template("about.html")



@app.route("/search", methods=["GET","POST"])
def search():
    return render_template("search.html")



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
                print(data)
                print(type(data))

                with open('last_id.txt', 'a') as file:
                    file. truncate(0)
                    file.write(str(id_))
                    file.close()

                from_c = request.form['from_c']
                to_c = request.form['to_c']
                agency = request.form['agency']
                start = request.form['start']
                end = request.form['end']
                price = request.form['price']
                seats = request.form['seats']

                posts_db.insert_one({"id":id_, "from_c":from_c, "to_c":to_c,"agency":agency,"start":start,"end":end,"price":price,"seats":seats})
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
    return redirect(url_for("login"))



@app.route("/view", methods=["GET","POST"])
def view():
    if "name" in session and "password" in session:
        if session["name"] == "root" and session["password"] == "sb3125":
            return render_template("view.html")
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



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



if __name__ == "__main__":
    app.run(debug=True)
