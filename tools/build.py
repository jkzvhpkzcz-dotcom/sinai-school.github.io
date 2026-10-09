#!/usr/bin/env python3
"""Build the portal app (index.html) from the published school-system page.
usage: python3 tools/build.py SOURCE.html [OUT_DIR]
Prints CHANGED or SAME (compares the embedded timetable snapshot + app code)."""
import sys, re, json, hashlib, os
src = open(sys.argv[1], encoding='utf-8').read()
out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = re.search(r'<script type="application/json" id="snap">(.*?)</script>', src, re.S)
if not m or not re.search(r'<script id="appjs">', src): sys.exit('ERROR: not the school system page')
snap = json.loads(m.group(1).replace('<\\/', '</'))
if not snap or not snap.get('cells'): sys.exit('ERROR: no published timetable in the page')
ver = '%s-%s' % (snap.get('ver', ''), snap.get('at', ''))
head = ('<script>window.OFFLINE_COPY=1;document.documentElement.classList.add("offline")</script>\n'
  '<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#0c362f"><link rel="apple-touch-icon" href="icon-512.png"><link rel="icon" href="icon-192.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="إعدادية سيناء للبنين"><meta name="application-name" content="إعدادية سيناء للبنين">'
  '<script>window.APP_VER=' + json.dumps(ver) + ";if('serviceWorker' in navigator)addEventListener('load',function(){navigator.serviceWorker.register('sw.js').then(function(r){r.update()}).catch(function(){})});navigator.serviceWorker&&navigator.serviceWorker.addEventListener('controllerchange',function(){if(!window.__rl){window.__rl=1;location.reload()}});</script>\n")
k = src.find('<title')
html = src[:k] + head + src[k:] if k >= 0 else head + src
dst = os.path.join(out, 'index.html')
old = open(dst, encoding='utf-8').read() if os.path.exists(dst) else ''
strip = lambda h: re.sub(r'window\.APP_VER="[^"]*"', '', h)
if strip(old) == strip(html):
    print('SAME'); sys.exit(0)
open(dst, 'w', encoding='utf-8').write(html)
print('CHANGED', ver, len(html))
