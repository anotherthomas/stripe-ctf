import os
import subprocess
import shlex
import sqlite3
from flask import Flask, render_template
from flask.ext.misaka import Misaka

import random
import string

app = Flask(__name__)
Misaka(app)

location='http://localhost'
baseport=8000
install_path = '/opt/ctf'
install_path = '/home/tom/projects/stripe-ctf2/stripe-ctf-2.0'

def generate_password(length=8):
    return ''.join(random.choice(string.printable[:-10]) for x in range(length)).replace("'", "_")

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


def randomize_level0(instance):
    db_path = os.path.join(install_path, instance, '0/level00.db')
    connection = sqlite3.connect(db_path)
    connection.execute('update secrets set secret = ? where key like "hidden%"', (generate_password(),))

def randomize_level1(instance):
    randomize_file(instance, 1, 'level02-password.txt')
    randomize_file(instance, 1, 'secret-combination.txt')

def randomize_level2(instance):
    randomize_file(instance, 2 , 'password.txt')

def randomize_level3(instance):
    level_path = get_level_path(instance, '3')
    randomizer = os.path.join(level_path,'generate_data.py')
    return subprocess.check_output(
            shlex.split(randomizer + " '{path}' '{password}' 'I have a great proof, but the column is too short to put it here' 'Plan for tomorrow: Take over the world'".format(path=level_path, password=generate_password())))

def randomize_level4(instance):
    password = 'password.txt'
    randomize_file(instance, 4, password)
    level_path = get_level_path(instance, 4)
    os.mkdir(os.path.join(level_path, 'public_html'))
    os.link(os.path.join(level_path, password), os.path.join(level_path, 'public_html', password))

def randomize_level5(instance):
    randomize_file(instance, 5, 'password.txt')

def randomize_level6(instance):
    password = 'password.txt'
    randomize_file(instance, 6, password)
    level_path = get_level_path(instance, 6)
    os.mkdir(os.path.join(level_path, 'public_html'))
    os.link(os.path.join(level_path, password), os.path.join(level_path, 'public_html', password))

def randomize_level7(instance):
    level_path = get_level_path(instance, '7')
    randomizer = os.path.join(level_path,'7/bin/python')
    return subprocess.check_output(
            shlex.split(randomizer + " initialize_db.py '{password}'".format(password=generate_password())), cwd=level_path)

def get_level_path(instance, level):
    return os.path.join(install_path, instance, str(level))

def randomize_file(instance, level, filename):
    fullname = os.path.join(get_level_path(instance, level), filename)
    with open(fullname, 'w') as f:
        f.write(generate_password())

randomizers = [locals().get('randomize_level{0}'.format(i), lambda x: x) for i in range(9)]


@app.route('/<instance>/<int:level>/randomize')
def randomize_level(instance, level):
    return randomizers[level](instance) or "randomized"
if __name__ == '__main__':
    app.run(debug=True, port=1025)
