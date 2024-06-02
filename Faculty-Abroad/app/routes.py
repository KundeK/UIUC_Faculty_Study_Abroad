""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/delete/<string:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<string:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()
    print(task_id, data)

    try:
        if "first_name" in data:
            db_helper.update_exp_entry(task_id,
                                       data["first_name"], 
                                       data['last_name'], 
                                       data['course'], 
                                       data['semester'],
                                       data['year']
                                    )
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


# @app.route("/create", methods=['POST'])
# def create():
#     """ recieves post requests to add new task """
#     data = request.get_json()
#     db_helper.insert_new_task(data['first_name'], data['last_name'], data['course'], data['semester'], data['year'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)


@app.route("/")
def landingPage():
    """ returns landing page """
    return render_template("landing.html")


@app.route("/webapp")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_todo()
    rand_unis = db_helper.stored_procedure()
    return render_template("index.html", items=items, rand_unis=rand_unis)


@app.route('/create', methods=['POST'])
def add_experience():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    course = data.get('course')
    semester = data.get('semester')
    year = data.get('year')

    # Call the insert_new_experience function and pass the required parameters.
    experience_id = db_helper.insert_new_task(first_name, last_name, course, semester, year)

    # Return a success response with the new experience ID.
    return jsonify({'experience_id': experience_id}), 200


@app.route('/stored_proc', methods=['POST'])
def stored_procedure():
    result = db_helper.stored_procedure()
    return jsonify(result), 200