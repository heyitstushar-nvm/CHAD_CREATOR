# app.py
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'purple_fitness_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    action = request.form.get('action')
    if action == 'register':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['region'] = request.form['region']
    else:
        session['name'] = 'Guest User'
        session['email'] = request.form['email']
    session['profile_img'] = ''
    return redirect(url_for('index'))

@app.route('/api/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        activity = request.json
        activities = session.get('activities', [])
        activities.append(activity)
        session['activities'] = activities
        return {'status': 'saved'}
    return {'activities': session.get('activities', [])}

@app.route('/api/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        session['profile_img'] = request.form['img']
        return {'status': 'updated'}
    return {
        'name': session.get('name', 'Guest'),
        'region': session.get('region', 'Unknown'),
        'img': session.get('profile_img', '')
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
