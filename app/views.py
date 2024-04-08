"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from app import app, db
from flask import render_template, url_for, request, make_response, jsonify, send_file, flash, redirect
from flask_wtf.csrf import generate_csrf
from datetime import datetime
import os

from app.forms import MovieForm
from app.models import Movies
from werkzeug.utils import secure_filename, send_from_directory

app.config['UPLOAD_FOLDER'] = './uploads'
###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm() # Initialize Form

    if form.validate_on_submit(): 
        # Create a new Movie object with the form data
        file = form.photo.data

        new_movie = Movies(
            title=form.title.data,
            description=form.description.data,
            poster=secure_filename(file.filename),
            created_at=datetime.now()
        )

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        db.session.add(new_movie)
        db.session.commit()
        flash('Movie Added Successfully', 'success')
        
        response = make_response(jsonify({"message": "Movie successfully created", "title": new_movie.title, "poster": new_movie.poster, "description": new_movie.description}), 201)
        return response
    else:
        errors = form_errors(form)
        response = jsonify({"errors": errors})
        return make_response(response, 400)
    
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()}) 

@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    try:
        # print("success")
        movies = Movies.query.all()
        movies_list = []
        for movie in movies:
            movie_data = {
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                # 'poster': f'/api/v1/posters/{movie.poster}'

                'poster': movie.poster  # Assuming poster is a filename
            }
            # get_poster(movie_data['poster'])
            movies_list.append(movie_data)
        return jsonify({'movies': movies_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Below function does not work for me
@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        os.abort(404)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404