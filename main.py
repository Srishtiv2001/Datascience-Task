from flask import Flask, render_template,request
from gingerit.gingerit import GingerIt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('firstpage.html')

@app.route('/results',methods=['POST'])
def result():
    txt=request.form.get('description')
    parser = GingerIt()
    dic=parser.parse(txt)
    num=len(dic["corrections"])
    if num==0:
        dic={'corrections':'None','result':txt}
    return render_template('second page.html',dic=dic,num=num)

@app.route('/',methods=['POST'])
def index2():
    return render_template('firstpage.html')
    


if __name__=="__main__":
    app.run(debug=True)







