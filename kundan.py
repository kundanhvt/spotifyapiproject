import json
import requests

response = requests.get("https://api.spotify.com/v1/browse/new-releases", headers={'Authorization':'Bearer BQC1DPIcN56QEP0GP-UhcPacfP5bpjSyX_ss9nMp_3VKp2cG2FvfVb0Z1B7LkUyjCX5pZCFxpP-ffkpn32hASrvRLGtQ4YsIqJeK7FkawSMeybg-eJ5Ki_g-N1eSdOhdFinK_AHZwQlF4y2vQAi0c4S6zZLGz_o08Q3C5CLS1VUa0kz5Xcw_LPsotb-PuNqTLXblUGn0anIfugc8j7sx-P60PvgNcEEw1eHtQ3qqRGHXp_yO5DnLLqYAHgc2lPNzRI6kIRzuvCAuyg' })

response = response.json()
single_data = []
album_data = []
for item in response["albums"]["items"]:
    if item["album_type"] == "single":
        single_data.append(item)
    elif item["album_type"] == "album":
        single_data.append(item)

print(json.dumps(str(single_data),indent=4))