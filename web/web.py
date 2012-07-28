from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def main():
    return "Hello World"
    
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    if request.method == 'POST':
        print request.form
        print request.files
        return "POST"
    else:
        return "post: " + str(post_id)
    
if __name__ == "__main__":
    app.debug = True
    app.run()