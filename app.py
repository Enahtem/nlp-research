from flask import Flask, render_template, request, jsonify
import spacy
import networkx as nx
import matplotlib.pyplot as plt
import json

app = Flask(__name__)

def rst_parsing(text):
    return text.split(".")

def extract_knowledge(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    knowledge_units = []
    
    for token in doc:   
        if token.dep_ == "nsubj":
            entity1 = token.text
            relation = ""
            entity2 = ""
            for ancestor in token.ancestors:
                if ancestor.dep_ == "ROOT":
                    relation = ancestor.text
                    for child in ancestor.children:
                        if child.dep_ == "attr" or child.dep_ == "dobj":
                            entity2 = child.text
                            break
                    if entity2:
                        break
            if relation and entity2:
                knowledge_units.append((entity1, relation, entity2))
            
    return knowledge_units

def generate_graph_data(text):
    sentences = rst_parsing(text)
    G = nx.DiGraph()
    
    for sentence in sentences:
        if sentence.strip():
            knowledge_units = extract_knowledge(sentence)
            for triple in knowledge_units:
                entity1, relation, entity2 = triple
                G.add_edge(entity1, entity2, label=relation)
    return {"nodes": [{"id": node} for node in G.nodes], "links": [{"source": source, "target": target, "label": data["label"]} for source, target, data in G.edges(data=True)]}









@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    text = request.form['text']
    
    graph_data = generate_graph_data(text)
    return render_template('result.html', graph_data=json.dumps(graph_data))

if __name__ == '__main__':
    app.run(debug=True)
