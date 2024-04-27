from flask import*
import pyrebase
from datetime import datetime
from datetime import datetime,timedelta
import urllib.request
import time
import smtplib


firebaseConfig = {
  "apiKey": "AIzaSyBBcWYtHdZSg6UWBYorbUxRU7t4OPcb50Q",
  "authDomain": "watch24x7-e05c1.firebaseapp.com",
  "databaseURL": "https://watch24x7-e05c1-default-rtdb.firebaseio.com",
  "projectId": "watch24x7-e05c1",
  "storageBucket": "watch24x7-e05c1.appspot.com",
  "messagingSenderId": "1030555093614",
  "appId": "1:1030555093614:web:001c3006e9e4a94938747f",
  "measurementId": "G-4Y9ZN4KLGR"
}

'''firebaseConfig = {
 "apiKey": "AIzaSyC0fzM9LaUtydwHrPS1N0gtJcvu-Ff_bvI",
  "authDomain": "picstanew.firebaseapp.com",
  "databaseURL": "https://picstanew-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "picstanew",
  "storageBucket": "picstanew.appspot.com",
  "messagingSenderId": "690459338329",
  "appId": "1:690459338329:web:12414949439a77dca53348",
  "measurementId": "G-54JM47BZEW"
}'''
firebase= pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()

data=firebase.database()
storage=firebase.storage()



app=Flask(__name__)
app.secret_key="watch24x7adminbasecode1127_navpreetsingh_developer"

@app.route("/")
def loading():
    return render_template("loading.html")
@app.route("/Home")
def home():
    yes=None
    nol=None
    nop=None
    images=None
    response = data.get("videos")
    post =response.val()
    images = []
    if post is not None:
              timestamps = []
              for postid, postcontent in post.items():
                  if isinstance(postcontent, dict):
                      postsdata = postcontent.get("videos")
                      if postsdata is not None:
                          for postin in postsdata.values():
                              timestamps.append(postin["time"])
              sorted_timestamps = sorted(timestamps, reverse=True)
              images = []
              for timestamp in sorted_timestamps:
                   for postid, postcontent in post.items():
                       if isinstance(postcontent, dict):
                           postsdata = postcontent.get("videos")
                           if postsdata is not None:
                               for postin in postsdata.values():
                                   if postin["time"] == timestamp:
                                       images.append({"postid":postid,"verified":postin["verified"],"userid":postin["userid"],"userdp": postin["userdp"], "username": postin["username"], "time": postin["time"], "caption": postin["caption"],"image_url": postin["image_url"] })
        
    cookie=request.cookies.get("userid")
    if cookie:
        ush=data.child(cookie).get().val()
        pre=ush.get("verified",True)
        if pre:

            
             yes=" "
        else:
            nop=" "


     
    else:
        nol="  "
        


    return render_template("home.html",yes=yes,nol=nol,nop=nop,images=images)

@app.route("/Search", methods=["POST", "GET"])
def search():
    yes = None
    nol = None
    nop = None
    images = None
    notfound=None

    response = data.get("posts")

    post = response.val()
    images = []

    if post is not None:
        timestamps = []
        for postid, postcontent in post.items():
            if isinstance(postcontent, dict):
                postsdata = postcontent.get("videos")
                if postsdata is not None:
                    for postin in postsdata.values():
                        timestamps.append(postin["time"])
        sorted_timestamps = sorted(timestamps, reverse=True)

        for timestamp in sorted_timestamps:
            for postid, postcontent in post.items():
                if isinstance(postcontent, dict):
                    postsdata = postcontent.get("videos")
                    if postsdata is not None:
                        for postin in postsdata.values():
                            if postin["time"] == timestamp:
                                images.append({"postid": postid,"verified": postin["verified"],"userid": postin["userid"],"userdp": postin["userdp"],"username": postin["username"],"time": postin["time"],"caption": postin["caption"],"image_url": postin["image_url"]})

    if request.method == "POST":
        searchcap = request.form["searchname"].lower()
        mposts = []
        if post is not None:
            for postid, postcontent in post.items():
                if isinstance(postcontent, dict):
                    postsdata = postcontent.get("videos")
                    if postsdata is not None:
                        for postin in postsdata.values():
                           caption = postin.get("caption", "").lower()
                           userid = postin.get("userid", "").lower()

                           if searchcap in caption or searchcap in userid:
                            
                                mposts.append({"postid": postid,"verified": postin["verified"],"userid": postin["userid"],"userdp": postin["userdp"],"username": postin["username"], "time": postin["time"],"caption": postin["caption"],"image_url": postin["image_url"]})
        if not mposts:
                notfound = f"{searchcap}"
        return render_template("searchvideo.html", mposts=mposts,notfound=notfound)


    return render_template("search.html", yes=yes, nol=nol, nop=nop, images=images)
       
@app.route("/Upload",methods=["POST","GET"])
def upload():
    user_id=request.cookies.get("userid")

    if user_id:
        e=None
        uploading=None
        if request.method=="POST":

            uploading=" "
            try:
                
                caption=request.form["caption"]
                vid=request.files["filename"]
            
                vid_path = f"video/{vid.filename}"
                storage.child(vid_path).put(vid)
             
            
                  

            
                userdata = data.child(user_id).child('Handle').get().val()

                nimg=data.child(user_id).child("Images").get().val()
                if nimg is not None:
                      v=data.child(user_id).child("Images").get()
                      for img in v.each():
                         imgc=img.val()
                         userdp=imgc
                else:
                      userdp="https://img.icons8.com/fluency-systems-filled/48/737373/user.png"
                now = datetime.now()
                dt = now.strftime("%d / %m / %y")
                dtt = now.strftime("%I:%M %p")
                captiondata = f"{caption}"
                time=f"Shared on: {dt} at {dtt}"
                suspen=data.child(user_id).get().val()
                verified=suspen.get("verified",True)
                if verified:
                     url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Eo_circle_grey_checkmark.svg/768px-Eo_circle_grey_checkmark.svg.png?20200417135205"
                else:
                     url="https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png"
                post_data = {"verified":url,"userid":user_id,"userdp":userdp,"username":userdata,"caption": captiondata, "image_url": storage.child(vid_path).get_url(None),"time":time}
                data.child(user_id).child("videos").push(post_data)

                
                return redirect(url_for("home"))
             
            
            except Exception as e :
                e=e
                
        return render_template("upload.html",e=e,uploading=uploading)
          
    else:
        return redirect(url_for("login"))
@app.route("/Login",methods=["POST","GET"])
def login():
    error=None
    if request.method=="POST":
        email=request.form["email"]
        passw=request.form["password"]
        if not email or not passw:
            return "Please enter your email and password"
        else:
            try:
                user=auth.sign_in_with_email_and_password(email,passw)
                user_id=user["localId"]
                session["userid"] = user_id
                max_age_in_years = 500
                max_age_in_seconds = max_age_in_years * 365.25 * 24 * 60 * 60 

               
                abc=make_response(redirect(url_for("home")))
                abc.set_cookie("userid",value=user_id,expires="500000")
                return abc

               
                #return redirect(url_for("index"))
                

            except :
                
                error="Invalid email or password!"
                

    return render_template("login.html",error=error)

@app.route("/Register",methods=["POST","GET"])
def register():
    error=None
    if request.method=="POST":
        email=request.form["email"]
        passw=request.form["password"]
        handle=request.form["name"]
        bd=request.form["birthday"]
        password=request.form["password"]
       

        if not email or not passw:
            return "Please enter your email and password"
        else:
            try:
               
                user=auth.create_user_with_email_and_password(email,passw)
                data.child(user["localId"]).child("Handle").set(handle)
                data.child(user["localId"]).child("ID").set(user["localId"])
                dateofjoin = datetime.now().strftime("%d-%m-%y")
                dateofjoinadd="Joined on :"+dateofjoin
                data.child(user["localId"]).child("date").push(dateofjoinadd)
                bd=bd
                dateofbday=bd
                data.child(user["localId"]).child("birthday").push(dateofbday)
                data.child(user["localId"]).child("suspended").set(False)

                data.child(user["localId"]).child("password").push(password)
                data.child(user["localId"]).child("verified").set(False)
                data.child(user["localId"]).child("email").push(email)

                

                
                
                
                

                return redirect(url_for("login"))
                

            except:
                error="Invalid email or user already exists"
    return render_template("register.html",error=error)
    
@app.route("/Forgot-password",methods=["POST","GET"])
def forgot():
     error=None
     success=None
     if request.method=="POST":
        email=request.form["email"]

        try:
             auth.send_password_reset_email(email)
             success=f"Password reset link has been successfully sent to  {email}!"
        except:
            error="Invalid email address"
     return render_template("forgot.html",error=error,success=success)
    
@app.route("/Profile")
def profile():
    user_id=request.cookies.get("userid")
    if user_id:
        return render_template("profile.html")
    else:
        return redirect(url_for("login"))
    
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
