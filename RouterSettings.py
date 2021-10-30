from flask import Flask,render_template,request,url_for,flash,redirect
import sqlite3
import smtplib
import email
import random
from email.mime.text import MIMEText
from email.header import Header
import hashlib
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'welcome to my blog'
app.debug = True

@app.route('/index')
def index():
	return render_template('index.html')



@app.route('/sign_up',methods=('GET','POST'))
def sign_up_email():
	if request.method == 'POST':
		global EMAIL
		EMAIL = request.form['email']
		if not EMAIL:
			flash('EMAIL ERROR')
		else:
			a = str(random.randint(0,9))
			b = str(random.randint(0,9))
			c = str(random.randint(0,9))
			d = str(random.randint(0,9))
			e = str(random.randint(0,9))
			f = str(random.randint(0,9))
			global check
			check = a+b+c+d+e+f
			mail_host = 'smtp.exmail.qq.com'
			mail_user = 'variflight@feiyou.chat'
			mail_pass = 'Jason050910-'

			sender = 'variflight@feiyou.chat'
			receivers = [EMAIL]

			message = MIMEText('BLOG OF PVGOBSERVER SIGN UP EMAIL CHECK YOUR CHECK CODE :'+check,'plain','utf-8')
			message['From'] = Header('ADMIN OF BLOG','utf-8')
			message['To'] = Header('WELCOME','utf-8')

			subject = 'THANKS YOUR SIGN UP'
			message['Subject'] = Header(subject,'utf-8')

			try:
				smtpObj = smtplib.SMTP()
				smtpObj.connect(mail_host,25)
				smtpObj.login(mail_user,mail_pass)
				smtpObj.sendmail(sender,receivers,message.as_string())
				return redirect(url_for('sign_up_next'))
			except smtplib.SMTPException:
				flash('WORNING : SENGDING CHECK EMAIL ERROR')
	return render_template('sign_up_email.html')
@app.route('/sign_up_next',methods=('GET','POST'))
def sign_up_next():
	if request.method == 'POST':
		USERNAME = request.form['username']
		WECHAT_ID = request.form['wechat_id']
		PASSWORD_1 = request.form['password_1']
		PASSWORD_2 = request.form['password_2']
		INTRODUCTION = request.form['introduction']
		CHECK = request.form['check']
		if not CHECK:
			flash('CHECK MUST NOT BE NULL')
		else:
			if CHECK == check:
				if not USERNAME:
					flash('USERNAME ERROR')
				elif not WECHAT_ID:
					flash('WECHAT ID ERROR')
				elif not PASSWORD_1:
					flash('FIRST PASSWORD ERROR')
				elif not PASSWORD_2:
					flash('SECOND PASSWORD ERROR')
				elif not INTRODUCTION:
					flash('INTRODUCTION ERROR')
				else:
					if PASSWORD_1 != PASSWORD_2:
						flash('FIRST PASSWORD SECOND PASSWORD MUST BE SAME')
					else:
						handle = hashlib.md5()
						code = PASSWORD_2.encode(encoding='UTF-8')
						handle.update(code)
						HASHPASSWORD = handle.hexdigest()
						conn = sqlite3.connect('blog.db')
						cur =  conn.cursor()
						conn.execute("insert into USER(USERNAME,EMAIL,PASSWORD,WECHAT_ID,INTRODUCTION) values (?,?,?,?,?)",(USERNAME,EMAIL,HASHPASSWORD,WECHAT_ID,INTRODUCTION))
						conn.commit()
						conn.close()
						flash('YOUR ACCOUNT OK')
						return redirect(url_for('login'))
			else:
				flash('YOUR EMAIL CHECK NOT CORRECT')
	return render_template('sign_up.html')
@app.route('/admin')
def admin():
	return render_template('admin.html')
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/')
def first():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/recent')
def recent():
	return render_template('recent.html')

@app.route('/plan')
def plan():
	return render_template('plan.html')
@app.route('/article/<int:article_id>')
def article(article_id):
	return render_template('article.html')
app.run(host="0.0.0.0")
