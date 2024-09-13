from flask import Flask, render_template, request, redirect, url_for
import couchdb

app = Flask(__name__, template_folder='../public', static_folder='../public')

# CouchDB connection
couch = couchdb.Server('http://render:render@localhost:5985/')

if 'rendercouch' in couch:
    db = couch['rendercouch']
else:
    db = couch.create('rendercouch')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    number = request.form['number']
    
    # Save to CouchDB
    doc = {'name': name, 'email': email, 'number': number}
    db.save(doc)
    
    return redirect(url_for('userinfo', name=name))


@app.route('/userinfo')
def userinfo():
    name = request.args.get('name')
    
    # Use list() to convert the map object to a list
    result = list(db.find({'selector': {'name': name}}))
    
    # Check if any results are found
    if result:
        user = result[0]
    else:
        user = None  # Handle case where no user is found
    
    return render_template('userinfo.html', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
