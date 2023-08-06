#Import library
from chatbot import *

#set model name
model = "my-model"

#create model
create_model(model)

#load CSV dataset , Mention input column (question) and label column (answer)
dataset("sample2.csv","input","label",model)


#run in loop
while True:
 prompt = input("You: ")
 #run model and parse input
 print("Bot: ",model_load("pywriter",prompt,model))