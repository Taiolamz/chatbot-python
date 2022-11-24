import random


def random_string():
    random_list = [
        "I do not understand.",
        "Do you mind rephrasing that?",
        "I'm sorry to say, but I didn't get that.",
        "Can u be more descrptive?",
        "I think you should try the Internet"
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]