from flask import Flask,request,render_template,redirect
import pymongo
import os
import smtplib, ssl
# from flask_googlemaps import GoogleMaps,Map
from random import randint
from werkzeug.utils import secure_filename


app = Flask(__name__)
# GoogleMaps(app,key="AIzaSyCFZk0815fQx9-tS2SdhebLLiVr_bfPz7o")
app.config['UPLOAD_FOLDER'] ="C:/Users/Suleiman Jabir/Desktop/WorkSpace/website/static"
app.config['ALLOWED_EXT'] = ['PNG','JPG','GIF','JPEG','AVI','MP4','MWV']
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")  
db = client.arewastack_database      
data = db.user 


code = ""

em = ""
_id = ""
user_name = ""
buss_name = ""
buss_type = ""
buss_loct = ""
manager = ""
bank = ""
psw = ""
account_no = ""
pro_name=""
pro_price=""
logged = False

def allowed(filename):
    if filename == "":
        return False
    if not "." in filename:
        return False
    ext = filename.rsplit(".",1)[1]
    if ext.upper() in app.config['ALLOWED_EXT']:
        return True
@app.route("/",methods=['POST','GET'])
def index():
    
    a =  data.find()
    product = [d for d in data.find({"product":"product"})]
    try:
        return render_template("index.html", product = product,d=a,logged = logged)
    except Exception:
        return render_template("index.html", product = product,d=a)
@app.route("/home",methods=['POST','GET'])
def home():
    err="The Username or Password you entered is Incorrect!,\n "+"Please Check and try again!"
    product = [d for d in data.find({"product":"product"})]
    a = data.find({"verified":True})
    if request.method=='POST':
        
        global _id
        _id = request.form['_id']
        psw = request.form['psw']
        account = data.find_one({"buss_name":_id,"psw":psw})
        
        if data.find_one({"buss_name":_id,"psw":psw,"verified":True}) is not None:
            global logged
            logged = True
            global bank,account_no
            bank = account['bank']
            account_no = account['account_no']
            return render_template("index.html", product = product,logged=logged\
            ,bank = bank, account_no = account_no)
        else:
            return render_template("login.html",err=err)
    return render_template("index.html", product = product,logged=logged)
    
@app.route("/upload",methods=['POST'])
def upload():
    global pro_price,pro_name
    pro_name = request.form['pro_name']
    pro_price = request.form['pro_price']
    pro_dsc = request.form['pro_dsc']
    if request.files:
        image = request.files['pro_file']
        if allowed(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            data.insert({"product":"product",\
            "pro_name":pro_name,"pro_price":pro_price,"pro_dsc":pro_dsc,\
            "pro_file":filename,"account_no":account_no,"bank":bank})
            return redirect("home")
        
@app.route("/registered",methods=['POST'])
def registered():
    global email,user_name,buss_name,buss_type,buss_loct,manager,bank,psw,account_no
    email = request.form['buss_contact']
    
    user_name = request.form['user_name']
    buss_name = request.form['buss_name']
    buss_type = request.form['buss_type']
    buss_loct = request.form['buss_loct']
    manager = request.form['manager']
    bank = request.form['bank_name']
    psw = request.form['psw']
    account_no = request.form['account_no']
    a=randint(0,9)
    b=randint(0,9)
    c=randint(0,9)
    d=randint(0,9)
    e=randint(0,9)
    f=randint(0,9)
    global code
    code = str(a)+str(b)+str(c)+str(d)+str(e)+str(f)
    global em
    if "," in email:
        
        em =email.rsplit(",",1)[0]
    else:
        
        em = email
    data.insert({"account":"account","email":em,"user_name":user_name,\
    "buss_name":buss_name,"buss_type":buss_type,"location":buss_loct,\
    "manager":manager,"bank":bank,"account_no":account_no,"verified":False,"psw":psw})
    try:
        port = 587
        smtp_server = "smtp.gmail.com"
        sender_mail = "arewastack@gmail.com"
        reciever= e
        password = "arewa1234"
        message= code
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server,port) as server:
            server.starttls(context=context)
            server.login(sender_mail,password)
            server.sendmail(sender_mail,reciever,message)
            return render_template("otp.html",e=em)
    except Exception:
        # return "<h1>Error : 5000</h1><br><li>Check weather your email is correct </li>\
        # <li>check your Connection</li>"
        return render_template("otp.html",otp=code,e=em)
        
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/order")
def order():
    return render_template("order.html")
@app.route("/notification")
def notification():
    return render_template("notification.html")
@app.route("/cart")
def cart():
    cart =  data.find({"cart":user_name})
    prices = [int(d['pro_price']) for d in data.find({"cart":user_name})]
    total = sum(prices)
    return render_template("cart.html", cart= cart,total = total)
# @app.route("/map")
# def map():
#     mymap = Map(
#         identifier = "veiw-side",
#         varname = "mymap",
#         style ="height:50vh;width:80vw;margin:0;",
#         lat = 37.449,
#         lng = 122.1419,
#         zoom = 15,
#         makers = [(37.4419, -122.1419)]
#     )
#     return render_template("map.html", mymap = mymap)
@app.route("/otp",methods=['POST'])
def otp():
    err="Failed to verify!"
    
    verify = request.form['verify']
    if verify==code:
        print(em)
        data.update({"verified":False},{"user_name":user_name\
        ,"buss_name":buss_name,"buss_type":buss_type,"buss_loct":buss_loct\
        ,"manager":manager,"bank":bank,"psw":psw,"account_no":account_no,\
        "verified":True})
        data.remove({"verified":False})
        return redirect("home")
    else:
        return render_template("otp.html",err=err)
@app.route("/purchase",methods=['POST'])
def purchase():
    value = request.form["name"]
    price = request.form["price"]
    
    data.insert({"cart":user_name,"pro_name":value,"pro_price":price})
    return redirect("home")

if __name__=="__main__":
    app.run(debug=True,host="127.0.0.1",port="4000",use_reloader=True)