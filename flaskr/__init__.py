import os

from flask import Flask
from flask import render_template, request, redirect, url_for, session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def main():
        return render_template(
            'index.html',
            static_url_path='', 
            static_folder='static'
        )
        # return 'Hello, World!'

    @app.route('/screen', methods=['GET', 'POST'])
    def screen():
        form = request.form
        if request.method == "POST":
            total_score = 0
            
            for key in request.form:
                if key.startswith('answer-'):
                    total_score += float(request.form[key])

            print('total_score', total_score)
            if total_score >= 2:
                diagnosis="Probable migraine - consider triptan therapy (imitrex 50 mg, relpax 40 mg)"
            else:
                diagnosis="Not likely to be migraine - consider other types of headaches and referral to neurology."
            return redirect(url_for('results', form=form, diagnosis=diagnosis))

        return render_template(
            'screen.html',
            static_url_path='', 
            static_folder='static'
        )
    
    @app.route('/results', methods=['GET', 'POST'])
    def results():
        if 'diagnosis' in str(request):
            diagnosis = request.args.get('diagnosis')
        else:
            diagnosis = 'test'
        return render_template(
            'results.html',
            static_url_path='',
            static_folder='static',
            diagnosis=diagnosis
        )
    
    return app