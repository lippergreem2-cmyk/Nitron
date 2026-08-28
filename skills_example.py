from skills import skills

def hello():
    return "Hello Boss, Nitron is online."

def system():
    return "All systems are operational."

skills.register("hello", hello)
skills.register("system", system)
