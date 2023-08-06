from cloudscraper import create_scraper
import requests.adapters
import re
import time
import json
import platform
from fnmatch import fnmatch
from urllib.parse import quote
from .utils import RapidUpload


plat_table = (
    ('windows', ('windows', 'cygwin*')),
    ('darwin', ('darwin',)),
    ('ios', ('ios',)),
    ('linux', ('linux*',)),
    ('freebsd', ('freebsd*', 'openbsd*', 'isilon onefs')),
    ('poky', ('poky',)),
)
def _match_features(patterns, s):
    for pat in patterns:
        if fnmatch(s, pat):
            return True
plat = platform.system().lower()
for alias, platlist in plat_table:
    if _match_features(platlist, plat):
        plat = alias
        break
if plat == 'linux':
    from .pkg_data.linux.obf import obf
    from .pkg_data.linux.express import express
elif plat in ('darwin', 'ios'):
    from .pkg_data.darwin.obf import obf
    from .pkg_data.darwin.express import express
elif plat == 'windows':
    from .pkg_data.windows.obf import obf
    from .pkg_data.windows.express import express
elif plat in ('freebsd', 'poky'):
    from .pkg_data.linux.obf import obf
    from .pkg_data.linux.express import express
else:
    raise NotImplementedError(plat)


class BDWP:
    utils = RapidUpload()
    browser_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36"
    client_useragent = "netdisk;7.24.1.2;PC;PC-Windows;10.0.19044;WindowsBaiduYunGuanJia"
                      #"netdisk;7.23.0.10;PC;PC-Windows;10.0.18363;WindowsBaiduYunGuanJia"
    download_useragent = "netdisk;P2SP;3.0.0.183"

    def _getBDSTOKEN(self):
        if not hasattr(self, "_bdstoken"):
            url = "https://pan.baidu.com/api/gettemplatevariable?fields=[\"bdstoken\"]"
            headers = {
                "user-agent": self.browser_useragent,
                "cookie": "BDUSS={}; STOKEN={}".format(self.BDUSS, self.STOKEN)
            }
            r = self.s.get(url, headers=headers)
            setattr(self, "_bdstoken", r)
        return getattr(self, "_bdstoken")

    def getBDSTOKEN(self):
        return self._getBDSTOKEN().json()

    def _getSignCore(self, surl):
        if not hasattr(self, "_signcore"):
            url = "https://pan.baidu.com/share/tplconfig?surl={}&fields=sign,timestamp&channel=chunlei&web=1&app_id=250528&clienttype=0".format(surl)
            headers = {
                "user-agent": self.browser_useragent,
                "cookie": "BDUSS={}; STOKEN={}".format(self.BDUSS, self.STOKEN)
            }
            r = self.s.get(url, headers=headers)
            setattr(self, "_signcore", r)
        return getattr(self, "_signcore")

    def getSignCore(self, surl):
        return self._getSignCore(surl).json()

    def _getList(self, code, pw, path):
        url = "https://pan.baidu.com/share/wxlist?channel=weixin&version=2.2.2&clienttype=25&web=1"
        # self.s.get("https://pan.baidu.com")
        headers = {
            "user-agent": self.browser_useragent,
            "cookie": "BAIDUID=;BAIDUID_BFESS;",
        }
        return self.s.post(url, data={
            "shorturl": "1"+code,
            "dir": path,
            "root": "0" if path else "1",
            "pwd": pw,
            "page": "1",
            "num": "9999",
            "order": "time",
        }, headers=headers)

    def getList(self, code, pw, path):
        return self._getList(code, pw, path).json()

    def _getDlink(self, fs_id, ts, sign, randsk, share_id, uk, appid=250528):
        url = "https://pan.baidu.com/api/sharedownload?app_id={}&channel=chunlei&clienttype=12&sign={}&timestamp={}&web=1".format(
            appid,
            sign,
            ts
        )
        headers = {
            "User-Agent": self.browser_useragent,
            "Cookie": self.cookies.split("; version=")[0],
            "Referer": "https://pan.baidu.com/disk/main",
        }
        r = self.s.post(url, data={
            "encrypt": "0",
            "extra": '{"sekey":"'+randsk+'"}',
            "fid_list": "[{}]".format(fs_id),
            "primaryid": share_id,
            "uk": uk,
            "product": "share",
            "type": "nolimit",
        }, headers=headers)
        return r

    def getDlink(self, fs_id, ts, sign, randsk, share_id, uk, appid=250528):
        return self._getDlink(fs_id, ts, sign, randsk, share_id, uk, appid=appid).json()

    def getFiles(self, code, pw, path, cb=None):
        lists = self.getList(code, pw, path)
        # print(lists)
        randsk = lists["data"]["seckey"].replace("-", "+").replace("~", "=").replace("_", "/")
        share_id = lists["data"]["shareid"]
        uk = lists["data"]["uk"]
        # print(randsk, share_id, uk)
        for _ in lists["data"]["list"]:
            if int(_["isdir"]) == 1:
                print(_["path"])
                self.getFiles(code, pw, _["path"], cb)
            else:
                r = self.getFile(code, randsk, share_id, uk, _)
                callable(cb) and cb(r)

    def getFile(self, code, randsk, share_id, uk, item, vip, _raise=False):
        orandsk = randsk
        randsk = randsk.replace("-", "+").replace("~", "=").replace("_", "/")
        def method_1():
            signcore = self.getSignCore("1"+code)
            # print(signcore)
            ts = signcore["data"]["timestamp"]
            sign = signcore["data"]["sign"]
            # print("\tdebug", sign, ts)
            fs_id = item["fs_id"]
            dlink = self.getDlink(fs_id, ts, sign, randsk, share_id, uk)
            # print(dlink)
            dlink = dlink["list"][0]["dlink"]
            # print("\tdebug", dlink)
            # print(self.cookies)
            r = express.main(create_scraper, dlink, item, dict([_.split("=", 1) for _ in self.cookies.split("; ")]), self.download_useragent)
            # r["ua"] = self.download_useragent
            return r
            #     dlink = dlink["list"][0]["dlink"]
            #     r = self.s.head(dlink, headers={
            #         "Cookie": "BDUSS={}".format(self.BDUSS),
            #         "User-Agent": self.download_useragent
            #     }, allow_redirects=False)
            # print("\tdebug", r.status_code, r.headers)
            # if "Location" not in r.headers:
            #     print(r.content)
            # return {
            #     "url": r.headers["Location"],
            #     "path": "/".join(item["path"].split("/")[:-1]),
            #     "name": item["server_filename"],
            #     "size": item["size"],
            #     "md5": item["md5"],
            # }
        def method_2():
            return obf.main(create_scraper, code, orandsk, share_id, uk, item)
        if vip:
            a = method_1
            method_1 = method_2
            method_2 = a
        try:
            return method_2()
        except Exception as e:
            if _raise:
                raise e
            import traceback
            traceback.print_exc()
            return method_1()

    def rapid_upload_getFile(self, md5, size, path, name, version):
        s = create_scraper()
        s.headers.update({
            "cookie": self.cookies.split("; version=")[0],
        })
        r = {
            "md5": md5,
            "size": size,
            "path": path+"/"+name,
        }
        bdstoken = self.getBDSTOKEN()["result"]["bdstoken"]
        rs = self.utils.saveFile2(s, bdstoken, r)
        # for r in rs:
        #     print(r.status_code, r.headers, r.content.decode(), r.request.body, r.url)
        if any(r.json()["errno"] for r in rs):
            raise TypeError("error", md5, size, path, name, [r.content.decode() for r in rs])
        r = self.utils.getFile(create_scraper(), self.cookies, quote(path+"/"+name), self.client_useragent)
        def b4exit():
            r2=None
            try:
                r2=s.post(
                    "https://pan.baidu.com/api/filemanager?async=2&onnest=fail&opera=delete&bdstoken=" + bdstoken + "&newVerify=1&clienttype=0&app_id=250528&web=1", data={
                        "filelist": json.dumps(["/".join(path.split("/")[:3])])
                    },
                    timeout=10
                )
            except Exception as e:
                print("failed to recycle ru items", md5, size, path, name, r2, e)
        if r.status_code == 200 and b"urls" in r.content:
            r = {"urls": [_["url"].replace("https://", "http://") for _ in r.json()["urls"]]}
            # print(r)
            r["url"] = r["urls"][0]
            urls2 = [_ for _ in r["urls"] if not any("http://" + __ in _ for __ in [
                "allall",
                "bjbgp",
                "qdall",
            ])]
            if int(size)>100*1024*1024:
                if urls2:
                    r["urls"] = urls2
                    b4exit()
                    return r
            else:
                r["urls"] = urls2
                b4exit()
                return r
            try:
                pw, r3 = self.utils.shareFile(create_scraper(), self.cookies, path+"/"+name)
                # print(r3.content.decode())
                r3 = r3.json()
                if r3["errno"]:
                    raise
            except RuntimeError as e:
                b4exit()
                if version:
                    return r
                else:
                    raise e
            except Exception as e:
                b4exit()
                raise e
                # if version:
                #     return r
                # else:
                #     raise RuntimeError("error version 0", md5, size, path, name)
            time.sleep(2)
            code = r3["shorturl"].split(".com/s/1")[-1]
            try:
                # print(code, pw)
                r4 = self._getList(code, pw, "")
                # print(r4.content.decode())
                r4 = r4.json()
                uk = r4["data"]["uk"]
                shareid = r4["data"]["shareid"]
                randsk = r4["data"]["seckey"]
                fs_id = r4["data"]["list"][0]["fs_id"]
                item = {
                    "fs_id": fs_id,
                    "path": "//",
                    "server_filename": "",
                    "size": "",
                    "md5": "",
                }
                r = self.getFile(code, randsk, shareid, uk, item, vip=False, _raise=True)
                r.pop("path")
                r.pop("name")
                r.pop("size")
                r.pop("md5")
                if version:
                    r["urls"] = [r["url"]]
                b4exit()
                return r
            except Exception as e:
                print("failed to kelongwo items", md5, size, path, name, r3, e)
                b4exit()
                raise ConnectionError(e)
        b4exit()
        raise TypeError("error", md5, size, path, name, r.status_code, r.content.decode())

    def __init__(self, cookies, source_address=None):
        self.cookies = cookies
        self.BDUSS = cookies.split("BDUSS=")[1].split(";")[0]
        self.STOKEN = cookies.split("STOKEN=")[1].split(";")[0]
        s = create_scraper()
        if source_address:
            for prefix in ('http://', 'https://'):
                s.get_adapter(prefix).init_poolmanager(
                    connections=requests.adapters.DEFAULT_POOLSIZE,
                    maxsize=requests.adapters.DEFAULT_POOLSIZE,
                    source_address=(source_address, 0),
                )
        self.s = s

    def extract_code_pw(self, url):
        m = re.search(r"/s/1([a-zA-Z0-9\-\_]{22})(?:\?pwd=([a-zA-Z0-9]{4}))?$", url)
        if not m:
            m = re.search(r"/share/init\?surl=([a-zA-Z0-9\-\_]{22})(?:&pwd=([a-zA-Z0-9]{4}))?$", url)
            if not m:
                raise
        return m.groups()


