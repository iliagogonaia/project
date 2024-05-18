import os
from flask import Flask, redirect, url_for, render_template, request, session as flask_session, flash, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
Base = declarative_base()

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    years = Column(String(4), nullable=False)
    budget = Column(Float, nullable=False)
    filename = Column(String(100), nullable=True)
    filmslink = Column(String(100), nullable=True) 
    
    def __str__(self):
        return f'Film title: {self.title}; years: {self.years}; budget: {self.budget}; filename: {self.filename}'

engine = create_engine('sqlite:///films.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
db_session = Session()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        flask_session['user'] = username
        return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        flask_session['user'] = username
        return redirect(url_for('user'))
    return render_template('register.html')
@app.route('/user')
def user():
    if 'user' in flask_session:
        count = flask_session.get('count', 0)  
        subjects = [count, 'Calculus', 'DB']
        return render_template('user.html', subjects=subjects)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flask_session.pop('user', None)
    return 'You are logged out'

@app.route('/delete_film/<int:film_id>', methods=['POST'])
@app.route('/films', methods=['GET', 'POST'])
def films():
    if request.method == 'POST':
        title = request.form['title']
        years = request.form['years']
        budget = request.form['budget']
        file = request.files['file']
        
        if title and years and budget and file and allowed_file(file.filename):
            try:
                years = int(years)
                budget = float(budget)
                
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                new_film = Film(title=title, years=years, budget=budget, filename=filename)
                db_session.add(new_film)
                db_session.commit()
                flash('Data added successfully')
                return redirect(url_for('films'))
            except ValueError:
                flash('Invalid input for years or budget')
        else:
            flash('Please fill out all fields and ensure the file is an allowed type')
    films = db_session.query(Film).all()
    return render_template('films.html', films=films)

@app.route('/')
def home():
    films = db_session.query(Film).all()
    return render_template('index.html', films=films)
if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)


