from flask import Flask, render_template, request, redirect, abort, send_from_directory, url_for, send_file

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_SLIDER = 'sliders/'
app.config['UPLOAD_SLIDER'] = UPLOAD_SLIDER

# Directory to store generated HTML files
HTML_DIR = os.path.join(os.getcwd(), 'html_files')

# Directory to store contact files
CONTACTS_DIR = os.path.join(os.getcwd(), 'contacts')

# Directory to store uploaded images
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')


# Directory to store uploaded banner images
UPLOAD_FOLDER_BANNERS = os.path.join(os.getcwd(), 'banners')

# Directory to store uploaded banner images
UPLOAD_FOLDER_Limages = os.path.join(os.getcwd(), 'landingpageimages')


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(HTML_DIR):
    os.makedirs(HTML_DIR)

if not os.path.exists(CONTACTS_DIR):
    os.makedirs(CONTACTS_DIR)

if not os.path.exists(UPLOAD_FOLDER_BANNERS):
    os.makedirs(UPLOAD_FOLDER_BANNERS)

if not os.path.exists(UPLOAD_SLIDER):
    os.makedirs(UPLOAD_SLIDER)

# Allowed extensions for image upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'vcf'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Index route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/email')
def email():
    return render_template('email.html')
@app.route('/home')
def home1():
    return render_template('home-smartconnect.html')
@app.route('/smartconnect')
def home2():
    return render_template('smartconnect.html')
@app.route('/welcome')
def welcome():
    return render_template('Welcomepage.html')

@app.route('/homearabic')
def home3():
    return render_template('home-smartconnectarab.html')



# Generate route
@app.route('/generate', methods=['POST'])
def generate():
    project_name = request.form['project_name']
    project_description = request.form['project_description']
    role = request.form['role']
    background_color = request.form['background_color']

    
    # Check if an image file was uploaded
    if 'image' not in request.files:
        return redirect(request.url)

    image = request.files['image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if image.filename == '':
        return redirect(request.url)

    # Check if the file is allowed
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
    else:
        return abort(400, 'Invalid file format')

    # Check if a banner image file was uploaded
    if 'banner' in request.files:
        banner = request.files['banner']

        if banner and allowed_file(banner.filename):
            banner_filename = secure_filename(banner.filename)
            banner_path = os.path.join(UPLOAD_FOLDER_BANNERS, banner_filename)
            banner.save(banner_path)
        else:
            return abort(400, 'Invalid banner image format')
    # Check if a contact file was uploaded
    if 'contact' in request.files:
      contact = request.files['contact']
      if contact and allowed_file(contact.filename):
         contact_filename = secure_filename(contact.filename)
         contact_path = os.path.join(CONTACTS_DIR, contact_filename)
         contact.save(contact_path)
    else:
         return abort(400, 'Invalid contact file format')
        


    
    link_pairs = [(request.form.get(f'name{i}'), request.form.get(f'url{i}'), request.form.get(f'icon{i}')) for i in range(1, 6) if request.form.get(f'name{i}') and request.form.get(f'url{i}')]

    map_url = request.form.get('map_url')
    video_url = request.form.get('video_url')
    video_url2 = request.form.get('video_url2')
    video_url3 = request.form.get('video_url3')

    # Pass project name, image path, banner path, link pairs, and background color to the page.html template
    rendered_template = render_template('page.html', 
                                         page_name=project_name, 
                                         project_description=project_description, 
                                         role=role, 
                                         image_path=os.path.basename(image_path),
                                         banner_path=os.path.basename(banner_path),
                                         links=link_pairs, 
                                         map_url=map_url,
                                         video_url=video_url,
                                         video_url2=video_url2,
                                         video_url3=video_url3,
                                         contact_path=os.path.basename(contact_path),  
                                         background_color=background_color
                                         )
  

    # Save the rendered template to an HTML file
    html_filename = os.path.join(HTML_DIR, f"{project_name}.html")
    with open(html_filename, 'w') as html_file:
        html_file.write(rendered_template)
    

    
    return redirect(url_for('show_page', page_name=project_name))




# Show page route
@app.route('/pages/<string:page_name>')
def show_page(page_name):
    # Check if the HTML file exists
    filename = os.path.join(HTML_DIR, f"{page_name}.html")
    if os.path.exists(filename):
        return send_from_directory(HTML_DIR, f"{page_name}.html")
    else:
        abort(404)

# Uploaded image route
@app.route('/uploads/<path:filename>')
def get_uploaded_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Banner route
@app.route('/banners/<path:filename>')
def get_banner(filename):
    return send_from_directory(UPLOAD_FOLDER_BANNERS, filename)


@app.route('/landingpageimages/<path:filename>')
def get_limages(filename):
    return send_from_directory(UPLOAD_FOLDER_Limages, filename)





# Contract generator route
@app.route('/contractgenerator')
def contract_generator():
    return render_template('contractgenerator.html', banners=os.listdir(UPLOAD_FOLDER_BANNERS))


if __name__ == '__main__':
    app.run(debug=True)
