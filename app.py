from flask import Flask, request, redirect, url_for, render_template, flash
from pymongo import MongoClient
from bson.objectid import ObjectId  # Import ObjectId to work with MongoDB IDs

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb+srv://web:web@cluster0.poowfhi.mongodb.net/web?retryWrites=true&w=majority&appName=Cluster0")
db = client.web

@app.route('/')
def home():
    updates = db.updates.find()
    return render_template('index.html', updates=updates)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'pcsdfgjij345jiorigjjv':
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
        return redirect(url_for('home'))
    return render_template('add_update.html')

@app.route('/delete_update/<update_id>', methods=['POST'])
def delete_update(update_id):
    if request.method == 'POST':
        db.updates.delete_one({'_id': ObjectId(update_id)})
        flash('Update deleted successfully', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
