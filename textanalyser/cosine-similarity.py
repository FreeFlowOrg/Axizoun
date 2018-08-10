import nltk
from nltk.corpus import stopwords

stop_en = stopwords.words('english')

def preprocesing(raw):
    wordlist = nltk.word_tokenize(raw)
    text = [w.lower() for w in wordlist if w not in stop_en ]
    return text

f1 = open('cv.txt','r')
text1 = preprocesing(f1.read())

f2 = open('job_req.txt','r')
text2 = preprocessing(f2.read())

from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
taggeddocs = []
doc1 = TaggedDocument(words= text1, tags = [u'CV'])
taggeddocs.append(doc1)
doc2 = TaggedDocument(words= text2, tags = [u'JOB_REQ'])
taggeddocs.append(doc2)

max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
  
model.build_vocab(taggeddocs)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(taggeddocs,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

similarity = model.n_similarity(text1,text2)
print("Similarity Index : {:4.2f}%".format(similarity*100))

