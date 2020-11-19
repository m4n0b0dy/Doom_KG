import spacy
from spacy.lang.en import English
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine

def appendChunk(original, chunk):
    return original + ' ' + chunk

def isRelationCandidate(token):
    deps = ["ROOT", "adj", "attr", "agent", "amod"]
    return any(subs in token.dep_ for subs in deps)

def isConstructionCandidate(token):
    deps = ["compound", "prep", "conj", "mod"]
    return any(subs in token.dep_ for subs in deps)

def processSubjectObjectPairs(tokens, entities):
    subject = ''
    object = ''
    relation = ''
    subjectConstruction = ''
    objectConstruction = ''
    for token in tokens:
        #printToken(token)
        if "punct" in token.dep_:
            continue
        if isRelationCandidate(token):
            relation = appendChunk(relation, token.lemma_)
        if isConstructionCandidate(token):
            if subjectConstruction:
                subjectConstruction = appendChunk(subjectConstruction, token.text)
            if objectConstruction:
                objectConstruction = appendChunk(objectConstruction, token.text)
        if "subj" in token.dep_ and token.text in entities:
            subject = appendChunk(subject, token.text)
            subject = appendChunk(subjectConstruction, subject)
            subjectConstruction = ''
        if "obj" in token.dep_ and token.text in entities:
            object = appendChunk(object, token.text)
            object = appendChunk(objectConstruction, object)
            objectConstruction = ''

    print (subject.strip(), ",", relation.strip(), ",", object.strip())
    return (subject.strip(), relation.strip(), object.strip())

def processSentence(sentence, nlp_model):
    tokens = nlp_model(sentence)
    entities = [_.text for _ in tokens.ents]
    return processSubjectObjectPairs(tokens, entities)

def printGraph(triples):
    G = nx.Graph()
    for triple in triples:
        G.add_node(triple[0])
        G.add_node(triple[1])
        G.add_node(triple[2])
        G.add_edge(triple[0], triple[1])
        G.add_edge(triple[1], triple[2])

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='seagreen', alpha=0.9,
            labels={node: node for node in G.nodes()})
    plt.axis('off')
    plt.show()

REL_TYPES = [('relate','related to'),
             ('interacted','related to'),
             ('perform','performed with'),
             ('worked with','performed with'),
             ('count','count'),
            ('many','count'),
            ('amount','count')]

def findClosestMatch(rel, nlp_model):
    rel_vec = nlp_model(rel).vector
    cls_dist = 1
    mtch = None
    for rel_typ in REL_TYPES:
        _dist = cosine(rel_vec, nlp_model(rel_typ[0]).vector)
        if _dist < cls_dist:
            cls_dist = _dist
            mtch = rel_typ[1]
    return mtch, cls_dist
            
        
        
    