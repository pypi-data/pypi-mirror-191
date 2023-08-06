import traceback

import requests

from eintf.db.db import insert_to_collection

release_dict = {}
util_repos = [
    ("PazerOP", "tf2_bot_detector"),
    ("mastercomfig", "mastercomfig"),
    ("JarateKing", "CleanTF2plus"),
    ("CriticalFlaw", "TF2HUD.Editor"),
    ("Narcha", "DemoMan"),
]


class Tool:
    def latest_release(self, repo):
        name = repo[1]
        owner = repo[0]
        release = requests.get(f"https://api.github.com/repos/{owner}/{name}/releases/latest").json()
        if "message" in release and release["message"] == "Not Found":
            release = requests.get(f"https://api.github.com/repos/{owner}/{name}/commits/master").json()
            return {
                "name": name,
                "release": release["commit"]["message"],
                "published_at": release["commit"]["committer"]["date"],
                "assets": list(f"https://github.com/{owner}/{name}/archive/refs/heads/master.zip"),
                "body": "",
                "owner": release["author"]["login"],
                "source": f"https://github.com/{owner}/{name}",
            }
        return {
            "name": name,
            "release": release["name"],
            "published_at": release["published_at"],
            "assets": list(map(self.minify_asset, release["assets"])),
            "body": release["body"],
            "owner": owner,
            "source": f"https://github.com/{owner}/{name}",
        }

    def minify_asset(self, asset: dict):
        return {
            "url": asset["url"],
            "name": asset["name"],
            "browser_download_url": asset["browser_download_url"],
        }

    def update(self):
        try:
            for r in util_repos:
                insert_to_collection("tools", self.latest_release(r))
            return {"success": True}
        except Exception as e:
            traceback.print_exception(e)
            return {"success": False}
