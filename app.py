from flask import Flask, request, redirect, url_for, render_template, flash
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb+srv://web:web@cluster0.poowfhi.mongodb.net/web?retryWrites=true&w=majority&appName=Cluster0")
db = client.web

# Store hashed password for security
admin_password_hash = generate_password_hash('sdfe53rf564gdfgerh')

@app.route('/')
def home():
    search_query = request.args.get('search', '')
    if search_query:
        updates = db.updates.find({'text': {'$regex': search_query, '$options': 'i'}}).sort('date', -1)  # Adjust sorting field as necessary
    else:
        updates = db.updates.find().sort('date', -1)  # Ensure 'date' or other sorting field is correct
    return render_template('index.html', updates=updates)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if check_password_hash(admin_password_hash, password):
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
        db.updates.insert_one({'photo': photo, 'text': text, 'link': link, 'date': datetime.datetime.utcnow()})
        flash('Update added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('add_update.html')

@app.route('/updates')
def updates():
    updates = db.updates.find().sort('date', -1)  # Ensure 'date' or other sorting field is correct
    return render_template('updates.html', updates=updates)

@app.route('/delete_update/<update_id>', methods=['POST'])
def delete_update(update_id):
    password = request.form.get('password')
    if check_password_hash(admin_password_hash, password):
        db.updates.delete_one({'_id': ObjectId(update_id)})
        flash('Update deleted successfully', 'success')
    else:
        flash('Incorrect password', 'error')
    return redirect(url_for('updates'))

if __name__ == '__main__':
    app.run(debug=True)
