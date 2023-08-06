import csv

def get_index(input_list, word):
    try:
        index = input_list.index(word)
        return index
    except ValueError:
        return -1

def replace_word(word, label, list1, list2):
    index = get_index(list1, word)
    if index != -1:
        label = label.replace("[mask]", list2[index])
    return label

inputs = []
labels = []

with open('sample.csv', 'r') as f:
    reader = csv.DictReader(f)
    for col in reader:
        inputs.append(col["input"])
        labels.append(col["label"])

list1 = []
list2 = []

with open('sample2.csv', 'r') as f:
    reader = csv.DictReader(f)
    for col in reader:
        list1.append(col["input"])
        list2.append(col["label"])

while True:
    user_input = input("Enter a word: ")
    if user_input == "quit":
        break
    index = get_index(inputs, user_input)
    if index != -1:
        label = labels[index]
        words = label.split()
        for word in words:
            if "[mask]" in word:
                label = replace_word(user_input, label, list1, list2)
                break
        print("Label:", label)
    else:
        print("Word not found in inputs")
