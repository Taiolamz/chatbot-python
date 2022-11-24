import json
import re
import random_response


# To load the JSON data
def load_json(document):
    with open(document) as chatbot_responses:
        print("Bot is here to help! :)")
        return json.load(chatbot_responses)


# to store the json data
response_data = load_json("chatbot.json")


def fetch_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):

            for word in split_message:

                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)

#  To confirm empty inputs
    if input_string == "":
        return "I don't speak quiet, Kindly type in something ;)"

    
    if best_response != 0:
        return response_data[response_index]["chatbot_response"]

    return random_response.random_string()


while True:
    user_input = input("You: ")
    print("Bot:", fetch_response(user_input))
