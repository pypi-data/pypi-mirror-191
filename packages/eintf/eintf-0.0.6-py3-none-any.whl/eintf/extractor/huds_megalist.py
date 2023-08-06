import re

import requests

from eintf.common.helper import user_agent
from eintf.db.db import insert_to_collection, get_collection


class HudsMegalist:
    __active_url = "https://raw.githubusercontent.com/Hypnootize/TF2-HUDs-Megalist/master/Active%20Huds%20List.md"

    def update(self):
        return self.__extract(self.__active_url)

    def __extract(self, url):
        try:
            response = requests.get(url, headers=user_agent())
            rows = response.text.split('\n')
            rows = filter(lambda l: "|" in l and "---" not in l, rows)
            rows = map(lambda l: l.replace('\t', ''), rows)
            rows = map(lambda l: re.sub("\\[(.*?)]", "", l), rows)
            rows = list(rows)
            #
            headers = rows.pop(0)
            headers = re.sub('[^a-zA-Z0-9|\n]', ' ', headers.replace('&', '|').lower()).split('|')
            headers = list(map(lambda t: t.replace(' ', '-'), map(lambda h: h.strip(), headers)))
            #

            for row in rows:
                self.__hud_info(row, headers)
            return {"success": True}
        except Exception as e:
            return {"success": False}

    def __hud_info(self, row, headers) -> (str, dict):
        columns = row.split("|")
        headers = list(map(lambda x: x.replace('hud-', ''), headers))
        headers = list(map(lambda x: x.replace('direct-download', 'download'), headers))
        creator_maintainer = columns[1]
        creator = ''
        maintainer = ''
        if '`' in creator_maintainer:
            creator = re.search('`(.*)`', creator_maintainer).group(1)
        if '*' in creator_maintainer:
            maintainer = re.search('\*(.*)\*', creator_maintainer).group(1)
        columns.remove(creator_maintainer)
        columns.insert(1, creator)
        columns.insert(2, maintainer)

        columns = list(map(lambda c: c.strip("()"), columns))

        repositories = columns[4].split(") (")
        columns[4] = repositories

        hud_discussion = columns[7].split(") (")
        columns[7] = hud_discussion
        hud_json = dict(zip(headers, columns))

        if get_collection("huds").find_one({"name": hud_json['name']}) is None:
            insert_to_collection("huds", hud_json)
