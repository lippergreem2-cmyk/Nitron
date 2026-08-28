# ==========================================================
# NITRON SPEECH SYSTEM v5.0
# SMART INTERRUPT + CONVERSATION VOICE
# ==========================================================

import os
import subprocess
import threading
import time



# ==========================================================
# SPEECH STATE
# ==========================================================

speech_state = {

    "speaking": False,

    "listening": True,

    "interrupted": False,

    "ignore_input": False,

    "process": None

}



# ==========================================================
# STOP SPEAKING
# ==========================================================

def stop_speaking():

    speech_state["interrupted"] = True

    speech_state["ignore_input"] = True

    speech_state["speaking"] = False


    process = speech_state.get(
        "process"
    )


    if process:

        try:

            process.terminate()


        except Exception:

            pass



    try:

        os.system(

            "pkill -f termux-tts-speak"

        )


    except Exception:

        pass



# ==========================================================
# TEXT TO SPEECH
# ==========================================================

def speak(text):

    if not text:

        return


    speech_state["speaking"] = True

    speech_state["interrupted"] = False


    try:

        process = subprocess.Popen(

            [

                "termux-tts-speak",

                str(text)

            ]

        )


        speech_state["process"] = process



        while process.poll() is None:


            if speech_state["interrupted"]:

                break



            time.sleep(0.1)



    except Exception as error:


        print(

            "Speech error:",

            error

        )



    finally:


        speech_state["speaking"] = False

        speech_state["process"] = None# ==========================================================
# SPEECH TO TEXT
# ==========================================================

def listen():

    try:

        result = subprocess.check_output(

            [

                "termux-speech-to-text"

            ],

            text=True

        )


        if result:

            return result.strip()



    except Exception as error:


        print(

            "Listen error:",

            error

        )


    return ""



# ==========================================================
# INTERRUPT MONITOR
# ==========================================================

def interrupt_monitor():

    while True:


        try:


            if speech_state["speaking"]:


                voice = listen()



                if voice:


                    command = voice.lower()



                    if any(

                        word in command

                        for word in [

                            "stop",

                            "quiet",

                            "keep quiet",

                            "shut up",

                            "be quiet",

                            "nitron stop"

                        ]

                    ):


                        stop_speaking()



        except Exception as error:


            print(

                "Interrupt error:",

                error

            )



        time.sleep(0.2)



# ==========================================================
# USER TALKING
# ==========================================================

def user_started_talking():


    if speech_state["speaking"]:


        stop_speaking()



    speech_state["listening"] = True



# ==========================================================
# LISTENING CONTROL
# ==========================================================

def start_listening():


    speech_state["listening"] = True



def stop_listening():


    speech_state["listening"] = False



def is_speaking():


    return speech_state["speaking"]



def is_listening():


    return speech_state["listening"]



# ==========================================================
# START INTERRUPT THREAD
# ==========================================================

threading.Thread(

    target=interrupt_monitor,

    daemon=True

).start()



print(

    "[OK] Nitron Speech System v5.0 Online"

)
