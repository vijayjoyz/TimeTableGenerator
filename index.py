
from flask import Flask, render_template, request
from timeproc import main,TeachersPartialSolutionPrinter

app = Flask(__name__)

@app.route('/')
def student():
  return render_template('index.html')

@app.route('/load',methods = ['POST', 'GET'])
def load():
  if request.method == 'POST':
      res1 = int(request.form['num_teacher'])
      res2 = int(request.form['num_periods'])
      res3 = int(request.form['num_days'])
      
      my_dict=main(res1,res2,res3)

      return render_template("next.html",result=my_dict)


if __name__ == '__main__':
  app.run(debug = True)