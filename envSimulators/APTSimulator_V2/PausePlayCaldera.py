
def pause():
    try:
        with open("Pause.yaml", "r") as file:
            config = yaml.safe_load(file)

        if config["Pause"] == False:
            config["Pause"] = True
            with open("Pause.yaml", "w") as file:
                yaml.dump(config, file)
            print("Pause value set to TRUE.")
        else:
            print("Pause value already set to TRUE.")

    except Exception as e:
        print("An error occurred:", e)


def play():
    try:
        with open("Pause.yaml", "r") as file:
            config = yaml.safe_load(file)

        if config["Pause"] == True:
            config["Pause"] = False
            with open("Pause.yaml", "w") as file:
                yaml.dump(config, file)
            print("Pause value set to FALSE.")
        else:
            print("Pause value already set to FALSE.")

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    import yaml
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python filename.py <function>")
        sys.exit(1)

    function_name = sys.argv[1]

    if function_name == "pause":
        pause()
    elif function_name == "play":
        play()
    else:
        print("Invalid function name. Available functions: pause, play")
