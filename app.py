from flask import Flask, request, redirect, url_for, render_template, flash
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb+srv://web:web@cluster0.poowfhi.mongodb.net/web?retryWrites=true&w=majority&appName=Cluster0")
db = client.web

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/updates', methods=['GET', 'POST'])
def updates():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'sdfe53rf564gdfgerh':
            update_id = request.form['update_id']
            db.updates.delete_one({'_id': ObjectId(update_id)})
            flash('Update deleted successfully', 'success')
        else:
            flash('Incorrect password', 'error')
    updates = db.updates.find().sort('_id', -1)  # Sort updates in reverse order
    return render_template('updates.html', updates=updates)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'sdfe53rf564gdfgerh':
            return redirect(url_for('add_update'))
        else:
            flash('Incorrect password', 'error')
    return render_template('admin.html')

@app.route('/add_update', methods=['GET', 'POST'])
def add_update():
    if request.method == 'POST':
        photo = request.form['photo']
        text = request.form['text']
        link = request.form['link']
        db.updates.insert_one({'photo': photo, 'text': text, 'link': link})
        flash('Update added successfully', 'success')
        return redirect(url_for('updates'))
    return render_template('add_update.html')

if __name__ == '__main__':
    app.run(debug=True)
