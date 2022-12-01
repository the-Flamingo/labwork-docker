import requests

session = requests.Session()
def handle_timing_sidechannel(assignment, endpoint):
    user = assignment["user"]
    print("User:", user)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    password = ""
    while True:
        slowest = {}
        # Used to try the timing for all chars multiple times to counter variation
        # It made it in 6 iterations with my testcases. Increased it to 10 to be sure on your end
        for illfuckingdoitagain in range(0,10):
            #print(illfuckingdoitagain)
            timed = {}
            for char in alphabet:
                test_pw = password + char
                request = session.post(endpoint + "/oracle/timing_sidechannel", headers={"Content-Type": "application/json", "Accept": "application/json"}, json = {"user": user, "password": test_pw}).json()
                if request["status"] != "auth_failure":
                    print("Found Password!  ", test_pw)
                    session.close()
                    return {"password": test_pw}
                test_pw = test_pw + "!"
                request = session.post(endpoint + "/oracle/timing_sidechannel", headers={"Content-Type": "application/json", "Accept": "application/json"}, json = {"user": user, "password": test_pw}).json()
                timed[char] = request["time"]
            timed = {key: value for key, value in sorted(timed.items(), key=lambda x: x[1], reverse=True)}
            #print("Timed:", timed)
            if list(timed.keys())[0] not in slowest:
                slowest[list(timed.keys())[0]] = 1
            else:
                slowest[list(timed.keys())[0]] += 1
        #print(slowest)
        slowest= {key: value for key, value in sorted(slowest.items(), key=lambda x: x[1], reverse=True)}
        #print("Slowest:", list(slowest.keys())[0])
        password += list(slowest.keys())[0]
        #print("Current Password:", password)