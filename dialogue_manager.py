import numpy as np # Math
import requests # Getting text from websites
import html2text # Converting wiki pages to plain text
from googlesearch import search # Performing Google searches
import re
from simpletransformers.question_answering import QuestionAnsweringModel
from bs4 import BeautifulSoup
from markdown import markdown


 
   
        
class DialogueManager(object):
    def __init__(self):
 
        self.model = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad',use_cuda=False)
         
        
    def predict_answer(self,model, question, contexts, seq_len=512):
        split_context = []
        
        if not isinstance(contexts, list):
            contexts = [contexts]
        
        for context in contexts:
            for i in range(0, len(context), seq_len):
                split_context.append(context[i:i+seq_len])
                
         
        f_data = []
        
        for i, c in enumerate(split_context):
            f_data.append(
                {'qas': 
                  [{'question': question,
                   'id': i,
                   'answers': [{'text': ' ', 'answer_start': 0}],
                   'is_impossible': False}],
                  'context': c
                })
            
        prediction = model.predict(f_data)
         
        preds = [x['answer'].lower().strip() for x in prediction if x['answer'].strip() != '']
        if preds:
          return max(set(preds), key=preds.count)
        return 'No answer'
    
    # Source: https://gist.github.com/lorey/eb15a7f3338f959a78cc3661fbc255fe
    def markdown_to_text(self,markdown_string):
        """ Converts a markdown string to plaintext """

        # md -> html -> text since BeautifulSoup can extract text cleanly
        html = markdown(markdown_string)

        # remove code snippets
        html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
        html = re.sub(r'<code>(.*?)</code >', ' ', html)

        # extract text
        soup = BeautifulSoup(html, "html.parser")
        text = ''.join(soup.findAll(text=True))

        return text

    def format_text(self,text):
        text = self.markdown_to_text(text)
        text = text.replace('\n', ' ')
        return text
        
    def query_pages(self,query, n=5):
        return list(search(query, stop=n))

    def query_to_text(self,query, n=5):
        html_conv = html2text.HTML2Text()
        html_conv.ignore_links = True
        html_conv.escape_all = True
        
        text = []
        for link in self.query_pages(query, n):
            print(link)
            req = requests.get(link)
            text.append(self.format_text(html_conv.handle(req.text)))
            
        return text
        
    def q_to_a(self,model, context, question, n=2):
        if len(context)==0: 
            context = self.query_to_text(question, n=n)
        pred = self.predict_answer(model, question, context)
        return pred
    
    def generate_answer(self, context, question):
        return self.q_to_a(self.model, context, question)
      
         