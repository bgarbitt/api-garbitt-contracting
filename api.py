from flask import (
    Flask, jsonify, 
    request, make_response
)
from flaskext.mysql import MySQL
from flask_mail import (Mail, Message)

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Bretzky2499'
app.config['MYSQL_DATABASE_DB'] = 'gcl'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Flask Mail configurations for telus
app.config['MAIL_SERVER']='smtp.telus.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'garbitt@telus.net'
app.config['MAIL_PASSWORD'] = 'Garbh1943'
app.config['MAIL_USE_SSL'] = True

mysql.init_app(app)

@app.route('/services/retrieve', methods=['POST'])
def retrieve():
    service = request.form['service']
    cur = mysql.connect().cursor()
    cur.execute(
        '''SELECT 'explanation', explanation FROM services WHERE title = %s UNION ALL SELECT 'image', url FROM images WHERE id = (SELECT id FROM services WHERE title = %s) UNION ALL SELECT 'video', url FROM videos WHERE id = (SELECT id FROM services WHERE title = %s)''',
        (service, service, service)
    )
    data = {}
    for row in cur.fetchall():
        if row[0] not in data:
            data[row[0]] = [row[1]]
        else:
            data[row[0]].append(row[1])
    resp = make_response(jsonify(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/', methods=['GET'])
def fleet():
    size = request.args.get('size')
    cur = mysql.connect().cursor()
    cur.execute(
        '''SELECT f.machine, fi.url FROM fleet f, fleet_images fi WHERE f.id = fi.id and fi.size = %s''', 
        (size,)
    )
    data = {}
    for row in cur.fetchall():
        if row[0] not in data:
            data[row[0]] = [row[1]]
        else:
            data[row[0]].append(row[1])
    resp = make_response(jsonify(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp



@app.route('/contact', methods=['POST'])
def contact():
    mail = Mail(app)

    # The fields the user has filled out (might be empty)
    name = request.form['name']
    organization = request.form['organization']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    if not name:
        name = "[no name given]"
    if not organization:
        organization = "[no organization given]"
    if not email:
        email = "[no email given]"
    if not phone:
        phone = "[no phone number given]"
    if not message:
        message = "[no message given]"
    body = \
        "Name: " + name + "\n" + \
        "Organization: " + organization + "\n" + \
        "Email: " + email + "\n" + \
        "Phone: " + phone + "\n" + \
        "Message: " + message + "\n"
    msg = Message(
        "Website Contact Message", 
        sender="garbitt@telus.net",
        recipients=["garbitt@telus.net"]
    )
    msg.body = body
    mail.send(msg)
    data = {"confirmed": True}
    resp = make_response(jsonify(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run()