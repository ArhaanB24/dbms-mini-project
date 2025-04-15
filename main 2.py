from flask import Flask,render_template,redirect,request,url_for,session,flash,jsonify
import random,string
from werkzeug.utils import secure_filename
from mailsend import sendmail
from supabase import create_client,StorageException,PostgrestAPIError
from datetime import timedelta,datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pymupdf 
from pathlib import Path
import markdown
import requests

#check cicd
app  = Flask(__name__)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
CAPTCHA_SECRET_KEY = os.environ.get("CAPTCHA_SECRET_KEY")
CAPTCHA_SITE_KEY = os.environ.get("CAPTCHA_SITE _KEY")
VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
app.secret_key = "please_work"
supabase = create_client(url,key)
genai.configure(api_key=GOOGLE_API_KEY)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=100)

@app.route("/",methods=["GET","POST"])
def index():
    session.permanent = True
    false_otp =False
    id = ""
    navsub = {}
    firstname = ""
    lastname = ""
    username = ""
    mail = ""
    password = ""
    num = ""
    subjectlst = []
    mode=''
    phone = ""
    otp = ""
    signinmail = ""
    checkuser = []
    specialchars=['@',"#",'$','%','^','&',"*","(",")","-","+","=","{","}","[","]",";",":","<",">","?","/",","]
    personal_storage = []
    validusername=True
    if session.get("user"):
        print(f"id:{session.get('user')}")
        return redirect(url_for("home",id=session.get("user")))
    if not session.get("user"):
        print("Shit doesnt exist")
        print(f"id:{session.get('user')}")
    if request.method == "POST":
        data=request.form.get("flag")
        if(data =='signup'):
            print("in signup")
            g_captcha_response = request.form["g-recaptcha-response"]
            check_bot = requests.post(url=f"{VERIFY_URL}?secret={CAPTCHA_SECRET_KEY}&response={g_captcha_response}").json()
            # print(check_bot)
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            username = request.form["username"]
            mail = request.form["email"].lower()
            num = int(request.form["numsub"])
            for i in username:
                if i in specialchars:
                    validusername=False
            if len(username)>30:
                validusername=False
            if not validusername:
                return render_template("invalidusername.html")
            userslst = supabase.table('users').select("*").eq('username',username).execute().data
            checkemail = supabase.table('users').select("*").eq('email',mail).execute().data
            if len(checkemail)>0:
                return render_template("usedemail.html")
            if(len(userslst)==0) and check_bot["score"] > 0.5:
                mode='sign-up-mode'
                for x in range(num):
                    try: 
                        subject = request.form[f"subject_{x}"].upper()
                        if subject == "CAL":
                            subject = "CALCULUS"
                        elif subject == "CALC":
                            subject = "CALCULUS"
                        elif subject == "PS" or subject == "P&S":
                            subject = "PES"
                        elif subject == "EOB":
                            subject = "EB"
                        if subject != "" and subject != " " and len(subject)!=0 and subject not in subjectlst:
                            subject = subject.strip()
                            subjectlst.append(subject)
                        if subjectlst:
                            session["subjectlist"] = str(subjectlst)

                            session["data"] = eval(session.get("subjectlist"))[0]
                    except KeyError:
                        pass
                try:
                    password = request.form["password"].strip()
                except KeyError:
                    pass
                if not session.get("otp"):
                    otp = "".join(random.sample(string.digits,6))
                    session["otp"] = otp
                sendmail(username,mail=mail,message=f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
</head>
<body style="color:  #F9F9F9;font-family: 'Poppins', sans-serif;">
    <div style="height: 50vh;background-color: #232323;">
    <h2 style="margin-left: 1rem;">Hello!<span style="margin-left: 0.3rem;color: #7655d2;"> {username}</span>,<br>Welcome To Our Portal!</h2>
    <h2 style="margin-left: 1rem;">Your OTP is: <span style="color: red;margin-left: 0.3rem;">{session.get("otp")}</spans></h2>
    </div>
</body>
</html> """)
                if password == session.get('otp'):
                    session["lastactive"] = datetime.now()
                    now = datetime.now()
                    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                    supabase.table('users').insert({"firstname": firstname,"lastname": lastname,"username": username,"email": mail,"subjects": session.get("subjectlist"),"lastactive":formatted_time}).execute()
                    id = supabase.table("users").select("id").eq("username",username).execute().data[0]["id"]
                    session["flag"] = 0
                    session["user"] = id
                    print(f"id:{session.get('user')} yele:{id}")
                    session.pop("otp")
                    return redirect(url_for("home",id=id))
            else:
                mode=''
                errorflag=0
                userdata = supabase.table('users').select("*").eq('username',username).execute().data[0]
                if(userdata['username']==username):
                    errorflag=1
                elif(userdata['email']==mail):
                    errorflag=2
                try:
                    session.pop("otp")
                except KeyError:
                    pass
                session["flag"] = 0
                return render_template('usedusername.html')
        elif(data =='signin'):
                g_captcha_response = request.form["g-recaptcha-response"]
                check_bot = requests.post(url=f"{VERIFY_URL}?secret={CAPTCHA_SECRET_KEY}&response={g_captcha_response}").json()
                navsub = {}
                signinmail = request.form["signinmail"].lower()
                if signinmail == "tusharislove":
                    return redirect("tusharjadhav")
                try:
                    password = request.form["password"].strip()
                except KeyError:
                    pass
                checkuser = supabase.table('users').select("email,username").eq('email',signinmail).execute().data
                if checkuser and check_bot["score"] > 0.5:
                    checkpass = supabase.table('users').select("otp").eq('email',signinmail).execute().data[0]["otp"]
                    if len(password) == 0:
                        otp = "".join(random.sample(string.digits,6))
                        supabase.table('users').update({"otp":otp}).eq('email',signinmail).execute()
                        checkpass = supabase.table('users').select("otp").eq('email',signinmail).execute().data[0]["otp"]
                    elif len(password) == 6 and password!=checkpass:
                        otp = "".join(random.sample(string.digits,6))
                        supabase.table('users').update({"otp":otp}).eq('email',signinmail).execute()
                        checkpass = supabase.table('users').select("otp").eq('email',signinmail).execute().data[0]["otp"]
                    elif checkpass == "0":
                        otp = "".join(random.sample(string.digits,6))
                        supabase.table('users').update({"otp":otp}).eq('email',signinmail).execute()
                        checkpass = supabase.table('users').select("otp").eq('email',signinmail).execute().data[0]["otp"]
                    sendmail(checkuser[0]["username"],mail=signinmail,message=f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">
</head>
<body style="color:  #F9F9F9;font-family: 'Poppins', sans-serif;">
    <div style="height: 50vh;background-color: #232323;">
    <h2 style="margin-left: 1rem;">Hello!<span style="margin-left: 0.3rem;color: #7655d2;"> {checkuser[0]["username"]}</span>,<br>Welcome Back To Our Portal!</h2>
    <h2 style="margin-left: 1rem;">Your OTP is: <span style="color: red;margin-left: 0.3rem;">{checkpass}</spans></h2>
    </div>
</body>
</html>
""")
                    flash("Yerwada")           
                    print("checkpass: ",checkpass,"password: ",password)         
                    if password == checkpass:
                        session["lastactive"] = datetime.now()
                        now = datetime.now()
                        formatted_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                        supabase.table('users').update({"lastactive":formatted_time}).eq("email",signinmail).execute()
                        tempdict = supabase.table('users').select("*").eq('otp',checkpass).execute().data
                        tempdict=tempdict[0]
                        try:
                            session["data"] = eval(tempdict["subjects"])[0]
                        except ValueError:
                            pass
                        for i,j in list(tempdict.items()):
                            navsub[i] = j
                        session['_flashes'].clear() 
                        session["user"] = navsub["id"]
                        return redirect(url_for("home",id=navsub["id"]))
                    elif password and password != checkpass:
                        false_otp = True
                        flash("Incorrect OTP")
                else:
                    flash("Please Sign Up first!")
    return render_template("index.html",false_otp=false_otp,checkuser=checkuser,signinmail=signinmail,phone=phone,mode=mode,num=num,firstname=firstname,lastname=lastname,username=username,mail=mail,id=id,password=password)

@app.route("/home/<id>",methods=["POST","GET"])
def home(id):
    navsub = supabase.table('users').select('*').eq('id',id).execute().data[0]
    favoritelist = supabase.table('users').select('favorites').eq('id',id).execute().data[0]["favorites"]
    datalist = []
    preview = ""
    tempnavsub = eval(navsub["subjects"])
    data = session.get("data")
    datalist = supabase.table('notes').select('*').eq('subjectname',data).execute().data
    active = ""
    active_r = ""
    active_u = "" 
    num= 0
    session["flag"] = 0
    print("Time: ",session.get("lastactive"))
    nikhil = "New Semester New Subjects?Click on the profile icon above to remove old subjects and add the new ones"
    if navsub["id"] == "7d4bb40a-4f0c-4074-95a1-b45ad6cc61ee":
        nikhil = "You can add and remove subjects by clicking on the profile icon on the top right corner!"
    if navsub["id"] == "8659567f-15f1-48b1-b53e-d8528fef3b25":
        nikhil = nikhil+'Nikhil says,"sexy ass notes bhai"'
    session["lastactive"] = datetime.now()
    customcolor = navsub["color"]
    print("CUSTOM COLOR ",customcolor)
    if not favoritelist:
        favoritelist = ""
    if not session.get("user"):
        return redirect(url_for("index"))
    if session.get("user") != id:
        return render_template("invalidurl.html")
    if request.method == "GET":
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        supabase.table('users').update({'lastactive':formatted_time}).eq('id',id).execute()
    if request.method == "POST":
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        supabase.table('users').update({'lastactive':formatted_time}).eq('id',id).execute()
        signout = request.form.get("signout")
        if signout:
            session.pop("lastactive")
            session.pop("user")
            now = datetime.now()
            formatted_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            supabase.table('users').update({'lastactive':formatted_time}).eq('id',id).execute()
            print("Im here")
            return redirect("/")
        try:
            data = request.form.get("navbarsubject")
            if data != None:
                session["data"] = data
                
                datalist = supabase.table('notes').select('*').eq('subjectname',data).execute().data
        except KeyError:
            pass
        favorite = request.form.get("favorite")
        print(data)
        if favorite and favorite not in str(favoritelist):
            data = session.get("data")
            datalist = supabase.table('notes').select('*').eq('subjectname',data).execute().data
            favoritelist += " " + favorite
            supabase.table('users').update({'favorites':favoritelist}).eq('id',id).execute()
        elif favorite and (favorite in favoritelist):
            data = session.get("data")
            datalist = supabase.table('notes').select('*').eq('subjectname',data).execute().data
            favoritelist = favoritelist.replace(favorite,"")
            supabase.table('users').update({'favorites':favoritelist}).eq('id',id).execute()
        try:
            num = int(request.form["numsub"]) 
            username = navsub["username"]
            print(num)
            if num:
                active = "active"
            try:
                for x in range(num):
                    subject = request.form[f"subject_{x}"].upper()
                    print(subject)
                    if subject != "" and subject != " " and len(subject)!=0 and subject not in tempnavsub:
                        subject = subject.strip()
                        tempnavsub.append(subject)
                navsub["subjects"] = str(tempnavsub)
                supabase.table('users').update({'subjects':tempnavsub}).eq('username',username).execute()
                num = 0
            except KeyError:
                pass
        except KeyError:
            pass
        try:
            tempnavsub = eval(navsub["subjects"])
            username = navsub["username"]
            editsub = request.form.get("editsubject")
            if editsub:
                active_r = "active"
            else:
                active_r = ""
            try:
                if editsub == "removeall":
                    tempnavsub.clear()
                    supabase.table('users').update({'subjects':tempnavsub}).eq('username',username).execute()
                    navsub["subjects"] = str(tempnavsub)
                    print(tempnavsub)
                else:
                    tempnavsub.remove(editsub)
                    supabase.table('users').update({'subjects':tempnavsub}).eq('username',username).execute()
                    navsub["subjects"] = str(tempnavsub)
                    print(tempnavsub)
            except ValueError:
                pass
        except KeyError:
            pass
        try:
            file = request.files["file"]
            subject = request.form["subject"].upper().strip()
            topic = request.form["topic"].upper()
            desc = request.form["desc"]
            filetype = file.filename.split(".")[-1]
            filename = secure_filename(subject+"_"+topic+"."+filetype)
            filelink = f"static/database/{filename}"
            file.save(filelink)
            if filetype !="pdf":
                flash("Please Upload Only PDFs")
                active_u = "active"
            else:
                try: 
                    active_u = ""
                    resp = supabase.storage.from_("userfilestorage").upload(filename,filelink,{"content-type":"application/pdf"})
                    fileurl = supabase.storage.from_("userfilestorage").get_public_url(filename)
                    supabase.table('notes').insert({"filename": filename,"subjectname": subject,"filetype": filetype,"filelink": fileurl,"uploaded_by":username,"description":desc}).execute()
                except StorageException:
                    active_u = "active"
                    flash("Resource Already Exists")
        except KeyError:
                    pass
    return render_template("home.html",customcolor=customcolor,nikhil=nikhil,active_u=active_u,active=active,navsublst=eval(navsub["subjects"]),pdflist=datalist,favoritelist=favoritelist,id=navsub["id"],data=data,username=navsub["username"],previewfile=preview,num=num,tempnavsub=tempnavsub,active_r=active_r,likedfiles = navsub["liked_files"])

@app.route("/favorites/<id>",methods=["POST","GET"])
def favorites(id):
    userdata=supabase.table("users").select("*").eq("id",id).execute().data[0]
    notesid = supabase.table('users').select('favorites').eq('id',id).execute().data[0]["favorites"]
    idlist = notesid.strip().split(" ")
    favoritelist = []
    if session.get("user") != id:
        return "Oversmart?"
    try:
        favoritelist = supabase.table("notes").select("*").in_("id",idlist).execute().data
    except PostgrestAPIError:
        idlist.remove("")
        favoritelist = supabase.table("notes").select("*").in_("id",idlist).execute().data
        #fix this
    if len(favoritelist) > 0:
        if request.method == "POST":
            unfavorite = request.form.get("unfavorite")
            if unfavorite:
                notesid = notesid.replace(unfavorite,"")
                supabase.table('users').update({'favorites':notesid}).eq('id',id).execute()
    return render_template("favorites.html",favoritelist=favoritelist,id=id,username=userdata['username'])

@app.route("/chatbot/<id>",methods=["POST","GET"])
def chatbot(id):
    userdata=supabase.table("users").select("*").eq("id",id).execute().data[0]
    response = ""
    prompt = ""
    model = genai.GenerativeModel("gemini-1.5-flash")
    if session.get("user") != id:
        return "Oversmart?"
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = model.generate_content(prompt).text    
        response = markdown.markdown(text=response)
    return render_template("chatbot.html",response=response,prompt=prompt,id=id,username=userdata['username'])

@app.route("/sharvil")
def sharvil():
    return render_template("sharvil.html")
@app.route("/ourteam")
def team():
    return render_template("team.html")

@app.route("/likes",methods=["POST","GET"])
def likes():
    if request.method == "POST":
        likedata = request.get_json()
        if likedata["is_in_list"] == 0:
            currlikes = supabase.table("notes").select("likes").eq("id",likedata["id"]).execute().data[0]["likes"]
            supabase.table("notes").update({"likes":int(currlikes)+1}).eq("id",likedata["id"]).execute()
            likedfiles = supabase.table("users").select("liked_files").eq("id",likedata["userid"]).execute().data[0]["liked_files"]
            likedfiles = likedfiles + " " +likedata["id"]
            supabase.table("users").update({"liked_files":likedfiles}).eq("id",likedata["userid"]).execute()
        elif likedata["is_in_list"] == 1:
            currlikes = supabase.table("notes").select("likes").eq("id",likedata["id"]).execute().data[0]["likes"]
            supabase.table("notes").update({"likes":int(currlikes)-1}).eq("id",likedata["id"]).execute()
            likedfiles = supabase.table("users").select("liked_files").eq("id",likedata["userid"]).execute().data[0]["liked_files"]
            likedfiles = likedfiles.replace(likedata["id"]," ")
            supabase.table("users").update({"liked_files":likedfiles}).eq("id",likedata["userid"]).execute()
        print("TEST TEST TEST ",likedata["is_in_list"],type(likedata["is_in_list"]))
    return "200"

@app.route("/tusharjadhav",methods=["POST","GET"])
def admin():
    admins = ["a0ee423e-263c-4bd1-8ce8-d58d879f9b1c","736d0a1f-212f-4575-b083-47edb46231da","4eae3ce9-a2ff-45c1-8a13-3f5bc9eddfb3","28b12242-d0ac-4462-8a64-a33ae9131a78"]
    if session.get("user") in admins:
        true = True
        formatted_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        activeusers = supabase.table("users").select("username,lastactive").execute().data
        activelist = []
        for x in activeusers:
            if (datetime.fromisoformat(formatted_time) - datetime.fromisoformat(x["lastactive"])) <= timedelta(minutes=10):
                activelist.append(x)
        if request.method == "POST":
            colchangeid = request.form["coldchangeid"]
            coldchangename = request.form["coldchangename"]
            supabase.table('users').update({"color":coldchangename}).eq('id',colchangeid).execute()
            print(colchangeid,coldchangename)
        return render_template("admin.html",activeusers=activelist,numusers=len(activeusers))
    else:
        return render_template("invalidurl.html")
@app.route("/smartsearch/<id>",methods=["POST","GET"])
def smartsearch(id):
    navsub = supabase.table('users').select('*').eq('id',id).execute().data[0]
    tempnavsub = eval(navsub["subjects"])
    return render_template("smartsearch.html",subjectlist = tempnavsub,id=id)

@app.route("/smartsubjectsfilenames",methods=["POST","GET"])
def smartsubjectsfilenames():
    if request.method == "POST":
        data = request.json["subjectname"]
        datalist = supabase.table('notes').select('*').eq('subjectname',data).execute().data
        print(type(datalist))
        return jsonify(datalist)
    return jsonify({"message": "Use POST method"})


@app.route("/<name>",methods=["GET","POST"])
def redirecturl(name):
    if not session.get("user"):
        return render_template('logintoaccess.html')
    elif "_" in name:
        return redirect(f"https://pgyqwtttvyezvyyexbfh.supabase.co/storage/v1/object/public/userfilestorage/{name}?")
    else:
        session["data"] = name.upper()
        return redirect("/")
    return render_template("invalidurl.html")
if "__main__" == __name__:
    app.run(debug=True,host='0.0.0.0',port=5000)