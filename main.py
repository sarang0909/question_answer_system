from flask import jsonify
import os
from flask import Flask, render_template, request,send_from_directory
import json
from dialogue_manager import *

 
 
 
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
app = Flask(__name__) 
 
dialogue_manager = DialogueManager()


      
@app.route('/')
def upload_form():
   return render_template('upload.html')       
             
         
 
	
@app.route("/upload", methods=['GET', 'POST'])
def upload():   

    context = request.args.get('context', 0, type=str)
    #print(context)
    question = request.args.get('question', 0, type=str)
    #print(question)
    
    answer = dialogue_manager.generate_answer(context,question) 
    return  jsonify(result= 'Answer: '+answer)  
       
       
      
		
if __name__ == '__main__':
   try:
    #app.run(debug = True)
        app.run(host = "0.0.0.0")
   except Exception as e:
        print("Failed in script at: " + str(e))
        #logging.error(str(e))
        
