from base64 import b64encode, b64decode
from subprocess import run, PIPE
import sys
import random
import string
import json
import os


class RapidUpload:
    def parse_rapid_upload(self, url):
        if url.startswith("bdpan"):
            return self.parse_pandl(url)
        if url.startswith("BaiduPCS-Go"):
            return self.parse_pcsgo(url)
        if url.startswith("BDLINK"):
            return self.parse_ali(url)
        if len(url.split("#", 3))==4 or len(url.split("#", 3))==3:
            url = url.split("#")
            if url[1].isdigit():
                url.insert(1, "")
            url = "#".join(url)
            return self.parse_std(url)
        raise ValueError("unknown rapid upload url format", url)

    @staticmethod
    def parse_pandl(o):
        r = b64decode(o.split("bdpan://")[1]).decode().split("|")
        return {
            "md5": r[2],
            "md5s": r[3],
            "size": r[1],
            "path": r[0],
        }

    @staticmethod
    def parse_pcsgo(o):
        r = o.split("=")
        r = [_.split(" ")[-2:] for _ in r]
        r[0].pop(0)
        name = r[-1].pop(1)
        r = {r[i-1][-1][1:]: r[i][0] for i in range(1, len(r))}
        try:
            IS_WIN32 = not sys.platform.startswith(("darwin", "cygwin", "linux"))
            out = run(" ".join(["\"{}\"".format(_) if " " in _ else _ for _ in [
                "python" if IS_WIN32 else "python3",
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "cli_parse.py"
                ),
                name
            ]]), shell=True, stdout=PIPE, stderr=PIPE)
            if out.returncode != 0:
                raise
            name = out.stdout.decode().strip()
        except:
            name = name[1:-1]
        r["path"] = name
        return r

    @staticmethod
    def parse_ali(o):
        x = o[6:]
        x = b64decode(x)
        if x[:5] != b"BDFS\x00":
            raise ValueError("unknown rapid upload url format", o)
        def readNumber(start, size):
            num = 0
            i = start+size
            while True:
                if i<=start:
                    return num
                i -= 1
                num = x[i] + num * 256
        def readULong(start):
            return readNumber(start, 8)
        def readUInt(start):
            return readNumber(start, 4)
        def readHex(start, length):
            return x[start:start+length].hex()
        def readUnicode(start, length):
            if length&1:
                length += 1
            r = []
            c = x[start:start+length]
            for ii in range(0, len(c), 2):
                r.append("\\u{:0>2}{:0>2}".format(hex(c[ii+1])[2:], hex(c[ii])[2:]))
            return json.loads('"'+"".join(r)+'"')
        total = readUInt(5)
        ptr = 9
        r = []
        for ii in range(0, total):
            size = readULong(ptr)
            md5 = readHex(ptr+0x8, 0x10)
            md5s = readHex(ptr+0x18, 0x10)
            name_length = readUInt(ptr+0x28) << 1
            ptr += 0x2c
            name = readUnicode(ptr, name_length)
            t = {
                "size": size,
                "md5": md5,
                "md5s": md5s,
                "name_length": name_length,
                "path": name,
            }
            r.append(t)
            ptr += name_length
        return r

    @staticmethod
    def parse_std(o):
        def Decrypt(e):
            if e[9] not in "0123456789abcdef":
                return decrypt(e)
            return e
        def decrypt(e):
            key = hex(ord(e[9])-ord("g"))[2:]
            key2 = e[0:9]+key+e[10:]
            d = ""
            for ii in range(0, len(key2)):
                d += hex(int(key2[ii], 16)^(15&ii))[2:]
            return d[8:16]+d[0:8]+d[24:32]+d[16:24]
        r = o.split("#", 3)
        return {
            "md5": Decrypt(r[0]),
            "md5s": Decrypt(r[1]) if r[1] else "",
            "size": r[2],
            "path": r[3],
        }

    def encrypt_std(self, md5):
        k = 0
        omd5 = md5
        md5 = md5[8:16]+md5[0:8]+md5[24:32]+md5[16:24]
        while True:
            if k<0 or k>15:
                raise ValueError("k", k, "(1 <= k <= 15)")
            d = ""
            key=hex(k)[2:]
            key2 = md5[0:9]+key+md5[10:]
            for ii in range(0, len(key2)):
                d += hex(int(key2[ii], 16)^(15&ii))[2:]
            e = d[0:9]+chr(ord('g')+k)+d[10:]
            if self.parse_rapid_upload(e+"#0#a")["md5"] == omd5:
                return e
            k+=1

    def saveFile2(self, s, bdstoken, o):
        r1 = s.post("https://pan.baidu.com/rest/2.0/xpan/file?method=precreate&bdstoken="+bdstoken, data={
            "size": o["size"],
            "path": o["path"],
            "block_list": json.dumps([o["md5"].lower()]),
            "rtype": "0",
            "isdir": "0",
        }, timeout=10)
        r2 = s.post("https://pan.baidu.com/rest/2.0/xpan/file?method=create&bdstoken="+bdstoken, data={
            "size": o["size"],
            "path": o["path"],
            "block_list": json.dumps([o["md5"].lower()]),
            "rtype": "0",
            "isdir": "0",
        }, timeout=10)
        # return [r2]
        return [r1, r2]
    
    def getFile(self, s, cookie, path, ua):
        version = cookie.split("version=")[1].split("; ")[0]
        rand = cookie.split("rand=")[1].split("; ")[0]
        time = cookie.split("time=")[1].split("; ")[0]
        devuid = cookie.split("devuid=")[1].split("; ")[0]
        url = "https://d.pcs.baidu.com/rest/2.0/pcs/file?app_id=250528&method=locatedownload&check_blue=1&es=1&esl=1&path=" + path + "&ver=4.0&dtype=1&err_ver=1.0&ehps=0&clienttype=8&channel=00000000000000000000000000000000&version=" + version + "&devuid=" + devuid + "&rand=" + rand + "&time=" + time + "&vip=2"
        r = s.post(url, headers={
            "cookie": cookie.split("; version=")[0],
            "user-agent": ua,
            "content-type": "application/x-www-form-urlencoded"
        }, timeout=10, data=b" ")
        return r

    def shareFile(self, s, cookie, path, pwd=None, period="1"):
        pwd = (pwd or "".join(random.choices(string.ascii_lowercase + string.digits, k=4)))[:4]
        version = cookie.split("version=")[1].split("; ")[0]
        rand = cookie.split("rand=")[1].split("; ")[0]
        time = cookie.split("time=")[1].split("; ")[0]
        devuid = cookie.split("devuid=")[1].split("; ")[0]
        url = "http://pan.baidu.com/share/pset?clienttype=8&channel=00000000000000000000000000000000&version=" + version + "&devuid=" + devuid + "&rand=" + rand + "&time=" + time + "&vip=2&wp_retry_num=2"
        r = s.post(url, headers={
            "cookie": cookie.split("; version=")[0],
            "user-agent": "netdisk;7.24.1.2;PC;PC-Windows;10.0.19044;WindowsBaiduYunGuanJia",
        }, data={
            "path_list": json.dumps([path]),
            "channel_list": "[]",
            "public": "0",
            "period": period,
            "shorturl": "1",
            "schannel": "4",
            "pwd": pwd,
            "pwd_type": "1",
            "eflag_disable": "1",
        }, timeout=10)
        return [pwd, r]


def test():
    r0 = RapidUpload().parse_rapid_upload(
        "bdpan://dGVzdC5leGV8NjQ2NzY1OXxENUFBQkVGQzMyOTBGN0EzQzA5OTEyMjI4QjEzNkQwQ3w4MjFBOUYwRDI3RkNEMTlDODA0NzREMjE0MEVEMkQ4NQ==")
    print(r0)
    r1 = RapidUpload().parse_rapid_upload(
        "BaiduPCS-Go rapidupload -length=6467659 -md5=D5AABEFC3290F7A3C09912228B136D0C -slicemd5=821A9F0D27FCD19C80474D2140ED2D85 \"/test.exe\"")
    print(r1)
    r2 = RapidUpload().parse_rapid_upload(
        "BDLINKQkRGUwAHAAAA0/AgXQEAAABvU6INa3SryWsF1pGpw7ALjjjB7lz4B3zYkhccg7C38ToAAABXAG8AcgBsAGQALgBXAGEAcgAuAFoALgAyADAAMQAzAC4AVQBuAHIAYQB0AGUAZAAuAEMAdQB0AC4ANwAyADAAcAAuAEIAbAB1AFIAYQB5AC4AeAAyADYANAAuAEQAVABTAC0AVwBpAEsAaQAuAG0AawB2AO4R0tEAAAAAFRyooon5Gjpr2PNCXDDiicea/BToo7MXRzn+Xqrh9QwdAAAAdgBlAGQAZQB0AHQALQBkAGUAcwBwAGkAYwBhAGIAbABlAG0AZQAyAC0ANwAyADAAcAAuAG0AawB2AIYxraEBAAAA8PUXRFc1LCIAi3+YLQ0xSqBzMBwhiwzN9Q/o7RUU2d49AAAARgBhAHMAdAAuAGEAbgBkAC4ARgB1AHIAaQBvAHUAcwAuADYALgAyADAAMQAzAC4ARQBYAFQARQBOAEQARQBEAC4AQgBsAHUAUgBhAHkALgA3ADIAMABwAC4ARABUAFMALgB4ADIANgA0AC0AQwBIAEQALgBtAGsAdgAwr4FAAQAAAGtznIezSTcggschTwyDeSpJXXOr1WTZzn1K6Byfvru3LQAAAEUAbgBkAGUAcgBzAC4ARwBhAG0AZQAuADIAMAAxADMALgBCAGwAdQBSAGEAeQAuADcAMgAwAHAALgBEAFQAUwAuAHgAMgA2ADQALQBDAEgARAAuAG0AawB2AC90N/wBAAAAzg+7wDIkqZ3dMofyRkiNe/HvEFRva/sn7UaMwnpEUDovAAAARABlAGEAZAAuAE0AYQBuAC4ARABvAHcAbgAuADIAMAAxADMALgAxADAAOAAwAHAALgBCAGwAdQBSAGEAeQAuAHgAMgA2ADQALQBTAFAAQQBSAEsAUwAuAG0AawB2ANs0gBcBAAAAls56xu/daOjUFfYnqAPVizbpxqmp1s/7HIb2xXFohvoUAAAAZABhAGEALQBlAGwAeQBzAGkAdQBtAC0ANwAyADAAcAAuAG0AawB2AJrzxRcBAAAAAJ/LCuSf1sSsoG4MPpZcW/Iv+/EEwjAk7n2vqmjPfZIXAAAAYwBiAGcAYgAtAGMAbABhAHMAaAB0AGkAdABhAG4AcwA3ADIAMAAuAG0AawB2AAA=")
    print(r2)
    r3 = RapidUpload().parse_rapid_upload(
        "d5aabefc3290f7a3c09912228b136d0c#821a9f0d27fcd19c80474d2140ed2d85#6467659#test.exe")
    print(r3)
    r4 = RapidUpload().parse_rapid_upload("d5aabefc3290f7a3c09912228b136d0c#6467659#test.exe")
    print(r4)

    for i in range(0, 16):
        r = RapidUpload().encrypt_std("d{}aabefc3290f7a3c09912228b136d0c".format(hex(i)[2:]))
        print(r)


if __name__ == "__main__":
    # test()
    r5=RapidUpload().parse_rapid_upload("17a2bcb8a2994df79a3453dcbc623865#6923159484#/防无双压#1.zip")
    print(r5)
    from cloudscraper import create_scraper
    def getBDSTOKEN():
        url = "https://pan.baidu.com/api/gettemplatevariable?fields=[\"bdstoken\"]"
        return s.get(url).json()["result"]["bdstoken"]
    s = create_scraper()
    cookie = open(r"D:\test_panbaidu\testapi\cookies\vip1.txt", "rb").read().decode()
    s.headers.update({
        "cookie": cookie
    })
    t = getBDSTOKEN()
    r = {
        "md5": "202cb962ac59075b964b07152d234b70",
        "size": "3",
        "path": "/abc/gg2/-test.txt",
    }
    from urllib.parse import quote
    r5["path"] = "/ru_task/a/"+r5["path"]#.replace("#", quote("#"))
    # rs=RapidUpload().saveFile2(s, t, r2[0])
    rs=RapidUpload().saveFile2(s, t, r5)
    for r in rs:
        print(r.status_code, r.headers, r.content.decode(), r.request.body, r.url)
    pwd,r=RapidUpload().shareFile(s, cookie, r5["path"])
    print(pwd,r.status_code, r.headers, r.content.decode(), r.request.body, r.url)
    # import time
    # print("sleep 10")
    # time.sleep(10)
    # r = s.post("https://pan.baidu.com/api/filemanager?async=2&onnest=fail&opera=delete&bdstoken="+t+"&newVerify=1&clienttype=0&app_id=250528&web=1", data={
    #     "filelist": json.dumps(["/abc/gg3/"])
    # })
    # print(r.status_code, r.headers, r.content.decode(), r.request.headers, r.request.body, r.url)


