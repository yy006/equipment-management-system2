from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20))
    acquisition_date = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String(20))
    university_item_number = db.Column(db.String(20))
    budget = db.Column(db.String(20))

@app.route('/api/posts', methods=['GET', 'POST'])
def api_posts():
    if request.method == 'GET':
        posts = Post.query.all()
        post_list = []
        for post in posts:
            post_data = {
                'id': post.id,
                'object': post.object,
                'username': post.username,
                'acquisition_date': post.acquisition_date.strftime('%Y-%m-%d'),
                'place': post.place,
                'university_item_number': post.university_item_number,
                'budget': post.budget
            }
            post_list.append(post_data)
        return jsonify(post_list)
    elif request.method == 'POST':
        data = request.get_json()
        id = data.get('id')
        object = data.get('object')
        acquisition_date = datetime.strptime(data.get('acquisition_date'), '%Y-%m-%d')
        username = data.get('username')
        place = data.get('place')
        university_item_number = data.get('university_item_number')
        budget = data.get('budget')

        new_post = Post(id=id, object=object, acquisition_date=acquisition_date, username=username, place=place, university_item_number=university_item_number, budget=budget)

        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message": "success"})

if __name__ == "__main__":
    app.run(debug=True)
