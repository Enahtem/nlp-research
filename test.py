import spacy
import networkx as nx
import matplotlib.pyplot as plt
def extract_knowledge(sentence):
    # Load English tokenizer, tagger, parser, NER, and word vectors
    nlp = spacy.load("en_core_web_sm")
    
    # Process the sentence
    doc = nlp(sentence)
    
    knowledge_units = []
    
    # Extract entities and relations
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


# Example text with multiple sentences
text = "All humans are mortal. Socrates is a human. All birds have feathers. A sparrow is a bird."

# Split the text into sentences
sentences = text.split(".")

# Create a directed graph
G = nx.DiGraph()

# Extract knowledge triples for each sentence and add edges to the graph
for sentence in sentences:
    if sentence.strip():  # Ensure the sentence is not empty
        knowledge_units = extract_knowledge(sentence)
        for triple in knowledge_units:
            entity1, relation, entity2 = triple
            G.add_edge(entity1, entity2, label=relation)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, edge_color="black", linewidths=1, font_size=15, arrows=True)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
