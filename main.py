from flask import Flask, render_template,request
from gingerit.gingerit import GingerIt
import nltk
import pysbd, re 

app = Flask(__name__)

segmentor = pysbd.Segmenter(language="en", clean=False)
subsegment_re = r'[^;:\n•]+[;,:\n•]?\s*'

def runGinger(par):
    fixed = []
    cor={'corrections':[],'result':'','text':''}
    for sentence in segmentor.segment(par):
        if len(sentence) < 300:
            fixed.append(GingerIt().parse(sentence)['result'])
            if len(GingerIt().parse(sentence)['corrections'])>0:
              cor['corrections'].append(GingerIt().parse(sentence)['corrections'])
        else:
            subsegments = re.findall(subsegment_re, sentence)
            if len(subsegments) == 1 or any(len(v) < 300 for v in subsegments):
                # print(f'Skipped: {sentence}') // No grammar check possible
                fixed.append(sentence)
            else:
                res = []
                for s in subsegments:
                    res.append(GingerIt().parse(s)['result'])
                    if len(GingerIt().parse(sentence)['corrections'])>0:
                      cor['corrections'].append(GingerIt().parse(sentence)['corrections'])
                fixed.append("".join(res))
    cor['result']=" ".join(fixed)
    cor['text']=par
    return cor

@app.route('/')
def index():
    return render_template('firstpage.html')

@app.route('/results',methods=['POST'])
def result():
    txt=request.form.get('description')                
    yes = runGinger(txt)
    num=len(yes['corrections'])
    if num==0:
        yes={'corrections':'None','result':txt}
    return render_template('second page.html',dic=yes,num=num)

@app.route('/',methods=['POST'])
def index2():
    return render_template('firstpage.html')
    


if __name__=="__main__":
    app.run(debug=True)







