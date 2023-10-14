from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np


# popular_df = pickle.load(open('../popular.pkl', 'rb'))
# pt = pickle.load(open('../pt.pkl', 'rb'))
# books = pickle.load(open('../books.pkl', 'rb'))
# similarity_scores = pickle.load(open('../similarity_scores.pkl', 'rb'))

popular_df = pd.read_pickle(open('../popular.pkl', 'rb'))
pt = pd.read_pickle(open('../pt.pkl', 'rb'))
books = pd.read_pickle(open('../books.pkl', 'rb'))
similarity_scores = pd.read_pickle(open('../similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    # index = np.where(pt.index == user_input)[0][0]
    indices = np.where(pt.index == user_input)[0]
    if indices.size > 0:
        index = indices[0]
    else:
        # Handle the case where no match is found
        index = None
        print(f"No match found for {user_input}.")
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)
        
        data.append(item)
    
    print(data)
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)