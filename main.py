from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os
from zipfile import ZipFile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key' 

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    return render_template('index.html')

class User(UserMixin):
  pass


@login_manager.user_loader
def user_loader(username):
  user = User()
  user.id = username
  return user


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
      password = request.form['password']
      if password == 'admin':  
          user = User()
          user.id = 'admin'
          login_user(user)
          return redirect(url_for('admin_panel'))
  return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    class_section = request.form['class_section']
    name = request.form['name']
    reg_number = request.form['reg_number']

    if file.filename == '':
        return redirect(request.url)

    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], class_section)
    os.makedirs(folder_path, exist_ok=True)

    filename = f'{name}_{reg_number}{os.path.splitext(file.filename)[1]}'
    file.save(os.path.join(folder_path, filename))

    return redirect(url_for('index'))

@app.route('/admin_panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if request.method == 'POST':
        section = request.form['section']
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], section)):
            zip_filename = f'{section}_files.zip'
            zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
            with ZipFile(zip_path, 'w') as zip_file:
                folder_path = os.path.join(app.config['UPLOAD_FOLDER'], section)
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zip_file.write(file_path, arcname=arcname)

            # Serve the zip file for download
            return send_from_directory(app.config['UPLOAD_FOLDER'], zip_filename, as_attachment=True)

        else:
            return render_template('admin_panel.html', message='Section not found!')

    return render_template('admin_panel.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
