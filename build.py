# -*- coding: utf-8 -*-
import os, io, re
from html import escape

ROOT = "apps"
CSS = ("body{margin:0;font-family:sans-serif;background:#eee;color:#222}"
       ".w{padding:10px}h1{font-size:22px;margin:10px 0}"
       ".i{display:block;background:#fff;border:1px solid #ccc;"
       "padding:14px;margin:8px 0;color:#222;text-decoration:none}"
       ".b{display:block;background:#4caf50;color:#fff;text-align:center;"
       "padding:16px;margin:14px 0;text-decoration:none;font-size:18px}"
       "h2{font-size:16px;margin:16px 0 4px;color:#555}"
       ".s{color:#777;font-size:13px}a.u{color:#06c}")

def read_txt(path):
    data, key = {}, None
    with io.open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\r\n")
            m = re.match(r"^\[(.+)\]$", line.strip())
            if m:
                key = m.group(1).strip().upper()
                data[key] = []
            elif key:
                data[key].append(line)
    return dict((k, "\n".join(v).strip()) for k, v in data.items())

def text(s):
    return escape(s).replace("\n", "<br>")

def page(title, body):
    return ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><style>%s</style></head>'
            '<body><div class="w">%s</div></body></html>'
            % (escape(title), CSS, body))

def write(path, html):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(html)

def dirs(path):
    return sorted(d for d in os.listdir(path)
                  if os.path.isdir(os.path.join(path, d)))

cats = []
for cat in dirs(ROOT):
    cpath = os.path.join(ROOT, cat)
    items = []
    for app in dirs(cpath):
        apath = os.path.join(cpath, app)
        files = os.listdir(apath)
        txts = [f for f in files if f.endswith(".txt")]
        apks = [f for f in files if f.endswith(".apk")]
        info = read_txt(os.path.join(apath, txts[0])) if txts else {}
        name = info.get("НАЗВАНИЕ") or app
        body = '<a class="u" href="../">&larr; Назад</a><h1>%s</h1>' % text(name)
        if apks:
            size = os.path.getsize(os.path.join(apath, apks[0])) / 1048576.0
            body += ('<a class="b" href="%s">Скачать APK (%.1f МБ)</a>'
                     % (escape(apks[0]), size))
        else:
            body += '<p class="s">APK пока нет</p>'
        body += "<h2>Описание</h2><div>%s</div>" % text(info.get("ОПИСАНИЕ", ""))
        body += "<h2>Системные требования</h2><div>%s</div>" % text(
            info.get("СИСТЕМНЫЕ ТРЕБОВАНИЯ", ""))
        write(os.path.join(apath, "index.html"), page(name, body))
        items.append((app, name))
    body = '<a class="u" href="../../">&larr; Назад</a><h1>%s</h1>' % text(cat)
    for app, name in items:
        body += '<a class="i" href="%s/">%s</a>' % (escape(app), text(name))
    write(os.path.join(cpath, "index.html"), page(cat, body))
    cats.append((cat, len(items)))

body = "<h1>OldMarket</h1>"
for cat, n in cats:
    body += ('<a class="i" href="apps/%s/">%s <span class="s">(%d)</span></a>'
             % (escape(cat), text(cat), n))
write("index.html", page("OldMarket", body))
