# Online-File-Handler

**What is Online File Handler?**
  This project was made by me for the problem that whenever teacher or a leader of a larger group requires members to upload their project file or work then they can use this project. Working is defined below.

**index.html**
  In `index.html` there is CSS and HTML Forms from which people can select and uplaod files by entering their name and Unique ID and section.
  Once they select upload then the backend file `main.py` handles it and then it stores the data inside a uploads folder inside a sub-folder of the section. Eg. `uploads->section_name->files`

**login.html**
  You need to login with the your desired password which you have selected in `main.py` file. And once you login you will be redirected to `admin_panel.html` by session authentication.

**admin_panel.html**
  I have used flask_login module to authenticate sessions. Once you logged in then you need to enter the section of which you want to download the file. And then from the `main.py` backend code the file will be downloaded as ZIP due to module `zipfile`.
