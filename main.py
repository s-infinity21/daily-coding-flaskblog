from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    slug = db.Column(db.String(50), nullable = False)
    img_file = db.Column(db.String(20), nullable = True, default="url_for('static', filepath = 'img/post.jpg')")
    content = db.Column(db.Text(), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.content}', '{self.slug}', '{self.date}')"

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    phno = db.Column(db.String(12), nullable = False)
    msg = db.Column(db.Text(), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return f"Contact('{self.name}', '{self.email}', '{self.phno}', '{self.msg}', {self.date}')"

@app.route("/")
def home():
    post = Post.query.filter_by().all()
    last = math.ceil(len(post)/2)
    page = request.args.get('page')
    if( not str(page).isnumeric()):
        page=1
    page = int(page)
    post = post[(page-1)*2 : (page-1)*2 + 2]
    if(page==1):
        prev="#"
        nxt="/?page="+str(page+1)
    elif(page==last):
        nxt="#"
        prev="/?page="+str(page-1)
    else:
        prev="/?page="+str(page-1)
        nxt="/?page="+str(page+1)


    return render_template('index.html', post=post, prev=prev, next=nxt)

@app.route("/contact", methods = ['GET','POST'])
def cont():
    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name = name, phno = phone, msg = message, email = email, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')


@app.route("/logout")
def logOut():
    session.pop('user')
    return redirect('/dashboard')

@app.route("/delete/<string:post_id>", methods = ['GET','POST'])
def delIt(post_id):
    if ('user' in session and session['user'] == "Shubh2103"):    
        post = Post.query.filter_by(id = post_id).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')
    

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/edit/<string:post_id>", methods = ['GET','POST'])
def edit(post_id):
    if ('user' in session and session['user'] == "Shubh2103"):
        
        if (request.method == 'POST'):
            box_title = request.form.get('title')
            box_slug = request.form.get('slug')
            box_content = request.form.get('content')
            date = datetime.now()
            
            if(post_id == '0'):
                post = Post(title = box_title, slug = box_slug, content = box_content, date = date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Post.query.filter_by(id = post_id).first()
                post.title = box_title
                post.slug = box_slug
                post.content = box_content
                post.date = date
                db.session.commit()
                return redirect("/edit/"+post_id)

    post = Post.query.filter_by(id = post_id).first()
    return render_template('edit.html', post = post, id = post_id)

@app.route("/dashboard", methods= ['GET','POST'])
def dashboard():
    if ('user' in session and session['user'] == "Shubh2103"):
        post = Post.query.all()
        return render_template('dashboard.html', post = post)


    if (request.method == 'POST'):
        username = request.form.get('uname')
        passwrd = request.form.get('password')
        if(username=="Shubh2103" and passwrd=="Shubh Shubh"):
            session['user'] = username
            post = Post.query.all()
            return render_template('dashboard.html', post = post)
    
    return render_template('login.html')

@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route(post_slug):
    post = Post.query.filter_by(slug = post_slug).first()
    return render_template('post.html',post = post) 

@app.route("/people", methods = ['GET','POST'])
def post_contact():
    if ('user' in session and session['user'] == "Shubh2103"):
        contact = Contact.query.all()
        return render_template('people.html', contact = contact)

@app.route("/deleteCon/<string:contact_id>", methods = ['GET','POST'])
def delContact(contact_id):
    if ('user' in session and session['user'] == "Shubh2103"):    
        contact = Contact.query.filter_by(id = contact_id).first()
        db.session.delete(contact)
        db.session.commit()
    return redirect('/people')

if(__name__ == '__main__'):
    app.run(debug=True)