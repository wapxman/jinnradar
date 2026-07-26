# -*- coding: utf-8 -*-
"""
JinnRadar · автономный CEO-движок (ежечасно).
Каждый час: снимает метрики -> запускает claude как CEO (одно улучшение) ->
считает, что стало лучше -> кладёт почасовой отчёт в Telegram «Избранное» (Saved Messages).

Задача Планировщика: «JinnRadarCEO», каждый час. MultipleInstances=IgnoreNew.
Флаги: --no-improve (пропустить шаг claude), --no-send (не слать в ТГ).
"""
import os, sys, json, ssl, time, glob, datetime, subprocess, urllib.request
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

ROOT   = os.path.dirname(os.path.abspath(__file__))
TGDIR  = r"C:\Users\User\tg-claude-bot"
CLAUDE = os.path.join(TGDIR, "claude.exe")
GHDIR  = r"C:\Users\User\Desktop\GitHub"          # cwd для claude (как у бота)
PROMPT = os.path.join(ROOT, "ceo_prompt.txt")
METRICS= os.path.join(ROOT, "ceo-metrics.json")
LOCK   = os.path.join(ROOT, ".ceo.lock")
SITE   = "https://jinnradar.com/"
SB_URL = "https://zwzmcihwtwgjajjjsbms.supabase.co"
ANON   = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
          "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3em1jaWh3dHdnamFqampzYm1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU0OTQ0MzksImV4cCI6MjA5MTA3MDQzOX0."
          "X4UnLTta5Pm70sOwZkwJgvA8EkQtJPDmsn-2dMlkqjA")
CLAUDE_TIMEOUT = 20*60
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE

def http(url, timeout=20, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.getcode(), r.read().decode("utf-8","replace")

def snapshot():
    m = {"ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
         "hour": datetime.datetime.now().strftime("%Y-%m-%d %H")}
    # метрики визитов
    try:
        _,body = http(SB_URL+"/rest/v1/jr_hits?select=day,count&order=day.desc&limit=8",
                      headers={"apikey":ANON,"Authorization":"Bearer "+ANON})
        rows=json.loads(body); by={r["day"]:int(r["count"]) for r in rows}
        today=datetime.date.today().isoformat()
        m["today"]=by.get(today,0)
        vals=list(by.values())[:7]; m["avg7"]=round(sum(vals)/len(vals)) if vals else 0
        m["total"]=sum(by.values())
    except Exception:
        m["today"]=m["avg7"]=m["total"]=None
    # сайт
    try:
        t0=time.time(); code,_=http(SITE); m["http"]=code; m["ms"]=int((time.time()-t0)*1000)
    except Exception:
        m["http"]=0; m["ms"]=0
    # контент
    m["articles"]=len(glob.glob(os.path.join(ROOT,"g","*.html")))
    m["langs"]=len([p for p in glob.glob(os.path.join(ROOT,"l","*.html"))
                    if not p.endswith("index.html")])
    return m

def run_ceo():
    """Запускает claude как CEO, возвращает его текстовый итог (что улучшено)."""
    try:
        prompt=open(PROMPT,encoding="utf-8").read()
    except Exception as e:
        return f"(нет промпта: {e})"
    try:
        p=subprocess.Popen([CLAUDE,"-p","--dangerously-skip-permissions"], cwd=GHDIR,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err=p.communicate(input=prompt.encode("utf-8"), timeout=CLAUDE_TIMEOUT)
        txt=(out or b"").decode("utf-8","replace").strip()
        if not txt: txt=(err or b"").decode("utf-8","replace").strip()[:500] or "(claude ничего не вернул)"
        return txt[-1800:]
    except subprocess.TimeoutExpired:
        try:
            subprocess.run(["taskkill","/F","/T","/PID",str(p.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception: pass
        return "(улучшение не успело за отведённое время в этот час)"
    except Exception as e:
        return f"(ошибка запуска CEO-claude: {e})"

def load_metrics():
    try: return json.load(open(METRICS,encoding="utf-8"))
    except Exception: return {"history":[]}

def d(cur,prev,key):
    a=cur.get(key); b=prev.get(key) if prev else None
    if a is None or b is None: return ""
    n=a-b
    return f" (Δ {'+' if n>=0 else ''}{n})"

def build_report(cur, prev, improved):
    def f(v): return "—" if v is None else str(v)
    avg7=cur.get("avg7")
    if avg7:
        pct=min(100,round(avg7/1000*100)); bar="█"*(pct//10)+"░"*(10-pct//10)
        prog=f"{bar} {pct}% ({avg7}/1000)"
    else: prog="копится статистика"
    L=[
      f"🏢 <b>JinnRadar · CEO-отчёт</b> · {cur['ts']}",
      f"🌐 {SITE}",
      "",
      "📊 <b>Метрики (Δ за час):</b>",
      f"• Визиты сегодня: <b>{f(cur.get('today'))}</b>{d(cur,prev,'today')}",
      f"• Всего визитов: <b>{f(cur.get('total'))}</b>{d(cur,prev,'total')}",
      f"• Среднее/день (7д): <b>{f(avg7)}</b> → KPI 1000",
      f"• Прогресс к KPI: {prog}",
      f"• Сайт: HTTP {cur.get('http')} · {cur.get('ms')} мс",
      f"• Контент: {cur.get('articles')} статей{d(cur,prev,'articles')}, {cur.get('langs')} языков{d(cur,prev,'langs')}",
      "",
      "🛠 <b>Что я как CEO улучшила за этот час:</b>",
      improved,
      "",
      "🔁 Следующий час — новая задача из бэклога. Работаю автономно.",
    ]
    return "\n".join(L)

def send_saved(text):
    sys.path.insert(0, TGDIR)
    from telethon.sync import TelegramClient
    c=json.load(open(os.path.join(TGDIR,"tg_creds.json"),encoding="utf-8"))
    cl=TelegramClient(os.path.join(TGDIR,"claudia_reader"),int(c["api_id"]),c["api_hash"])
    cl.connect()
    if not cl.is_user_authorized(): print("tg: not authorized"); return
    cl.send_message("me", text, parse_mode="html", link_preview=False)  # me = Избранное
    print("отчёт отправлен в Избранное")
    cl.disconnect()

def main():
    no_improve="--no-improve" in sys.argv
    no_send="--no-send" in sys.argv
    # защита от наложения запусков
    if os.path.exists(LOCK):
        try:
            age=time.time()-os.path.getmtime(LOCK)
            if age < CLAUDE_TIMEOUT+300:
                print("другой CEO-прогон ещё идёт, пропускаю"); return
        except Exception: pass
    open(LOCK,"w").write(str(time.time()))
    try:
        data=load_metrics()
        prev=data["history"][-1] if data["history"] else None
        improved = "(шаг улучшения пропущен)" if no_improve else run_ceo()
        cur=snapshot()               # метрики ПОСЛЕ улучшения
        cur["improved"]=improved
        data["history"].append(cur); data["history"]=data["history"][-500:]
        json.dump(data, open(METRICS,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
        report=build_report(cur, prev, improved)
        try: print(report)
        except Exception: pass
        if not no_send:
            try: send_saved(report)
            except Exception as e: print("tg fail:", e)
    finally:
        try: os.remove(LOCK)
        except Exception: pass

if __name__=="__main__":
    main()
