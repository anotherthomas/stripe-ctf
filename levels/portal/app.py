from flask import Flask, render_template

app = Flask(__name__)

location='http://localhost'
baseport=8000


def define_environments(baseport, number):
    return [{'port': baseport+x*50, 'number': x} for x in xrange(number)]

@app.route('/')
def index():
    return render_template('index.html', location=location, environments=define_environments(8000, 10))


@app.route('/<int:instance>')
def levels(instance):
    return render_template('levels.html', location=location, baseport=baseport+(instance*50), user_id=instance)

@app.route('/<int:instance>/nginx')
def nginx(instance):
    return render_template('instance.conf', instance=instance, baseport=baseport)

@app.route('/<int:instance>/supervisor')
def supervisor(instance):
    return render_template('instance.supervisor', instance=instance, baseport=baseport)


if __name__ == '__main__':
    app.run(debug=True, port=1025)
