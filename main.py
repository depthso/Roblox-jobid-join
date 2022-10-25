import time, requests, pathlib, urllib.parse, os

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
        f'https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame{"Job"}&placeId={PlaceID}{"&gameId=" + JobID}&isPlayTogetherGame=false&isTeleport=true+robloxLocale:en_us+gameLocale:en_us+channel:')
    os.startfile(f"roblox-player:1+launchmode:play+gameinfo:{ticket}+launchtime:{timestamp}+placelauncherurl:{url}")

    time.sleep(5)

config = {
    "Cookies": [
        "Cookie Here"
    ]
}

Cookies = config["Cookies"]

""" 
This is for if you have multiple accounts and sessions.

I recommend using this browser extension:

    https://chrome.google.com/webstore/detail/roblox-multi-accounts/cmeicimcdhgohgjmpmcdpakjjdohhocg
    

You could use the cookies for 

for Cookie in config["Cookies"]:
    startroblox(PlaceID, JobID, Cookie)
    time.sleep(4)

"""

startroblox(PlaceID=4984400432, JobID="8ffdf369-fa67-4226-9f64-8748b335836b", Cookie=Cookies[0])
