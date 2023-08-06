import time
from pprint import pprint
import json
import hashlib
import click
import requests


class Client:
    def __init__(
        self,
        appId="sentry",
        appSec="NpOSWh2OybjHYK2Q",
        baseUrl="https://ea-common.bytedance.net/infra-sd",
    ):
        self.appId = appId
        self.appSec = appSec
        self.baseUrl = baseUrl

    def request(self, path: str, params: dict) -> dict:
        ts = str(int(time.time()))
        js = json.dumps(params)
        txt = "%s%s%s" % (self.appSec, ts, js)
        sig = hashlib.md5(txt.encode()).hexdigest()

        params["bizParams"] = js
        url = self.baseUrl + path
        headers = {
            "Content-Type": "application/json",
            "timestamp": ts,
            "app-id": self.appId,
            "request-type": "HTTP",
            "sign": sig,
        }

        data = requests.post(url, json=params, headers=headers).json()
        if "000000" != data["code"]:
            raise RuntimeError(("invalid response", data))
        return data["data"]["results"]

    def getByIds(self, uids):
        return self.request(
            "/api/employee/getByEmployeeNumbers", {"employeeNumbers": uids}
        )

    def getByEmails(self, emails):
        return self.request("/api/employee/searchByEmails", {"emails": emails})


@click.command(help="query employee info by uids / email prefixes")
@click.argument("args", nargs=-1)
def cli(args):
    if not args:
        return

    uids = emails = None
    try:
        uids = list(map(int, args))
    except ValueError:
        emails = [i + "@bytedance.com" for i in args]

    c = Client()
    if uids:
        res = c.getByIds(uids)
    else:
        res = c.getByEmails(emails)
    pprint(res)


if __name__ == "__main__":
    cli()
