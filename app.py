from flask import Flask, render_template, session, request

id_by_name = {}
guild_by_id = {}

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

    try:
        cur_user_name = request.args.get('name')
        user_id = id_by_name[cur_user_name]
        guild_name = guild_by_id[user_id]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((BROTHER_IP,9100))
            printjob = BrotherPrint(s)
            printjob.template_mode()
            printjob.template_init()
            printjob.select_and_insert("id", cur_user_name)
            printjob.select_and_insert("group", guild_name)
            print(cur_user_name)
            print(guild_name)
            printjob.template_print()
        return render_template("index.html")
    except:
        return render_template("index.html", invalid_name=True)

@app.route("/init")
def map_data():
    map_id_and_name()
    map_id_and_guild("42data/gun")
    map_id_and_guild("42data/gon")
    map_id_and_guild("42data/gam")
    map_id_and_guild("42data/lee")
    
    return render_template("index.html")


def map_id_and_name():
    file = open("42data/id_and_intra_name", "r")
    while True:
        line = file.readline()
        if not line:
            break
        user_id, user_name = line.strip().split(sep=":")
        id_by_name[user_name] = user_id
    file.close()


def map_id_and_guild(path):
    file = open(path, "r")
    while True:
        line = file.readline()
        if not line:
            break
        user_id, guild = line.strip().split(sep=":")
        guild_by_id[user_id] = guild
    file.close()
    

if __name__=='__main__':
    app.run(host='0.0.0.0')
