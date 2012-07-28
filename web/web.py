from flask import Flask, request
from pymongo import Connection
import os

app = Flask(__name__)

@app.route('/')
def main():
    return "Hello World"
    
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        try: 
            
            doc = {
                'author': request.form['author'],
                'location': request.form['location'],
                'commit_message': request.form['commit_message'],
                'photo': request.form['photo']
            }
            connection = Connection()
            db = connection.developerhealth
            db.payloads.insert(doc)
            
            
            path = os.path.dirname(os.path.abspath(__file__))
            filename = request.form['photo']
            filename = os.path.join(path, filename)
            f = request.files['photofile']
            f.save(filename)
            return "SUCCESS"
        except Exception, ex:
            print ex
            return "argh"
    else:
        return "post: " + str(post_id)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")