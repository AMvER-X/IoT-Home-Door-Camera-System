from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
import dropbox
from io import BytesIO
import base64
import paramiko

# Creates a mapping for our urls
views = Blueprint('views', __name__)

@views.route('/')
def index():
    return redirect(url_for('auth.login'))


@views.route('/home', methods=['GET','POST'])
@login_required
def home():
    image_base64 = get_image()
    return render_template("home.html", user=current_user, image_base64=image_base64)
    
@views.route('/get_image')
@login_required
def get_image_from_dropbox():
    image_base64 = get_image()
    return image_base64 if image_base64 else "Error: Could not fetch image", 200

@views.route('/capture_photo', methods=['POST'])
@login_required
def capture_photo():
    try:
        remote_script_exec()  # This will take the photo on the Raspberry Pi and upload it to Dropbox
        image_base64 = get_image()  # Retrieve the image from Dropbox in base64 format
        return jsonify(success = True, image_base64 = image_base64)
    except Exception as e:
        return jsonify(success=False, error=str(e))


# Gets imgage from drop box and and returns it as a base 64 image to be displayed on the website
def get_image():
    access_token = 'Your Token Here'
    photo_path = '/photos.jpg'

    try:
            drop_box = dropbox.Dropbox(access_token)

            #_, dbx_response = drop_box.files_download(photo_path)
            metadata, dbx_response = drop_box.files_download(photo_path)

            # Convert the file content to Base64
            image_data = dbx_response.content
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            return image_base64

    except dropbox.exceptions.DropboxException as e:
        print("Error:", e)
        return
    except dropbox.exceptions.ApiError as e:
        print("API Error:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

# Executes python script on raspberry pi to take the photo and upload to dropbox
def remote_script_exec():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    
    ssh.connect(hostname="192.168.18.105", username="pi", password="password") 

    command = """
    if [ -z "$VIRTUAL_ENV" ]; then
        source /home/pi/ENGproject/env/bin/activate;
    fi
    cd /home/pi/ENGproject && python CamSnapper.py
    """

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    ssh.close()

    if error:
        raise Exception(f"Error executing script: {error}")
    return output