import sys, pickle

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.feature_extraction.text import TfidfVectorizer

from imblearn.under_sampling import RandomUnderSampler

from nltk.corpus import stopwords

def load_data(file_name):
    
    with open(file_name, "rb") as f:
        return pickle.load(f)

print("Reading input files..")
x = load_data("./" + sys.argv[1])
y = load_data("./" + sys.argv[2])

print("Running vectorizer..")
vectorizer = TfidfVectorizer(min_df=3, stop_words=stopwords.words("english"))
x = vectorizer.fit_transform(x)

print("Splitting..")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
del x,y # Free up ~3 gigabytes (with full dataset).

# print("Undersampling..")
# rus = RandomUnderSampler(random_state=0)
# x_train, y_train = rus.fit_resample(x_train,y_train)

print("Running..")

# Still gives ConvergenceWarnings with complete_output.
svc = LinearSVC(max_iter=1000, class_weight='balanced')

#[2**x for x in range(-15,17)]

classifier = GridSearchCV(svc, {'C': [1, 10, 100,]}, cv=5, 
                            scoring='f1', n_jobs=20, pre_dispatch=20)

classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

# import pdb
# pdb.set_trace()

print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1:", f1_score(y_test, y_pred))

with open('../partial_1000iter_svm', 'wb') as f:
    pickle.dump(classifier, f)