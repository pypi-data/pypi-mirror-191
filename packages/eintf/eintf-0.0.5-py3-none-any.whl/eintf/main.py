import argparse
import sys

from fastapi import FastAPI
from fastapi.params import Query
from starlette.responses import JSONResponse

import uvicorn

from .db.db import get_collection
from .extractor.git import Tool
from .extractor.huds_megalist import HudsMegalist
from .extractor.map.map_crawler import MapSpider
from .extractor.news.news import News

app = FastAPI()


@app.exception_handler(500)
async def exception_handler(request, exc):
    return JSONResponse(content={"success": False, "error": str(exc)}, status_code=500)


@app.get("/")
def read_root():
    return {}


@app.get("/huds/megalist")
def active_huds():
    return list(get_collection("huds").find({}, {"_id": 0}))


@app.get("/huds/megalist/{hud}")
def active_hud(hud):
    return list(get_collection("huds").find_one({"name": hud}, {"_id": 0}))


@app.get("/tools")
def tools():
    return list(get_collection("tools").find({}, {"_id": 0}))


@app.get("/tools/{tool_}")
def tool(tool_):
    return list(get_collection("tools").find({"name": tool_}, {"_id": 0}))


@app.get("/news")
def news(source: str = Query(None, alias="source"), page: int = Query(1, alias="page")):
    if source is None:
        source = {"$ne": None}
    else:
        source = {"$in": source.split(",")}
    return list(get_collection("news").find(
        {"source": source}, {"_id": 0}
    ).sort("date", -1).limit(10).skip(10 * (page - 1)))


@app.get("/maps")
def maps(
        author=Query(None, alias="author"),
        category=Query(None, alias="category"),
        page: int = Query(1, alias="page")
):
    if author is None:
        author = {"$ne": None}
    if category is None:
        category = {"$ne": None}
    return list(get_collection("maps").find({
        "author": author,
        "category": category,
    }, {"_id": 0}).limit(10).skip(10 * (page - 1)))


def update_data(it):
    if it == "huds":
        return HudsMegalist().update()

    elif it == "tools":
        return Tool().update()

    elif it == "news":
        return News().update()

    elif it == "maps":
        return MapSpider().update()


def run():
    parser_ = argparse.ArgumentParser(description="TF2 api")
    parser_.add_argument(
        "-s",
        metavar="start",
        nargs="?",
        const="0.0.0.0:8000",
        help="start server",
    )
    parser_.add_argument(
        "-u",
        metavar="update",
        type=str,
        default=None,
        help="updates data in db",
        required=False,
    )
    args = parser_.parse_args()
    if "-s" in sys.argv:
        address = args.s.split(":")
        uvicorn.run("eintf.main:app", host=address[0], port=int(address[1]), reload=True)
    elif "-u" in sys.argv and args.u:
        update_data(args.u)
