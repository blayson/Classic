from flask import render_template
from flask import Flask, session
from flask import request
from flask.ext.session import Session


app = Flask(__name__)
app.config.from_object(__name__)
sess = Session()

users = []

@app.route('/', methods=['GET', 'POST'])
def index():
    register_template = 'index.html'
    if request.method == 'POST':
        data = request.form
        if data.get('register'):
            username = data.get('username')
            name = data.get('name')
            password = data.get('password')
            users.append({
                'username':username,
                'name':name,
                'password':password    
            })
            session['username'] = username
            session['name'] = name
            return render_template(
                    register_template, 
                    username=username, 
                    name=name
                )
        elif data.get('login'):
            username = data.get('username')
            password = data.get('password')
            if check_login(username, password):
                session['username'] = username
                session['name'] = name
                return render_template(
                    register_template, 
                    username=username, 
                    name=name
                )
        else:
            return render_template(register_template)
    elif session.get('username'):
        return render_template(
            register_template, 
            username=session['username'], 
            name=session['name']
        )
    return render_template(register_template)


def check_login(username, password):
    return True


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.debug = True
    app.run()
