import requests

response = requests.get(url="https://type.fit/api/quotes").json()
quotes = [quote["text"].strip(".") for quote in response]

with open("score.txt", "r") as score_file:
    highscore = float(score_file.read())

