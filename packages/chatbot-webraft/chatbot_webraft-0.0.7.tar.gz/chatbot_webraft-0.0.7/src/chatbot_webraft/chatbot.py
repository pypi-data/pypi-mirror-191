# Library Created By Webraft on 9/2/22
import csv
import ast
import textwrap
import os.path
import difflib
import os.path
import random

def create_model(name):
    global model_name
    model_name = name


def importerror(filename,cmd):
    if os.path.exists(filename):
        return
    else:
        print("Error 3: No File Found with Name ",filename," in ",cmd)
        exit()


def nameerror(name,FUNCTION):
    global model_name
    if model_name == name:
        return
    else:
        print("Error 1: Model ",name, " NOT Found in ",FUNCTION)
        exit()


def dataset(filepath, input, label, model):
    global model_name
    nameerror(model,"chatbot.dataset()")
    importerror(filepath, "chatbot.dataset()")
    filename = open(filepath, 'r')
    file = csv.DictReader(filename)
    global words_list1
    global words_list2
    words_list1 = []
    words_list2 = []
    # creating dictreader object
    for col in file:
        words_list1.append(col[input])
        words_list2.append(col[label])
    for i in range(len(words_list1)):
        words_list1[i] = words_list1[i].lower()
    for i in range(len(words_list2)):
        words_list2[i] = words_list2[i].lower()

def add_data(model, input, label):
    global words_list1
    global words_list2
    nameerror(model,"chatbot.add_data()")
    words_list1.append(input)
    words_list2.append(label)


def spim(word, model,words_list1,words_list2):

    nameerror(model,"chatbot.model_run")

    closest_index = -1
    closest_distance = float("inf")
    for i, w in enumerate(words_list1):
        distance = abs(len(word) - len(w))
        if distance < closest_distance:
            closest_index = i
            closest_distance = distance
    return words_list2[closest_index]


def spimx(word,model,words_list1,words_list2):
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    nltk.download('stopwords',quiet=True)
    nltk.download('punkt',quiet=True)

    def preprocess_text(text):
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-z]+', ' ', text)
        # Tokenize the text
        words = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        # Stem the words
        stemmer = PorterStemmer()
        words = [stemmer.stem(word) for word in words]
        return words

    def load_data(words_list1,words_list2):
        # Open the CSV file

            input_data = words_list1
            label_data = words_list2
            # Iterate through each row

            return input_data, label_data

    def get_similarity(word, words_list):
        # Preprocess the input word
        word = preprocess_text(word)
        # Initialize a list to store the similarity scores
        similarity_scores = []
        # Iterate through each word in the words list
        for w in words_list:
            # Preprocess the word in the words list
            w = preprocess_text(w)
            # Calculate the similarity score between the two words
            if len(set(word).union(w)) == 0:
                score = random.randint(0,20)
            else:
                score = len(set(word).intersection(w)) / len(set(word).union(w))


            similarity_scores.append(score)
        # Return the index of the most similar word
        return similarity_scores.index(max(similarity_scores))


        # Load the data from the CSV file

    input_data, label_data = load_data(words_list1,words_list2)
    # Get the user input
    input_word = word
    # Find the index of the most similar word in the input data
    index = get_similarity(input_word, input_data)
    # Output the corresponding label from the label data
    return label_data[index]

def rasv(word,model,words_list1,words_list2):
    def get_similar_word2(input_word, words_list):
        match = difflib.get_close_matches(input_word, words_list, n=1, cutoff=0.6)
        if match:
            return match[0]
        else:
            return None

    def get_answer(input_word, words_list1, words_list2):
        similar_word = get_similar_word2(input_word, words_list1)
        if similar_word:
            index = words_list1.index(similar_word)
            return words_list2[index]
        else:
            return "No output in dataset for this input"



    return get_answer(word, words_list1, words_list2)
def spimxr(word,model,words_list1,words_list2):
    closest_indices = [-1, -1]
    closest_distances = [float("inf"), float("inf")]
    for i, w in enumerate(words_list1):
        distance = abs(len(word) - len(w))
        if distance < closest_distances[0]:
            closest_indices[1] = closest_indices[0]
            closest_distances[1] = closest_distances[0]
            closest_indices[0] = i
            closest_distances[0] = distance
        elif distance < closest_distances[1]:
            closest_indices[1] = i
            closest_distances[1] = distance
    return words_list2[closest_indices[0]], words_list2[closest_indices[1]]
def mask(prompt,answer,maskdataset1):
    filename = open(maskdataset1, 'r')
    file = csv.DictReader(filename)
    global mask_list1
    global mask_list2
    mask_list1 = []
    mask_list2 = []
    # creating dictreader object
    for col in file:
        mask_list1.append(col["mask"])
        mask_list2.append(col["return"])
    for i in range(len(mask_list1)):
        mask_list1[i] = mask_list1[i].lower()
    for i in range(len(mask_list2)):
        mask_list2[i] = mask_list2[i].lower()

def load_file_as_function(file_path):
    # Open the file for reading
    importerror(file_path, "model_load()")
    with open(file_path, 'r') as file:
        # Read the contents of the file
        file_contents = file.read()

    # Define a function with the contents of the file as its body

    exec(f'def loaded_function(word,wordslist1,wordslist2):\n{textwrap.indent(file_contents, "    ")}', locals())

    # Return the newly defined function
    return locals()['loaded_function']

def modeltype_load(modelfile,word,wordslist1,wordslist2):
    global words_list1
    global words_list2

    loaded_func = load_file_as_function(modelfile)
    return loaded_func(word,wordslist1,wordslist2)

def model_load(modeltype,input, model):
    global words_list1
    global words_list2
    global model_name
    input = input.lower()
    nameerror(model,"chatbot.model_load()")
    if modeltype == "spim":
        return spim(input,model,words_list1,words_list2)
    elif modeltype == "spimx":
        return spimx(input,model,words_list1,words_list2)
    elif modeltype == "rasv":
        return rasv(input,model,words_list1,words_list2)
    elif modeltype == "spimxr":
        return spimxr(input,model,words_list1,words_list2)
    else:
        return modeltype_load(modeltype,input,words_list1,words_list2)





