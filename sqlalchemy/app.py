
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="somekey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)

class users(db.Model):
    _id=db.Column("id",db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    password=db.Column(db.String(100))
    email=db.Column(db.String(100))

    def __init__(self,name,password,email):
        self.name = name
        self.password = password 
        self.email = email


@app.route('/',methods=["GET", "POST"])
def register():
    

    if request.method=="POST":
        if request.form.get('login') == 'login':
            return redirect(url_for("login"))
        elif request.form.get('register' ) == 'register':    
            usrnm=request.form["unm"]
            session["nu"]=usrnm
            pswd=request.form["upass"]
            session["np"]=pswd

            usr = users(usrnm, pswd, "")
            db.session.add(usr)
            db.session.commit()
            flash("Registration Successfull")
            return redirect(url_for("login"))
            
    else:
        return render_template("reg.html")
        
@app.route('/login',methods=["GET","POST"])
def login():
    flag=0
    if request.method=="POST":
        user=request.form["nam"]
        session["u"]=user
        passwd=request.form["pass"]
        session["p"]=passwd
        values=users.query.all()
        for item in values:
            if user==item.name:
                flag=1
                return redirect(url_for("user"))
        if flag==0:
            flash("User not registered")
            return redirect(url_for("register"))
    else:
        return render_template("login.html")
@app.route('/user', methods=["GET","POST"])
def user():
    if request.method=="GET":
        name=session["u"]
        passwd=session["p"]
        if name != "" and passwd=="123":
            flash("Logged in successfully","info")
            flash(f"Welcome {name}")
        elif name=="":
            flash("Please enter user name","info")
        elif passwd!="123":
            flash("Wrong password","error")
        else:
            flash("Something went wrong","error")
        return render_template("profile.html")
      
    else:
        email=request.form["email"]
        session["em"]=email
        usrnm=session["nu"]
        values=users.query.all()
        for items in values:
            if usrnm==items.name:
                items.email=email
                db.session.commit()


        return redirect(url_for("logout"))

    
        

@app.route('/logout')
def logout():
    user=session["u"]
    passwd=session["p"]
    if user != "" and passwd=="123":
        flash("Logged out successfully","info")
    else:
        flash("Try again","info")
    session.pop("u", None)
    session.pop("p",None)
    session.pop("nu",None)
    session.pop("np",None)
    return redirect(url_for("login"))


@app.route('/admindb')
def view():
    return render_template("admindb.html", values=users.query.all())

if __name__=='__main__':
    db.create_all()
    app.run()