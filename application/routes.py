from application import app
import requests
import imdb 
from imdb import IMDb, IMDbError
from flask import render_template,request

mv = imdb.IMDb()

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        movie_name = request.form.get('movie')
        movies = mv.search_movie(movie_name,results=5)
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
    all_ratings={}  
    plot= ""
    cast={}
    poster="No information is availble"
    rating_category={}
    try:
        #Various rating scales and votes
        no_of_votes_per_rating= mv.get_movie_vote_details(id)
        rating_category = no_of_votes_per_rating['data']['number of votes']
        #cover url
        movie = mv.get_movie(id)
        poster = movie["full-size cover url"]
        #cast details
        cast_details= mv.get_movie_full_credits(id)
        cast = cast_details['data']['cast']
        #plot details
        plot_details=mv.get_movie_plot(id)
        plot=plot_details['data']['plot']
        #movie ratings
        movie_ratings= mv.get_movie_vote_details(id)
        all_ratings = movie_ratings['data']['demographics']
    except KeyError:
        pass 
    return render_template('results.html',**locals())   
    
@app.route('/actor,<person_id>')
def actor(person_id):
    dob={"DOB" : "No info"}
    try:
        person_details = mv.get_person(person_id)
        dob = person_details['birth info']
    except KeyError:
        pass     
    return render_template('actor.html',**locals())