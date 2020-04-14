from application import app
import requests
import imdb 
from imdb import IMDb, IMDbError
from flask import render_template,request

mv = imdb.IMDb()

@app.route('/',methods=['GET', 'POST'])
def index():
    """Returns the names and details of four movies based on the search string of user from IMDB database """
    if request.method == "POST":
        movie_name = request.form.get('movie')
        movies = mv.search_movie(movie_name,results=4)
        content=[] 
        for i in movies:
            try:
                info={
                    "title": i["title"],
                    "type": i["kind"],
                    "year": i["year"],
                    "id": i.getID(),
                    "poster": i["full-size cover url"]
                }
            except KeyError:
                continue
            content.append(info)
        return render_template('index.html',**locals())    
    else:
        return render_template('index.html')    

@app.route('/results,<id>')
def results(id):
    """Returns various dettails about the specific movie, which user wants to know about. details of ratings,star cast, plot etc are provided using IMDBPY"""
    all_ratings={}  
    plot= ""
    cast={}
    poster="No information is availble"
    rating_category={}
    try:      
        no_of_votes_per_rating= mv.get_movie_vote_details(id)
        rating_category = no_of_votes_per_rating['data']['number of votes']

        movie = mv.get_movie(id)
        poster = movie["full-size cover url"]

        cast_details= mv.get_movie_full_credits(id)
        cast = cast_details['data']['cast']

        plot_details=mv.get_movie_plot(id)
        plot=plot_details['data']['plot']
 
        movie_ratings= mv.get_movie_vote_details(id)
        all_ratings = movie_ratings['data']['demographics']
    except KeyError:
        pass 
    return render_template('results.html',**locals())   
    
@app.route('/actor,<person_id>')
def actor(person_id):
    try:
        person_details = mv.get_person(person_id)
        film1 = person_details['filmography']
        film2= film1[0]
        film3 =film2[" ".join(film2.keys())]
    except KeyError:
        pass    
    try:
        biography = person_details['mini biography']
    except KeyError:
        pass
    try:
        spouse = person_details['spouse']
    except KeyError:
        pass
    try:
        trivia = person_details['trivia']
    except KeyError:
        pass
    try:
        dob = person_details['birth info']
    except KeyError:
        pass                    

    return render_template('actor.html',**locals())
