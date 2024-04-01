import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app=Flask(__name__)


@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/simpan', methods = ['POST'])
def simpan_card() :
    judul_img = request.form['judul_gambar']
    deskripsi_img = request.form['deskripsi_gambar']

    today = datetime.now()
    filetime = today.strftime('%Y-%m-%d-%H-%M-%S')
    datefiletime = today.strftime('%Y-%m-%d')

    file = request.files['gambar_img']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{filetime}.{extension}'
    file.save(filename)

    profile = request.files['profile_img']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{filetime}.{extension}'
    profile.save(profilename)

    doc = {
        'profile' : profilename,
        'file' : filename,
        'judul' : judul_img,
        'deskripsi' : deskripsi_img,
        'waktu' : datefiletime
    }
    db.data1.insert_one(doc)
    return jsonify({
        'msg' : 'data Tersimpan!'
    })


@app.route("/data", methods=["GET"])
def data_get():
    data_gambar = list(db.data1.find({}, {'_id' : False}))
    return jsonify({'gambar': data_gambar})


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)