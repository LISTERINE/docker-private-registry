# Copyright 2014 Evan Hazlett and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import (Flask, redirect, request, abort, render_template, url_for,
        flash)
import os
import htpasswd
from htpasswd.basic import UserExists, UserNotExists
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '1f214b8e0330ba5a39d6304')

USER_DB = os.getenv('USER_DB', '/etc/registry.users')

registry_url = "http://localhost:5000/v1/"

@app.route("/")
def index():
    auth = request.authorization
    if not app.config['DEBUG']:
        # only allow the admin user
        if auth.username != 'admin':
            abort(403)
    with htpasswd.Basic(USER_DB) as userdb:
        users = userdb.users
    ctx = {
        'users': userdb.users,
    }
    return render_template('index.html', **ctx)

@app.route('/add/', methods=["POST"])
def add_user():
    username = request.form['username']
    password = request.form['password']
    with htpasswd.Basic(USER_DB) as userdb:
        try:
            userdb.add(username, password)
        except UserExists: # user exists
            flash('Error: user already exists', 'danger')
    return redirect(url_for('index'))

@app.route('/delete/<username>/')
def delete_user(username=None):
    # do not allow the admin user to be deleted
    if username == 'admin':
        flash('Error: you cannot delete the admin user', 'danger')
    else:
        with htpasswd.Basic(USER_DB) as userdb:
            try:
                userdb.pop(username)
                print("User deleted: {}".format(username))
            except UserNotExists:
                pass
    return redirect(url_for('index'))

@app.route('/update/<username>/', methods=["POST"])
def change_password(username=None):
    password = request.form['password']
    print("Updating password for {}".format(username))
    with htpasswd.Basic(USER_DB) as userdb:
        try:
            userdb.change_password(username, password)
            flash('Password updated', 'success')
        except UserNotExists:
            flash('Error: unknown user', 'danger')
    return redirect(url_for('index'))

@app.route('/raw/<path:registry_path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def raw(registry_path):
    target_url = registry_url+registry_path
    registry_response = {}
    if request.method == "GET":
        target_url = target_url+"?"+request.query_string if request.query_string else target_url
        registry_response = requests.get(target_url).json()
    elif request.method == "POST":
        registry_response = requests.post(target_url, json=request.get_json())
    elif request.method == "PUT":
        registry_response = requests.put(target_url, json=request.get_json())
    else:
        registry_response = {"success":False, "reason":"unsupported method"}
    return json.dumps(registry_response)

@app.route('/registry/repos')
def repositories():
    repos = []
    response = requests.get(registry_url+'search').json()
    for result in response['results']:
        repo, image = result['name'].split('/')
        repos.append({"repository": repo, "image": image})
    return json.dumps({"data":repos})

@app.route('/registry')
def registry():
    return render_template('registry.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
