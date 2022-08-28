"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import base64
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import SortForm, UserForm, EncryptionForm
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



##################

def encrypt(message): 
    return base64.b64encode(message.encode('utf-8'))

def decrypt(message_to_decrypt):
    return base64.b64decode(message_to_decrypt).decode('utf-8')

####### BEGIN HERE #######

@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt_decrypt():

    encryption_form = EncryptionForm()
    encrypted = ""

    text_to_encrypt = ""

    if request.method == 'POST':
        if encryption_form.validate_on_submit():
            # Get validated data from form
       
            text_to_encrypt = encryption_form.text_to_encrypt.data # You could also have used request.form['text_to_encrypt']
            text_to_decrypt = encryption_form.text_to_decrypt.data # You could also have used request.form['text_to_decrypt']

            #   Converting to bytes
            # key = str.encode(key)
            # text_to_encrypt = str.encode(text_to_encrypt)
            # text_to_decrypt = str.encode(text_to_decrypt)
            #ENCRYPTION
            if text_to_encrypt and not text_to_decrypt:
 
                encrypted = encrypt(text_to_encrypt)
                
                print(type(encrypted))
                print("\nenc:  {}".format(encrypted))

                flash("Your encrypted text is   " + str(encrypted))
            #DECRYPTION
            if not text_to_encrypt and text_to_decrypt:
       

                decrypted = decrypt(text_to_decrypt)
                print("dec:  {}".format(decrypted))
                print("\ndata match: {}".format(text_to_decrypt == decrypted))


                flash("Your decrypted text is   " + str(decrypted))
            
            #ERROR - 2 inputs
            if text_to_encrypt and text_to_decrypt:

                flash("Put text in only 1 box")

            

    # flash_errors(encryption_form)
    return render_template('encrypt.html', form=encryption_form)






######### number sorting
@app.route('/sort', methods=['POST', 'GET'])
def sorting():

    sort_form = SortForm()

    if request.method == 'POST':
        if sort_form.validate_on_submit():
            # Get validated data from form
       
            numbers_to_sort = sort_form.table_to_sort.data # You could also have used request.form['text_to_encrypt']
          
            #   Converting to bytes
            # key = str.encode(key)
            # text_to_encrypt = str.encode(text_to_encrypt)
            # text_to_decrypt = str.encode(text_to_decrypt)
          

            flash("Your decrypted text is   " + str(decrypted))
            
            #ERROR - 2 inputs
            if text_to_encrypt and text_to_decrypt:

                flash("Put text in only 1 box")

    # flash_errors(encryption_form)
    return render_template('encrypt.html', form=sort_form)



#################################### REST
def bubble_sort(array):
    n = len(array)

    for i in range(n):
        # Create a flag that will allow the function to
        # terminate early if there's nothing left to sort
        already_sorted = True

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                array[j], array[j + 1] = array[j + 1], array[j]

                # Since you had to swap two elements,
                # set the `already_sorted` flag to `False` so the
                # algorithm doesn't finish prematurely
                already_sorted = False

        # If there were no swaps during the last iteration,
        # the array is already sorted, and you can terminate
        if already_sorted:
            break

    return array

import time
@app.route('/api/bubblesort', methods=['POST'])
def bubblesort():
    """
    Sorts specified numbers from ascending to descending 

    Input:
    {
    "numbers_to_sort": [
        5,
        1,
        2,
        ...
    ]
    }

    Output:
    {"sorted_numbers": [1, 2, 5, ...]}
    """
    # for(key, value) in request.headers.items():
    #     print(key, value)
    # print(request.json)
    # print(type(request.json))
    time_of_execution = 0

    try:
        table_to_sort = request.json["numbers_to_sort"]

        number_of_elements = len(table_to_sort)

        print("Number of elements in the list: ", number_of_elements)


        # COUNTER START https://towardsdatascience.com/execution-times-in-python-ed45ecc1bb4d
        start_counter_ns = time.perf_counter_ns()
        # for :
        sorted_table = bubble_sort(table_to_sort)
        end_counter_ns = time.perf_counter_ns()
        # COUNTER STOP
        timer_ns = end_counter_ns - start_counter_ns
        print(timer_ns)

        timer_ns = float((timer_ns / 1000000))

        
        time_of_execution = timer_ns
        print(time_of_execution)
        print(sorted_table)
        print(type(sorted_table))

        return json.dumps({'number_of_elements': number_of_elements, 'time_of_execution (ms)':time_of_execution, 'sorted_numbers': sorted_table}), 201
    except:
        print("Something went wrong with sorting numbers")
        return 'Something went wrong with sorting numbers', 400

    




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

