from flask import Flask, render_template
from flask.ext.misaka import Misaka

app = Flask(__name__)
Misaka(app)

location='http://localhost'
baseport=8000


def define_environments(baseport, number):
    return [{'port': baseport+x*50, 'number': x} for x in xrange(number)]

@app.route('/')
def index():
    return render_template('index.html', location=location, environments=define_environments(8000, 10))

@app.route('/user<int:instance>')
@app.route('/<int:instance>')
def levels(instance):
    return render_template('levels.html', location=location, baseport=instance_baseport(instance), user_id=instance)

@app.route('/<int:instance>/nginx')
def nginx(instance):
    return render_template('instance.conf', instance=instance, baseport=instance_baseport(instance))

@app.route('/<int:instance>/supervisor')
def supervisor(instance):
    return render_template('instance.supervisor', instance=instance, baseport=instance_baseport(instance))

@app.route('/<int:instance>/passwords')
def set_password(instance):
    pass

@app.route('/user<int:instance>/level<int:level>')
def show_level(instance, level):
  return render_template('levels/level{0}.html'.format(level), user_id=instance, level=level, baseport=instance_baseport(instance), readme=open('static/{0}.readme'.format(level)).read())
  
@app.route('/readmes/<int:level>')
def show_readme(level):
    return render_template('readme.html', readme=open('static/{0}.readme'.format(level)).read())

def instance_baseport(instance):
  return baseport+(instance*50)

if __name__ == '__main__':
    app.run(debug=True, port=1025)
