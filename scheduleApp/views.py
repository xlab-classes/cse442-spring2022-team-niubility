from fileinput import filename
from scheduleApp import app
from flask import request, render_template, redirect,url_for,flash
from scheduleApp.models import Accounts, db
import bcrypt
import os
from werkzeug.utils import secure_filename
from PIL import Image
import base64
import io
@app.route('/', methods=['GET'])
def home():
    return render_template('Login_in.html',msg="hello world!")

@app.route('/Niubility.html', methods=['GET'])
def home1():
    return render_template('Niubility.html')

@app.route('/history.html', methods=['GET'])
def home2():
    return render_template('history.html')

@app.route('/Tasks.html', methods=['GET'])
def home3():
    return render_template('Tasks.html')

@app.route('/register.html', methods=['GET'])
def home4():
    return render_template('register.html')


