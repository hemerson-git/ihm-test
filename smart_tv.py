from os import access
import re
from time import sleep
from zoneinfo import available_timezones
import face_recognition
import secrets
import random
import faker
import json
import simpy

CONFIG_FILE = "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/users.json"
SERVICES_DB = "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/services.json"

USERS_PICTURES = [
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/angela1.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/angela2.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/angela3.jpeg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/darlene1.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/darlene2.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/darlene3.jpg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/elliot1.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/elliot2.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/elliot3.jpg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/price1.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/price2.jpg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/price3.jpg",

    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/tyrell1.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/tyrell2.jpeg",
    "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/faces/tyrell3.jpeg"
]

USER_RECOGNITION_INTERVAL = 500
REGISTER_VERIFICATION_INTERVAL = 200


def prepare():
    global configs
    global stream_services

    stream_services = None
    with open(SERVICES_DB, "r") as services_db:
        stream_services = json.load(services_db)
        if stream_services:
            print("\033[36m[INFO] Stream services loaded from DB \033[37m")

    configs = None
    with open(CONFIG_FILE, 'r') as config_file:
        configs = json.load(config_file)
        if configs:
            print("\033[36m[INFO] Configs loaded, version {}\033[37m".format(
                configs["version"]))

    global recognized_users
    recognized_users = {}

    global faker_generator
    faker_generator = faker.Faker()


def simulate_detect_user():
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
    sleep(1)
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

        if (picture_matchs / len(db_pictures) >= 0.7):
            is_recognized = True

            user['name'] = faker_generator.name()
            user['age'] = random.randint(1, 100)
            user['services'] = []

            for service in stream_services['services']:
                is_registered = random.randint(0, 1)

                if is_registered:
                    user['services'].append(service)

        return is_recognized, user


def get_age_recommendation():
    choices = [1, 10, 12, 14, 16, 18]
    age = random.choice(choices)

    return age


def identify_user(env):
    global configs
    global faker_generator
    global recognized_users

    while True:
        detected_person = simulate_detect_user()
        is_recognized, user = recognize_user(detected_person)

        if is_recognized:
            print("\033[32mUser: {} recognized \033[37m".format(user['name']))

            access_id = secrets.token_hex(nbytes=16).upper()
            recognized_users[access_id] = user
        else:
            print("\033[31mUser not recognized \033[37m")

        yield env.timeout(USER_RECOGNITION_INTERVAL)


def print_available_services(username, services):
    print("\033[32m{} has the following services: \033[37m".format(username))
    for service in services:
        print("\t- {}".format(service['name']))


def verify_user_access(user):
    global stream_services

    available_services = []

    for service in user['services']:
        for stream_service in stream_services['services']:
            if (service['name'] == stream_service['name']):
                available_services.append(stream_service)

    print_available_services(user['name'], available_services)


def verify_registration(env):
    global recognized_users
    global stream_services

    while True:
        if len(recognized_users):
            for access_id, user in list(recognized_users.items()):
                verify_user_access(user)
                recognized_users.pop(access_id)

        yield env.timeout(REGISTER_VERIFICATION_INTERVAL)


if __name__ == '__main__':
    prepare()

    env = simpy.Environment()
    env.process(identify_user(env))
    env.process(verify_registration(env))

    env.run(until=10000)
