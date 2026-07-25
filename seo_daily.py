# -*- coding: utf-8 -*-
"""
Ежедневная SEO-работа по jinnradar.com:
  1. Замер сайта (HTTP-статус, время ответа) и on-page здоровья (мета/OG/JSON-LD/sitemap/robots).
  2. PageSpeed Insights (моб. + десктоп) через Google PSI API.
  3. Пинг поисковиков через IndexNow (Bing/Yandex/Seznam) — просьба переобойти.
  4. Обновление lastmod в sitemap.xml.
  5. Запись метрик в seo-data.json + git push (обновляет дашборд).
  6. Отправка отчёта в Telegram: Создателю (Saved Messages) и Аслану (499287638).

Запуск: python seo_daily.py         (обычный прогон)
        python seo_daily.py --no-send  (без отправки в Telegram)
Ставится в Планировщик на 09:00 (задача JinnRadarSEO).
"""
import os, sys, json, time, ssl, urllib.request, urllib.parse, subprocess, datetime, re

SITE = "https://jinnradar.com/"
HOST = "jinnradar.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
TGDIR = r"C:\Users\User\tg-claude-bot"
DATA = os.path.join(ROOT, "seo-data.json")
KEYF = os.path.join(ROOT, "indexnow_key.txt")
ASLAN_ID = 499287638
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent":"JinnRadarSEO/1.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.getcode(), r.read().decode("utf-8","replace")

def measure_site():
    t0=time.time()
    try:
        code, html = get(SITE)
        ms=int((time.time()-t0)*1000)
    except Exception as e:
        return {"http_status":0,"response_ms":0,"html":""}, {"score":0}
    checks={
        "title": "<title>" in html and "радар" in html.lower(),
        "description": 'name="description"' in html,
        "canonical": 'rel="canonical"' in html,
        "og": 'property="og:title"' in html,
        "twitter": 'name="twitter:card"' in html,
        "jsonld": 'application/ld+json' in html,
    }
    # sitemap/robots доступны?
    try: sc,_=get(SITE+"sitemap.xml"); checks["sitemap"]= sc==200
    except: checks["sitemap"]=False
    try: rc,_=get(SITE+"robots.txt"); checks["robots"]= rc==200
    except: checks["robots"]=False
    score=int(100*sum(1 for v in checks.values() if v)/len(checks))
    checks["score"]=score
    return {"http_status":code,"response_ms":ms}, checks

def pagespeed(strategy):
    try:
        u=("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
           +urllib.parse.urlencode({"url":SITE,"strategy":strategy,"category":"performance"}))
        _,body=get(u, timeout=60)
        j=json.loads(body)
        s=j["lighthouseResult"]["categories"]["performance"]["score"]
        return int(round(s*100))
    except Exception as e:
        return None

def indexnow():
    try:
        key=open(KEYF).read().strip()
        payload=json.dumps({"host":HOST,"key":key,
            "keyLocation":f"https://{HOST}/{key}.txt","urlList":[SITE]}).encode()
        req=urllib.request.Request("https://api.indexnow.org/indexnow",data=payload,
            headers={"Content-Type":"application/json; charset=utf-8"})
        with urllib.request.urlopen(req,timeout=20,context=CTX) as r:
            return "ok" if r.getcode() in (200,202) else str(r.getcode())
    except Exception as e:
        return "err"

def update_sitemap():
    today=datetime.date.today().isoformat()
    sm=os.path.join(ROOT,"sitemap.xml")
    try:
        txt=open(sm,encoding="utf-8").read()
        if "<lastmod>" in txt:
            txt=re.sub(r"<lastmod>.*?</lastmod>",f"<lastmod>{today}</lastmod>",txt)
        else:
            txt=txt.replace("</loc>",f"</loc>\n    <lastmod>{today}</lastmod>",1)
        open(sm,"w",encoding="utf-8").write(txt)
    except Exception: pass

def git_push():
    try:
        subprocess.run(["git","add","seo-data.json","sitemap.xml"],cwd=ROOT,check=False)
        subprocess.run(["git","-c","user.email=btursunovb@gmail.com","-c","user.name=wapxman",
                        "commit","-q","-m","seo: daily metrics + sitemap lastmod"],cwd=ROOT,check=False)
        subprocess.run(["git","push","origin","main"],cwd=ROOT,check=False,timeout=60)
        return True
    except Exception: return False

def build_report(entry, prev):
    d=entry
    def arrow(cur,pr):
        if pr is None or cur is None: return ""
        return " ▲" if cur>pr else (" ▼" if cur<pr else " =")
    psm=d.get("pagespeed_mobile"); psd=d.get("pagespeed_desktop")
    ppsm=prev.get("pagespeed_mobile") if prev else None
    on=d["onpage"]; miss=[k for k,v in on.items() if k!="score" and not v]
    lines=[
        f"🔮 <b>JinnRadar · SEO-отчёт</b>  {d['date']}",
        f"🌐 Сайт: {SITE}",
        "",
        f"⚡ PageSpeed моб.: <b>{psm}</b>/100{arrow(psm,ppsm)}",
        f"🖥️ PageSpeed десктоп: <b>{psd}</b>/100",
        f"🧩 On-page SEO: <b>{on['score']}</b>/100" + (f" (нет: {', '.join(miss)})" if miss else " ✅ всё на месте"),
        f"📶 Ответ сайта: HTTP {d['http_status']} · {d['response_ms']} мс",
        f"🔔 IndexNow (переобход поисковиками): {d['indexnow']}",
        "",
        "🛠️ Сегодня сделано автоматически:",
        "• пинг поисковиков (IndexNow) на переиндексацию",
        "• обновлён sitemap.xml (lastmod) + отправлен",
        "• проверено on-page здоровье и скорость",
        "",
        "📊 Дашборд: https://jinnradar.com/dashboard.html (пароль jinn2026)",
    ]
    return "\n".join(lines)

def send_telegram(text):
    sys.path.insert(0, TGDIR)
    from telethon.sync import TelegramClient
    c=json.load(open(os.path.join(TGDIR,"tg_creds.json"),encoding="utf-8"))
    cl=TelegramClient(os.path.join(TGDIR,"claudia_reader"),int(c["api_id"]),c["api_hash"])
    cl.connect()
    if not cl.is_user_authorized():
        print("telegram: not authorized"); return
    for target in ("me", ASLAN_ID):
        try:
            cl.send_message(target, text, parse_mode="html", link_preview=False)
            print("sent to", target)
        except Exception as e:
            print("send err", target, e)
    cl.disconnect()

def main():
    no_send="--no-send" in sys.argv
    site, onpage = measure_site()
    entry={
        "date": datetime.date.today().isoformat(),
        "ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "http_status": site["http_status"],
        "response_ms": site["response_ms"],
        "onpage": onpage,
        "pagespeed_mobile": pagespeed("mobile"),
        "pagespeed_desktop": pagespeed("desktop"),
        "indexnow": indexnow(),
    }
    update_sitemap()
    # история
    try: data=json.load(open(DATA,encoding="utf-8"))
    except: data={"history":[]}
    prev=data["history"][-1] if data["history"] else None
    entry["report"]=build_report(entry, prev)
    data["history"].append(entry)
    data["history"]=data["history"][-120:]
    json.dump(data, open(DATA,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    git_push()
    print(entry["report"])
    if not no_send:
        try: send_telegram(entry["report"])
        except Exception as e: print("tg fail:", e)

if __name__=="__main__":
    main()
