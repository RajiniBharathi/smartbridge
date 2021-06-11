#flask is our framework which we are going to use to run our application

import numpy as np #used for numerical calculations
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,request,render_template 
import requests
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app=Flask(__name__,template_folder="templates")
model=load_model("fruits.h5")
print("Loaded Model From Disk")

@app.route('/')                         #route to display the home page
def home():
    return render_template('home.html') #rendering the home page

@app.route('/image1',methods=['GET','POST'])  #routes to the index html
def image1():
    return render_template('image.html')

@app.route('/predict',methods=['GET','POST']) #route to show the predictions in a web UI
def uploads():
    if request.method=='POST':
        f=request.files['file'] #resquesting the file
        basepath=os.path.dirname('__file__') #storing the file directory
        filepath=os.path.join(basepath, 'uploads',f.filename) #storing the file in uploads folder
        f.save(filepath) #saving the file
        
        img=image.load_img(filepath,target_size=(64,64)) #loading the reshaped image
        x=image.img_to_array(img) #converting image to array
        
        x=np.expand_dims(x,axis=0)  #changing the diemnsions of the image
        preds=np.argmax(model.predict(x),axis=1)
        print("prediction",preds) #printing the preediction
        index=['GUAVA','APPLE','ORANGE']
        result="The classified Fruit is:"+str(index[preds[0]])
        x=result
        print(x)
        result=nutrition(result)
    return render_template("0.html",showcase=(result),showcase1=(x))
def nutrition(index):
             url="https://calorieninjas.p.rapidapi.com/v1/nutrition"
        
             querystring = {"query":index}
            
             headers = {
                'x-rapidapi-key': "5d797ab107mshe668f26bd044e64p1ffd34jsnf47bfa9a8ee4",
                'x-rapidapi-host': "calorieninjas.p.rapidapi.com"
                }
             response=requests.request("GET",url,headers=headers, params=querystring)
             print(response.text)
             return response.json()['items']
    
if __name__=='__main__':
    #running the app
    app.run(debug=False)