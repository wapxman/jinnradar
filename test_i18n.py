# -*- coding: utf-8 -*-
"""Живой тест мультиязычности jinnradar.com: страницы, кнопки, тексты, ссылки."""
import sys, ssl, re, urllib.request
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
from build_langs import LANGS, SITE, ANON

CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"JinnRadarTest/1.0"})
    with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
        return r.getcode(), r.read().decode("utf-8","replace")

fails=[]; ok=0
def check(cond, msg):
    global ok
    if cond: ok+=1
    else: fails.append(msg)

print("=== Тест 50 языковых страниц (живой сайт) ===")
for c,(name,d,title,desc,h1,p1,p2,cta) in LANGS.items():
    url=f"{SITE}l/{c}.html"
    try:
        code,html=fetch(url)
    except Exception as e:
        fails.append(f"{c}: НЕ ОТКРЫЛАСЬ ({e})"); continue
    check(code==200, f"{c}: HTTP {code}")
    check(f'lang="{c}"' in html, f"{c}: нет lang={c}")
    check(f'dir="{d}"' in html, f"{c}: нет dir={d}")
    check(f"<title>{title}</title>" in html, f"{c}: title не совпал/битая кодировка")
    check(h1 in html, f"{c}: H1 не совпал/битый текст")
    check(p1 in html and p2 in html, f"{c}: тексты абзацев не совпали")
    check(cta in html, f"{c}: текст кнопки CTA не совпал")
    # кнопка ведёт на радар
    check(f'class="cta" href="{SITE}"' in html, f"{c}: кнопка CTA не ведёт на радар")
    # beacon-ключ цел
    check(ANON in html, f"{c}: beacon-ключ повреждён")
    # hreflang alternates
    check(html.count('rel="alternate"')>=51, f"{c}: мало hreflang ({html.count('rel=\"alternate\"')})")
    # canonical на себя
    check(f'rel="canonical" href="{url}"' in html, f"{c}: canonical неверный")

print(f"страниц проверено: {len(LANGS)}")

print("\n=== Тест кнопок/ссылок выбора языка на ГЛАВНОЙ ===")
_,home=fetch(SITE)
check('id="langSel"' in home, "на главной нет селектора языка")
opts=re.findall(r'<option value="([^"]+)"', home)
opts=[o for o in opts if o]  # убрать пустой placeholder
print(f"пунктов в селекторе: {len(opts)}")
for o in opts:
    tgt = SITE.rstrip('/')+o if o.startswith('/') else o
    try:
        code,_=fetch(tgt); check(code==200, f"пункт селектора битый: {o} -> HTTP {code}")
    except Exception as e:
        fails.append(f"пункт селектора не открылся: {o} ({e})")

print("\n=== Тест языкового хаба /l/ и переключателя внизу страниц ===")
_,hub=fetch(SITE+"l/")
for c in LANGS: check(f'l/{c}.html' in hub, f"хаб /l/: нет ссылки на {c}")
# переключатель внизу en-страницы указывает на все языки
_,en=fetch(SITE+"l/en.html")
for c in LANGS: check(f'{SITE}l/{c}.html' in en, f"переключатель en: нет ссылки на {c}")

print("\n=== Тест страниц-статей /g/ и их кнопок ===")
G=["g/","g/dzhinny-v-islame.html","g/vidy-dzhinnov.html","g/kak-uznat-dzhinna.html",
   "g/dzhinn-v-dome-priznaki.html","g/kak-zashchititsya-ot-dzhinnov.html","g/jinlar-haqida.html"]
for g in G:
    try:
        code,html=fetch(SITE+g)
        check(code==200, f"/{g}: HTTP {code}")
        check(ANON in html, f"/{g}: beacon-ключ повреждён")
        check('href="/"' in html or f'href="{SITE}"' in html, f"/{g}: нет ссылки на радар")
    except Exception as e:
        fails.append(f"/{g}: не открылась ({e})")

print("\n"+"="*44)
if fails:
    print(f"❌ ПРОБЛЕМ: {len(fails)} (успешных проверок: {ok})")
    for f in fails: print("  •", f)
else:
    print(f"✅ ВСЁ РАБОТАЕТ — {ok} проверок пройдено, 0 ошибок")
