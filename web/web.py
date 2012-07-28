from flask import Flask, request
from pymongo import Connection
import os
import time

app = Flask(__name__)

@app.route('/')
def main():
    return "Hello World"
    
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        try: 
            connection = Connection()
            db = connection.developerhealth
            # get the latest hrm
            recent_hrm = db.hrm.find().sort('time', -1).limit(1).next()
            
            doc = {
                'author': request.form['author'],
                'location': request.form['location'],
                'commit_message': request.form['commit_message'],
                'photo': request.form['photo'],
                'hrm': recent_hrm['value'],
                'hrm_time': recent_hrm['time'],
                'time': time.time()
            }
            
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