import random
import json 
import pickle
import numpy  as np 

import nltk
from nltk.stem import WordNetLemmatizer


# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Activation, Dropout 
# from tensorflow.keras.optimizers import SGD

from tensorflow import keras
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD





lemmatizer = WordNetLemmatizer()

objectives = json.loads(open('objectives.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!','.', ',']

for objective in objectives['objectives']:
    for pattern in objective['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, objective['tag']))
        if objective['tag'] not in classes:
            classes.append(objective['tag'])

# print(documents)    

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

instruction = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0) 

        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        instruction.append([bag, output_row])

random.shuffle(instruction)
instruction = np.array(instruction)

train_x = list(instruction[:, 0])
train_y = list(instruction[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

history = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.model', history)
print("Done")


print(word)
