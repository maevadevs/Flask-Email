# Dependencies
from flask import Flask
from flask_mail import Mail, Message
from dotenv import dotenv_values

# Load env variables from .env file
config = dotenv_values('.env')

# Initiate a Flask Server
server = Flask(__name__)

# server.config defines all the configuration of the mail server
# print(server.config)

# Customizing the server for our purpose
server.config['MAIL_SERVER'] = config['mail_server']                                    # Address of mail server: Default 'localhost'
server.config['MAIL_PORT'] = int(config['mail_port'])                                   # Port of the mail server: Default 25 (SMTP)
server.config['MAIL_USE_TLS'] = bool(int(config['mail_use_tls']))                       # Whether to use TLS or not: Default False
server.config['MAIL_USE_SSL'] = bool(int(config['mail_use_ssl']))                       # Whether to use SSL or not: Default False
server.config['MAIL_DEBUG'] = bool(int(config['mail_debug']))                           # Given the same value as the overall DEBUG config in the app
server.config['MAIL_USERNAME'] = config['mail_username']                                # Login account for mail server: Default None
server.config['MAIL_PASSWORD'] = config['mail_password']                                # Login account for mail server: Default None   
server.config['MAIL_DEFAULT_SENDER'] = config['mail_default_sender']                    # Default of the "From" field as origin of emails: Default None. Use tuple (name, address) if wanting name
server.config['MAIL_MAX_EMAILS'] = int(config['mail_max_emails'])                       # Max limits of emails to send per call: Default None
server.config['MAIL_SUPRESS_SEND'] = bool(int(config['mail_supress_send']))             # Given the same value as the overall TESTING config: Default False
server.config['MAIL_ASCII_ATTACHMENTS'] = bool(int(config['mail_ascii_attachments']))   # Convert attachement names to ASCII: Default False

# Instantiate and Initialize the mail server
mail_server = Mail()
mail_server.init_app(server)


# Useless index
@server.route('/')
def index():
    return 'Nothing here. Move along!'


# Create a Route to send emails
@server.route('/send')
def send():

    # Create a new message
    msg = Message(
        subject ="Title of the Message",
        sender="maeva@ralafi.com",       # Can be skipped since we have a default sender
        recipients=['maevadevs@gmail.com'],  # Can also add more recipients with msg.add_recipient(address)
        cc=[],
        bcc=[],
        attachments=[], # Using the attach() method is recommended
        reply_to=[],
        date=None, # A Date object
        charset='',
        extra_headers={},
        mail_options=[],
        rcpt_options=[]
    )

    # We can also set the message options as additional settings
    msg.body = "Hi there! This is the body of the message. Thank you for testing the email option!"

    # If we want to use custom HTML, we can use html instead of body
    # If we use both, the HTML is prioritized
    msg.html = "Hi there! This is the <em>body of the message</em>. There are some <strong>custom HTML</strong> here!"

    # We can also add file attachments
    with server.open_resource('./images/cat.jpg') as image_file:
        msg.attach(
            filename='cat.jpg', 
            content_type='image/jpeg', # MIME Type
            data=image_file.read()
        )

    with server.open_resource('./images/dog.jpg') as image_file:
        msg.attach(
            filename='dog.jpg', 
            content_type='image/jpeg', # MIME Type
            data=image_file.read()
        )

    # Send the message
    mail_server.send(msg)

    # Return a response
    return 'Message has been successfully sent!'


# Create a Route to send bulk emails
@server.route('/bulk')
def bulk():

    # list of users
    users = [{
        'name': 'john',
        'email': 'john@test.com'
    }, {
        'name': 'marie',
        'email': 'maria@test.com'
    }]

    # Open a connection for sending all emails
    # Connection will close and restart once the MAIL_MAX_EMAILS limit is reached
    with mail_server.connect as conn:
        for user in users:
            # Create a new message
            msg = Message(
                subject ="Title of the Message",
                sender="maevadevs@gmail.com",       # Can be skipped since we have a default sender
                recipients=[user.email],            # Can also add more recipients with msg.add_recipient(address)
                html="Hi there! This is the <em>body of the message</em>. There are some <strong>custom HTML</strong> here!"
            )

            # Send the email via the connection
            conn.send(msg)


# Start server
if __name__ == '__main__':
    server.run()