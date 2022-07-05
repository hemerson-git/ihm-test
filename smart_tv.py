import re
from time import sleep
import face_recognition
import secrets
import random
import faker
import json
import simpy

CONFIG_FILE = "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/users.json"
SERVICES_DB = "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/services.json"

USERS_PICTURES = [
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/angela1.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/angela2.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/angela3.jpeg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/darlene1.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/darlene2.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/darlene3.jpg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/elliot1.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/elliot2.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/elliot3.jpg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/price1.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/price2.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/price3.jpg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/tyrell1.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/tyrell2.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/images/tyrell3.jpeg"
]

USER_RECOGNITION_INTERVAL = 500


def prepare():
    global configs
    global stream_services

    stream_services = None
    with open(SERVICES_DB, "r") as services_db:
        stream_services = json.load(services_db)
        if stream_services:
            print("\033[32m [INFO] Stream services loaded from DB \033[37m")

    configs = None
    with open(CONFIG_FILE, 'r') as config_file:
        configs = json.load(config_file)
        if configs:
            print("Configs loaded, version {}".format(configs["version"]))

    global recognized_users
    recognized_users = {}

    global faker_generator
    faker_generator = faker.Faker()


def simulate_detect_user():
    global stream_services

    user = {
        "picture": random.choice(USERS_PICTURES),
        "services": {}
    }

    return user


def recognize_user(user):
    global configs
    global faker_generator

    print("Starting to recognize visitor...")

    # to cause a suspense in the simulation
    sleep(3)
    user_picture = face_recognition.load_image_file(user["picture"])
    encoded_user_picture = face_recognition.face_encodings(user_picture)[
        0]

    is_recognized = False
    for user in configs['registered_users']:
        db_pictures = user['pictures']
        picture_matchs = 0

        for db_pic in db_pictures:
            db_picture = face_recognition.load_image_file(db_pic)
            encoded_db_picture = face_recognition.face_encodings(db_picture)[0]

            match = face_recognition.compare_faces(
                [encoded_db_picture], encoded_user_picture)[0]

            if match:
                picture_matchs += 1

        if (picture_matchs / len(db_pictures) > 0.7):
            is_recognized = True

            user['name'] = faker_generator.name()
            user['age'] = random.randint(1, 100)
            user['services'] = random.choices(stream_services)

        return is_recognized, user


def generate_age_recommendation():
    choices = ['free', '10', '12', '14', '16', '18+']
    print(choices)


def identify_user(env):
    global configs
    global faker_generator

    while True:
        user = simulate_detect_user()
        print(user)


def verify_registration(env):
    pass


if __name__ == '__main__':
    prepare()

    env = simpy.Environment()
    env.process(identify_user(env))
