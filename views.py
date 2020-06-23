from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = 'random string'


app = Flask(__name__)
app.secret_key = "abc"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'nishant'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'library'


mysql = MySQL(app)



@app.route('/' , methods=['GET', 'POST'])
def front_page():
    conn = mysql.connect
    return render_template('admusr.html')

@app.route('/select', methods=['POST'])
def select():
    conn = mysql.connect
    value=request.form["Radio1"]
    if value == "V1":
        return render_template("Login_admin.html")
    elif value == "V2":
        return render_template("login_user.html")

@app.route('/login', methods=['POST'])
def admin():
    conn = mysql.connect
    if request.method == 'POST':
        name = request.form['name']
        pin = request.form['pin']
        print(name)
        print(type(name))
        print(type(pin))
        print(pin)
        cur = mysql.connection.cursor()
        if type(name)!=str and type(pin)!=str:
            return 'Enter valid credentials'

        if len(name) == 0 or len(pin) == 0:
            print('entered len')
            return 'Name or Pin missing'



        else:
            cur.execute("SELECT * FROM Admin where Name = '"+name+"' and pin = "+pin)
            rows = cur.fetchall()

            if cur.rowcount!=0:
                return render_template("Admin View.html")
            else:
                return 'No account found'







@app.route('/login2', methods=['GET','POST'])
def login2():
    if request.method == 'POST':
        name=request.form['name']
        pin=request.form['pin']

        print(type(name),type(pin))
        cur = mysql.connection.cursor()

        if len(name)==0 or len(pin)==0:
            print('entered len')
            return 'Name or Pin missing'

        elif type(name)!=str and type(pin)!=str:
            print('entered type')
            return 'kindly enter valid credentials'

        else:

            cur.execute('SELECT * FROM user where Name = \''+name+'\' and pin = \''+ pin + '\'')
            if cur.rowcount==0:
                return 'Invalid'
            else:
                return render_template('UserView.html')

@app.route('/UserView', methods=['GET','POST'])
def userView():
    if request.method=='POST':
        value=request.form['R']
        if value=='V1':
            return render_template('issue2.html')
        if value=='V2':
            return render_template('return.html')
        if value=='V3':
            return render_template('ser.html')


@app.route('/AdminView', methods=['GET','POST'])
def AdminView():
    if request.method=='POST':
        value=request.form['R']
        if value=='V1':
            return render_template('issue2.html')
        if value=='V4':
            return render_template('add_books.html')
        if value=='V2':
            return render_template('return.html')
        if value == 'V3':
            return render_template('ser.html')
        if value == 'V5':
            return render_template('del.html')

@app.route('/View', methods=['GET','POST'])
def issue():
    conn = mysql.connect

    print("################################################################################")
    if request.method == 'POST':
        print("============================================================================")
        Student_id = request.form['S_ID']
        Book_id = request.form['B_ID']
        cur = mysql.connection.cursor()
        print(type(Student_id))
        cur.execute("Select * from user where ID =" +Student_id)
        rows = cur.fetchone()
        cur.execute("Select * from Books where Book_ID =" + Book_id)
        row=cur.fetchone()
        print(type(row))
        print(type(rows))

        if type(row)!=tuple or type(rows)!=tuple:
            print('nnnnnnnnnnnnnnnn')
            return 'Book ID or Student ID not available'



        else:

            print("Else mei gaya")
            Student_id = request.form['S_ID']
            Book_id = request.form['B_ID']
            print(type(Student_id))
            print(type(Book_id))
            cur = mysql.connection.cursor()
            cur.execute('Select Name from Books where Book_id=\'' +Book_id+'\'')
            a=cur.fetchone()
            print('**************************************')
            x=a[0]
            print(x)
            print(type(x))
            i='select  Number_of_books_issued from Books_Actions where Name=\'' +x+'\''
            print(1)
            cur.execute(i)
            books_num=cur.fetchone() #isme number of books  issued aaegi
            print(books_num)
            print(type(books_num))
            issue=books_num[0]
            a='select  Number_of_books from Books_Actions where Name=\'' +x+'\''
            cur.execute(a)
            print(3)
            ava=cur.fetchone()
            available=ava[0]
            print('**************')
            print(available)
            print(issue)

            while(available>issue):
                #cur.execute('update Books_Actions where Name=\'' + Name + '\'' set Number_of_books_issued=' + Number_of_books_issued+1 +  )

                    no='update Books_Actions set Number_of_books_issued=Number_of_books_issued+1  where Name=\'' +x+'\''
                    ava='update Books_Actions set Number_of_books_available=Number_of_books_available-1  where Name=\'' +x+'\''
                    cur.execute(no)
                    cur.execute(ava)
                    print('C1')
                    conn.commit()
                    return 'issued'

            else:
                return 'Else'





@app.route('/search', methods=['GET','POST'])
def search():
    if request.method== 'POST':
        a=request.form['Radio1']
        print("=====================================================================")

        value = request.form['T']
        print(value)
        print(a)
        print("=====================================================================")
        print(a)
        if a=='Name':
            cur = mysql.connection.cursor()
            cur.execute('Select * from Books_Actions where Name =\'' +value+'\'')
            rows=cur.fetchall()
            if cur.rowcount==0:
                return 'No records found'
            else:
                return render_template("Book_list.html", rows=rows)

        if a == 'Subject':
            cur = mysql.connection.cursor()
            cur.execute('Select * from Books_Actions where Subject =\'' +value+'\'')
            rows = cur.fetchall()
            if cur.rowcount == 0:
                return 'No records found'
            else:
                return render_template("Book_list.html", rows=rows)
        if a == 'Author':
            cur = mysql.connection.cursor()
            cur.execute('Select * from Books_Actions where Author =\'' +value+'\'')
            rows = cur.fetchall()
            if cur.rowcount == 0:
                return 'No records found'
            else:
                return render_template("Book_list.html", rows=rows)

        if a == 'id':
            cur = mysql.connection.cursor()
            cur.execute('Select * from Books_Actions where Book_ID =\'' +value+'\'')
            rows = cur.fetchall()
            print(a)
            print(rows)
            if cur.rowcount == 0:
                return 'No records found'
            else:
                return render_template("Book_list.html", rows=rows)



@app.route('/add', methods=['GET','POST'])
def add():
    conn = mysql.connect
    if request.method=='POST':
        ID=request.form['ID']
        Name = request.form['Name']
        Author =request.form['Author']
        Subject =request.form['Subject']
        Category = request.form['Category']
        cur = mysql.connection.cursor()
        cur.execute("Select * from Books where Book_ID=" +ID)
        if cur.rowcount==0: #Agar table mei same ID nhi hai, to it will insert
            cur.execute("insert into Books(Book_ID,Name,Author,Subject,Category) Values(%s,%s,%s,%s,%s)" ,(ID, Name,Author,Subject,Category))
            print('select * from Books_Actions where Name=\''+Name+'\'')
            print('+++++++++++++++')
            cur.execute('Select * from Books_Actions where Name=\''+Name+'\'')
            print(cur.rowcount)

            if cur.rowcount==0: #checking if the book with same name is present. If no than insert items.....
                cur.execute("insert into Books_Actions(Book_ID,Name,Author) Values(%s,%s,%s)" ,(ID, Name,Author))

                print('8888888888888888888888')

                cur.execute('update Books_Actions set Number_of_books=1 where Name=\''+Name+'\'')
                cur.execute('update Books_Actions set Number_of_books_issued=1 where Name=\'' + Name + '\'')
                cur.execute('update Books_Actions set Number_of_books_available=1 where Name=\'' + Name + '\'')
                conn.commit()
                print('8888888888888888888888lkjhgfd')
                print('8888888888888888888888****************/')
            else: #agar book with same name is there in the table then only we need to update the number
                cur.execute('select Number_of_books from Books_Actions where Name=\'' +Name+'\'')
                No1_books=cur.fetchone()
                cur.execute('select Number_of_books_issued from Books_Actions where Name=\'' + Name + '\'')
                No2_books_issued=cur.fetchone()
                cur.execute('select Number_of_books_available from Books_Actions where Name=\'' + Name + '\'')
                No3_books_available=cur.fetchone()
                print('--------++++++++++++-----------')
                print(type(No1_books))
                No_books=No1_books[0]
                No_books_issued =No2_books_issued[0]
                No_books_available = No3_books_available[0]
                print(No_books)
                print(No_books_issued)
                print(No_books_available)


                No_books_available=No_books_available+1
                No_books=No_books+1

                print('===================================================================')
                print(No_books,No_books_available, No_books_issued)
                cur.execute('update Books_Actions set Number_of_books =' +str(No_books))
                conn.commit()
                cur.execute('update Books_Actions set Number_of_books_available=' +str(No_books_available))
                conn.commit()
                print(cur.fetchall())
                print('saari queries chal gai, ho jaana chahie add')


                print('*******************************************************************')

            return 'Book Added'
        else:
            return 'ID Exist, try with another ID as a primary key'

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method=='POST':
        id=request.form['ID']
        cur = mysql.connection.cursor()
        cur.execute('select Name from Books where Book_ID=' +id)
        name=cur.fetchone()
        if cur.rowcount==0:
            return 'No record found'
        else:
            Name=''.join(name)
            cur.execute('delete from Books where Book_ID=\'' + id + '\'')
            Num = 'select Number_of_books from Books_Actions where Name= \'' +Name+ '\''
            cur.execute(Num)
            Number=cur.fetchone()
            print(Number)
            print(type(Number))
            Number=Number[0]

            print(type(Number))
            print(Number)
            Issued = 'select Number_of_books_issued from Books_Actions where Name= \'' + Name + '\''
            cur.execute(Issued)
            Issue=cur.fetchone()
            Issue=Issue[0]#Ye hai main
            cur.execute('select Number_of_books_available from Books_Actions where Name=\'' +Name+ '\'')
            avail = cur.fetchone()
            avail =avail[0]
            avail=int(avail)
            Issue=int(Issue)
            Number=int(Number)
            avail=avail-1
            Issue=Issue-1
            Number=Number-1
            Number=str(Number)
            avail=str(avail)
            if Number==Issue:
                return 'Book Issued, cannot delete'
            elif avail==0:
                return 'Books Issued, cannot delete'
            elif Number==1:
                cur.execute('delete from Books_Actions where Name=\'' +Name+ '\'')
            else:
                cur.execute('update Books_Actions set Number_of_books=\''+Number+'\'')
                cur.execute('update Books_Actions set Number_of_books_available=' +avail)
                return 'Deleted'







if __name__ == '__main__':
    app.debug = True
    PYCHARM_DEBUG = True
    app.run(port=5050)
