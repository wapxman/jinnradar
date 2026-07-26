# -*- coding: utf-8 -*-
"""
Генератор мультиязычных лендингов jinnradar.com — по одной странице на язык (/l/<code>.html).
Каждая страница: локализованные title/description/H1/интро/CTA, hreflang-alternate на все языки
(+ x-default), JSON-LD, beacon посещения. Плюс языковой хаб /l/ и полный sitemap.xml.

Запуск: python build_langs.py
После — git push (Vercel задеплоит) и IndexNow-пинг.
"""
import os
import json
import html as _html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://jinnradar.com/"
ANON = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3em1jaWh3dHdnamFqampzYm1zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU0OTQ0MzksImV4cCI6MjA5MTA3MDQzOX0."
        "X4UnLTta5Pm70sOwZkwJgvA8EkQtJPDmsn-2dMlkqjA")

# code: (endonym, dir, title, desc, h1, p1, p2, cta)
LANGS = {
"en": ("English","ltr","Jinn Radar — see how many jinn are near you online","Online jinn radar: it uses your GPS to show the jinn around you like a sonar, with a live world counter. A fun project based on Islamic lore.","Jinn Radar — who's near you right now?","JinnRadar is an online radar that uses your location to show the jinn around you like a submarine sonar — with a sweep, sound and a live world population counter.","It's an entertainment project inspired by Islamic lore. Open it on your phone and see how many jinn are near you right now.","📡 Open the radar"),
"es": ("Español","ltr","Radar de Yinn — cuántos yinn hay cerca de ti online","Radar de yinn online: usa tu GPS para mostrar los yinn a tu alrededor como un sonar, con un contador mundial en vivo. Proyecto de entretenimiento sobre el folclore islámico.","Radar de Yinn — ¿quién está cerca de ti ahora?","JinnRadar es un radar online que usa tu ubicación para mostrar los yinn a tu alrededor como el sonar de un submarino: con barrido, sonido y un contador mundial en vivo.","Es un proyecto de entretenimiento inspirado en el folclore islámico. Ábrelo en tu teléfono y mira cuántos yinn hay cerca de ti ahora.","📡 Abrir el radar"),
"pt": ("Português","ltr","Radar de Gênios (Jinn) — quantos estão perto de você","Radar de jinn online: usa o seu GPS para mostrar os jinn ao seu redor como um sonar, com um contador mundial ao vivo. Projeto de entretenimento sobre o folclore islâmico.","Radar de Jinn — quem está perto de você agora?","O JinnRadar é um radar online que usa a sua localização para mostrar os jinn ao seu redor como o sonar de um submarino — com varredura, som e um contador mundial ao vivo.","É um projeto de entretenimento inspirado no folclore islâmico. Abra no seu telefone e veja quantos jinn estão perto de você agora.","📡 Abrir o radar"),
"fr": ("Français","ltr","Radar à Djinns — combien de djinns sont près de vous","Radar à djinns en ligne : il utilise votre GPS pour afficher les djinns autour de vous comme un sonar, avec un compteur mondial en direct. Projet ludique sur le folklore islamique.","Radar à Djinns — qui est près de vous maintenant ?","JinnRadar est un radar en ligne qui utilise votre position pour afficher les djinns autour de vous comme le sonar d'un sous-marin — avec balayage, son et un compteur mondial en direct.","C'est un projet de divertissement inspiré du folklore islamique. Ouvrez-le sur votre téléphone et voyez combien de djinns sont près de vous.","📡 Ouvrir le radar"),
"de": ("Deutsch","ltr","Dschinn-Radar — wie viele Dschinn sind in deiner Nähe","Online-Dschinn-Radar: Es nutzt dein GPS, um die Dschinn um dich herum wie ein Sonar anzuzeigen, mit einem Live-Weltzähler. Ein Spaßprojekt zur islamischen Überlieferung.","Dschinn-Radar — wer ist gerade in deiner Nähe?","JinnRadar ist ein Online-Radar, das deinen Standort nutzt, um die Dschinn um dich herum wie das Sonar eines U-Boots anzuzeigen — mit Sweep, Ton und einem Live-Weltzähler.","Es ist ein Unterhaltungsprojekt, inspiriert von der islamischen Überlieferung. Öffne es auf dem Handy und sieh, wie viele Dschinn in deiner Nähe sind.","📡 Radar öffnen"),
"it": ("Italiano","ltr","Radar dei Jinn — quanti jinn ci sono vicino a te","Radar dei jinn online: usa il tuo GPS per mostrare i jinn intorno a te come un sonar, con un contatore mondiale in tempo reale. Progetto di intrattenimento sul folclore islamico.","Radar dei Jinn — chi c'è vicino a te adesso?","JinnRadar è un radar online che usa la tua posizione per mostrare i jinn intorno a te come il sonar di un sottomarino — con scansione, suono e un contatore mondiale live.","È un progetto di intrattenimento ispirato al folclore islamico. Aprilo sul telefono e guarda quanti jinn ci sono vicino a te ora.","📡 Apri il radar"),
"nl": ("Nederlands","ltr","Djinn-radar — hoeveel djinn zijn er bij jou in de buurt","Online djinn-radar: gebruikt je GPS om de djinn om je heen te tonen als een sonar, met een live wereldteller. Een vermaakproject over islamitische folklore.","Djinn-radar — wie is er nu bij jou in de buurt?","JinnRadar is een online radar die je locatie gebruikt om de djinn om je heen te tonen als de sonar van een onderzeeër — met sweep, geluid en een live wereldteller.","Het is een vermaakproject geïnspireerd op islamitische folklore. Open het op je telefoon en zie hoeveel djinn er bij je in de buurt zijn.","📡 Open de radar"),
"ru": ("Русский","ltr","Радар джиннов — сколько джиннов рядом с тобой онлайн","Онлайн-радар джиннов: по GPS показывает джиннов вокруг тебя как сонар, с живым мировым счётчиком. Развлекательный проект по мотивам исламских преданий.","Радар джиннов — кто рядом с тобой прямо сейчас?","JinnRadar — онлайн-радар, который по твоей геолокации показывает джиннов вокруг тебя как сонар подлодки: со свипом, звуком и живым счётчиком мировой популяции.","Это развлекательный проект по мотивам исламских преданий. Открой на телефоне и посмотри, сколько джиннов рядом с тобой прямо сейчас.","📡 Открыть радар"),
"uk": ("Українська","ltr","Радар джинів — скільки джинів поруч із тобою онлайн","Онлайн-радар джинів: за GPS показує джинів навколо тебе як сонар, із живим світовим лічильником. Розважальний проєкт за мотивами ісламських переказів.","Радар джинів — хто поруч із тобою зараз?","JinnRadar — онлайн-радар, що за твоєю геолокацією показує джинів навколо тебе як сонар підводного човна: зі свіпом, звуком і живим світовим лічильником.","Це розважальний проєкт за мотивами ісламських переказів. Відкрий на телефоні й подивись, скільки джинів поруч із тобою зараз.","📡 Відкрити радар"),
"pl": ("Polski","ltr","Radar dżinnów — ile dżinnów jest w pobliżu ciebie online","Radar dżinnów online: używa GPS, by pokazać dżinny wokół ciebie jak sonar, z żywym światowym licznikiem. Rozrywkowy projekt o islamskim folklorze.","Radar dżinnów — kto jest teraz w pobliżu ciebie?","JinnRadar to radar online, który wykorzystuje twoją lokalizację, by pokazać dżinny wokół ciebie jak sonar okrętu podwodnego — z omiataniem, dźwiękiem i żywym licznikiem.","To projekt rozrywkowy inspirowany islamskim folklorem. Otwórz na telefonie i zobacz, ile dżinnów jest w pobliżu ciebie.","📡 Otwórz radar"),
"ro": ("Română","ltr","Radar de djinni — câți djinni sunt lângă tine online","Radar de djinni online: folosește GPS-ul pentru a arăta djinnii din jurul tău ca un sonar, cu un contor mondial live. Proiect de divertisment despre folclorul islamic.","Radar de djinni — cine e lângă tine acum?","JinnRadar este un radar online care folosește locația ta pentru a arăta djinnii din jurul tău ca sonarul unui submarin — cu baleiaj, sunet și un contor mondial live.","Este un proiect de divertisment inspirat din folclorul islamic. Deschide-l pe telefon și vezi câți djinni sunt lângă tine acum.","📡 Deschide radarul"),
"tr": ("Türkçe","ltr","Cin Radarı — yakınında kaç cin var, çevrimiçi öğren","Çevrimiçi cin radarı: GPS'ini kullanarak çevrendeki cinleri bir sonar gibi gösterir, canlı dünya sayacıyla. İslami folklordan esinlenen eğlence projesi.","Cin Radarı — şu anda yakınında kim var?","JinnRadar, konumunu kullanarak çevrendeki cinleri bir denizaltı sonarı gibi gösteren çevrimiçi bir radardır — tarama, ses ve canlı dünya sayacıyla.","İslami folklordan esinlenen bir eğlence projesidir. Telefonunda aç ve şu anda yakınında kaç cin olduğunu gör.","📡 Radarı aç"),
"ar": ("العربية","rtl","رادار الجن — كم جنيًا حولك الآن عبر الإنترنت","رادار الجن أونلاين: يستخدم موقعك لعرض الجن من حولك مثل السونار، مع عدّاد عالمي مباشر. مشروع ترفيهي مستوحى من التراث الإسلامي.","رادار الجن — من حولك الآن؟","جِنّ رادار هو رادار على الإنترنت يستخدم موقعك لعرض الجن من حولك مثل سونار الغواصة — مع مسح وصوت وعدّاد عالمي مباشر.","إنه مشروع ترفيهي مستوحى من التراث الإسلامي. افتحه على هاتفك وشاهد كم جنيًا حولك الآن.","📡 افتح الرادار"),
"fa": ("فارسی","rtl","رادار جن — چند جن نزدیک شما هستند، آنلاین","رادار جن آنلاین: با GPS شما جن‌های اطرافتان را مانند سونار نشان می‌دهد، با شمارنده زنده جهانی. پروژه‌ای سرگرم‌کننده بر پایه باورهای اسلامی.","رادار جن — چه کسی الان نزدیک شماست؟","جِن رادار یک رادار آنلاین است که با موقعیت مکانی شما جن‌های اطرافتان را مانند سونار زیردریایی نشان می‌دهد — با جاروب، صدا و شمارنده زنده جهانی.","این یک پروژه سرگرمی الهام‌گرفته از باورهای اسلامی است. آن را روی گوشی باز کنید و ببینید چند جن الان نزدیک شماست.","📡 باز کردن رادار"),
"ur": ("اردو","rtl","جن ریڈار — آپ کے قریب کتنے جن ہیں، آن لائن","آن لائن جن ریڈار: آپ کے GPS سے آپ کے ارد گرد جنات کو سونار کی طرح دکھاتا ہے، لائیو عالمی کاؤنٹر کے ساتھ۔ اسلامی روایات پر مبنی تفریحی منصوبہ۔","جن ریڈار — اس وقت آپ کے قریب کون ہے؟","جن ریڈار ایک آن لائن ریڈار ہے جو آپ کے مقام سے آپ کے ارد گرد جنات کو آبدوز کے سونار کی طرح دکھاتا ہے — سویپ، آواز اور لائیو عالمی کاؤنٹر کے ساتھ۔","یہ اسلامی روایات سے متاثر ایک تفریحی منصوبہ ہے۔ اسے اپنے فون پر کھولیں اور دیکھیں کہ اس وقت آپ کے قریب کتنے جن ہیں۔","📡 ریڈار کھولیں"),
"he": ("עברית","rtl","רדאר שדים (ג'ין) — כמה ג'ין נמצאים לידך אונליין","רדאר ג'ין אונליין: משתמש ב-GPS כדי להציג את הג'ין סביבך כמו סונאר, עם מונה עולמי חי. פרויקט בידור בהשראת הפולקלור האסלאמי.","רדאר ג'ין — מי נמצא לידך עכשיו?","JinnRadar הוא רדאר מקוון שמשתמש במיקום שלך כדי להציג את הג'ין סביבך כמו סונאר של צוללת — עם סריקה, צליל ומונה עולמי חי.","זהו פרויקט בידור בהשראת הפולקלור האסלאמי. פתחו בטלפון וראו כמה ג'ין נמצאים לידכם עכשיו.","📡 פתחו את הרדאר"),
"hi": ("हिन्दी","ltr","जिन्न रडार — आपके पास कितने जिन्न हैं, ऑनलाइन देखें","ऑनलाइन जिन्न रडार: आपके GPS से आपके आसपास के जिन्न को सोनार की तरह दिखाता है, लाइव विश्व काउंटर के साथ। इस्लामी लोककथाओं पर आधारित मनोरंजन परियोजना।","जिन्न रडार — अभी आपके पास कौन है?","JinnRadar एक ऑनलाइन रडार है जो आपके स्थान से आपके आसपास के जिन्न को पनडुब्बी के सोनार की तरह दिखाता है — स्वीप, ध्वनि और लाइव विश्व काउंटर के साथ।","यह इस्लामी लोककथाओं से प्रेरित एक मनोरंजन परियोजना है। इसे फ़ोन पर खोलें और देखें कि अभी आपके पास कितने जिन्न हैं।","📡 रडार खोलें"),
"bn": ("বাংলা","ltr","জিন রাডার — আপনার কাছে কতজন জিন আছে, অনলাইনে দেখুন","অনলাইন জিন রাডার: আপনার GPS দিয়ে আপনার চারপাশের জিনদের সোনারের মতো দেখায়, লাইভ বিশ্ব কাউন্টার সহ। ইসলামি লোককথা অবলম্বনে বিনোদনমূলক প্রকল্প।","জিন রাডার — এখন আপনার কাছে কে আছে?","JinnRadar একটি অনলাইন রাডার যা আপনার অবস্থান দিয়ে আপনার চারপাশের জিনদের সাবমেরিনের সোনারের মতো দেখায় — সুইপ, শব্দ ও লাইভ বিশ্ব কাউন্টার সহ।","এটি ইসলামি লোককথা অনুপ্রাণিত একটি বিনোদনমূলক প্রকল্প। ফোনে খুলুন এবং দেখুন এখন আপনার কাছে কতজন জিন আছে।","📡 রাডার খুলুন"),
"id": ("Bahasa Indonesia","ltr","Radar Jin — berapa banyak jin di dekatmu secara online","Radar jin online: memakai GPS untuk menampilkan jin di sekitarmu seperti sonar, dengan penghitung dunia langsung. Proyek hiburan berdasarkan cerita rakyat Islam.","Radar Jin — siapa yang ada di dekatmu sekarang?","JinnRadar adalah radar online yang memakai lokasimu untuk menampilkan jin di sekitarmu seperti sonar kapal selam — dengan sapuan, suara, dan penghitung dunia langsung.","Ini proyek hiburan yang terinspirasi cerita rakyat Islam. Buka di ponselmu dan lihat berapa banyak jin di dekatmu sekarang.","📡 Buka radar"),
"ms": ("Bahasa Melayu","ltr","Radar Jin — berapa banyak jin berdekatan dengan anda","Radar jin dalam talian: menggunakan GPS untuk memaparkan jin di sekeliling anda seperti sonar, dengan pembilang dunia langsung. Projek hiburan berdasarkan cerita rakyat Islam.","Radar Jin — siapa berdekatan dengan anda sekarang?","JinnRadar ialah radar dalam talian yang menggunakan lokasi anda untuk memaparkan jin di sekeliling anda seperti sonar kapal selam — dengan imbasan, bunyi dan pembilang dunia langsung.","Ini projek hiburan yang diilhamkan daripada cerita rakyat Islam. Buka pada telefon anda dan lihat berapa banyak jin berdekatan dengan anda sekarang.","📡 Buka radar"),
"zh-Hans": ("简体中文","ltr","镇尼雷达（Jinn）——看看你附近有多少镇尼","在线镇尼雷达：用你的 GPS 像声呐一样显示你周围的镇尼，并有实时全球计数器。基于伊斯兰传说的娱乐项目。","镇尼雷达——现在谁在你附近？","JinnRadar 是一个在线雷达，利用你的位置像潜艇声呐一样显示你周围的镇尼——带有扫描、声音和实时全球计数器。","这是一个受伊斯兰传说启发的娱乐项目。在手机上打开，看看现在你附近有多少镇尼。","📡 打开雷达"),
"zh-Hant": ("繁體中文","ltr","鎮尼雷達（Jinn）——看看你附近有多少鎮尼","線上鎮尼雷達：用你的 GPS 像聲納一樣顯示你周圍的鎮尼，並有即時全球計數器。基於伊斯蘭傳說的娛樂專案。","鎮尼雷達——現在誰在你附近？","JinnRadar 是一個線上雷達，利用你的位置像潛艇聲納一樣顯示你周圍的鎮尼——帶有掃描、聲音和即時全球計數器。","這是一個受伊斯蘭傳說啟發的娛樂專案。在手機上打開，看看現在你附近有多少鎮尼。","📡 開啟雷達"),
"ja": ("日本語","ltr","ジン・レーダー — あなたの近くに何体のジンがいるか","オンラインのジン・レーダー：GPSを使い、あなたの周りのジンをソナーのように表示します。ライブの世界カウンター付き。イスラムの伝承にもとづく娯楽プロジェクト。","ジン・レーダー — いまあなたの近くにいるのは？","JinnRadarは、あなたの位置情報を使って周囲のジンを潜水艦のソナーのように表示するオンラインレーダーです。スイープ、音、ライブの世界人口カウンター付き。","イスラムの伝承に着想を得た娯楽プロジェクトです。スマホで開いて、いまあなたの近くに何体のジンがいるか見てみましょう。","📡 レーダーを開く"),
"ko": ("한국어","ltr","진 레이더 — 내 근처에 진이 몇이나 있는지 온라인으로","온라인 진 레이더: GPS로 주변의 진을 소나처럼 보여주고 실시간 세계 카운터를 제공합니다. 이슬람 전승을 바탕으로 한 오락 프로젝트.","진 레이더 — 지금 내 근처에는 누가?","JinnRadar는 당신의 위치를 이용해 주변의 진을 잠수함 소나처럼 보여주는 온라인 레이더입니다. 스윕, 소리, 실시간 세계 인구 카운터가 있습니다.","이슬람 전승에서 영감을 받은 오락 프로젝트입니다. 휴대폰에서 열고 지금 내 근처에 진이 몇이나 있는지 확인해 보세요.","📡 레이더 열기"),
"vi": ("Tiếng Việt","ltr","Radar Thần Đèn (Jinn) — có bao nhiêu jinn gần bạn","Radar jinn trực tuyến: dùng GPS để hiển thị jinn quanh bạn như một sonar, kèm bộ đếm thế giới trực tiếp. Dự án giải trí dựa trên truyền thuyết Hồi giáo.","Radar Jinn — ai đang ở gần bạn ngay bây giờ?","JinnRadar là radar trực tuyến dùng vị trí của bạn để hiển thị jinn quanh bạn như sonar tàu ngầm — với quét, âm thanh và bộ đếm thế giới trực tiếp.","Đây là dự án giải trí lấy cảm hứng từ truyền thuyết Hồi giáo. Mở trên điện thoại và xem có bao nhiêu jinn gần bạn ngay bây giờ.","📡 Mở radar"),
"th": ("ไทย","ltr","เรดาร์ญิน (Jinn) — มีญินอยู่ใกล้คุณกี่ตนแบบออนไลน์","เรดาร์ญินออนไลน์: ใช้ GPS แสดงญินรอบตัวคุณเหมือนโซนาร์ พร้อมตัวนับทั่วโลกแบบเรียลไทม์ โปรเจกต์เพื่อความบันเทิงจากตำนานอิสลาม","เรดาร์ญิน — ตอนนี้ใครอยู่ใกล้คุณ?","JinnRadar คือเรดาร์ออนไลน์ที่ใช้ตำแหน่งของคุณแสดงญินรอบตัวคุณเหมือนโซนาร์เรือดำน้ำ พร้อมการกวาด เสียง และตัวนับประชากรโลกแบบเรียลไทม์","เป็นโปรเจกต์เพื่อความบันเทิงที่ได้แรงบันดาลใจจากตำนานอิสลาม เปิดบนมือถือแล้วดูว่าตอนนี้มีญินอยู่ใกล้คุณกี่ตน","📡 เปิดเรดาร์"),
"fil": ("Filipino","ltr","Jinn Radar — ilang jinn ang malapit sa iyo online","Online na jinn radar: ginagamit ang GPS mo para ipakita ang mga jinn sa paligid mo na parang sonar, may live na world counter. Proyektong panlibang batay sa alamat Islamiko.","Jinn Radar — sino ang malapit sa iyo ngayon?","Ang JinnRadar ay online radar na gumagamit ng lokasyon mo para ipakita ang mga jinn sa paligid mo na parang sonar ng submarino — may sweep, tunog at live na world counter.","Isa itong proyektong panlibang na hango sa alamat Islamiko. Buksan sa telepono mo at tingnan kung ilang jinn ang malapit sa iyo ngayon.","📡 Buksan ang radar"),
"sw": ("Kiswahili","ltr","Rada ya Majini — majini wangapi wako karibu nawe mtandaoni","Rada ya majini mtandaoni: hutumia GPS kuonyesha majini walio karibu nawe kama sonar, ikiwa na kihesabu cha dunia moja kwa moja. Mradi wa burudani kutokana na hadithi za Kiislamu.","Rada ya Majini — nani yuko karibu nawe sasa?","JinnRadar ni rada ya mtandaoni inayotumia eneo lako kuonyesha majini walio karibu nawe kama sonar ya nyambizi — ikiwa na msukumo, sauti na kihesabu cha dunia moja kwa moja.","Ni mradi wa burudani ulioongozwa na hadithi za Kiislamu. Fungua kwenye simu yako uone majini wangapi wako karibu nawe sasa.","📡 Fungua rada"),
"ha": ("Hausa","ltr","Radar Aljannu — aljannu nawa ke kusa da kai a yanar gizo","Radar aljannu ta yanar gizo: tana amfani da GPS don nuna aljannu kewaye da kai kamar sonar, tare da ma'auni na duniya kai tsaye. Aikin nishaɗi bisa tatsuniyar Musulunci.","Radar Aljannu — wa ke kusa da kai yanzu?","JinnRadar radar ce ta yanar gizo da ke amfani da wurin ka don nuna aljannu kewaye da kai kamar sonar na jirgin ruwa — tare da share, sauti da ma'auni na duniya kai tsaye.","Aiki ne na nishaɗi wanda tatsuniyar Musulunci ta yi wahayi. Buɗe shi a wayarka ka gani aljannu nawa ke kusa da kai yanzu.","📡 Buɗe radar"),
"az": ("Azərbaycan","ltr","Cin Radarı — yaxınlığında neçə cin var, onlayn","Onlayn cin radarı: GPS-dən istifadə edərək ətrafındakı cinləri sonar kimi göstərir, canlı dünya sayğacı ilə. İslam folkloruna əsaslanan əyləncə layihəsi.","Cin Radarı — indi yaxınlığında kim var?","JinnRadar məkanından istifadə edərək ətrafındakı cinləri sualtı qayığın sonarı kimi göstərən onlayn radardır — tarama, səs və canlı dünya sayğacı ilə.","Bu, İslam folklorundan ilhamlanan əyləncə layihəsidir. Telefonunda aç və indi yaxınlığında neçə cin olduğunu gör.","📡 Radarı aç"),
"kk": ("Қазақша","ltr","Жын радары — қасыңда қанша жын бар, онлайн","Онлайн жын радары: GPS арқылы айналаңдағы жындарды сонар сияқты көрсетеді, тірі әлемдік санауышпен. Ислам аңыздары негізіндегі ойын-сауық жобасы.","Жын радары — қазір қасыңда кім бар?","JinnRadar — орналасуыңды пайдаланып айналаңдағы жындарды сүңгуір қайықтың сонары сияқты көрсететін онлайн радар: сканермен, дыбыспен және тірі әлемдік санауышпен.","Бұл ислам аңыздарынан шабыт алған ойын-сауық жобасы. Телефоннан ашып, қазір қасыңда қанша жын бар екенін көр.","📡 Радарды ашу"),
"ky": ("Кыргызча","ltr","Жин радары — жаныңда канча жин бар, онлайн","Онлайн жин радары: GPS аркылуу тегерегиңдеги жиндерди сонар сыяктуу көрсөтөт, тирүү дүйнөлүк эсептегич менен. Ислам уламыштарына негизделген көңүл ачуу долбоору.","Жин радары — азыр жаныңда ким бар?","JinnRadar — жайгашкан жериңди колдонуп тегерегиңдеги жиндерди суу астындагы кайыктын сонары сыяктуу көрсөткөн онлайн радар: сканер, үн жана тирүү дүйнөлүк эсептегич менен.","Бул ислам уламыштарынан шыктанган көңүл ачуу долбоору. Телефондон ачып, азыр жаныңда канча жин бар экенин көр.","📡 Радарды ачуу"),
"uz": ("Oʻzbekcha","ltr","Jin radari — yoningda nechta jin bor, onlayn","Onlayn jin radari: GPS orqali atrofingdagi jinlarni sonar kabi koʻrsatadi, jonli dunyo hisoblagichi bilan. Islom rivoyatlariga asoslangan koʻngilochar loyiha.","Jin radari — hozir yoningda kim bor?","JinnRadar — joylashuvingdan foydalanib atrofingdagi jinlarni suvosti kemasi sonari kabi koʻrsatadigan onlayn radar: skanerlash, ovoz va jonli dunyo hisoblagichi bilan.","Bu islom rivoyatlaridan ilhomlangan koʻngilochar loyiha. Telefoningda ochib, hozir yoningda nechta jin borligini koʻr.","📡 Radarni ochish"),
"tg": ("Тоҷикӣ","ltr","Радари ҷин — дар наздикии ту чанд ҷин ҳаст, онлайн","Радари ҷини онлайн: бо GPS ҷинҳои атрофи туро мисли сонар нишон медиҳад, бо ҳисобкунаки зиндаи ҷаҳонӣ. Лоиҳаи фароғатӣ дар асоси ривоятҳои исломӣ.","Радари ҷин — ҳозир дар наздикии ту кист?","JinnRadar радари онлайнест, ки бо ҷойгиршавии ту ҷинҳои атрофатро мисли сонари зериобӣ нишон медиҳад — бо сканкунӣ, садо ва ҳисобкунаки зиндаи ҷаҳонӣ.","Ин лоиҳаи фароғатист, ки аз ривоятҳои исломӣ илҳом гирифтааст. Дар телефон кушо ва бубин, ки ҳозир дар наздикии ту чанд ҷин ҳаст.","📡 Кушодани радар"),
"tk": ("Türkmençe","ltr","Jyn radary — ýanyňda näçe jyn bar, onlaýn","Onlaýn jyn radary: GPS arkaly töweregiňdäki jynlary sonar ýaly görkezýär, janly dünýä hasaplaýjy bilen. Yslam rowaýatlaryna esaslanýan güýmenje taslamasy.","Jyn radary — häzir ýanyňda kim bar?","JinnRadar ýerleşişiňi ulanyp töweregiňdäki jynlary suwasty gäminiň sonary ýaly görkezýän onlaýn radardyr — skanirleme, ses we janly dünýä hasaplaýjy bilen.","Bu yslam rowaýatlaryndan ylham alan güýmenje taslamasydyr. Telefonyňda aç we häzir ýanyňda näçe jyn barlygyny gör.","📡 Radary aç"),
"el": ("Ελληνικά","ltr","Ραντάρ Τζίνι — πόσα τζίνι είναι κοντά σου online","Διαδικτυακό ραντάρ τζίνι: χρησιμοποιεί το GPS σου για να δείξει τα τζίνι γύρω σου σαν σόναρ, με ζωντανό παγκόσμιο μετρητή. Ψυχαγωγικό έργο βασισμένο στην ισλαμική παράδοση.","Ραντάρ Τζίνι — ποιος είναι κοντά σου τώρα;","Το JinnRadar είναι ένα διαδικτυακό ραντάρ που χρησιμοποιεί την τοποθεσία σου για να δείξει τα τζίνι γύρω σου σαν σόναρ υποβρυχίου — με σάρωση, ήχο και ζωντανό παγκόσμιο μετρητή.","Είναι ένα ψυχαγωγικό έργο εμπνευσμένο από την ισλαμική παράδοση. Άνοιξέ το στο κινητό και δες πόσα τζίνι είναι κοντά σου τώρα.","📡 Άνοιξε το ραντάρ"),
"hu": ("Magyar","ltr","Dzsinn-radar — hány dzsinn van a közeledben, online","Online dzsinn-radar: a GPS-eddel szonárként mutatja a körülötted lévő dzsinneket, élő világszámlálóval. Szórakoztató projekt az iszlám folklór nyomán.","Dzsinn-radar — ki van most a közeledben?","A JinnRadar egy online radar, amely a helyzeted alapján tengeralattjáró-szonárként mutatja a körülötted lévő dzsinneket — pásztázással, hanggal és élő világszámlálóval.","Ez egy szórakoztató projekt az iszlám folklór ihlette. Nyisd meg telefonon, és nézd meg, hány dzsinn van most a közeledben.","📡 Radar megnyitása"),
"bg": ("Български","ltr","Радар за джинове — колко джина има около теб онлайн","Онлайн радар за джинове: използва GPS, за да покаже джиновете около теб като сонар, с жив световен брояч. Забавен проект по мотиви от ислямския фолклор.","Радар за джинове — кой е около теб сега?","JinnRadar е онлайн радар, който използва местоположението ти, за да покаже джиновете около теб като сонар на подводница — с обхождане, звук и жив световен брояч.","Това е забавен проект, вдъхновен от ислямския фолклор. Отвори го на телефона и виж колко джина има около теб сега.","📡 Отвори радара"),
"sr": ("Српски","ltr","Радар џина — колико је џина близу тебе онлајн","Онлајн радар џина: користи ГПС да прикаже џине око тебе као сонар, уз живи светски бројач. Забавни пројекат по мотивима исламског фолклора.","Радар џина — ко је сада близу тебе?","JinnRadar је онлајн радар који користи твоју локацију да прикаже џине око тебе као сонар подморнице — уз скенирање, звук и живи светски бројач.","То је забавни пројекат инспирисан исламским фолклором. Отвори га на телефону и погледај колико је џина сада близу тебе.","📡 Отвори радар"),
"hr": ("Hrvatski","ltr","Radar džina — koliko je džina blizu tebe online","Online radar džina: koristi GPS da prikaže džine oko tebe kao sonar, uz živi svjetski brojač. Zabavni projekt prema motivima islamskog folklora.","Radar džina — tko je sada blizu tebe?","JinnRadar je online radar koji koristi tvoju lokaciju da prikaže džine oko tebe kao sonar podmornice — uz skeniranje, zvuk i živi svjetski brojač.","To je zabavni projekt nadahnut islamskim folklorom. Otvori ga na telefonu i pogledaj koliko je džina sada blizu tebe.","📡 Otvori radar"),
"sq": ("Shqip","ltr","Radari i Xhinëve — sa xhinë janë pranë teje online","Radar xhinësh online: përdor GPS-in për të treguar xhinët rreth teje si një sonar, me numërues botëror të drejtpërdrejtë. Projekt argëtues bazuar në folklorin islamik.","Radari i Xhinëve — kush është pranë teje tani?","JinnRadar është një radar online që përdor vendndodhjen tënde për të treguar xhinët rreth teje si sonari i një nëndetëseje — me skanim, tingull dhe numërues botëror të drejtpërdrejtë.","Është një projekt argëtues i frymëzuar nga folklori islamik. Hape në telefon dhe shih sa xhinë janë pranë teje tani.","📡 Hap radarin"),
"ka": ("ქართული","ltr","ჯინების რადარი — რამდენი ჯინია შენს გვერდით ონლაინ","ონლაინ ჯინების რადარი: GPS-ით აჩვენებს შენ გარშემო ჯინებს სონარივით, ცოცხალი მსოფლიო მთვლელით. გასართობი პროექტი ისლამური ფოლკლორის მიხედვით.","ჯინების რადარი — ვინ არის ახლა შენს გვერდით?","JinnRadar არის ონლაინ რადარი, რომელიც შენს მდებარეობას იყენებს შენ გარშემო ჯინების საჩვენებლად წყალქვეშა ნავის სონარივით — სკანირებით, ხმით და ცოცხალი მსოფლიო მთვლელით.","ეს გასართობი პროექტია ისლამური ფოლკლორის შთაგონებით. გახსენი ტელეფონში და ნახე, რამდენი ჯინია ახლა შენს გვერდით.","📡 რადარის გახსნა"),
"hy": ("Հայերեն","ltr","Ջինների ռադար — քանի՞ ջին կա քո մոտ առցանց","Առցանց ջինների ռադար. GPS-ով ցույց է տալիս քո շուրջը ջիններին սոնարի պես՝ կենդանի համաշխարհային հաշվիչով։ Ժամանցային նախագիծ իսլամական բանահյուսության հիման վրա։","Ջինների ռադար — ո՞վ է հիմա քո մոտ","JinnRadar-ը առցանց ռադար է, որը քո տեղադրությամբ ցույց է տալիս քո շուրջը ջիններին սուզանավի սոնարի պես՝ սկանավորմամբ, ձայնով և կենդանի համաշխարհային հաշվիչով։","Սա ժամանցային նախագիծ է՝ ներշնչված իսլամական բանահյուսությունից։ Բացիր հեռախոսով և տես, թե քանի ջին կա հիմա քո մոտ։","📡 Բացել ռադարը"),
"cs": ("Čeština","ltr","Radar džinů — kolik džinů je poblíž tebe online","Online radar džinů: pomocí GPS zobrazuje džiny kolem tebe jako sonar, s živým světovým počítadlem. Zábavní projekt podle islámského folkloru.","Radar džinů — kdo je teď poblíž tebe?","JinnRadar je online radar, který pomocí tvé polohy zobrazuje džiny kolem tebe jako sonar ponorky — se skenováním, zvukem a živým světovým počítadlem.","Je to zábavní projekt inspirovaný islámským folklorem. Otevři ho v telefonu a podívej se, kolik džinů je teď poblíž tebe.","📡 Otevřít radar"),
"sv": ("Svenska","ltr","Djinn-radar — hur många djinner finns nära dig online","Djinn-radar online: använder din GPS för att visa djinnerna runt dig som en sonar, med en levande världsräknare. Ett underhållningsprojekt baserat på islamisk folklore.","Djinn-radar — vem är nära dig just nu?","JinnRadar är en onlineradar som använder din plats för att visa djinnerna runt dig som en ubåtssonar — med svep, ljud och en levande världsräknare.","Det är ett underhållningsprojekt inspirerat av islamisk folklore. Öppna det i telefonen och se hur många djinner som finns nära dig nu.","📡 Öppna radarn"),
"fi": ("Suomi","ltr","Djinni-tutka — montako djinniä on lähelläsi verkossa","Verkossa toimiva djinni-tutka: näyttää GPS:n avulla ympärilläsi olevat djinnit kuin kaikuluotain, mukana elävä maailmanlaskuri. Viihdeprojekti islamilaisen kansanperinteen pohjalta.","Djinni-tutka — kuka on nyt lähelläsi?","JinnRadar on verkkotutka, joka näyttää sijaintisi avulla ympärilläsi olevat djinnit kuin sukellusveneen kaikuluotain — pyyhkäisyllä, äänellä ja elävällä maailmanlaskurilla.","Se on islamilaisesta kansanperinteestä inspiroitunut viihdeprojekti. Avaa se puhelimella ja katso, montako djinniä on nyt lähelläsi.","📡 Avaa tutka"),
"da": ("Dansk","ltr","Djinn-radar — hvor mange djinner er der nær dig online","Online djinn-radar: bruger din GPS til at vise djinnerne omkring dig som en sonar, med en levende verdenstæller. Et underholdningsprojekt baseret på islamisk folklore.","Djinn-radar — hvem er nær dig lige nu?","JinnRadar er en online radar, der bruger din placering til at vise djinnerne omkring dig som en ubådssonar — med sweep, lyd og en levende verdenstæller.","Det er et underholdningsprojekt inspireret af islamisk folklore. Åbn det på telefonen og se, hvor mange djinner der er nær dig nu.","📡 Åbn radaren"),
"no": ("Norsk","ltr","Djinn-radar — hvor mange djinner er nær deg på nett","Djinn-radar på nett: bruker GPS-en din til å vise djinnene rundt deg som en sonar, med en levende verdensteller. Et underholdningsprosjekt basert på islamsk folklore.","Djinn-radar — hvem er nær deg akkurat nå?","JinnRadar er en nettradar som bruker posisjonen din til å vise djinnene rundt deg som en ubåtsonar — med sveip, lyd og en levende verdensteller.","Det er et underholdningsprosjekt inspirert av islamsk folklore. Åpne det på telefonen og se hvor mange djinner som er nær deg nå.","📡 Åpne radaren"),
"ps": ("پښتو","rtl","د پیریانو راډار — ستا نږدې څومره پیریان دي، آنلاین","آنلاین د پیریانو راډار: ستا GPS په کارولو سره ستا شاوخوا پیریان لکه سونار ښیي، د ژوندي نړیوال شمېرونکي سره. د اسلامي روایتونو پر بنسټ ساتیري پروژه.","د پیریانو راډار — اوس ستا نږدې څوک دي؟","JinnRadar یو آنلاین راډار دی چې ستا موقعیت په کارولو سره ستا شاوخوا پیریان د سب مرین د سونار په څیر ښیي — د سکن، غږ او ژوندي نړیوال شمېرونکي سره.","دا د اسلامي روایتونو څخه الهام اخیستې ساتیري پروژه ده. په خپل ټیلیفون یې پرانیزئ او وګورئ چې اوس ستاسو نږدې څومره پیریان دي.","📡 راډار پرانیزئ"),
"ku": ("Kurdî","ltr","Radara Cinan — çend cin li nêzîkî te ne, serhêl","Radara cinan a serhêl: bi GPSa te cinên li dora te wek sonarê nîşan dide, bi hejmêra cîhanî ya zindî. Projeyeke şahiyê li ser bingeha folklora îslamî.","Radara Cinan — niha kî li nêzîkî te ye?","JinnRadar radareke serhêl e ku bi cihê te cinên li dora te wek sonara keştiya binê avê nîşan dide — bi şopandin, deng û hejmêrek cîhanî ya zindî.","Ev projeyeke şahiyê ye ku ji folklora îslamî îlham girtiye. Li ser telefona xwe veke û bibîne ka niha çend cin li nêzîkî te ne.","📡 Radarê veke"),
"bs": ("Bosanski","ltr","Radar džina — koliko je džina blizu tebe online","Online radar džina: koristi GPS da prikaže džine oko tebe kao sonar, uz živi svjetski brojač. Zabavni projekt prema motivima islamskog folklora.","Radar džina — ko je sada blizu tebe?","JinnRadar je online radar koji koristi tvoju lokaciju da prikaže džine oko tebe kao sonar podmornice — uz skeniranje, zvuk i živi svjetski brojač.","To je zabavni projekt inspirisan islamskim folklorom. Otvori ga na telefonu i pogledaj koliko je džina sada blizu tebe.","📡 Otvori radar"),
"mk": ("Македонски","ltr","Радар за џинови — колку џинови има околу тебе онлајн","Онлајн радар за џинови: со GPS ги прикажува џиновите околу тебе како сонар, со жив светски бројач. Забавен проект по мотиви од исламскиот фолклор.","Радар за џинови — кој е сега околу тебе?","JinnRadar е онлајн радар што ја користи твојата локација за да ги прикаже џиновите околу тебе како сонар на подморница — со скенирање, звук и жив светски бројач.","Тоа е забавен проект инспириран од исламскиот фолклор. Отвори го на телефон и види колку џинови има сега околу тебе.","📡 Отвори го радарот"),
"sk": ("Slovenčina","ltr","Radar džinov — koľko džinov je blízko teba online","Online radar džinov: pomocou GPS zobrazuje džinov okolo teba ako sonar, so živým svetovým počítadlom. Zábavný projekt podľa islamského folklóru.","Radar džinov — kto je teraz blízko teba?","JinnRadar je online radar, ktorý pomocou tvojej polohy zobrazuje džinov okolo teba ako sonar ponorky — so skenovaním, zvukom a živým svetovým počítadlom.","Je to zábavný projekt inšpirovaný islamským folklórom. Otvor ho v telefóne a pozri sa, koľko džinov je teraz blízko teba.","📡 Otvoriť radar"),
"sl": ("Slovenščina","ltr","Radar džinov — koliko džinov je blizu tebe na spletu","Spletni radar džinov: z GPS-om prikaže džine okoli tebe kot sonar, z živim svetovnim števcem. Zabavni projekt po motivih islamskega ljudskega izročila.","Radar džinov — kdo je zdaj blizu tebe?","JinnRadar je spletni radar, ki s tvojo lokacijo prikaže džine okoli tebe kot sonar podmornice — s skeniranjem, zvokom in živim svetovnim števcem.","To je zabavni projekt, navdihnjen z islamskim ljudskim izročilom. Odpri ga na telefonu in poglej, koliko džinov je zdaj blizu tebe.","📡 Odpri radar"),
"lt": ("Lietuvių","ltr","Džinų radaras — kiek džinų yra šalia tavęs internetu","Internetinis džinų radaras: naudodamas GPS rodo džinus aplink tave kaip sonaras, su gyvu pasaulio skaitikliu. Pramoginis projektas pagal islamo folklorą.","Džinų radaras — kas dabar yra šalia tavęs?","JinnRadar yra internetinis radaras, kuris pagal tavo vietą rodo džinus aplink tave kaip povandeninio laivo sonaras — su skenavimu, garsu ir gyvu pasaulio skaitikliu.","Tai pramoginis projektas, įkvėptas islamo folkloro. Atsidaryk jį telefone ir pažiūrėk, kiek džinų dabar yra šalia tavęs.","📡 Atverti radarą"),
"lv": ("Latviešu","ltr","Džinu radars — cik džinu ir tev tuvumā tiešsaistē","Tiešsaistes džinu radars: izmantojot GPS, rāda džinus tev apkārt kā sonārs, ar dzīvu pasaules skaitītāju. Izklaides projekts pēc islāma folkloras motīviem.","Džinu radars — kas tagad ir tev tuvumā?","JinnRadar ir tiešsaistes radars, kas pēc tavas atrašanās vietas rāda džinus tev apkārt kā zemūdenes sonārs — ar skenēšanu, skaņu un dzīvu pasaules skaitītāju.","Tas ir izklaides projekts, iedvesmots no islāma folkloras. Atver to telefonā un paskaties, cik džinu tagad ir tev tuvumā.","📡 Atvērt radaru"),
"et": ("Eesti","ltr","Džinniradar — mitu džinni on sinu lähedal internetis","Veebipõhine džinniradar: kasutab GPS-i, et näidata sinu ümber olevaid džinne nagu sonar, elava maailmaloenduriga. Meelelahutusprojekt islami folkloori ainetel.","Džinniradar — kes on praegu sinu lähedal?","JinnRadar on veebiradar, mis kasutab sinu asukohta, et näidata sinu ümber olevaid džinne nagu allveelaeva sonar — pühkimise, heli ja elava maailmaloenduriga.","See on islami folkloorist inspireeritud meelelahutusprojekt. Ava see telefonis ja vaata, mitu džinni on praegu sinu lähedal.","📡 Ava radar"),
"af": ("Afrikaans","ltr","Djinn-radar — hoeveel djinns is naby jou aanlyn","Aanlyn djinn-radar: gebruik jou GPS om die djinns rondom jou soos 'n sonar te wys, met 'n lewende wêreldteller. 'n Vermaakprojek gebaseer op Islamitiese folklore.","Djinn-radar — wie is nou naby jou?","JinnRadar is 'n aanlyn radar wat jou ligging gebruik om die djinns rondom jou soos 'n duikboot se sonar te wys — met 'n veeg, klank en 'n lewende wêreldteller.","Dit is 'n vermaakprojek geïnspireer deur Islamitiese folklore. Maak dit op jou foon oop en sien hoeveel djinns nou naby jou is.","📡 Maak die radar oop"),
"ne": ("नेपाली","ltr","जिन रडार — तपाईंको नजिक कति जिन छन्, अनलाइन","अनलाइन जिन रडार: तपाईंको GPS प्रयोग गरेर तपाईं वरपरका जिनहरूलाई सोनारझैं देखाउँछ, प्रत्यक्ष विश्व काउन्टरसहित। इस्लामी लोककथामा आधारित मनोरञ्जन परियोजना।","जिन रडार — अहिले तपाईंको नजिक को छ?","JinnRadar एउटा अनलाइन रडार हो जसले तपाईंको स्थान प्रयोग गरेर तपाईं वरपरका जिनहरूलाई पनडुब्बीको सोनारझैं देखाउँछ — स्विप, ध्वनि र प्रत्यक्ष विश्व काउन्टरसहित।","यो इस्लामी लोककथाबाट प्रेरित मनोरञ्जन परियोजना हो। यसलाई आफ्नो फोनमा खोल्नुहोस् र हेर्नुहोस् अहिले तपाईंको नजिक कति जिन छन्।","📡 रडार खोल्नुहोस्"),
"si": ("සිංහල","ltr","ජින් රේඩාර් — ඔබ අසල ජින් කී දෙනෙක් සිටිද, ඔන්ලයින්","ඔන්ලයින් ජින් රේඩාරය: ඔබේ GPS භාවිතයෙන් ඔබ වටා සිටින ජින්වරු සෝනාර් එකක් සේ පෙන්වයි, සජීවී ලෝක ගණකයක් සමඟ. ඉස්ලාමීය ජනකතා පදනම් කරගත් විනෝද ව්‍යාපෘතියකි.","ජින් රේඩාර් — දැන් ඔබ අසල සිටින්නේ කවුද?","JinnRadar යනු ඔබේ පිහිටීම භාවිතයෙන් ඔබ වටා සිටින ජින්වරු සබ්මැරීනයක සෝනාරයක් සේ පෙන්වන ඔන්ලයින් රේඩාරයකි — ස්කෑන් කිරීම, ශබ්දය සහ සජීවී ලෝක ගණකයක් සමඟ.","මෙය ඉස්ලාමීය ජනකතාවලින් ආභාසය ලැබූ විනෝද ව්‍යාපෘතියකි. එය ඔබේ දුරකථනයෙන් විවෘත කර දැන් ඔබ අසල ජින් කී දෙනෙක් සිටිද බලන්න.","📡 රේඩාරය විවෘත කරන්න"),
"my": ("မြန်မာ","ltr","ဂျင်ရေဒါ — သင့်အနီးတွင် ဂျင်ဘယ်နှစ်ကောင်ရှိသလဲ၊ အွန်လိုင်း","အွန်လိုင်း ဂျင်ရေဒါ — သင့် GPS ကိုသုံး၍ သင့်ပတ်ဝန်းကျင်ရှိ ဂျင်များကို ဆိုနာကဲ့သို့ ပြသည်၊ တိုက်ရိုက်ကမ္ဘာ့ရေတွက်ကိရိယာနှင့်အတူ။ အစ္စလာမ့်ဒဏ္ဍာရီအခြေခံ ဖျော်ဖြေရေးစီမံကိန်း။","ဂျင်ရေဒါ — ယခု သင့်အနီးတွင် ဘယ်သူရှိသလဲ?","JinnRadar သည် သင့်တည်နေရာကိုသုံး၍ သင့်ပတ်ဝန်းကျင်ရှိ ဂျင်များကို ရေငုပ်သင်္ဘော၏ ဆိုနာကဲ့သို့ ပြသည့် အွန်လိုင်းရေဒါဖြစ်သည် — စကင်ဖတ်ခြင်း၊ အသံနှင့် တိုက်ရိုက်ကမ္ဘာ့ရေတွက်ကိရိယာနှင့်အတူ။","ဤသည်မှာ အစ္စလာမ့်ဒဏ္ဍာရီမှ လှုံ့ဆော်မှုရသော ဖျော်ဖြေရေးစီမံကိန်းဖြစ်သည်။ ဖုန်းတွင်ဖွင့်၍ ယခု သင့်အနီးတွင် ဂျင်ဘယ်နှစ်ကောင်ရှိသည်ကို ကြည့်ပါ။","📡 ရေဒါဖွင့်ရန်"),
"km": ("ខ្មែរ","ltr","រ៉ាដាជិន — មានជិនប៉ុន្មាននៅជិតអ្នក អនឡាញ","រ៉ាដាជិនអនឡាញ៖ ប្រើ GPS របស់អ្នកដើម្បីបង្ហាញជិននៅជុំវិញអ្នកដូចសូណា ជាមួយឧបករណ៍រាប់ពិភពលោកបន្តផ្ទាល់។ គម្រោងកម្សាន្តផ្អែកលើរឿងព្រេងឥស្លាម។","រ៉ាដាជិន — តើអ្នកណានៅជិតអ្នកឥឡូវនេះ?","JinnRadar គឺជារ៉ាដាអនឡាញដែលប្រើទីតាំងរបស់អ្នកដើម្បីបង្ហាញជិននៅជុំវិញអ្នកដូចសូណានៃនាវាមុជទឹក — ជាមួយការស្កេន សំឡេង និងឧបករណ៍រាប់ពិភពលោកបន្តផ្ទាល់។","នេះជាគម្រោងកម្សាន្តដែលបំផុសគំនិតដោយរឿងព្រេងឥស្លាម។ បើកវានៅលើទូរស័ព្ទរបស់អ្នក ហើយមើលថាមានជិនប៉ុន្មាននៅជិតអ្នកឥឡូវនេះ។","📡 បើករ៉ាដា"),
}

# Метки кнопки «Поделиться» (fallback → en). Для распространения (виральность).
SHARE = {
"en":("📤 Share","Link copied ✅"),"ru":("📤 Поделиться","Ссылка скопирована ✅"),
"uz":("📤 Ulashish","Havola nusxalandi ✅"),"ar":("📤 مشاركة","تم نسخ الرابط ✅"),
"tr":("📤 Paylaş","Bağlantı kopyalandı ✅"),"fa":("📤 اشتراک‌گذاری","لینک کپی شد ✅"),
"ur":("📤 شیئر کریں","لنک کاپی ہو گیا ✅"),"id":("📤 Bagikan","Tautan disalin ✅"),
"az":("📤 Paylaş","Keçid kopyalandı ✅"),"kk":("📤 Бөлісу","Сілтеме көшірілді ✅"),
"ky":("📤 Бөлүшүү","Шилтеме көчүрүлдү ✅"),"tg":("📤 Мубодила","Пайванд нусхабардорӣ шуд ✅"),
"tk":("📤 Paýlaş","Salgy göçürildi ✅"),"ps":("📤 شریکول","لینک کاپي شو ✅"),
"hi":("📤 शेयर करें","लिंक कॉपी हो गया ✅"),"bn":("📤 শেয়ার","লিঙ্ক কপি হয়েছে ✅"),
"ms":("📤 Kongsi","Pautan disalin ✅"),"es":("📤 Compartir","Enlace copiado ✅"),
"fr":("📤 Partager","Lien copié ✅"),"de":("📤 Teilen","Link kopiert ✅"),
"pt":("📤 Partilhar","Ligação copiada ✅"),"sw":("📤 Shiriki","Kiungo kimenakiliwa ✅"),
"ha":("📤 Raba","An kwafi mahaɗi ✅"),
"it":("📤 Condividi","Link copiato ✅"),"nl":("📤 Delen","Link gekopieerd ✅"),
"uk":("📤 Поділитися","Посилання скопійовано ✅"),"pl":("📤 Udostępnij","Link skopiowano ✅"),
"ro":("📤 Distribuie","Link copiat ✅"),"he":("📤 שיתוף","הקישור הועתק ✅"),
"zh-Hans":("📤 分享","链接已复制 ✅"),"zh-Hant":("📤 分享","連結已複製 ✅"),
"ja":("📤 シェア","リンクをコピーしました ✅"),"ko":("📤 공유","링크가 복사되었습니다 ✅"),
"vi":("📤 Chia sẻ","Đã sao chép liên kết ✅"),"th":("📤 แชร์","คัดลอกลิงก์แล้ว ✅"),
"fil":("📤 Ibahagi","Nakopya ang link ✅"),"el":("📤 Κοινοποίηση","Ο σύνδεσμος αντιγράφηκε ✅"),
"hu":("📤 Megosztás","Link másolva ✅"),"bg":("📤 Сподели","Връзката е копирана ✅"),
"sr":("📤 Подели","Веза је копирана ✅"),"hr":("📤 Podijeli","Poveznica kopirana ✅"),
"sq":("📤 Shpërnda","Lidhja u kopjua ✅"),"ka":("📤 გაზიარება","ბმული დაკოპირდა ✅"),
"hy":("📤 Կիսվել","Հղումը պատճենվեց ✅"),"cs":("📤 Sdílet","Odkaz zkopírován ✅"),
"sv":("📤 Dela","Länk kopierad ✅"),"fi":("📤 Jaa","Linkki kopioitu ✅"),
"da":("📤 Del","Link kopieret ✅"),"no":("📤 Del","Lenke kopiert ✅"),
"ku":("📤 Parve bike","Girêdan hate kopîkirin ✅"),"bs":("📤 Podijeli","Link kopiran ✅"),
"mk":("📤 Сподели","Врската е копирана ✅"),"sk":("📤 Zdieľať","Odkaz skopírovaný ✅"),
"sl":("📤 Deli","Povezava kopirana ✅"),"lt":("📤 Dalintis","Nuoroda nukopijuota ✅"),
"lv":("📤 Kopīgot","Saite nokopēta ✅"),"et":("📤 Jaga","Link kopeeritud ✅"),
"af":("📤 Deel","Skakel gekopieer ✅"),"ne":("📤 सेयर गर्नुहोस्","लिंक कपी भयो ✅"),
"si":("📤 බෙදාගන්න","සබැඳිය පිටපත් විය ✅"),"my":("📤 မျှဝေရန်","လင့်ခ်ကူးယူပြီး ✅"),
"km":("📤 ចែករំលែក","បានចម្លងតំណ ✅"),
}

# FAQ для лендингов: НАТИВНЫЕ Q&A (видимый блок + FAQPage JSON-LD должны совпадать
# по правилам Google). Языки без записи FAQ не получают блок — никаких смешанных языков.
# Заголовок «FAQ» и подписи вопросов остаются в контенте пар. Ключ "t" — заголовок секции.
FAQ = {
"en": ("FAQ", [
  ("Is JinnRadar real?", "No. JinnRadar is an entertainment project inspired by Islamic lore. The jinn on the radar are generated for fun — it does not really detect anything."),
  ("Is JinnRadar free?", "Yes, JinnRadar is completely free. Just open it in your browser and allow location access to see the sonar.")]),
"ru": ("Частые вопросы", [
  ("Радар джиннов работает по-настоящему?", "Нет. JinnRadar — развлекательный проект по мотивам исламских преданий. Джинны на радаре генерируются для развлечения — на самом деле он ничего не обнаруживает."),
  ("JinnRadar бесплатный?", "Да, JinnRadar полностью бесплатный. Просто откройте его в браузере и разрешите доступ к геолокации, чтобы увидеть сонар.")]),
"ar": ("الأسئلة الشائعة", [
  ("هل رادار الجن حقيقي؟", "لا. جِن رادار مشروع ترفيهي مستوحى من التراث الإسلامي. الجن الظاهر على الرادار مُولَّد للتسلية — وهو لا يكتشف شيئًا في الواقع."),
  ("هل جِن رادار مجاني؟", "نعم، جِن رادار مجاني تمامًا. افتحه في متصفحك واسمح بالوصول إلى موقعك لرؤية السونار.")]),
"tr": ("Sıkça Sorulan Sorular", [
  ("Cin Radarı gerçek mi?", "Hayır. JinnRadar, İslami folklordan esinlenen bir eğlence projesidir. Radardaki cinler eğlence için üretilir — gerçekte hiçbir şey tespit etmez."),
  ("JinnRadar ücretsiz mi?", "Evet, JinnRadar tamamen ücretsizdir. Tarayıcında aç ve sonarı görmek için konum iznini ver.")]),
"fa": ("پرسش‌های متداول", [
  ("آیا رادار جن واقعی است؟", "خیر. جِن‌رادار یک پروژه سرگرمی الهام‌گرفته از باورهای اسلامی است. جن‌های روی رادار برای سرگرمی ساخته می‌شوند — در واقع چیزی را شناسایی نمی‌کند."),
  ("آیا جِن‌رادار رایگان است؟", "بله، جِن‌رادار کاملاً رایگان است. کافی است آن را در مرورگر باز کنید و اجازه دسترسی به موقعیت مکانی را بدهید تا سونار را ببینید.")]),
"ur": ("عام سوالات", [
  ("کیا جن ریڈار حقیقی ہے؟", "نہیں۔ جن ریڈار اسلامی روایات سے متاثر ایک تفریحی منصوبہ ہے۔ ریڈار پر نظر آنے والے جن تفریح کے لیے بنائے جاتے ہیں — یہ حقیقت میں کچھ نہیں ڈھونڈتا۔"),
  ("کیا جن ریڈار مفت ہے؟", "جی ہاں، جن ریڈار بالکل مفت ہے۔ اسے اپنے براؤزر میں کھولیں اور سونار دیکھنے کے لیے لوکیشن کی اجازت دیں۔")]),
"id": ("Pertanyaan Umum", [
  ("Apakah Radar Jin nyata?", "Tidak. JinnRadar adalah proyek hiburan yang terinspirasi cerita rakyat Islam. Jin di radar dibuat untuk hiburan — ia tidak benar-benar mendeteksi apa pun."),
  ("Apakah JinnRadar gratis?", "Ya, JinnRadar sepenuhnya gratis. Cukup buka di browser dan izinkan akses lokasi untuk melihat sonar.")]),
"uz": ("Koʻp beriladigan savollar", [
  ("Jin radari haqiqiymi?", "Yoʻq. JinnRadar islom rivoyatlaridan ilhomlangan koʻngilochar loyiha. Radardagi jinlar koʻngilochar uchun yaratilgan — u aslida hech narsani aniqlamaydi."),
  ("JinnRadar bepulmi?", "Ha, JinnRadar butunlay bepul. Uni brauzerda oching va sonarni koʻrish uchun joylashuvga ruxsat bering.")]),
"es": ("Preguntas frecuentes", [
  ("¿El Radar de Yinn es real?", "No. JinnRadar es un proyecto de entretenimiento inspirado en el folclore islámico. Los yinn del radar se generan por diversión — en realidad no detecta nada."),
  ("¿JinnRadar es gratis?", "Sí, JinnRadar es completamente gratis. Solo ábrelo en tu navegador y permite el acceso a la ubicación para ver el sonar.")]),
"fr": ("Foire aux questions", [
  ("Le Radar à Djinns est-il réel ?", "Non. JinnRadar est un projet de divertissement inspiré du folklore islamique. Les djinns du radar sont générés pour s'amuser — il ne détecte rien en réalité."),
  ("JinnRadar est-il gratuit ?", "Oui, JinnRadar est entièrement gratuit. Ouvrez-le simplement dans votre navigateur et autorisez la localisation pour voir le sonar.")]),
"de": ("Häufige Fragen", [
  ("Ist das Dschinn-Radar echt?", "Nein. JinnRadar ist ein Unterhaltungsprojekt, inspiriert von der islamischen Überlieferung. Die Dschinn auf dem Radar werden zum Spaß erzeugt — es erkennt in Wirklichkeit nichts."),
  ("Ist JinnRadar kostenlos?", "Ja, JinnRadar ist völlig kostenlos. Öffne es einfach im Browser und erlaube den Standortzugriff, um das Sonar zu sehen.")]),
"pt": ("Perguntas frequentes", [
  ("O Radar de Jinn é real?", "Não. O JinnRadar é um projeto de entretenimento inspirado no folclore islâmico. Os jinn no radar são gerados para diversão — ele não detecta nada de verdade."),
  ("O JinnRadar é gratuito?", "Sim, o JinnRadar é totalmente gratuito. Basta abrir no navegador e permitir o acesso à localização para ver o sonar.")]),
"hi": ("अक्सर पूछे जाने वाले सवाल", [
  ("क्या जिन्न रडार असली है?", "नहीं। JinnRadar इस्लामी लोककथाओं से प्रेरित एक मनोरंजन परियोजना है। रडार पर दिखने वाले जिन्न मनोरंजन के लिए बनाए जाते हैं — यह वास्तव में कुछ भी पता नहीं लगाता।"),
  ("क्या JinnRadar मुफ़्त है?", "हाँ, JinnRadar पूरी तरह मुफ़्त है। बस इसे अपने ब्राउज़र में खोलें और सोनार देखने के लिए लोकेशन की अनुमति दें।")]),
}


# og:locale требует формат language_TERRITORY, иначе Facebook/соцсети его игнорируют
# (для остальных языков территория = язык в верхнем регистре: de→de_DE, и т.п.).
OG_TERRITORY = {
"en":"US","pt":"BR","sv":"SE","zh-Hans":"CN","zh-Hant":"TW","ar":"SA","fa":"IR",
"ur":"PK","hi":"IN","bn":"BD","uk":"UA","sr":"RS","he":"IL","ja":"JP","ko":"KR",
"vi":"VN","ms":"MY","fil":"PH","sw":"KE","ha":"NG","el":"GR","cs":"CZ","da":"DK",
"et":"EE","sq":"AL","ka":"GE","hy":"AM","ku":"TR","ps":"AF","ne":"NP","si":"LK",
"my":"MM","km":"KH","uz":"UZ","kk":"KZ","ky":"KG","tg":"TJ","tk":"TM","az":"AZ",
"bs":"BA","af":"ZA",
}


def og_locale(code):
    base = code.split("-")[0]
    terr = OG_TERRITORY.get(code) or OG_TERRITORY.get(base) or base.upper()
    return f"{base}_{terr}"


def faq_blocks(code):
    """Возвращает (visible_html, jsonld_script) для языка или ('','') если FAQ нет."""
    entry = FAQ.get(code)
    if not entry:
        return "", ""
    title, pairs = entry
    qa = "".join(
        f'<div class="qa"><h3>{_html.escape(q)}</h3><p>{_html.escape(a)}</p></div>'
        for q, a in pairs
    )
    visible = f'<section class="faq"><h2>{_html.escape(title)}</h2>{qa}</section>'
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [
              {"@type": "Question", "name": q,
               "acceptedAnswer": {"@type": "Answer", "text": a}}
              for q, a in pairs]}
    script = ('<script type="application/ld+json">'
              + json.dumps(ld, ensure_ascii=False) + '</script>')
    return visible, script


TPL = """<!doctype html>
<html lang="{code}" dir="{dir}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{site}l/{code}.html"/>
<meta name="robots" content="index, follow"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="JinnRadar"/>
<meta property="og:title" content="{h1}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:image" content="{site}og.png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="{h1}"/>
<meta property="og:url" content="{site}l/{code}.html"/>
<meta property="og:locale" content="{og_locale}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{h1}"/>
<meta name="twitter:description" content="{desc}"/>
<meta name="twitter:image" content="{site}og.png"/>
<meta name="twitter:image:alt" content="{h1}"/>
{alts}
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3980078996117020" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"JinnRadar","inLanguage":"{code}","applicationCategory":"EntertainmentApplication","operatingSystem":"Web","offers":{{"@type":"Offer","price":"0"}},"url":"{site}l/{code}.html"}}</script>
{faq_ld}
<style>
  body{{margin:0;background:#02100b;color:#c8ffe6;font-family:"Segoe UI",Roboto,sans-serif;line-height:1.7}}
  a{{color:#22ff9b;text-decoration:none}}.wrap{{max-width:720px;margin:0 auto;padding:24px 18px}}
  header a{{font-weight:800}}
  h1{{font-size:27px;text-shadow:0 0 14px #22ff9b33;margin:20px 0 10px}}
  p{{color:#bfe9d4;font-size:17px}}
  .cta{{display:block;text-align:center;background:linear-gradient(135deg,#22ff9b,#12b98a);color:#04120c;font-weight:800;padding:18px;border-radius:14px;margin:26px 0;font-size:18px;box-shadow:0 8px 30px #25e0a355}}
  .share{{display:block;width:100%;text-align:center;background:transparent;color:#22ff9b;border:1px solid #22ff9b;font-weight:700;padding:14px;border-radius:14px;margin:-12px 0 20px;font-size:16px;cursor:pointer;font-family:inherit}}
  .share:hover{{background:#0a2418}}
  .faq{{border-top:1px solid #0f4d34;margin-top:8px;padding-top:14px}}
  .faq h2{{font-size:20px;color:#e7fff2;margin:0 0 6px}}
  .faq .qa{{margin:14px 0}}
  .faq h3{{font-size:16px;color:#22ff9b;margin:0 0 4px}}
  .faq .qa p{{margin:0;font-size:15px;color:#bfe9d4}}
  .langs{{border-top:1px solid #0f4d34;margin-top:26px;padding-top:14px;font-size:13px;line-height:2.2;color:#7fbfa0}}
  .langs a{{color:#8fd9bb;margin-inline-end:6px}}
  footer{{border-top:1px solid #0f4d34;margin-top:18px;padding:16px 0;color:#5fae86;font-size:12px}}
</style>
</head>
<body>
<div class="wrap">
<header><a href="{site}">🔮 JinnRadar</a></header>
<h1>{h1}</h1>
<p>{p1}</p>
<p>{p2}</p>
<a class="cta" href="{site}">{cta}</a>
<button class="share" id="shareBtn" data-copied="{share_ok}">{share}</button>
{faq_section}
<div class="langs"><b style="color:#c8ffe6">🌍 Languages:</b><br>{switch}</div>
<footer>© <span id="y"></span> JinnRadar</footer>
</div>
<script>document.getElementById('y').textContent=new Date().getFullYear();</script>
<script>(function(){{var b=document.getElementById('shareBtn');if(!b)return;var t=b.textContent,ok=b.getAttribute('data-copied');
var su=(function(){{try{{var u=new URL(location.href);u.searchParams.set('utm_source','share');u.searchParams.set('utm_medium','viral');u.searchParams.set('utm_campaign','landing');return u.href;}}catch(e){{return location.href;}}}})();
b.addEventListener('click',function(){{var d={{title:document.title,text:document.querySelector('meta[name=description]').content,url:su}};
if(navigator.share){{navigator.share(d).catch(function(){{}});return;}}
var done=function(){{b.textContent=ok;setTimeout(function(){{b.textContent=t;}},2000);}};
if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(su).then(done,done);}}
else{{var i=document.createElement('input');i.value=su;document.body.appendChild(i);i.select();try{{document.execCommand('copy');}}catch(e){{}}document.body.removeChild(i);done();}}}});}})();</script>
<script>(function(){{try{{if(sessionStorage.getItem('jrh'))return;sessionStorage.setItem('jrh','1');var A='{anon}';fetch('https://zwzmcihwtwgjajjjsbms.supabase.co/rest/v1/rpc/jr_hit',{{method:'POST',headers:{{'apikey':A,'Authorization':'Bearer '+A,'Content-Type':'application/json'}},body:'{{}}'}});}}catch(e){{}}}})();</script>
</body>
</html>
"""

def build():
    ldir = os.path.join(ROOT, "l")
    os.makedirs(ldir, exist_ok=True)
    codes = list(LANGS.keys())
    # hreflang alternates (общий блок для всех)
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{c}" href="{SITE}l/{c}.html"/>' for c in codes
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE}l/en.html"/>'
    # переключатель языков
    switch = " · ".join(f'<a href="{SITE}l/{c}.html">{LANGS[c][0]}</a>' for c in codes)
    for c in codes:
        name, d, title, desc, h1, p1, p2, cta = LANGS[c]
        sh, sh_ok = SHARE.get(c, SHARE["en"])
        faq_section, faq_ld = faq_blocks(c)
        html = TPL.format(code=c, dir=d, title=title, desc=desc, h1=h1, p1=p1, p2=p2,
                          cta=cta, site=SITE, anon=ANON, alts=alts, switch=switch,
                          share=sh, share_ok=sh_ok, faq_section=faq_section, faq_ld=faq_ld,
                          og_locale=og_locale(c))
        open(os.path.join(ldir, f"{c}.html"), "w", encoding="utf-8").write(html)
    # языковой хаб /l/index.html
    hub_cards = "\n".join(
        f'<a class="card" href="{SITE}l/{c}.html"><b>{LANGS[c][0]}</b></a>' for c in codes
    )
    hub = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>JinnRadar in your language — {len(codes)} languages</title>
<meta name="description" content="JinnRadar — the online jinn radar — available in {len(codes)} languages. Pick yours and see how many jinn are near you."/>
<link rel="canonical" href="{SITE}l/"/>
{alts}
<style>body{{margin:0;background:#02100b;color:#c8ffe6;font-family:Roboto,sans-serif}}.wrap{{max-width:760px;margin:0 auto;padding:20px}}
a{{color:#22ff9b;text-decoration:none}}h1{{text-shadow:0 0 14px #22ff9b33}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:16px}}
.card{{border:1px solid #0f4d34;border-radius:12px;padding:12px 14px;background:#04160f}}.card:hover{{border-color:#22ff9b}}
.card b{{color:#e7fff2}}.cta{{display:block;text-align:center;background:linear-gradient(135deg,#22ff9b,#12b98a);color:#04120c;font-weight:800;padding:16px;border-radius:14px;margin:22px 0}}</style>
</head><body><div class="wrap">
<header><a href="{SITE}" style="font-weight:800">🔮 JinnRadar</a></header>
<h1>Choose your language</h1>
<p style="color:#bfe9d4">JinnRadar is available in {len(codes)} languages. Pick yours 👇</p>
<a class="cta" href="{SITE}">📡 Open the radar</a>
<div class="grid">{hub_cards}</div>
</div></body></html>"""
    open(os.path.join(ldir, "index.html"), "w", encoding="utf-8").write(hub)

    # sitemap.xml — полностью пересобираем: корень + /g/ + /l/
    g_pages = ["g/","g/dzhinny-v-islame.html","g/vidy-dzhinnov.html","g/kak-uznat-dzhinna.html",
               "g/dzhinn-v-dome-priznaki.html","g/kak-zashchititsya-ot-dzhinnov.html","g/jinlar-haqida.html"]
    today = "2026-07-26"
    urls = [(SITE, "1.0", "daily"), (SITE+"l/", "0.9", "weekly")]
    urls += [(SITE+g, "0.8", "weekly") for g in g_pages]
    urls += [(SITE+f"l/{c}.html", "0.7", "weekly") for c in codes]
    body = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n"
        for (u, pr, cf) in urls
    )
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    print(f"built {len(codes)} language pages + hub + sitemap ({len(urls)} urls)")
    return codes

if __name__ == "__main__":
    build()
