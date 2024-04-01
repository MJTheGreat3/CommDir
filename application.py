from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

@app.after_request
def after_request(response):
response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
response.headers["Expires"] = 0
response.headers["Pragma"] = "no-cache"
return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///members.db")

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    
    if request.method == "POST":
    
        if not request.form.get("regnno"):
        return apology("must provide Regn. No.", 403)
        
        elif not request.form.get("password"):
        return apology("must provide password", 403)
        
        rows = db.execute("SELECT * FROM members WHERE RegnNo = :regnno",
        regnno=request.form.get("regnno"))
        
        if not check_password_hash(rows[0]["Password"], request.form.get("password")):
        return apology("invalid regn. no. and/or password", 403)
        
        session["user_id"] = rows[0]["RegnNo"]
        
        return redirect(url_for("directorym"))
    
    else:
        return render_template("loginm.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
    
        if not request.form.get("fname"):
            return apology("must provide first name", 400)
        
        elif not request.form.get("lname"):
            return apology("must provide last name", 400)
        
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        elif not request.form.get("password") == request.form.get("cpassword"):
            return apology("passwords do not match", 400)
        
        elif not request.form.get("maddress"):
            return apology("must provide your Mumbai Address", 400)
        
        elif not request.form.get("famname"):
            return apology("must provide family name", 400)
        
        elif not request.form.get("unit"):
            return apology("must provide unit", 400)
        
        elif not request.form.get("nadi"):
            return apology("must provide native diocese", 400)
        
        elif not request.form.get("napa"):
            return apology("must provide native parish", 400)

        elif not request.form.get("dob"):
            return apology("must provide date of birth", 400)
        
        elif not request.form.get("mob"):
            return apology("must provide date of birth", 400)
        
        elif not request.form.get("yob"):
            return apology("must provide date of birth", 400)
        
        bod = ((request.form.get("dob")) + "-" + (request.form.get("mob")) + "-" + (request.form.get("yob")))
        wbod = ((request.form.get("wdob")) + "-" + (request.form.get("wmob")) + "-" + (request.form.get("wyob")))
        name = ((request.form.get("fname")) + " " + (request.form.get("lname")))
        mem = ((str(request.form.get("regnno"))) + "A")
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO members (RegnNo, MemberId, Name, DateofBirth, FamilyName, NativeDiocese, NativeParish, Unit, MumbaiAddress, KeralaAddress, WeddingAnniversary, ContactNo, Occupation, BloodGroup, Password) VALUES(:regnno, :mem, :name, :bod, :famname, :nadi, :napa, :unit, :maddress, :kaddress, :wbod, :conno, :occp, :bdgp, :password)", regnno = request.form.get("regnno"), mem = mem, name = name, bod = bod, famname = request.form.get("famname"), nadi = request.form.get("nadi"), napa = request.form.get("napa"), unit = request.form.get("unit"), maddress = request.form.get("maddress"), kaddress = request.form.get("kaddress"), wbod = wbod, conno = request.form.get("conno"), occp = request.form.get("occp"), bdgp = request.form.get("bdgp"), password = hash)
        
        if not new_user_id:
            return apology("Registration Number taken", 400)
        
        session["user_id"] = new_user_id
        
        flash("Registered!")
        
        return redirect(url_for("directory"))
    
    else:
        return render_template("register.html")

@app.route("/logina", methods=["GET", "POST"])
def logina():

    session.clear()
    
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        
        elif request.form.get("username") != "MJoseph":
            return apology("username incorrect", 400)
    
        elif request.form.get("password") != "Password":
            return apology("password incorrect", 400)
        
        else:
            return redirect(url_for("directory"))
    else:
        return render_template("logina.html")

@app.route("/directory")
def directory():

    rows = db.execute("SELECT * FROM members")
    return render_template("directory.html", rows=rows)

@app.route("/directorym")
def directorym():

    rows = db.execute("SELECT * FROM members WHERE Activity = 'active'")
    return render_template("directorym.html", rows=rows)

@app.route("/portfolioa/<int:regnno>")
def portfolioa(regnno):

    rows = db.execute("SELECT * FROM members WHERE RegnNo = :no", no = regnno)
    return render_template("portfolioa.html", rows=rows, regnno=regnno)

@app.route("/portfoliom/<int:regnno>")
def portfoliom(regnno):

    rows = db.execute("SELECT * FROM members WHERE RegnNo = :no AND Activity = 'active'", no = regnno)
    return render_template("portfoliom.html", rows=rows, regnno=regnno)

@app.route("/logouta")
def logouta():

    session.clear()
    return redirect(url_for("login"))

@app.route("/logoutm")
@login_required
def logoutm():

    session.clear()
    return redirect(url_for("login"))

@app.route("/change_password_m", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":
    
        if not request.form.get("regnno"):
            return apology("must provide registration number", 400)
        
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)
        
        rows = db.execute("SELECT Password FROM members WHERE RegnNo = :regnno", regnno=request.form.get("regnno"))
    
        if not check_password_hash(rows[0]["Password"], request.form.get("current_password")):
            return apology("invalid password", 400)
        
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)
        
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 400)
        
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 400)
        
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE members SET Password = :hash WHERE RegnNo = :regnno", regnno=request.form.get("regnno"), hash=hash)
        
        flash("Changed!")
        
        return redirect(url_for("directorym"))
    
    return render_template("change_password_m.html")

@app.route("/change_password_a", methods=["GET", "POST"])
def change_passworda():

    if request.method == "POST":
    
        if not request.form.get("user"):
            return apology("must provide username", 400)
        
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)
        
        rows = db.execute("SELECT Password FROM members WHERE RegnNo = :regnno", user_id=session["user_id"])
        
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 400)
        
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)
        
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 400)
        
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 400)
        
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE admin SET Password = :hash WHERE Username = :user", user=request.form.get("user"), hash=hash)
        
        flash("Changed!")
        
        return redirect(url_for("directory"))
    
    else:
        return render_template("change_password_a.html")

@app.route("/add/<int:regnno>/<string:famname>/<string:nadi>/<string:napa>/<string:unit>/<string:maddress>/<string:kaddress>/<string:password>", methods=["GET", "POST"])
def add(regnno, famname, nadi, napa, unit, maddress, kaddress, password):

    if request.method == "POST":
    
        if not request.form.get("fname"):
            return apology("must provide first name", 400)
        
        elif not request.form.get("lname"):
            return apology("must provide last name", 400)
        
        elif not request.form.get("rel"):
            return apology("must provide relation", 400)
        
        elif not request.form.get("dob"):
            return apology("must provide date of birth", 400)
        
        elif not request.form.get("mob"):
            return apology("must provide date of birth", 400)
        
        elif not request.form.get("yob"):
            return apology("must provide date of birth", 400)
        
        bod = ((request.form.get("dob")) + "-" + (request.form.get("mob")) + "-" + (request.form.get("yob")))
        wbod = ((request.form.get("wdob")) + "-" + (request.form.get("wmob")) + "-" + (request.form.get("wyob")))
        name = ((request.form.get("fname")) + " " + (request.form.get("lname")))
        mem = (str(str(regnno) + (request.form.get("mid"))))
        new_user_id = db.execute("INSERT INTO members (RegnNo, MemberId, Name, DateofBirth, Relation, FamilyName, NativeDiocese, NativeParish, Unit, MumbaiAddress, KeralaAddress, WeddingAnniversary, ContactNo, Occupation, BloodGroup, Password) VALUES(:regnno, :mem, :name, :bod, :rel, :famname, :nadi, :napa, :unit, :maddress, :kaddress, :wbod, :conno, :occp, :bdgp, :password)", regnno = regnno, mem = mem, name = name, bod = bod, rel = request.form.get("rel"), famname = famname, nadi = nadi, napa = napa, unit = unit, maddress = maddress, kaddress = kaddress, wbod = wbod, conno = request.form.get("conno"), occp = request.form.get("occp"), bdgp = request.form.get("bdgp"), password = password)
        
        if not new_user_id:
            return apology("Member ID taken", 400)
        
        flash("Registered!")
        
        return redirect(url_for("directory"))
    
    else:
        rows = db.execute("SELECT * FROM members WHERE RegnNo = :no", no=regnno)
        return render_template("add.html", rows=rows)

@app.route("/editor/<string:mem>/<int:regnno>/<string:famname>/<string:nadi>/<string:napa>/<string:unit>/<string:maddress>/<string:kaddress>/<string:password>", methods=["GET", "POST"])
def editor(mem, regnno, famname, nadi, napa, unit, maddress, kaddress, password):
    
    if request.method == "POST":
    
        if not request.form.get("fname"):
            return apology("must provide first name", 400)
        
        elif not request.form.get("lname"):
            return apology("must provide last name", 400)
        
        elif not request.form.get("rel"):
            return apology("must provide relation", 400)
        
        elif not request.form.get("dob"):
            return apology("must provide date of birth", 400)
        
        elif not request.form.get("mob"):
            return apology("must provide date of birth", 400)
        
        elif not request.form.get("yob"):
            return apology("must provide date of birth", 400)
        
        bod = ((request.form.get("dob")) + "-" + (request.form.get("mob")) + "-" + (request.form.get("yob")))
        wbod = ((request.form.get("wdob")) + "-" + (request.form.get("wmob")) + "-" + (request.form.get("wyob")))
        name = ((request.form.get("fname")) + " " + (request.form.get("lname")))
        
        new_user_id = db.execute("UPDATE members SET Name = :name WHERE MemberID = :mem", name=name, mem=mem)
        new_user_id = db.execute("UPDATE members SET Relation = :rel WHERE MemberID = :mem", rel=request.form.get("rel"), mem=mem)
        new_user_id = db.execute("UPDATE members SET DateofBirth = :bod WHERE MemberID = :mem", bod=bod, mem=mem)
        new_user_id = db.execute("UPDATE members SET WeddingAnniversary = :wbod WHERE MemberID = :mem", wbod=wbod, mem=mem)
        new_user_id = db.execute("UPDATE members SET BloodGroup = :bdgp WHERE MemberID = :mem", bdgp=request.form.get("bdgp"), mem=mem)
        new_user_id = db.execute("UPDATE members SET Occupation = :occp WHERE MemberID = :mem", occp=request.form.get("occp"), mem=mem)
        new_user_id = db.execute("UPDATE members SET ContactNo = :conno WHERE MemberID = :mem", conno=request.form.get("conno"), mem=mem)
        
        flash("Registered!")
        
        return redirect(url_for("directory"))
    
    else:
        row = db.execute("SELECT * FROM members WHERE MemberID = :no", no=mem)
        return render_template("editor.html", row=row)

@app.route("/edit/<int:regnno>/<string:famname>/<string:nadi>/<string:napa>/<string:unit>/<string:maddress>/<string:kaddress>/<string:password>", methods=["GET", "POST"])
def edit(regnno, famname, nadi, napa, unit, maddress, kaddress, password):

    rows = db.execute("SELECT * FROM members WHERE RegnNo = :no", no=regnno)
    return render_template("edit.html", rows=rows)

@app.route("/deactivate/<string:mem>/<int:regnno>/<string:famname>/<string:nadi>/<string:napa>/<string:unit>/<string:maddress>/<string:kaddress>/<string:password>", methods=["GET", "POST"])
def deactivate(mem, regnno, famname, nadi, napa, unit, maddress, kaddress, password):

    if request.method == "POST":
        db.execute("UPDATE members SET Activity = 'inactive' WHERE MemberID = :no", no=mem)
        db.execute("UPDATE members SET Comment = :text WHERE MemberID = :no", text=request.form.get("comment"), no=mem)
        return redirect(url_for("directory"))

    else:
        row = db.execute("SELECT * FROM members WHERE MemberID = :no", no=mem)
        return render_template("deactivate.html", row=row)

@app.route("/activate/<string:mem>/<int:regnno>/<string:famname>/<string:nadi>/<string:napa>/<string:unit>/<string:maddress>/<string:kaddress>/<string:password>")
def activate(mem, regnno, famname, nadi, napa, unit, maddress, kaddress, password):

    db.execute("UPDATE members SET Activity = 'active' WHERE MemberID = :no", no=mem)
    return redirect(url_for("directory"))

@app.route("/reset/<int:regnno>")
def reset(regnno):

    db.execute("UPDATE members SET Password = :hash WHERE RegnNo = :no", hash = generate_password_hash('P@$$w0d~'), no=regnno)
    return redirect(url_for("directory"))
