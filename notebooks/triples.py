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

REL_TYPES = [('relate','relation'),
             ('perform with','relation_bool'),
             ('worked with','relation_bool'),
             ('make','relation_bool'),
             ('sing on','relation_bool'),
             ('rap on','relation_bool'),
             ('sing','open_query'),
             ('rap','open_query'),
             ('count','count'),
            ('many','count'),
            ('amount','count')]

def findClosestMatch(rel, nlp_model, obj_exist=True):
    rel_vec = nlp_model(rel).vector
    cls_dist = 1
    mtch = None
    for rel_typ in REL_TYPES:
        _dist = cosine(rel_vec, nlp_model(rel_typ[0]).vector)
        if _dist < cls_dist:
            if obj_exist and rel_typ[1] == 'open_query':
                continue
            cls_dist = _dist
            mtch = rel_typ[1]
    return mtch, cls_dist
        
def cypher_relation(subj,obj):
    query = '''
    MATCH p=(n)-[*3]-(m)
    WHERE toLower(n.name) = "{subj}"
    AND toLower(m.name) = "{obj}"
    RETURN p
    '''.format(subj=subj, obj=obj)
    return query

def cypher_relation_bool(subj,obj):
    query = '''
    MATCH (n),(m)
    WHERE toLower(n.name) = "{subj}"
    AND toLower(m.name) = "{obj}"
    RETURN exists((n)-[*3]-(m))
    '''.format(subj=subj, obj=obj)
    return query

def cypher_open_query(subj,obj):
    query = '''
    MATCH (n)--(m)
    WHERE toLower(n.name) = "{subj}"
    RETURN m
    '''.format(subj=subj)
    return query

def cypher_count(subj,obj):
    query = '''
    MATCH r=(n)--(:Song)--(m)
    WHERE toLower(n.name) = "{subj}"
    AND toLower(m.name) = "{obj}"
    RETURN COUNT(r)
    '''.format(subj=subj, obj=obj)
    return query


def run_cypher_query(subj, rel, obj, sess):
    subj, rel, obj = subj.lower(), rel.lower(), obj.lower()
    if rel=='relation':
        query=cypher_relation(subj, obj)
    elif rel=='relation_bool':
        query=cypher_relation_bool(subj, obj)
    elif rel=='open_query':
        query=cypher_open_query(subj, obj)
    elif rel=='count':
        query=cypher_count(subj, obj)
    query = query.replace('\n','')
    return query, sess.run(query)
    