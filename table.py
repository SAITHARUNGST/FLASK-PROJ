from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql+psycopg2://postgres:saitharun@localhost/student'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

ITEMS_PER_PAGE = 3


class students1(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sname = db.Column(db.String(30))
    sclass= db.Column(db.String(2000))
    hobbies=db.Column(db.String(1000))
    grades=db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    page_number = request.args.get('page', 1, type=int)

    if request.args.get('search_term'):
        search_term = request.args.get('search_term')
        filtered_students = students1.query.filter(
            db.or_(students1.sname.like('%' + search_term + '%'), students1.sclass.like('%' + search_term + '%'), students1.hobbies.like('%' + search_term + '%'), students1.grades.like('%' + search_term + '%'))
        )
        value = filtered_students.paginate(page=page_number, per_page=ITEMS_PER_PAGE, error_out=False)
    else:
        all_students = students1.query.paginate(page=page_number, per_page=ITEMS_PER_PAGE, error_out=False)
        value = all_students

    return render_template('index.html', value=value)

@app.route('/student')
def student():
    return render_template('students.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        filtered_students = students1.query.filter(db.or_(students1.sname.like('%' + search_term + '%'), students1.sclass.like('%' + search_term + '%'), students1.hobbies.like('%' + search_term + '%'), students1.grades.like('%' + search_term + '%')))
        return render_template('index.html', value=filtered_students)
    else:
        return render_template('index.html', value=students1.query.all())


@app.route('/process',methods = ['POST'])
def process():
    sname = request.form['sname']
    sclass = request.form['sclass']
    grades= request.form['grades']
    hobbies=request.form['hobbies']
    studentdata= students1(sname=sname,sclass=sclass,grades=grades,hobbies=hobbies)
    db.session.add(studentdata)
    db.session.commit()

    return redirect(url_for('index'))