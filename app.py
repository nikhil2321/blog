from flask import *
import mysql.connector
from cmail import sendmail
from otp import genotp

app=Flask(__name__)

#secret key
app.config['SECRET_KEY'] = "secret key"
mydb=mysql.connector.connect(host='localhost',user='root',password='Nikhil#bl',db='blog')
with mysql.connector.connect(host='localhost',user='root',password='Nikhil#bl',db='blog'):
    cursor=mydb.cursor(buffered=True)
    cursor.execute("create table if not exists registration(username varchar(50) primary key,mobile varchar(20),email varchar(50) unique,address varchar(50),password varchar(20))")
mycursor=mydb.cursor()

@app.route( '/register',methods =['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form.get('username')
        mobile=request.form.get('mobile')
        email=request.form.get('email') 
        address=request.form.get('address')
        password=request.form.get('password') 
        otp=genotp()
        sendmail(to=email,subject='Thanks for registration',body=f'otp is : {otp}')
        return render_template('verification.html', username=username,mobile=mobile,email=email,address=address,password=password,otp=otp)
        #if you want to pass variables form one function to another function. It will be send to the template, in the template you should use the form action,
        #form there it will sent to the url. 
        #By that URL the values should be sent to the another function
    return render_template('registration.html')

@app.route('/otp/<username>/<mobile>/<email>/<address>/<password>/<otp>', methods=['GET','POST'])
def otp(username,mobile,email,address,password,otp):
    if request.method=='POST':
        uotp=request.form['uotp']
        if otp==uotp:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('insert into registration(username,mobile,email,address,password)values(%s,%s,%s,%s,%s)',[username,mobile,email,address,password])
            mydb.commit()
            cursor.close()
            return redirect(url_for('login'))
    return render_template('verification2.html', username=username,mobile=mobile,email=email,address=address,password=password,otp=otp)
@app.route('/blog')
def blogs():
    return render_template( 'blog.html')
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where username=%s && password=%s',[username,password])
        data=cursor.fetchone()[0]
        if data==1:
            session['username']=username
            if not session.get(session['username']):
                session[session['username']]={}
            return redirect(url_for('home'))
        else:
            return 'Invalid Username and Password'
    return render_template('login2.html')
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('homepage.html')

@app.route('/addpost', methods=['GET','POST'])
def add_post():
    if request.method=="POST":
        title = request.form["title"]
        content=request.form['content']
        slug=request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into posts(title,content,slug) values(%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html')
@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/view_posts')
def view_posts():
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT * FROM posts")
    posts=cursor.fetchall()
    cursor.close()
    return render_template('view_posts.html',posts=posts)    
#delete posts route
@app.route('/delete_posts/<int:id>',methods=['POST'])
def delete_posts(id):
    cursor = mydb.cursor(buffered=True)
    cursor.execute('delete from posts where id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('view_posts'))
@app.route('/update_posts/<int:id>', methods=['GET','POST'])
def update_posts(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        slug = request.form['slug']
        print(title)
        print(content)
        print(slug)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('UPDATE posts SET title=%s,content=%s,slug=%s WHERE id=%s',(title,content,slug,id))
        mydb.commit()
        cursor.close()
        return redirect(url_for('view_posts'))
    else:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select * from posts WHERE id=%s', (id,))
        post=cursor.fetchone()
        cursor.close()
        return render_template('update_posts.html',post=post)

app.run(debug=True, use_reloader=True)