from flask import Flask, render_template, request, session, redirect, url_for
from sql_lite_db import sql_lite_db
import sqlite3 as sql
from datetime import date,datetime
import sys,re
from distutils.log import debug
from sendgridmail import sendmail
from dotenv import load_dotenv

#Initialize the flask app
app = Flask(__name__)
app.secret_key = 'a'

# Call SQL Lite DB to setup the DB and Tables
sql_lite_db()

# Connect to SQL Lite
conn = sql.connect('plasmadatabase.db',check_same_thread=False)
sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
cursor = conn.cursor()
cursor.execute(sql_query)
conn.close()
# print(cursor.fetchall(), file=sys.stderr)

@app.route('/')
def home():
   return render_template('landingpage.html')

@app.route('/loginpage',methods=['GET', 'POST'])
def loginpage():
    global userid
    msg = ''
    if request.method == 'POST' :
        username = request.form['username'].lower()
        password = request.form['password']
        conn = sql.connect('plasmadatabase.db',check_same_thread=False)
        check_user_sql = f"SELECT pdapp_username FROM pd_app_user_creds WHERE pdapp_username='{username}'"
        user_data = conn.execute(check_user_sql)
        account = user_data.fetchone()
        # print (account)
        if account:
            check_user_pw_sql = f"SELECT * FROM pd_app_user_creds WHERE pdapp_username='{username}' AND pdapp_password='{password}'"
            conn = sql.connect('plasmadatabase.db',check_same_thread=False)
            user_pw_data = conn.execute(check_user_pw_sql)
            account_pw = user_pw_data.fetchone()
            conn.close()
            # print (account_pw)
            if account_pw:
                session['loggedin'] = True
                session['id'] = account[0]
                userid = account[0]
                session['username'] = account[0]
                msg = 'Logged in successfully !'
                #sendmail(account['email'],'Plasma donor App login','You are successfully logged in!')
                return redirect(url_for('dashboard'))
            else:
                msg = 'Logged in Failed, re-try with correct password !'
                #sendmail(account['email'],'Plasma donor App login','You are successfully logged in!')
        else:
            msg = 'User Not Found, Please Sign Up !'
    return render_template('landingpage.html', msg = msg)

@app.route('/registration')
def register():
    return render_template('register.html')

@app.route('/registration',methods=['GET', 'POST'])
def registration():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username'].lower()
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        dob = datetime.strptime(request.form['dob'],'%Y-%m-%d')
        covid19_status = request.form['infect']
        bloodgroup = request.form['blood']
        last_donated_date = request.form['last_donated_date']
        is_donor =  request.form['donor']
        today = date.today()
        donation_signedup_date = date.today()
        # print(dob, file=sys.stderr)
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        conn = sql.connect('plasmadatabase.db',check_same_thread=False)
        check_user_sql = f"SELECT * FROM pd_user_data WHERE pdapp_username = '{username}'"
        user_data = conn.execute(check_user_sql)
        account = user_data.fetchone()
        conn.close()
        if account:
            msg = 'Account already exists, please go ahead and login!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        elif age <= 16:
            msg = 'must be an have age greater than 16 to register into the Plasma Donation App !'
        else:
            conn = sql.connect('plasmadatabase.db',check_same_thread=False)
            insert_sql = f"INSERT INTO pd_user_data VALUES ('{username}', '{email}', '{phone}', '{address}', '{dob}' , '{covid19_status}')"
            conn.execute(insert_sql)
            conn.commit()
            conn.close()
            conn = sql.connect('plasmadatabase.db',check_same_thread=False)
            insert_sql = f"INSERT INTO pd_app_user_creds VALUES ('{username}', '{password}')"
            conn.execute(insert_sql)
            conn.commit()
            conn.close()
            if is_donor == 'Yes':
                conn = sql.connect('plasmadatabase.db',check_same_thread=False)
                insert_sql = f"INSERT INTO pd_donors VALUES ('{username}', '{bloodgroup}','{donation_signedup_date}','{last_donated_date}')"
                conn.execute(insert_sql)
                conn.commit()
                conn.close()
            msg = 'You have successfully registered !'
            # sendmail(email,'Plasma donor App Registration','You are successfully Registered {}!'.format(username))

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('landingpage.html', msg = msg)
    
@app.route('/dashboard')
def dashboard():
    if session['loggedin'] == True:
       conn = sql.connect('plasmadatabase.db',check_same_thread=False)
       donations_sql = "SELECT blood_group_With_RH,COUNT(*) Donors_Cnt FROM pd_donors where last_donated_date >= CURRENT_DATE-180 GROUP BY blood_group_With_RH"
       con = sql.connect("plasmadatabase.db")
       con.row_factory = sql.Row
       cur = con.cursor()
       cur.execute(donations_sql)
       rows = cur.fetchall();
       conn.close()
       return render_template('dashboard.html',rows = rows)
    else:
        msg = 'Please login!'
        return render_template('landingpage.html', msg = msg)

@app.route('/plasmarequestform')
def plasmarequest():
    return render_template('plasmarequest.html')

@app.route('/plasmarequestform',methods=['GET', 'POST'])
def plasmarequestform():
    msg = ''
    if request.method == 'POST' :
       username = userid.lower()
       bloodgroup = request.form['blood']
       requested_for_address = request.form['address']
       requestdate = date.today()
       request_status = 'Open'
       conn = sql.connect('plasmadatabase.db',check_same_thread=False)
       insert_sql = f"INSERT INTO pd_requests VALUES ('{username}', '{bloodgroup}', '{requested_for_address}', '{requestdate}','{request_status}')"
       conn.execute(insert_sql)
       conn.commit()
       conn.close()
       msg= 'Request Placed'
       return render_template('plasmarequest.html', msg = msg)
    else:
        msg = 'Please login!'
        return render_template('landingpage.html', msg = msg)
        
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('landingpage.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug='TRUE')