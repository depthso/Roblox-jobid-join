import time, requests, pathlib, urllib.parse, os, threading

currentpath = str(pathlib.Path(__file__).parent.absolute())


def startroblox(PlaceID: int, JobID: str, Cookie: str):
    print("checking latest version of ROBLOX... ", end="")

    version = requests.get("http://setup.roblox.com/version.txt").content.decode("ascii")
    path = os.getenv("LOCALAPPDATA") + "\\Roblox\\Versions\\" + version

    print("done! (" + version + ")")

    if not os.path.exists(path):
        print("updating ROBLOX, please wait... ", end="")

        bootstrapper = requests.get("http://setup.roblox.com/RobloxPlayerLauncher.exe")
        open(currentpath + "\\RobloxPlayerLauncher.exe", "wb").write(bootstrapper.content)
        os.system('"' + currentpath + '\\RobloxPlayerLauncher.exe" -install')

        print("done!")

    print("fetching CSRF token... ", end="")

    req = requests.post(
        "https://auth.roblox.com/v1/authentication-ticket",
        headers={"Cookie": ".ROBLOSECURITY=" + Cookie}
    )

    csrf = req.headers['x-csrf-token']
    print("done!")

    print("fetching authentication ticket... ", end="")

    req = requests.post(
        "https://auth.roblox.com/v1/authentication-ticket",
        headers=
        {
            "Cookie": ".ROBLOSECURITY=" + Cookie,
            "Origin": "https://www.roblox.com",
            "Referer": "https://www.roblox.com/",
            "X-CSRF-TOKEN": csrf
        }
    )

    ticket = req.headers['rbx-authentication-ticket']
    print("done!")

    print("\nstarting ROBLOX... ")

    timestamp = '{0:.0f}'.format(round(time.time() * 1000))
    url = urllib.parse.quote(
        #f'https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGameJob%26browserTrackerId%3D147062882894%26placeId%3D{PlaceID}%26gameId%{JobID}%26isPlayTogetherGame%3Dfalse+browsertrackerid:147062882894+robloxLocale:en_us+gameLocale:en_us+channel:+LaunchExp:InApp'
        f'https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame{"Job"}&browserTrackerId=147062882894&placeId={PlaceID}{"&gameId=" + JobID}&isPlayTogetherGame=false+browsertrackerid:147062882894+robloxLocale:en_us+gameLocale:en_us+channel:'
    )

    os.startfile(f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{timestamp}+placelauncherurl:{url}")

    time.sleep(5)

config = {
    "Cookies": [
        "Cookie"
    ]
}

Cookies = config["Cookies"]

""" 
This is for if you have multiple accounts and sessions.

I recommend using this browser extension:

    https://chrome.google.com/webstore/detail/roblox-multi-accounts/cmeicimcdhgohgjmpmcdpakjjdohhocg
    

You could use the cookies for 

for Cookie in config["Cookies"]:
    print(Cookie)
    threading.Thread(target=startroblox, args=(PlaceID, JobID, Cookie)).start()
    time.sleep(15)

"""
PlaceID = 5373028495
JobID = "9580db4a-e38b-4067-b6d4-10ffa63e229c"

startroblox(PlaceID=int(PlaceID), JobID=JobID, Cookie=Cookies[0])
