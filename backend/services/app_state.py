from fastapi import Request
from sqlmodel import Session
import aiohttp

"""Made these their own modules mainly because I needed to pass the db_session into pytest."""

def get_db_session(request: Request) -> Session:
    return request.state.db_session


def get_session(request: Request) -> aiohttp.ClientSession:
    return request.state.http_client
