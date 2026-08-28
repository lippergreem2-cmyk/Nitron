# ==========================================================
# NITRON ANIME QUOTES SYSTEM
# ==========================================================

import random


anime_quotes = {

    "dragon ball": [

        "A true fighter keeps growing beyond yesterday's limits.",

        "Power means nothing without the courage to protect others.",

        "Every challenge is a chance to become stronger."

    ],


    "jujutsu kaisen": [

        "A warrior's heart is tested when the battle becomes impossible.",

        "Fear may appear, but determination decides the outcome.",

        "The strongest path is built through sacrifice and effort."

    ],


    "bleach": [

        "A true protector stands tall when others need them.",

        "Your resolve is the blade that cuts through doubt.",

        "Strength comes from understanding what you fight for."

    ],


    "black clover": [

        "Hard work can challenge even the greatest talent.",

        "Never abandon your dream, even when others doubt you.",

        "A small beginning can create a legendary future."

    ],


    "one punch man": [

        "A hero is defined by the people they choose to help.",

        "True strength comes from discipline and consistency.",

        "A real hero keeps going even when nobody is watching."

    ],


    "solo leveling": [

        "Every battle is a step toward a stronger version of yourself.",

        "The darkest moments can create the strongest warriors.",

        "Growth begins when you decide not to remain the same."

    ],


    "seven deadly sins": [

        "A true warrior fights for the bonds they protect.",

        "Even broken hearts can find the strength to stand again.",

        "Loyalty and courage create legendary heroes."

    ]

}



def get_quote(anime=None):

    if anime:

        anime = anime.lower()


        for name in anime_quotes:

            if anime in name:

                return random.choice(
                    anime_quotes[name]
                )


    all_quotes = []


    for quotes in anime_quotes.values():

        all_quotes.extend(quotes)


    return random.choice(all_quotes)



def list_anime():

    return list(
        anime_quotes.keys()
    )
