from flask import Flask, request, jsonify, render_template
import math

app = Flask(__name__)

history_file = "history.txt"

def save_history(entry):
    with open(history_file, 'a') as file:
        file.write(entry + '\n')

def load_history():
    history = []
    with open(history_file, 'r') as file:
        for line in file:
            history.append(line.rstrip('\n'))
    return history


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.get_json()['expression']
    try:
        result = eval(expression)
        entry = f"Expression: {expression}, Result: {result}"
        save_history(entry)
        return jsonify({"result": result})
    except Exception as e:
        result = eval(expression, {'__builtins__': None}, math.__dict__)
        entry = f"Expression: {expression}, Result: {result}"
        save_history(entry)
        return jsonify({'result': result})


@app.route('/history', methods=['GET'])
def get_history():
    history = load_history()
    return jsonify(history)



if __name__ == '__main__':
    app.run()