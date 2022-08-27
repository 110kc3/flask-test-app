"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import UserForm, EncryptionForm
from app.models import User
# import sqlite3

###
# Routing for your application.
###
import json
import uuid


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/users')
def show_users():
    users = db.session.query(User).all() # or you could have used User.query.all()

    return render_template('show_users.html', users=users)

@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user_form = UserForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']
            email = user_form.email.data # You could also have used request.form['email']

            # save user to database
            user = User(name, email)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


########################



from Crypto.Cipher import AES
import base64, os

def generate_secret_key_for_AES_cipher():
        # AES key length must be either 16, 24, or 32 bytes long
    AES_key_length = 16 # use larger value in production
    # generate a random secret key with the decided key length
    # this secret key will be used to create AES cipher for encryption/decryption
    secret_key = os.urandom(AES_key_length)
    # encode this secret key for storing safely in database
    encoded_secret_key = base64.b64encode(secret_key)
    return encoded_secret_key

import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding



# my_password = b"SECRET KEY TO DECRYPT" # decrypt KEY
# print("##############################################")
# print(type(my_password))

# my_data = b"hello I'm text" #what you wand decrypted

# print("key:  {}".format(my_password))
# print("data: {}".format(my_data))
# encrypted = encrypt(my_password, my_data)
# print("\nenc:  {}".format(encrypted))
# decrypted = decrypt(my_password, encrypted)
# print("dec:  {}".format(decrypted))
# print("\ndata match: {}".format(my_data == decrypted))

# print("\nSecond round....")
# encrypted = encrypt(my_password, my_data)
# print("\nenc:  {}".format(encrypted))
# decrypted = decrypt(my_password, encrypted)
# print("dec:  {}".format(decrypted))
# print("\ndata match: {}".format(my_data == decrypted))


####### BEGIN HERE #######

@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt_decrypt():

    encryption_form = EncryptionForm()
    encrypted = ""

    text_to_encrypt = ""

    if request.method == 'POST':
        if encryption_form.validate_on_submit():
            # Get validated data from form
            key = encryption_form.key.data # You could also have used request.form['key']
            text_to_encrypt = encryption_form.text_to_encrypt.data # You could also have used request.form['text_to_encrypt']
            text_to_decrypt = encryption_form.text_to_decrypt.data # You could also have used request.form['text_to_decrypt']

            #   Converting to bytes
            key = (key)
            text_to_encrypt = str.encode(text_to_encrypt)
            text_to_decrypt = str.encode(text_to_decrypt)
            #ENCRYPTION
            if text_to_encrypt and not text_to_decrypt:
                
                
                print("key:  {}".format(key))
                print("data: {}".format(text_to_encrypt))
                encrypted = encrypt(key, text_to_encrypt)
                print(type(encrypted))
                print("\nenc:  {}".format(encrypted))



                flash("Your encrypted text is   " + str(encrypted))
            #DECRYPTION
            if not text_to_encrypt and text_to_decrypt:
                # decrypted = decrypt(my_password, encrypted)

                print(type(key))
                print(type(text_to_decrypt))
                decrypted = decrypt(key, text_to_decrypt)
                print("dec:  {}".format(decrypted))
                print("\ndata match: {}".format(text_to_decrypt == decrypted))


                flash("Your decrypted text is   " + str(decrypted))
            
            #ERROR - 2 inputs
            if text_to_encrypt and text_to_decrypt:
                print("lololo")
            # return redirect(url_for('show_users'))

            

    # flash_errors(encryption_form)
    return render_template('encrypt.html', form=encryption_form)

@app.route('/api/uuid', methods=['GET'])
def generate_uuid():
    """
    Generates a new UUID for the user
    """
    # for(key, value) in request.headers.items():
    #     print(key, value)
    # myuuids  =()
    myuuids = ""
    print(str(myuuids))
    print(type(myuuids))


    for x in range(10):
    
        useragent = str(request.headers.get('User-Agent'))
        myuuid = str(uuid.uuid4())
        myuuids = (myuuids, myuuid)

    print(type(myuuids))

    return json.dumps({'uuid': myuuids, 'useragent': useragent}), 201


# @app.route('/api/uuid', methods=['POST'])
# def generate_uuid_post():
#     """
#     Generates a new UUID for the user and saves it in DB
#     """
#     # for(key, value) in request.headers.items():
#     #     print(key, value)
#     if(request.form.get('generate') == "1"):
#         # print("hello")
        
#         useragent = str(request.headers.get('User-Agent'))

#         #generate uuid
#         myuuid = str(uuid.uuid4())


#         # checking if user already exists
#         # if the uuid exists - generate new one 
#         while UniqueIDs.query.filter_by(uuid=myuuid).first() is not None:
#             myuuid = str(uuid.uuid4())
        
#         try:
#             # save uuid to db
#             new_uuid = UniqueIDs(uuid=myuuid, useragent=useragent)
#             session.add(new_uuid)
#             session.commit()
#         except:
#             session.rollback()
#             raise
#         finally:
#             session.close()
#         return json.dumps({'uuid': myuuid, 'saved_to_db': "yes"}), 201
#     else:
#         return json.dumps({'saved_to_db': "no"}), 201




# @app.route('/view', methods=['GET'])
# def view():
#     """
#     Fetches all UUID saved in the DB
#     """
#     uuids = UniqueIDs.query.all()
#     # response list consisting user details
#     response = list()
 
#     for uuid in uuids:
#         response.append({
#             'id': uuid.id,
#             'uuid': uuid.uuid,
#             'useragent': uuid.useragent
#         })
#     return json.dumps({
#         'status' : 'success',
#         'message': response
#     }), 200

######################



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")

