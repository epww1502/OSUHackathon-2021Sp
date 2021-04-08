import requests
 
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
 
myToken = "xoxb-1940285825253-1967173782768-aWN7zF405rIpqnBG9PA4Syvr"
 
post_message(myToken,"#stock","testing code")