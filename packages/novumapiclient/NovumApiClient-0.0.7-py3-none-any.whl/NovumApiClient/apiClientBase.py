import json
import requests
import urllib
import math
from hashlib import md5
import jwt
import time
import base64
from threading import Timer

TOKEN_REFRESH_INTERVAL_SCALE = 0.9
UNMISTAKABLE_CHARS = "23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz"
PRODUCTION_API_HOST = "https://novum-batteries.com"


def with_filter_or_option(
    url: str,
    filter: dict,
    option: dict,
    fields: dict,
):
    query = {}
    if len(filter) != 0:
        query["filter"] = json.dumps(filter)
    if len(option) != 0:
        query["option"] = json.dumps(option)
    if len(fields) != 0:
        query["fields"] = json.dumps(fields)
    return url, query.json()  # withQuery


def getSHA256(toHash: str) -> str:
    return md5("sha256").update(toHash).hexdigest("hex")


def gen_mongo_id(charsCount=17) -> str:
    def choice(arrayOrString: str):
        index = math.floor(math.random() * len(arrayOrString))
        if type(arrayOrString) == "string":
            return arrayOrString.substr(index, 1)
        return arrayOrString[index]

    result = 0
    for i in range(0, charsCount):
        result += choice(UNMISTAKABLE_CHARS)
    return result


def user_name(user: dict) -> str:
    return user["profile"]["name"]


def full_name(user: dict) -> str:
    if len(user != None):
        return str(user["profile"]["first_name"]) + str(user["profile"]["family_name"])
    else:
        return "User not found!"


def parse_jwt(token: str) -> any:
    base64Input = token.split(".")[1]
    base64 = base64Input.replace("/-/g", "+").replace("/_/g", "/")
    return jwt.decode(base64, verify=False)


class APIError:
    def __init__(self, res: any):
        self._text = ""
        self._json = None
        self._res = res
        self._code = res.status
        self.details = None

    def resolve(self) -> str:
        try:
            response = str(self._res)
            self._text = response
            try:
                self._json = json.loads(self._text)
            except:
                self._json = {"body": self._text}
                self.details = {"json": self._json, "code": self._code, "headers": self._res.headers}
                return self._json["error"]
        except:
            return "Unknown API Error"


class BaseAPIClient:
    def __init__(
        self,
        user="",
        host=PRODUCTION_API_HOST,
        _refreshTokenWarning=True,
        _refreshIntervalScale=TOKEN_REFRESH_INTERVAL_SCALE,
        props=None,
    ):
        self.user = user
        self._host = host
        self._props = props
        self._refreshTokenWarning = _refreshTokenWarning
        self._refreshIntervalScale = _refreshIntervalScale

    @staticmethod
    def fromWindowLocation(window):
        return BaseAPIClient(window.location.origin)

    def _set_user(self, user):
        if user != "" and user["jwt"] != None:
            user["expires_at"] = self._get_expire_time_from_token_in_unix_time_millis(user["jwt"]).isoformat()
            self.user = user
            self._install_token_refresh_procedure(user)

    def _clear_user(self):
        self.user = None
        self._remove_relogin_timer_handle()

    def _remove_relogin_timer_handle(self):
        if self._reLoginTimerHandle != None:
            # clearTimeout(self._reLoginTimerHandle)
            self._reLoginTimerHandle = None

    def _get_expire_time_from_token_in_unix_time_millis(self, token: str) -> float:
        if token != None:
            innerToken = json.load(token)
            if innerToken != None and innerToken["exp"] != None and type(innerToken["exp"]) == str:
                return 1000 * innerToken["exp"]
        return 3600 * 1000

    def _install_token_refresh_procedure(self, user):
        self._remove_relogin_timer_handle()
        expire_time_In_millis = self._get_expire_time_from_token_in_unix_time_millis(self.user["jwt"])
        now = time.time()

        if expire_time_In_millis != None and expire_time_In_millis > 1000 + now:
            if user["refresh_token"] != None:
                refreshIntervalInMillis = math.round(self._refreshIntervalScale * (expire_time_In_millis - now))
                self._reLoginTimerHandle = Timer(self._refreshAccessToken, refreshIntervalInMillis)
            else:
                if self._refreshTokenWarning:
                    print("APIClient: There is no refreshToken! Autorefresh of access tokens is not possible.")
                else:
                    print("APIClient: Could not get expire_time_In_millis or token has already expired.")

    def _refresh_access_token(self):
        if self.user != None and self.user.refresh_token != None:
            print("APIClient._refreshAccessToken - Refreshing the accesToken for userId" + self.user["id"])
            refresh_token = self.user
            new_access_object = self._post("/api/batman/v1/refresh", {refresh_token})
            if new_access_object["jwt"] != None:
                self._set_user(self.user, new_access_object)
            else:
                print("APIClient._refreshAccessToken - Error no user or refesh token found!")

    def _fetch_by_URL(self, url: str, options: any):
        response = self._get_json(url, option=options)
        if response["ok"] == False:
            error = APIError(f"Failed to load resource {url} -> Status:" + response["status"], response)
            error.resolve()
            return error
        return response

    def _post_by_URL(self, url: str, options: any):
        response = self._post_json(url, option=options)
        if response["ok"] == False:
            error = APIError(f"Failed to load resource {url} -> Status:" + response["status"], response)
            error.resolve()
            return error
        return response

    def _fetch_by_path(self, path: str, options: any):
        return self._fetch_by_URL(self._host + path, options)

    def _post_by_path(self, path: str, options: any):
        return self._post_by_URL(self._host + path, options)

    def _encode_auth_header(self, username: str, password: str):
        return {"Authorization": "Basic " + str(base64.b64encode(username, password).decode("utf-8"))}

    def _headers(self, headers):
        if self.user != None and self.user["jwt"] != None:
            headers["Authorization"] = "Bearer " + str(self.user["jwt"])
        return headers

    def _get_json(self, url: str, filter=None, option=None, timeout: float = 4.0):
        full_url = self.host + url
        headers = dict({"Content-Type": "application/json", "Authorization": "Bearer " + self.user["jwt"]})
        param = {"filter": json.dumps(filter), "option": json.dumps(option)}
        params = urllib.parse.urlencode(param)

        response = requests.get(
            url=full_url,
            headers=headers,
            params=params,
            timeout=timeout,
        )

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Error: Unable to get the data.", response.status_code)

    def _post_file(self, path: str, file, headers):
        files = {"upload_file": open(file)}
        response = self._post_by_path(path, headers=headers, files=files)
        return response.json()

    def _post_json(self, url: str, data=None, filter=None, option=None, timeout: float = 4.0):
        full_url = self.host + url
        headers = dict({"Content-Type": "application/json", "Authorization": "Bearer " + self.user["jwt"]})
        param = {"filter": json.dumps(filter), "option": json.dumps(option)}
        params = urllib.parse.urlencode(param)
        data = json.dumps(data)

        response = requests.post(
            url=full_url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
        )

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Error: The data could not be posted.", response.status_code)

    def _put_json(self, url: str, data=None, filter=None, option=None, timeout: float = 4.0):
        full_url = self.host + url
        headers = dict({"Content-Type": "application/json", "Authorization": "Bearer " + self.user["jwt"]})
        param = {"filter": json.dumps(filter), "option": json.dumps(option)}
        params = urllib.parse.urlencode(param)
        data = json.dumps(data)

        response = requests.put(
            url=full_url,
            headers=headers,
            params=params,
            data=data,
            timeout=timeout,
        )

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Error: The data was nou updated.", response.status_code)

    def _delete_json(self, url: str, filter=None, option=None, timeout: float = 4.0):
        full_url = self.host + url
        headers = dict({"Content-Type": "application/json", "Authorization": "Bearer " + self.user["jwt"]})
        param = {"filter": json.dumps(filter), "option": json.dumps(option)}
        params = urllib.parse.urlencode(param)

        response = requests.delete(
            url=full_url,
            headers=headers,
            params=params,
            timeout=timeout,
        )
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Error: The data was not removed.", response.status_code)

    def _get_text(self, path: str, headers=None):
        headers = headers.update({"Content-Type": "application/text"})
        response = self._fetch_by_path(path, headers=headers)
        return response.text()

    def _get_array_buffer(self, path: str, headers):
        headers = headers.update({"Content-Type": "application/text"})
        response = self._fetch_by_path(path, headers=headers)
        return [int(i) for i in response.content]

    def host(self) -> str:
        return self._host

    def authenticated(self) -> bool:
        return self._authenticated

    def set_new_endpoint(self, newEndPoint: str):
        self._host = newEndPoint

    def _is_APIError(self, objectOrError) -> bool:
        return objectOrError != None and objectOrError.details != None and objectOrError.details.code != None
