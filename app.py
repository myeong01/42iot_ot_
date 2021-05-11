from flask import Flask, render_template, session, request
app = Flask(__name__)
app.secret_key = 'app secret key'
import os
BROTHER_IP = os.environ["BROTHER_IP"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/print", methods=['GET'])
def print_test():
    from brother import BrotherPrint
    import socket
    import json
    from datetime import datetime

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((BROTHER_IP,9100))
        printjob = BrotherPrint(s)
        printjob.template_mode()
        printjob.template_init()
        printjob.select_and_insert("id", request.args.get('id'))
        printjob.select_and_insert("group", request.args.get('guild'))
        printjob.template_print()
    return render_template("index.html")


#@app.route("/print", methods=['GET'])
def test():
    print("test")
    return ('test')


if __name__=='__main__':
    app.run(host='0.0.0.0')
