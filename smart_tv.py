import face_recognition
import secrets
import random
import faker
import json
import simpy

CONFIG_FILE = "/mnt/c/Users/hemer/OneDrive/Área de Trabalho/ihm/005_smart_tv/users.json"

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


def prepare():
    global configs

    configs = None
    with open(CONFIG_FILE, 'r') as config_file:
        configs = json.load(config_file)
        if configs:
            print("Configs loaded, version {}".format(configs["version"]))

    global recognized_users
    recognized_users = {}


def identify_user(env):
    pass


def verify_registration(env):
    pass


if __name__ == '__main__':
    env = simpy.Environment()
    prepare()

    env.process(identify_user(env))
