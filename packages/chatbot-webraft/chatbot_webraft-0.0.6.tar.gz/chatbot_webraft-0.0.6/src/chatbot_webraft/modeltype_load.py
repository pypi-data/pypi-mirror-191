import ast
import textwrap
import os.path
def importerror(filename,cmd):
    if os.path.exists(filename):
        return
    else:
        print("Error 3: No File Found with Name ",filename," in ",cmd)
        exit()
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






