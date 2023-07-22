from flask import Flask,request,render_template
import requests
import pickle
import pandas as pd

movies=pd.read_csv('dataset.csv')
similarity=pickle.load(open('similarity.pkl','rb'))

app = Flask(__name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    
    poster_path = data['poster_path']
    try:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        full_path='https://media.istockphoto.com/vectors/error-document-icon-vector-id1060550172?k=6&m=1060550172&s=612x612&w=0&h=gdWxz8H1C8PaxEKF_ItZfo_S-cbQsxC415_n5v9irvs='
    return full_path

@app.route('/')
def home():
    return render_template('index.html',movie_list=sorted(movies['title']))

@app.route('/recommend',methods=['POST','GET'])
def recommend():
    movie=request.form.get('movie_list')
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return render_template('index.html',movie_list=sorted(movies['title']),name=movie,title1=recommended_movie_names[:5],image1=recommended_movie_posters[:5],title2=recommended_movie_names[5:],image2=recommended_movie_posters[5:])



if __name__ == '__main__':
  app.run(debug=True)
