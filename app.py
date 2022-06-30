from flask import Flask, render_template, request
import os
from deeplearning import object_detection
from flask_mail import Mail, Message

# webserver gateway interface
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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'
app.config['MAIL_DEFAULT_SENDER'] = 'manovaama@gmail.com'
mail = Mail(app)

# Call the image path
BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'static/upload/')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        print(email)
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)
        
        result = object_detection(path_save)
        
        # Check if the result is Benign send this message
        if result == 'Benign':
            print('sending......')
            recipient = email
            msg = Message('Breast Cancer Test Result', recipients=[recipient])
            msg.body = f'Test Result: {result}, \n' \
                       f'Hello {full_name}, We advise that you visit the hospital so we can further discuss the test ' \
                       'result '
            msg.html = ('<h1>Breast Cancer Test Result</h1>'
                        f'<p><b>Test Result: {result}</b></p>'
                        f'<p>Hello {full_name}, We advise that you visit the hospital so we can further discuss the '
                        f'test result</p> '
                        '<p><b>FBC</b>!</p>')
            mail.send(msg)
        
        else:
            recipient = email
            msg = Message('Breast Cancer Test Result', recipients=[recipient])
            msg.body = f'Test Result: Available, \n' \
                       f'Hello {full_name}, We advise that you visit the hospital so we can further discuss the test ' \
                       'result. '
            msg.html = ('<h1>Breast Cancer Test Result</h1>'
                        f'<p><b>Test Result: Available</b></p>'
                        f'<p>Hello {full_name}, We advise that you visit the hospital so we can further discuss the '
                        f'test result</p> '
                        '<p><b>FBC</b>!</p>')
            mail.send(msg)

        return render_template('index.html', upload=True, upload_image=filename, text=result)

    return render_template('index.html', upload=False)



if __name__ == "__main__":
    app.run(debug=True)
