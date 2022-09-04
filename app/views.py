"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import base64
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import AlgorithmResultsForm, SortForm, UserForm, EncryptionForm
from app.models import AlgorithmResults, User
import json
import uuid
from app.utils.sorting_algorithms import bubble_sort, insertion_sort, quick_sort



@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response



## encryption functions - TODO, broken input and output
def encrypt(message): 
    return base64.b64encode(message.encode('utf-8'))

def decrypt(message_to_decrypt):
    return base64.b64decode(message_to_decrypt).decode('utf-8')


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


#################################### REST endpoints

import time
from time import perf_counter

@app.route('/api/bubblesort', methods=['POST'])
def bubblesort():
    """
    Sorts specified numbers from ascending to descending using bubble sort algorithm

    Input:
    {"numbers_to_sort": [5,1,2,...]}

    Output:
    {"number_of_elements": 5148, "sorting_algorithm": "bubble_sort", "time_of_execution (ms)": 1958.4866, "sorted_numbers": [1, 2, 5 ...]} 
    """
    try:
        table_to_sort = request.json["numbers_to_sort"]

        number_of_elements = len(table_to_sort)
 
        # COUNTER START https://towardsdatascience.com/execution-times-in-python-ed45ecc1bb4d
        start_counter_ns = time.perf_counter()
        sorted_table = bubble_sort(table_to_sort)
        # COUNTER STOP
        end_counter_ns = time.perf_counter()
        timer_s = end_counter_ns - start_counter_ns
        timer_s = float((timer_s))

        #if chosen to save data in db
        if(request.json["save_in_db"] == 1):
            results = AlgorithmResults(number_of_elements, "bubble_sort",timer_s)
            db.session.add(results)
            db.session.commit()

           
        return json.dumps({'number_of_elements': number_of_elements, "sorting_algorithm": "bubble_sort",
            'time_of_execution (ms)':timer_s, 'sorted_numbers': sorted_table}), 201
    except:
        print("Something went wrong with sorting using bubble sort algorithm")
        return 'Something went wrong with sorting using bubble sort algorithm', 400

    
# insertion_sort insertionsort
@app.route('/api/insertionsort', methods=['POST'])
def insertionsort():
    """
    Sorts specified numbers from ascending to descending using insertion sort algorithm

    Input:
    {"numbers_to_sort": [5,1,2,...]}

    Output:
    {"number_of_elements": 5148, "sorting_algorithm": "insertion_sort", "time_of_execution (ms)": 1958.4866, "sorted_numbers": [1, 2, 5 ...]} 
    """
    try:
        table_to_sort = request.json["numbers_to_sort"]

        number_of_elements = len(table_to_sort)
 
        # COUNTER START https://towardsdatascience.com/execution-times-in-python-ed45ecc1bb4d
        start_counter_ns = time.perf_counter()
        sorted_table = insertion_sort(table_to_sort)
        # COUNTER STOP
        end_counter_ns = time.perf_counter()
        timer_s = end_counter_ns - start_counter_ns
        timer_s = float((timer_s))

        #if chosen to save data in db
        if(request.json["save_in_db"] == 1):
            results = AlgorithmResults(number_of_elements, "insertion_sort",timer_s)
            db.session.add(results)
            db.session.commit()

           

        return json.dumps({'number_of_elements': number_of_elements, "sorting_algorithm": "insertion_sort",
            'time_of_execution (ms)':timer_s, 'sorted_numbers': sorted_table}), 201
    except:
        print("Something went wrong with sorting using insertionsort algorithm")
        return 'Something went wrong with sorting using insertionsort algorithm', 400

# quicksort

@app.route('/api/quicksort', methods=['POST'])
def quicksort():
    """
    Sorts specified numbers from ascending to descending using quicksort algorithm

    Input:
    {"numbers_to_sort": [5,1,2,...]}

    Output:
    {"number_of_elements": 5148, "sorting_algorithm": "quicksort", "time_of_execution (ms)": 1958.4866, "sorted_numbers": [1, 2, 5 ...]} 
    """
    try:
        table_to_sort = request.json["numbers_to_sort"]

        number_of_elements = len(table_to_sort)
 
        # COUNTER START https://towardsdatascience.com/execution-times-in-python-ed45ecc1bb4d
        start_counter_ns = time.perf_counter()
        sorted_table = quick_sort(table_to_sort)
        # COUNTER STOP
        end_counter_ns = time.perf_counter()
        timer_s = end_counter_ns - start_counter_ns
        #specifing time to float
        timer_s = float((timer_s))
        #if chosen to save data in db
        if(request.json["save_in_db"] == 1):
            results = AlgorithmResults(number_of_elements, "quicksort",timer_s)
            db.session.add(results)
            db.session.commit()

        return json.dumps({'number_of_elements': number_of_elements, "sorting_algorithm": "quicksort",
            'time_of_execution (s)':timer_s, 'sorted_numbers': sorted_table}), 201
    except:
        print("Something went wrong with sorting using quicksort algorithm")
        return 'Something went wrong with sorting using quicksort algorithm', 400

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

    useragent = str(request.headers.get('User-Agent'))
    myuuid = str(uuid.uuid4())
    myuuids = (myuuids, myuuid)

    print(type(myuuids))

    return json.dumps({'uuid': myuuids, 'useragent': useragent}), 201




@app.route('/api/view', methods=['GET'])
def view():
    """
    Fetches all data saved in the DB for algorithms results
    """
    results = AlgorithmResults.query.all()
    # response list consisting user details
    response = list()
 
    for result in results:
        response.append({
            'number_of_elements': result.number_of_elements,
            'sorting_algorithm': result.sorting_algorithm,
            'time_of_execution': result.time_of_execution
        })
    return json.dumps({
        'status' : 'success',
        'message': response
    }), 200

######################



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")

