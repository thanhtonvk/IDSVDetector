from flask import *

import Prediction
import Validate

app = Flask(__name__)

@app.route('/')  
def upload():  
    return render_template("index.html")

@app.route('/', methods = ['POST','GET'])
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        dir = './static/'+f.filename
        f.save(dir)
        list = Prediction.prediction(dir)
        sv = Validate.StudentInfo(list)
        return render_template("index.html", student = sv,image = dir)
    else:
        return render_template("index.html")
if __name__ == '__main__':
    app.run()