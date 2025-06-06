from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
db = SQLAlchemy(app)

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    entries = DiaryEntry.query.order_by(DiaryEntry.date_created.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_entry = DiaryEntry(title=title, content=content)
        
        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/')
        except:
            return '投稿中にエラーが発生しました'
    
    return render_template('add.html')

@app.route('/entry/<int:id>')
def entry(id):
    entry = DiaryEntry.query.get_or_404(id)
    return render_template('entry.html', entry=entry)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    entry = DiaryEntry.query.get_or_404(id)
    
    if request.method == 'POST':
        entry.title = request.form['title']
        entry.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect(url_for('entry', id=entry.id))
        except:
            return '編集中にエラーが発生しました'
    
    return render_template('edit.html', entry=entry)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    entry = DiaryEntry.query.get_or_404(id)
    try:
        db.session.delete(entry)
        db.session.commit()
        return redirect('/')
    except:
        return '削除中にエラーが発生しました'

if __name__ == '__main__':
    app.run(debug=True) 