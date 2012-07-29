from flask import Flask, request, render_template
from pymongo import Connection
from bson import ObjectId
import os
import time
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def main():
    
    previous_day = datetime.now() - timedelta(hours = 6)
    timestamp = time.mktime(previous_day.timetuple())
    
    connection = Connection()
    db = connection.developerhealth
    hrm = []
    for row in db.hrm.find({"time": {'$gt': timestamp}}):
        hrm.append((row['value'], row['time'] * 1000))
    
    commits = []
    for row in db.payloads.find({"time": {'$gt': timestamp}}).sort('time', -1):
        commits.append(row)
    
    return render_template('index.html', hrm = hrm, commits = commits)
    
@app.route('/details/<string:detail_id>')
def details(detail_id):
    
    connection = Connection()
    db = connection.developerhealth
    
    try:
        time_id = float(detail_id) / 1000
        print time_id
        result = db.payloads.find_one({'time': time_id})
    except:
        detail_id = ObjectId(detail_id)
        result = db.payloads.find_one({'_id': detail_id})
    print result
    
    return render_template('details.html', payload = result)
    
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
            filename = os.path.join(path, 'static/uploads/', filename)
            f = request.files['photofile']
            f.save(filename)
            return "SUCCESS"
        except Exception, ex:
            print ex
            return "argh"
    else:
        return "post: " + str(post_id)
    
if __name__ == "__main__":
    #app.debug = True
    app.run(host="0.0.0.0")
    #app.run()