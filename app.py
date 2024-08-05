from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'profile-pic' not in request.files or 'images' not in request.files:
            return redirect(request.url)
        profile_pic = request.files['profile-pic']
        images = request.files.getlist('images')
        name = request.form['name']
        bio = request.form['bio']
        
        if profile_pic and allowed_file(profile_pic.filename):
            profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic.filename))
        
        for image in images:
            if image and allowed_file(image.filename):
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        
        # Save other data like name and bio to a database here
        
        return redirect(url_for('profiles'))
    
    return render_template('upload.html')

@app.route('/profiles')
def profiles():
    # Retrieve and display profiles from the database or file system
    return render_template('profiles.html')

@app.route('/profile/<profile_id>')
def profile(profile_id):
    # Retrieve profile details by profile_id
    return render_template('profile_detail.html', profile_id=profile_id)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
