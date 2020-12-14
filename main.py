from flask import Flask, redirect, render_template, url_for, request
app = Flask(__name__, static_folder='static')

@app.route('/home')
@app.route('/home/<name>')
def home(name=None):
    return render_template('index.html', args={"name": name})

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    context = {}
    if request.method == 'POST':
        context['name'] = request.form['name']
    return render_template('form.html', context=context)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')