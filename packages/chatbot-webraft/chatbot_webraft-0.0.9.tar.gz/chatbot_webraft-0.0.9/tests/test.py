#Import library
from chatbot_webraft import chatbot

#set model name
model = "my-model"

#create model
chatbot.create_model(model)

#load CSV dataset , Mention input column (question) and label column (answer)
chatbot.dataset("sample2.csv","input","label",model)


#run in loop
while True:
 prompt = input("You: ")
 #run model and parse input
 print("Bot: ",chatbot.model_load("pywriter",prompt,model))