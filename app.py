#!/usr/bin/env python3

from flask import Flask, render_template, abort
import os, json

app = Flask(__name__)

result = {}
title_list = []

directory = os.path.join(os.path.abspath(os.path.dirname(__name__)), '.', 'files')
for f_n in os.listdir(directory):
    file_path = os.path.join(directory, f_n)
    with open(file_path, 'r') as f:
        ctt = json.load(f)
        result[f_n[:-5]] = ctt
        title_list.append(f_n[:-5]) 

@app.route('/')
def index():
    return render_template('index.html', title_list=title_list)

@app.route('/files/<filename>')
def file(filename):
    file_item = result[filename]
    return render_template('file.html', file_item=file_item)

