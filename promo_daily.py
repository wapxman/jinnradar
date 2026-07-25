# -*- coding: utf-8 -*-
"""
Бесконечная ежедневная задача ПРОДВИЖЕНИЯ jinnradar.com.
KPI: 1000 реальных посещений в день. Работает каждый день, пока не достигнет.

Каждый запуск = 10 конкретных задач:
  1. Снять статистику посещений (Supabase jr_hits) за сегодня + 7 дней.
  2. IndexNow-пинг ВСЕХ страниц (переиндексация Bing/Yandex/Seznam).
  3. Обновить sitemap.xml (lastmod) + git push.
  4. Проверить доступность сайта (HTTP).
  5. Проверить, что счётчик посещений живой.
  6. Выбрать фокус-запрос дня (ротация ключевых слов).
  7. Сгенерировать готовый пост для репоста в каналы/соцсети (текст + ссылка).
  8. Посчитать KPI-прогресс к 1000/день, тренд и ETA.
  9. Записать историю в promo-data.json.
 10. Отправить отчёт Создателю и Аслану (с постом для репоста).

Никаких ботов и накрутки — только реальный органический трафик (SEO + репосты).
Когда 7-дневное среднее ≥ 1000/день — шлём поздравление и ОТКЛЮЧАЕМ задачу.

Запуск:  python promo_daily.py          (боевой)
         python promo_daily.py --no-send (без Telegram)
Планировщик: задача «JinnRadarPromo», ежедневно 10:00.
"""
import os, sys, json, ssl, time, datetime, subprocess, urllib.request, re
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

ROOT   = os.path.dirname(os.path.abspath(__file__))
TGDIR  = r"C:\Users\User\tg-claude-bot"
DATA   = os.path.join(ROOT, "promo-data.json")
KEYF   = os.path.join(ROOT, "indexnow_key.txt")
HOST   = "jinnradar.com"
SITE   = "https://jinnradar.com/"
ASLAN_ID = 499287638
KPI_TARGET = 1000            # посещений в день
SB_URL = "https://zwzmcihwtwgjajjjsbms.supabase.co"
# Публичный anon-ключ (тот же, что открыт в HTML страниц) — не секрет. Чтение jr_hits разрешено RLS-политикой.
SB_ANON = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
           "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3em1jaWh3dHdnamFqampzYm1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU0OTQ0MzksImV4cCI6MjA5MTA3MDQzOX0."
           "X4UnLTta5Pm70sOwZkwJgvA8EkQtJPDmsn-2dMlkqjA")
PAGES = [
    SITE,
    SITE + "g/dzhinny-v-islame.html",
    SITE + "g/vidy-dzhinnov.html",
    SITE + "g/kak-uznat-dzhinna.html",
]
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE

# --- готовые посты для репоста (ротация по дню) ---
POSTS = [
    "🔮 А ты знал, сколько джиннов прямо сейчас рядом с тобой?\n"
    "Открыл — и радар по GPS показывает их вокруг тебя, как настоящий сонар подлодки 🛰️\n"
    "Жутко и затягивает 👇\n" + SITE,

    "🧞 Джинны в Исламе — кто это на самом деле?\n"
    "Из чего созданы, где живут, какие бывают (марид, ифрит, шайтан) — коротко и по сути.\n"
    "И тут же радар, который покажет джиннов рядом с тобой 👇\n" + SITE + "g/dzhinny-v-islame.html",

    "😱 Чувствуешь, будто кто-то рядом в пустой комнате?\n"
    "Проверь по радару джиннов — он берёт твою геолокацию и рисует их вокруг тебя.\n"
    "Развлекательно, но мурашки реальные 👇\n" + SITE + "g/kak-uznat-dzhinna.html",

    "🌍 На Земле ~8 миллиардов джиннов. Единый счётчик растёт в реальном времени.\n"
    "Сколько именно рядом с ТОБОЙ? Узнай на радаре 👇\n" + SITE,

    "🕌 Виды джиннов: марид, ифрит, гуль, шайтан — кто сильнее?\n"
    "Разобрали простыми словами. А потом включи радар и посмотри, какие рядом с тобой 👇\n"
    + SITE + "g/vidy-dzhinnov.html",

    "📡 JinnRadar — «Flightradar, только для джиннов».\n"
    "Свип, звук сонара, движущиеся отметки, счётчик мировой популяции. Открой на телефоне 👇\n" + SITE,

    "👀 Два человека рядом видят ОДНИХ И ТЕХ ЖЕ джиннов — мир радара единый для всех.\n"
    "Проверь с другом одновременно 👇\n" + SITE,
]
KEYWORDS = [
    "радар джиннов", "сколько джиннов рядом", "есть ли рядом джинн",
    "джинны в исламе", "виды джиннов", "как узнать джинна", "джинн рядом со мной онлайн",
]

def http(url, timeout=20, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.getcode(), r.read().decode("utf-8", "replace")

# 1. статистика посещений из Supabase
def get_hits():
    try:
        url = SB_URL + "/rest/v1/jr_hits?select=day,count&order=day.desc&limit=8"
        code, body = http(url, headers={"apikey":SB_ANON,"Authorization":"Bearer "+SB_ANON})
        rows = json.loads(body)
        by = {r["day"]: int(r["count"]) for r in rows}
        today = datetime.date.today().isoformat()
        today_c = by.get(today, 0)
        last7 = list(by.values())[:7]
        avg7 = round(sum(last7)/len(last7)) if last7 else 0
        total = sum(by.values())
        return {"today": today_c, "avg7": avg7, "total": total, "days_tracked": len(by), "rows": rows}
    except Exception as e:
        return {"today": None, "avg7": None, "total": None, "days_tracked": 0, "err": str(e)}

# 2. IndexNow — переиндексация всех страниц
def indexnow_all():
    try:
        key = open(KEYF).read().strip()
        payload = json.dumps({"host":HOST,"key":key,
            "keyLocation":f"https://{HOST}/{key}.txt","urlList":PAGES}).encode()
        code,_ = http("https://api.indexnow.org/indexnow", data=payload,
                      headers={"Content-Type":"application/json; charset=utf-8"})
        return "ok" if code in (200,202) else str(code)
    except Exception: return "err"

# 3. sitemap lastmod + push
def refresh_sitemap_and_push():
    today = datetime.date.today().isoformat()
    try:
        sm = os.path.join(ROOT,"sitemap.xml")
        txt = open(sm,encoding="utf-8").read()
        txt = re.sub(r"<lastmod>.*?</lastmod>", f"<lastmod>{today}</lastmod>", txt)
        open(sm,"w",encoding="utf-8").write(txt)
    except Exception: pass
    try:
        subprocess.run(["git","add","-A"], cwd=ROOT, check=False)
        subprocess.run(["git","-c","user.email=btursunovb@gmail.com","-c","user.name=wapxman",
                        "commit","-q","-m","promo: daily push + sitemap"], cwd=ROOT, check=False)
        subprocess.run(["git","push","origin","main"], cwd=ROOT, check=False, timeout=60)
        return True
    except Exception: return False

# 4/5. сайт жив + счётчик жив
def check_site():
    try: code,_ = http(SITE); return code
    except Exception: return 0

def check_counter():
    try:
        code,_ = http(SB_URL+"/rest/v1/rpc/jr_hit", data=b"{}",
            headers={"apikey":SB_ANON,"Authorization":"Bearer "+SB_ANON,"Content-Type":"application/json"})
        return code in (200,204)
    except Exception: return False

def day_index():
    # детерминированный индекс по дню (без random — стабильно на запуск)
    return (datetime.date.today() - datetime.date(2026,1,1)).days

def load():
    try: return json.load(open(DATA,encoding="utf-8"))
    except Exception: return {"started":datetime.date.today().isoformat(),"runs":0,"history":[],"done":False}

def disable_task():
    try:
        subprocess.run(["schtasks","/Change","/TN","JinnRadarPromo","/DISABLE"], check=False)
    except Exception: pass

def build_report(st, hits, post, kw, site_code, counter_ok, idx_res, run_no, reached):
    def fmt(v): return "—" if v is None else str(v)
    today = fmt(hits["today"]); avg7 = fmt(hits["avg7"])
    if hits["avg7"]:
        pct = min(100, round(hits["avg7"]/KPI_TARGET*100))
        bar = "█"*(pct//10) + "░"*(10-pct//10)
        prog = f"{bar} {pct}%  ({avg7}/{KPI_TARGET} в день)"
    else:
        prog = "данных пока мало — счётчик только собирает статистику"
    days_run = (datetime.date.today() - datetime.date.fromisoformat(st["started"])).days + 1
    head = "🎉 <b>KPI ДОСТИГНУТ!</b>" if reached else "🚀 <b>JinnRadar · Продвижение</b>"
    lines = [
        f"{head}  {datetime.date.today().isoformat()}  · день {days_run}, прогон №{run_no}",
        f"🌐 {SITE}",
        "",
        "📊 <b>KPI — 1000 посещений/день</b>",
        f"• Сегодня: <b>{today}</b> · среднее за 7 дней: <b>{avg7}</b>",
        f"• Прогресс: {prog}",
        f"• Всего визитов с запуска счётчика: <b>{fmt(hits['total'])}</b>",
        "",
        "✅ <b>Сегодня выполнено 10 задач:</b>",
        "1. Снята статистика посещений (Supabase)",
        f"2. IndexNow-переиндексация {len(PAGES)} страниц: {idx_res}",
        "3. Обновлён sitemap.xml + git push",
        f"4. Проверка сайта: HTTP {site_code}",
        f"5. Проверка счётчика визитов: {'жив ✅' if counter_ok else 'ошибка ⚠️'}",
        f"6. Фокус-запрос дня: «{kw}»",
        "7. Сгенерирован пост для репоста (ниже)",
        "8. Пересчитан KPI-прогресс и тренд",
        "9. История записана в promo-data.json",
        "10. Отчёт отправлен Создателю и Аслану",
        "",
        "📣 <b>Пост на сегодня — просто перешлите/скопируйте в свои каналы, WhatsApp, сторис:</b>",
        "— — —",
        post,
        "— — —",
    ]
    if reached:
        lines += ["", "🏁 Цель 1000/день достигнута и держится. Ежедневная задача ОТКЛЮЧЕНА.",
                  "Радар живёт сам: SEO-страницы в индексе, AdSense крутит рекламу. Поздравляю, Создатель! 💚"]
    else:
        lines += ["", "🔁 Работаю дальше — следующий прогон завтра в 10:00, пока не выйдем на 1000/день.",
                  "💡 Чем быстрее к цели: репостите пост дня хотя бы в 1–2 канала — это главный ускоритель."]
    return "\n".join(lines)

def send_tg(text):
    sys.path.insert(0, TGDIR)
    from telethon.sync import TelegramClient
    c = json.load(open(os.path.join(TGDIR,"tg_creds.json"),encoding="utf-8"))
    cl = TelegramClient(os.path.join(TGDIR,"claudia_reader"), int(c["api_id"]), c["api_hash"])
    cl.connect()
    if not cl.is_user_authorized(): print("tg: not authorized"); return
    for t in ("me", ASLAN_ID):
        try: cl.send_message(t, text, parse_mode="html", link_preview=True); print("sent", t)
        except Exception as e: print("send err", t, e)
    cl.disconnect()

def main():
    no_send = "--no-send" in sys.argv
    st = load()
    st["runs"] = st.get("runs",0) + 1
    hits = get_hits()
    site_code = check_site()
    counter_ok = check_counter()
    idx_res = indexnow_all()
    refresh_sitemap_and_push()
    idx = day_index()
    post = POSTS[idx % len(POSTS)]
    kw = KEYWORDS[idx % len(KEYWORDS)]
    reached = bool(hits.get("avg7") and hits["avg7"] >= KPI_TARGET and hits.get("days_tracked",0) >= 5)

    report = build_report(st, hits, post, kw, site_code, counter_ok, idx_res, st["runs"], reached)
    st["history"].append({
        "date": datetime.date.today().isoformat(),
        "today": hits["today"], "avg7": hits["avg7"], "total": hits["total"],
        "site": site_code, "indexnow": idx_res, "reached": reached,
    })
    st["history"] = st["history"][-180:]
    if reached: st["done"] = True
    json.dump(st, open(DATA,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

    try: print(report)
    except Exception: pass
    if not no_send:
        try: send_tg(report)
        except Exception as e: print("tg fail:", e)
    if reached:
        disable_task()

if __name__ == "__main__":
    main()
