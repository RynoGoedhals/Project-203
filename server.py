import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 5000

server.bind((ip_address, port))
server.listen()

client_list = []

nicknames = []

questions = [
    "Is the Earth round? \n a. Yes\n b. No",
    "How many moons orbit Earth? \n a. 3 \n b. 4 \n c.2 \n d. 1",
    "What percent of Earth is made of water? \n a. 50% \n b. 30% \n c. 70% \n d. 90%",
    "How long does it take for the Earth to do a full rotation (in hours)? \n a. 10 hours \n b. 24 hours \n c. 14 hours \n d. 20 hours"
]

answers = [
    "a", 
    "d", 
    "c", 
    "b"
]

def clientthread(conn, nickname):
    score = 0

    conn.send("Welcome to the Trivia room!".encode('utf-8'))
    conn.send("When the questions pop up, type the letter that you think has the right answer!\n".encode('utf-8'))

    index, question, answer = random_question_answer(conn)
    print(answer)

    while True:
        try:
            message = conn.recv(2048).decode('utf-8')

            if message:
                if message.split(": ")[-1].lower() == answer:
                    score += 1

                    conn.send(f"Hurray! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect! :(\n\n".encode('utf-8'))
                
                remove_question(index)

                index, question, answer = random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove(nickname)
        except:
            continue

def random_question_answer(conn):
    random_index = random.randint(0, len(questions) -1)
    random_question = questions[random_index]
    random_answer = answers[random_index]

    conn.send(random_question.encode('utf-8'))

    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove(connection):
    if connection in client_list:
        client_list.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    client_list.append(conn)
    nicknames.append(nickname)
    message = "{} connected!".format(nickname)
    print(message)
    client_thread = Thread(target = clientthread, args = (conn, nickname))
    client_thread.start()