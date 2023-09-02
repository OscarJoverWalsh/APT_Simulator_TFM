import os
import sys
import uuid
import time
import json
import yaml
import shutil
import socket
import random
import requests
import threading
import subprocess
import pandas as pd
import modelGenerator


#########################################################################################

terminate_flag = False

payload = {"username": "admin", "password": "admin", "rememberMe": True}
url = "http://0.0.0.0:8888"

adversaries_list = []

# Create an interrupt event
interrupt_event = threading.Event()

#########################################################################################

def define_environment():
    global realAPT, platform, model_name, model_UUID, model_description, n_abilities, goal, desired_steps, pause_time, ability_time_step

    with open('ConfigurationFile.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    with open('realAPTs.json') as g:
        aptdata = json.load(g)
    
    platform = data['Platform'].lower()
    model_name = data['Name'].lower()
    
    adversaries_list = aptdata.keys()
    if model_name in adversaries_list:
        realAPT = True
        model_UUID = aptdata[model_name]['adversary_id']
        print(model_UUID)
        n_abilities = aptdata[model_name]['atomic_ordering_size']
        if platform not in aptdata[model_name]['platform']:
            print("Selected platform is not compatible")
            terminate_execution()
    else:
        realAPT = False
        model_UUID = str(uuid.uuid4())
        n_abilities = data['N_Abilities']
        if isinstance(data['Goal'], int):
            goal = data['Goal']
        else:
            abilities_df = pd.read_csv(f"BBDD/param_req_{platform.upper()}.csv")
            goal = random.randint(0, len(abilities_df) - 1)
            
        print("Goal:", goal)
        desired_steps = data['Desired_Steps']
    model_description = data['Description']

    pause_time = 0
    ability_time_step = data['TimeStep']

    data = {'Pause': False}
    with open('Pause.yaml', 'w') as file:
        yaml.dump(data, file)
    return realAPT


def close_environment(paw):
    print("Deleting agents...\n")
    subprocess.check_output("curl -s -X 'PATCH' " +  '-H "KEY:ADMIN123" ' + "'http://0.0.0.0:8888/api/v2/agents/" + paw + "' -d '" +  '{"watchdog": 1, "sleep_min": 0, "sleep_max": 0}' + "'\n", shell=True)
    time.sleep(15)
    agentOutput = ''
    while agentOutput != b'[]':
        subprocess.check_output('curl -s -X DELETE -H "KEY:ADMIN123" "http://0.0.0.0:8888/api/v2/agents/' + paw + '" -H "accept: application/json"\n', shell=True)
        agentOutput = subprocess.check_output('curl -s -X GET -H "KEY:ADMIN123" "http://0.0.0.0:8888/api/v2/agents" -H "accept: application/json"\n', shell=True)
        if agentOutput == b'[]':
            print("Shutting down CALDERA...\n")
#            os.system("pkill -f server.py")
            break


def get_adversary_file_path(model_UUID, calderaPath):
    try:
        cmd = ["find", os.path.expanduser("~/"), "-type", "f", "-name", model_UUID + ".yml"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        path = result.stdout.strip()[2:-3] if result.returncode == 0 else None
        path_to_adversary_file = os.path.join(calderaPath, 'plugins', 'stockpile', 'data', 'adversaries', model_UUID + '.yml')
        print(path_to_adversary_file)
        return path_to_adversary_file if os.path.exists(path_to_adversary_file) else None
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def upload_operation_file(model_UUID, model_name):
    paths = working_directories()
    workingPath = paths[0]
    calderaPath = paths[1]
    get_adversary_file_path(model_UUID, calderaPath)
    if not realAPT:
        shutil.copy("generatedFiles/APTscripts/" + model_UUID + ".yml", calderaPath + "/plugins/stockpile/data/adversaries/")
        #Decrypt FILE
        os.system("python3 " + calderaPath + "/app/utility/file_decryptor.py -k ADMIN123 -s REPLACE_WITH_RANDOM_VALUE " + calderaPath +"/plugins/stockpile/data/adversaries/" + model_UUID + ".yml")
        os.system("mv " + calderaPath + "/plugins/stockpile/data/adversaries/" + model_UUID + ".yml_decrypted " + calderaPath + "/plugins/stockpile/data/adversaries/" + model_UUID + ".yml\n")


def working_directories():
    global calderaPath, workingPath
    try:
        workingPath = os.getcwd()
        calderaPath = subprocess.run(["find", os.path.expanduser("~/"), "-type", "d", "-name", "caldera4.1"], capture_output=True, text=True).stdout.strip()
        return [workingPath, calderaPath]
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None


def reboot_caldera():
    os.system("pkill -f server.py")
    os.chdir(calderaPath)
    os.system('python3 server.py --insecure 2>&1 &')
    os.chdir(workingPath)
    print("\nBooting CALDERA...\n")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client.connect(('0.0.0.0', 8888))
            break
        except Exception as e:  
            time.sleep(0.1)
    with requests.Session() as s:
        response_op = s.post(url, json=payload)
        print("\nConnected to CALDERA server.\n")


def query_agent():
    global paw, ppid

    print("Connecting Agent...\n")
    agentOutput = b''  # Initialize agentOutput
    while True:
        agentOutput = subprocess.check_output('curl -s -X GET -H "KEY:ADMIN123" "http://0.0.0.0:8888/api/v2/agents" -H "accept: application/json"', shell=True)
        if agentOutput != b'[]':
            agentData = json.loads(agentOutput.decode("utf-8"))
            paw = agentData[-1]['paw']
            ppid = agentData[-1]['ppid']
            print("PAW:", paw, "- PPID:", ppid , "\n")
            status = -1
            while status != 0:
                try:
                    agentOutput = subprocess.check_output('curl -s -X GET -H "KEY:ADMIN123" "http://0.0.0.0:8888/api/v2/agents/' + paw + '" -H "accept: application/json"', shell=True)
                    agentData = json.loads(agentOutput.decode("utf-8"))
                    status = agentData["links"][-1]["status"]
                    if status == 0:
                        print("Agent " + paw + " connected.\n")
                        break
                    elif status != 0:
                        time.sleep(0.1)
                except Exception as e:
                    print("Exception occurred:", e)
                    print("Waiting...")
                    time.sleep(0.1)
            break
    return paw


def extract_real_APT_adversary_ID_list(model_UUID):
    agentOutput = subprocess.check_output("curl -s -X 'GET' -H 'KEY:ADMIN123' 'http://localhost:8888/api/v2/adversaries/'" + model_UUID + " -H 'accept: application/json'", shell=True)
    data = json.loads(agentOutput)
    abilityIDsList = data.get('atomic_ordering', [])
    return abilityIDsList


def run_autonomous_operation(model_UUID, abilityIDsList, model_name):
    #Running autonomous operation
    global OperationIDsList
    OperationIDsList = []
    operationResponse = subprocess.check_output('curl -s -X PUT -H "KEY:ADMIN123" -H "Content-Type: application/json" http://0.0.0.0:8888/api/rest -d ' + "'{" + '"index":"operations", "name":"Operation_' + model_name.upper() + '", "state":"running", "auto_close": true, "adversary_id": "'+ model_UUID +'"}' + "'\n", shell=True)
    print("Running Operation: " + model_name.upper()+ "...\n")
    operationID = extract_operation_ID(operationResponse)
    OperationIDsList.append(operationID)
    check_operation_state(operationID)
    return operationID, model_name


def extract_operation_ID(operationResponse):
    print("Extracting operation ID...\n")
    operationResponse = operationResponse.decode("utf-8")  # Convert bytes to string
    operationList = json.loads(operationResponse)
    operationID = str(operationList[0]['id'])
    print("Operation ID: " + operationID + "\n")
    return operationID


def check_operation_state(operationID):
    # Extract the status from the operation response
    print("Checking operation state...\n")
    while True:
        operationResponse = subprocess.check_output("curl -s -X 'GET' -H 'KEY:ADMIN123' 'http://0.0.0.0:8888/api/v2/operations/" + operationID + "' -H 'accept: application/json'",  shell=True).decode('utf8')
        response_data = json.loads(operationResponse)
        state = response_data.get('state')
        if state == 'finished':
            print("State:", state, "\n")
            extract_operation_report(operationID, abilityIDsList, model_name)
            break


def extract_operation_report(operationID, abilityIDsList, model_name):
    print("Extracting autonomous operation report...\n")
#    abilityID = extract_goal_ability_ID(abilityIDsList)
#    check_goal_ability(operationID, abilityID)
    while True:
        try:
            print("Printing report content to file...\n")
            reportExtraction = subprocess.check_output("curl -s -X 'POST' -H 'KEY:ADMIN123'" + ' -H "Content-Type: application/json"' + " 'http://0.0.0.0:8888/api/v2/operations/" + operationID + "/report' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{\"enable_agent_output\": true}'",  shell=True).decode('utf-8')
            with open('generatedFiles/Reports/Report' + model_name.upper() +'.json', 'w') as file:
                file.write(reportExtraction)
            break
        except Exception as e:
            print("Exception occurred:", e)
#    subprocess.check_output("curl -s -X 'DELETE' -H 'KEY:ADMIN123' 'http://0.0.0.0:8888/api/v2/operations/" + operationID + "' -H 'accept: application/json'",  shell=True)


def extract_goal_ability_ID(abilityIDsList):
    goalAbilityID = abilityIDsList[-1]
    print("Goal ability ID: " + goalAbilityID + "\n")
    return goalAbilityID


def check_goal_ability(operationID, abilityID):
    while True:
        goalAbilityResponse = subprocess.check_output("curl -s -X 'GET' -H 'KEY:ADMIN123' 'http://0.0.0.0:8888/api/v2/operations/" + operationID + "/links/" + abilityID + "/result' -H 'accept: application/json'",  shell=True).decode('utf8')
        if goalAbilityResponse != '{"error": "Link ' + abilityID + ' was not found in Operation ' + operationID + '"}':
            print("Goal ability reached.\n")
            break


def run_timestep_operation(model_UUID, abilityIDsList, model_name):
    global pause_time, ability_time_step, elapsed_time, sleep_time

    model_name = model_name + " 2.0"
    abilities_ids_run = []
    ability_counter = 0
    operationResponse = subprocess.check_output('curl -s -X PUT -H "KEY:ADMIN123" http://0.0.0.0:8888/api/rest -d ' + "'{" + '"index":"operations", "name":"Operation_' + model_name.upper() + '", "state":"run_one_link", "auto_close": true, "adversary_id": "'+ model_UUID +'"}' + "'\n", shell=True)
    operationID = extract_operation_ID(operationResponse)
    OperationIDsList.append(operationID)
    print("Running 1º ability from Operation: " + model_name.upper() + "...\n")
    abilities_run = 1
    while abilities_run < len(abilityIDsList):
        ability_start_time = time.time()
        if check_paused():
            while check_paused():
                time.sleep(1)
            elapsed_time = capture_time_elapsed(ability_start_time)
            sleep_time = resume_program(ability_start_time)
        else:
            sleep_time = ability_time_step
        # Check for interruption before sleeping
        interrupted = interrupt_event.wait(sleep_time)
        if interrupted:
            interrupt_event.clear()  # Clear the interrupt event
            pause_time = time.time()
            elapsed_time = capture_time_elapsed(ability_start_time)
            sleep_time = resume_program(ability_start_time)
            while check_paused():
                time.sleep(0.1)
        if sleep_time != ability_time_step:
            time.sleep(sleep_time)
        if not check_paused():
            ability_ids_run, ability_counter = get_last_ability_id(abilities_ids_run, operationID, ability_counter)
            if abilityIDsList[-1] == abilities_ids_run[-1]:
                break
            if len(abilities_ids_run)>=2:
                if abilities_ids_run[-1] != abilities_ids_run[-2]:
                    abilities_run += 1
            operationResponse = subprocess.check_output("curl -s -X 'PATCH' -H " + '"KEY:ADMIN123" ' + "'http://0.0.0.0:8888/api/v2/operations/" + operationID + "' -d '" + '{"state": "run_one_link", "auto_close": true' + "}'\n", shell=True)
            print("Running " + str(abilities_run + 1) + "º ability from Operation: " + model_name.upper() + "... \n")
    extract_operation_report(operationID, abilityIDsList, model_name)
    return operationID, model_name


def check_ability_run(operationResponse):
    # Extract the status from the operation response
    operationResponse = operationResponse.decode("utf-8")  # Convert bytes to string
    operationList = json.loads(operationResponse)
    operationID = str(operationList[0]['id'])
    print("Operation ID: " + operationID + "\n")
    return operationID
    print("Checking ability run...\n")
    while True:
        operationResponse = subprocess.check_output("curl -s -X 'GET' -H 'KEY:ADMIN123' 'http://0.0.0.0:8888/api/v2/operations/" + operationID + "' -H 'accept: application/json'",  shell=True).decode('utf8')
        response_data = json.loads(operationResponse)
        state = response_data.get('state')
        if state == 'finished':
            print("State:", state, "\n")
            extract_operation_report(operationID, abilityIDsList, model_name)
            break


def get_last_ability_id(abilities_ids_run, operationID, ability_counter):
    print("Getting ability IDs...\n")
    prevChainSize = 0
    try:
        operationResponse = subprocess.check_output("curl -s -X 'GET' -H " + '"KEY:ADMIN123" ' + "'http://0.0.0.0:8888/api/v2/operations/" + operationID + "' -H 'accept: application/json'", shell=True)
        response_json = operationResponse.decode("utf-8")
        data = json.loads(response_json)
        chain = data['chain']
        if prevChainSize != len(chain):
            last_ability = chain[ability_counter]['ability']
            ability_id = last_ability['ability_id']
            abilities_ids_run.append(ability_id)
        ability_counter += 1
        prevChainSize = len(chain)
        return abilities_ids_run, ability_counter
    except (KeyError, IndexError):
        return None


def check_paused():
    with open('Pause.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        if data is not None and 'Pause' in data:
            content = data['Pause']
            return content == True
    return False


def capture_time_elapsed(ability_start_time):
    global ability_time_step, pause_time, elapsed_time

    elapsed_time = pause_time - ability_start_time
    print("TIME START:", ability_start_time)
    print("TIME PAUSE:", pause_time)
    print("TIME ELAPSED:", elapsed_time)
    return max(0, elapsed_time)


def resume_program(ability_start_time):
    global ability_time_step, pause_time, elapsed_time

    pause_time = 0
    time_remaining = ability_time_step - elapsed_time
    print("TIME REMAINING:", time_remaining)
    return max(0, time_remaining)


def watchdog():
    global pause_time, interrupt_event

    while not terminate_flag:
        if check_paused():
            pause_time = time.time()
            interrupt_event.set()
            print("Execution paused.")
            while check_paused():
                time.sleep(1)
            print("Execution resumed.")
            interrupt_event.clear()
        time.sleep(0.1)


def terminate_execution():
    global realAPT, terminate_flag
    terminate_flag = True

    watchdog_thread.join()
    sys.exit()


if __name__ == "__main__":
    # Start the watchdog thread
    watchdog_thread = threading.Thread(target=watchdog)
    watchdog_thread.start()
    
    try:
        realAPT = define_environment()
        if not realAPT:
            abilityIDsList = modelGenerator.main(platform, model_name, model_UUID, model_description, n_abilities, goal, desired_steps)
        upload_operation_file(model_UUID, model_name)
        reboot_caldera()
        paw = query_agent()
        if realAPT:
            abilityIDsList = extract_real_APT_adversary_ID_list(model_UUID)
        operationID, model_name = run_autonomous_operation(model_UUID, abilityIDsList, model_name)
        operationID, model_name = run_timestep_operation(model_UUID, abilityIDsList, model_name)
        close_environment(paw)

    except Exception as e:
        print("An error occurred:", e)
        terminate_execution()

    # Terminate execution and return to the command line
    terminate_execution()
