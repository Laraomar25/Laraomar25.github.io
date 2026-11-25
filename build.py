"""Builds index.html (English, home page), ar.html and tr.html from data.json; en.html redirects home.

Edit data.json, then run:  python3 build.py
"""
import hashlib
import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = "https://laraomar25.github.io"
D = json.loads((HERE / "data.json").read_text(encoding="utf-8"))

LANGS = [
    {"code": "ar", "file": "ar.html", "path": "/ar", "href": "ar.html", "dir": "rtl", "short": "ع", "label": "العربية", "og": "ar_AR"},
    {"code": "en", "file": "index.html", "path": "/", "href": "index.html", "dir": "ltr", "short": "EN", "label": "English", "og": "en_US"},
    {"code": "tr", "file": "tr.html", "path": "/tr", "href": "tr.html", "dir": "ltr", "short": "TR", "label": "Türkçe", "og": "tr_TR"},
]

# Interface text that isn't in data.json
EXTRA = {
    "hero_hi": {"ar": "مرحبًا، أنا", "en": "Hi, I'm", "tr": "Merhaba, ben"},
    "nav_home": {"ar": "الصفحة الرئيسية", "en": "Home", "tr": "Ana sayfa"},
    "read_more": {"ar": "اقرأ المزيد", "en": "Read more", "tr": "Devamını oku"},
    "read_less": {"ar": "إخفاء التفاصيل", "en": "Show less", "tr": "Daha az göster"},
    "try_bot": {"ar": "جرّب البوت على تليجرام", "en": "Try the bot on Telegram", "tr": "Botu Telegram'da dene"},
    "copy": {"ar": "نسخ", "en": "Copy", "tr": "Kopyala"},
    "copied": {"ar": "تم النسخ", "en": "Copied", "tr": "Kopyalandı"},
    "github": {"ar": "حسابي على GitHub", "en": "My GitHub", "tr": "GitHub hesabım"},
    "live": {"ar": "يعمل الآن", "en": "Live", "tr": "Yayında"},
    "write_me": {"ar": "راسليني", "en": "Email me", "tr": "Bana yazın"},
    "projects_count": {"ar": "مشاريع", "en": "projects", "tr": "proje"},
    "langs_count": {"ar": "لغات للموقع", "en": "site languages", "tr": "site dili"},
    "live_count": {"ar": "مشاريع يمكنك تجربتها", "en": "projects you can try", "tr": "denenebilir proje"},
    "flip_hint": {"ar": "اضغط لرؤية المشروع الحقيقي", "en": "Tap to see the real project", "tr": "Gerçek projeyi görmek için dokun"},
    "cv_kicker": {"ar": "السيرة الذاتية", "en": "Résumé", "tr": "Özgeçmiş"},
    "cv_title": {"ar": "سيرتي الذاتية كاملة", "en": "My full CV", "tr": "Özgeçmişimin tamamı"},
    "cv_sub": {"ar": "صفحة واحدة: المشاريع والخبرة والتعليم والمهارات.", "en": "One page: projects, experience, education and skills.", "tr": "Tek sayfa: projeler, deneyim, eğitim ve yetenekler."},
    "cv_view": {"ar": "عرض", "en": "View", "tr": "Görüntüle"},
    "cv_download": {"ar": "تحميل PDF", "en": "Download PDF", "tr": "PDF indir"},
    "cv_alt": {"ar": "معاينة السيرة الذاتية للارا العثماني", "en": "Preview of Lara Alothmani's CV", "tr": "Lara Alothmani'nin özgeçmiş önizlemesi"},
    "nav_cv": {"ar": "السيرة الذاتية", "en": "CV", "tr": "Özgeçmiş"},
    "exp_tag": {"ar": "خبرة عملية", "en": "Experience", "tr": "Deneyim"},
    "cert_tag": {"ar": "شهادة", "en": "Certificate", "tr": "Sertifika"},
    "langs_title": {"ar": "اللغات", "en": "Languages", "tr": "Diller"},
    "zoom": {"ar": "تكبير الصورة", "en": "Enlarge image", "tr": "Görseli büyüt"},
    "collab_btn": {"ar": "اقترح تعاونًا", "en": "Suggest a collaboration", "tr": "İş birliği öner"},
    "collab_title": {"ar": "طلب تعاون", "en": "Collaboration request", "tr": "İş birliği talebi"},
    "collab_name": {"ar": "الاسم الكامل", "en": "Full name", "tr": "Ad soyad"},
    "collab_idea": {"ar": "وصف مختصر لفكرة التعاون", "en": "Short description of the idea", "tr": "İş birliği fikrinin kısa açıklaması"},
    "collab_file": {"ar": "مرفق PDF (وصف المشروع أو نموذج عمل، حتى 5 MB)", "en": "PDF attachment (project description or work sample, up to 5 MB)", "tr": "PDF eki (proje açıklaması veya çalışma örneği, en fazla 5 MB)"},
    "collab_pick": {"ar": "اختر ملف PDF", "en": "Choose a PDF", "tr": "PDF seç"},
    "collab_note": {"ar": "سيُحفظ الملف وبيانات الطلب في Google Drive الخاص بي لمراجعة طلبك.", "en": "Your file and request details will be saved in my Google Drive so I can review your request.", "tr": "Dosyanız ve talep bilgileriniz, talebinizi inceleyebilmem için Google Drive'ıma kaydedilir."},
    "collab_send": {"ar": "إرسال الطلب", "en": "Send request", "tr": "Talebi gönder"},
    "flip_back": {"ar": "اضغط للعودة إلى الرسمة", "en": "Tap to go back to the drawing", "tr": "Çizime dönmek için dokun"},
}

# Messages used by collab.js
COLLAB_TEXT = {
    "send": EXTRA["collab_send"],
    "sending": {"ar": "جارٍ الإرسال…", "en": "Sending…", "tr": "Gönderiliyor…"},
    "no_file": {"ar": "لم يُختر ملف بعد", "en": "No file chosen yet", "tr": "Henüz dosya seçilmedi"},
    "preparing": {"ar": "جارٍ تجهيز الطلب…", "en": "Preparing your request…", "tr": "Talebiniz hazırlanıyor…"},
    "uploading": {"ar": "جارٍ رفع الملف…", "en": "Uploading the file…", "tr": "Dosya yükleniyor…"},
    "retrying": {"ar": "انقطع الرفع، نعيد المحاولة…", "en": "The upload was interrupted, trying again…", "tr": "Yükleme kesildi, yeniden deneniyor…"},
    "verifying": {"ar": "جارٍ التأكد من حفظ الملف…", "en": "Checking that the file was saved…", "tr": "Dosyanın kaydedildiği doğrulanıyor…"},
    "success": {"ar": "وصل طلبك وحُفظ الملف بنجاح. رقم الطلب: {id}", "en": "Your request was received and the file is saved. Request number: {id}", "tr": "Talebiniz alındı ve dosya kaydedildi. Talep numarası: {id}"},
    "e_check": {"ar": "راجع الحقول المحدّدة ثم أعد الإرسال.", "en": "Please check the marked fields and send again.", "tr": "Lütfen işaretli alanları kontrol edip tekrar gönderin."},
    "e_name": {"ar": "اكتب الاسم الكامل (من حرفين إلى 80).", "en": "Enter your full name (2 to 80 characters).", "tr": "Ad soyad girin (2-80 karakter)."},
    "e_email": {"ar": "اكتب بريدًا إلكترونيًا صحيحًا.", "en": "Enter a valid email address.", "tr": "Geçerli bir e-posta adresi girin."},
    "e_idea": {"ar": "اكتب وصفًا من 20 إلى 2000 حرف.", "en": "Describe the idea in 20 to 2000 characters.", "tr": "Fikri 20-2000 karakterle açıklayın."},
    "e_file_missing": {"ar": "أرفق ملف PDF.", "en": "Attach a PDF file.", "tr": "Bir PDF dosyası ekleyin."},
    "e_file_type": {"ar": "يجب أن يكون المرفق ملف PDF.", "en": "The attachment must be a PDF file.", "tr": "Ek bir PDF dosyası olmalıdır."},
    "e_file_size": {"ar": "حجم الملف أكبر من 5 MB.", "en": "The file is larger than 5 MB.", "tr": "Dosya 5 MB'den büyük."},
    "e_bad_file": {"ar": "الملف الذي وصل ليس PDF سليمًا أو لم يصل كاملًا، ولم يُحفظ. اختر ملفًا آخر أو أعد الإرسال.", "en": "The file that arrived was incomplete or not a valid PDF, so it was not kept. Choose another file or send again.", "tr": "Gelen dosya eksik ya da geçerli bir PDF değil, bu yüzden saklanmadı. Başka bir dosya seçin veya tekrar gönderin."},
    "e_rate": {"ar": "أُرسلت طلبات كثيرة. حاول مجددًا بعد {n} دقيقة تقريبًا.", "en": "Too many requests. Please try again in about {n} min.", "tr": "Çok fazla istek gönderildi. Yaklaşık {n} dk sonra tekrar deneyin."},
    "e_network": {"ar": "تعذّر الاتصال بالخدمة. تحقّق من الإنترنت ثم اضغط إرسال مجددًا؛ لن يتكرر طلبك.", "en": "Could not reach the service. Check your connection and press send again; your request will not be duplicated.", "tr": "Hizmete ulaşılamadı. Bağlantınızı kontrol edip tekrar gönderin; talebiniz yinelenmez."},
    "e_upload": {"ar": "لم يكتمل رفع الملف. اضغط إرسال مجددًا للمتابعة؛ لن يتكرر طلبك.", "en": "The upload did not finish. Press send again to continue; your request will not be duplicated.", "tr": "Yükleme tamamlanmadı. Devam etmek için tekrar gönderin; talebiniz yinelenmez."},
    "e_direct": {"ar": "تعذّر رفع الملف مباشرة إلى Google Drive من هذا المتصفح. جرّب شبكة أو متصفحًا آخر، أو أرسل الملف بالبريد.", "en": "The file could not be uploaded directly to Google Drive from this browser. Try another network or browser, or send it by email.", "tr": "Dosya bu tarayıcıdan doğrudan Google Drive'a yüklenemedi. Başka bir ağ veya tarayıcı deneyin ya da e-postayla gönderin."},
    "e_server": {"ar": "حدث خطأ أثناء حفظ الطلب ولم يتأكد الحفظ. اضغط إرسال مجددًا بعد قليل؛ لن يتكرر طلبك.", "en": "Something went wrong and saving was not confirmed. Press send again shortly; your request will not be duplicated.", "tr": "Bir hata oluştu ve kayıt doğrulanamadı. Biraz sonra tekrar gönderin; talebiniz yinelenmez."},
    "e_off": {"ar": "استقبال الطلبات غير مفعّل بعد. راسلني بالبريد الإلكتروني.", "en": "Requests are not open yet. Please email me instead.", "tr": "Talep alımı henüz açık değil. Lütfen e-posta gönderin."},
}


def art_for(p):
    """The project's illustration from art/<id>.svg, or "" if there is none."""
    f = HERE / "art" / f"{p['id']}.svg"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""

# Each featured project gets its own colour pair
ACCENTS = {
    "cosigning": ("#B08D57", "#E2D3B8"),
    "employment-gap": ("#B08D57", "#E2D3B8"),
    "library-management-system": ("#B08D57", "#E2D3B8"),
    "coach-training-platform": ("#B08D57", "#E2D3B8"),
}
MORE_ICONS = {
    "bank-management-system": '<path d="M3 10 12 4l9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
    "online-bookstore": '<path d="M4 6h5a3 3 0 0 1 3 3v11a2 2 0 0 0-2-2H4zM20 6h-5a3 3 0 0 0-3 3v11a2 2 0 0 1 2-2h6z"/>',
    "wildfire-monitoring-with-gis": '<path d="M12 21c-4 0-7-2.7-7-6.5 0-3.6 3-5.6 3.5-9.5 2 1.3 3.2 3.2 3.4 5.3 1-.8 1.6-2 1.7-3.3C16.3 9 19 11.5 19 14.5 19 18.3 16 21 12 21z"/>',
}

ARROW = '<svg class="ico arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CODE_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m8 7-5 5 5 5M16 7l5 5-5 5"/></svg>'
MAIL_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg>'
COPY_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2.5"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/></svg>'
GH_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 19c-4 1.3-4-2-6-2.5M15 21v-3.4a3 3 0 0 0-.8-2.3c2.7-.3 5.6-1.3 5.6-6a4.6 4.6 0 0 0-1.3-3.2 4.3 4.3 0 0 0-.1-3.2s-1-.3-3.4 1.3a11.6 11.6 0 0 0-6 0C6.6 2.6 5.6 2.9 5.6 2.9a4.3 4.3 0 0 0-.1 3.2A4.6 4.6 0 0 0 4.2 9.3c0 4.6 2.9 5.7 5.6 6a3 3 0 0 0-.8 2.3V21"/></svg>'
DL_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>'
EYE_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>'
HANDS_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="9" r="3.2"/><circle cx="16" cy="9" r="3.2"/><path d="M2.5 19c.4-3 2.5-4.8 5.5-4.8 1.6 0 3 .5 4 1.4 1-.9 2.4-1.4 4-1.4 3 0 5.1 1.8 5.5 4.8"/></svg>'
FILE_ICO = '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8zM14 3v5h5M12 17v-5M9.5 14.5 12 12l2.5 2.5"/></svg>'
STAR = '<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M50 4 63 21l21-4-4 21 17 12-17 13 4 21-21-4-13 17-13-17-21 4 4-21L3 50l17-12-4-21 21 4z"/></svg>'


# ASSET_V
def asset_v(name):
    """Short hash of a file, so browsers fetch the new version after each change."""
    return hashlib.md5((HERE / name).read_bytes()).hexdigest()[:8]


def t(obj, lang):
    if isinstance(obj, dict):
        return obj.get(lang) or obj.get("en") or ""
    return obj or ""


def e(s):
    return escape(str(s), quote=True)


def build(L):
    lang = L["code"]
    ui = {**D["ui"], **EXTRA}
    u = lambda k: e(t(ui[k], lang))
    prof, site, contact = D["profile"], D["site"], D["contact"]
    name = t(prof["name"], lang)
    projects = D["projects"]
    featured = [p for p in projects if p.get("featured")]
    more = [p for p in projects if not p.get("featured")]
    live = [p for p in projects if p.get("demo")]
    new_tab = f'<span class="sr-only"> {u("new_tab")}</span>'

    # ---------- head ----------
    url = SITE + L["path"]
    alts = "\n".join(
        f'  <link rel="alternate" hreflang="{x["code"]}" href="{SITE}{x["path"]}">' for x in LANGS
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}/">'
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": name,
        "jobTitle": t(prof["title"], lang), "url": url, "email": contact.get("email"),
        "sameAs": [x for x in [contact.get("github"), contact.get("linkedin")] if x],
        "address": {"@type": "PostalAddress", "addressLocality": "Istanbul", "addressCountry": "TR"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Karabük University"},
    }, ensure_ascii=False).replace("</", "<\\/")

    # ---------- language switch ----------
    langsw = "".join(
        f'<a href="{x["href"]}" hreflang="{x["code"]}" lang="{x["code"]}" class="{"on" if x["code"] == lang else ""}"'
        f'{" aria-current=\"page\"" if x["code"] == lang else ""}>{x["short"]}<span class="sr-only"> {x["label"]}</span></a>'
        for x in LANGS
    )

    nav_items = [("work", "nav_projects"), ("about", "nav_about"), ("cv", "nav_cv"), ("skills", "nav_skills"), ("contact", "nav_contact")]
    nav = f'<a href="#main" class="on" aria-current="true">{u("nav_home")}</a>' + "".join(f'<a href="#{a}">{u(k)}</a>' for a, k in nav_items)

    # Tagline: the last two words get the yellow underline
    tag_words = t(prof["tagline"], lang).split(" ")
    tagline_html = e(" ".join(tag_words[:-2])) + f' <span class="mark">{e(" ".join(tag_words[-2:]))}</span>' 

    # ---------- hero code card ----------
    tech = []
    for g in D["skills"]:
        tech += g["items"]
    code_lines = [
        '<span class="k">const</span> <span class="v">lara</span> <span class="p">=</span> <span class="p">{</span>',
        f'  <span class="key">role</span><span class="p">:</span> <span class="s">"{e(t(prof["title"], "en"))}"</span><span class="p">,</span>',
        '  <span class="key">city</span><span class="p">:</span> <span class="s">"Istanbul"</span><span class="p">,</span>',
        '  <span class="key">stack</span><span class="p">:</span> <span class="p">[</span>' + '<span class="p">, </span>'.join(
            f'<span class="s">"{e(x)}"</span>' for x in tech[:4]) + '<span class="p">],</span>',
        f'  <span class="key">projects</span><span class="p">:</span> <span class="n">{len(projects)}</span><span class="p">,</span>',
        '  <span class="key">build</span><span class="p">:</span> <span class="p">()</span> <span class="p">=&gt;</span> <span class="s">"ideas → solutions"</span><span class="p">,</span>',
        '<span class="p">};</span><span class="caret" aria-hidden="true"></span>',
    ]
    code = "\n".join(f'<span class="ln">{i}</span>{l}' for i, l in enumerate(code_lines, 1))
    code_card = f'''<div class="code-card" dir="ltr">
          <div class="code-bar"><i></i><i></i><i></i><b class="tab on">Lara.ts</b><b class="tab">Python</b><b class="tab">SQL</b></div>
          <pre><code>{code}</code></pre>
        </div>'''

    # ---------- featured projects ----------
    def card3d(p, host, media):
        # Front: the illustration. Back (after a click): the real screenshot.
        return f'''
        <button class="card3d" type="button" aria-pressed="false"
                data-front="{u("flip_hint")}" data-back="{u("flip_back")}">
          <span class="card3d-inner">
            <span class="face front">
              <span class="art">{art_for(p)}</span>
              <span class="hint"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 0 1 15.5-6.2L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.5 6.2L3 16M3 21v-5h5"/></svg><span class="hint-text">{u("flip_hint")}</span></span>
            </span>
            <span class="face back">
              <span class="browser">
                <span class="browser-bar"><i></i><i></i><i></i><span dir="ltr">{e(host)}</span></span>
                <span class="browser-shot">{media}</span>
              </span>
              <span class="hint"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 0 1 15.5-6.2L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.5 6.2L3 16M3 21v-5h5"/></svg><span class="hint-text">{u("flip_back")}</span></span>
            </span>
          </span>
        </button>'''

    def zoom_btn(img, p):
        if not img:
            return ""
        return (f'<button class="zoom" type="button" data-src="{e(img["src"])}" data-alt="{e(t(img["alt"], lang))}">'
                f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4M11 8v6M8 11h6"/></svg>'
                f'<span>{u("zoom")}</span></button>')

    def project_card(p, i):
        a1, a2 = ACCENTS.get(p["id"], ("#B08D57", "#E2D3B8"))
        img = (p.get("images") or [None])[0]
        media = (
            f'<img src="{e(img["src"])}" alt="{e(t(img["alt"], lang))}" loading="lazy" width="1440" height="1080">'
            if img else f'<div class="media-ph">{e(t(p["title"], lang))}</div>'
        )
        host = (p.get("demo") or "").replace("https://", "").rstrip("/") or t(p["title"], lang)
        blocks = ""
        for k in ("problem", "solution", "role"):
            txt = t(p.get(k), lang)
            if txt:
                blocks += f'<div class="ps ps-{k}"><h4>{u(k)}</h4><p>{e(txt)}</p></div>'
        chips = "".join(f"<li>{e(x)}</li>" for x in p.get("tech", []))
        btns = ""
        if p.get("demo"):
            label = u("try_bot") if "t.me/" in p["demo"] else u("demo")
            btns += (f'<a class="btn-demo" href="{e(p["demo"])}" target="_blank" rel="noopener">'
                     f'<span class="pulse" aria-hidden="true"></span>{label}{ARROW}{new_tab}</a>')
        if p.get("code"):
            btns += f'<a class="btn-ghost" href="{e(p["code"])}" target="_blank" rel="noopener">{CODE_ICO}{u("code")}{new_tab}</a>'
        flip = " flip" if i % 2 else ""
        return f'''
    <article class="proj reveal{flip}" id="{e(p["id"])}" style="--a1:{a1};--a2:{a2}" aria-labelledby="{e(p["id"])}-t">
      <div class="proj-media">{card3d(p, host, media) + zoom_btn(img, p) if art_for(p) else f"""
        <div class="browser">
          <div class="browser-bar"><i></i><i></i><i></i><span dir="ltr">{e(host)}</span></div>
          <div class="browser-shot">{media}</div>
        </div>"""}
      </div>
      <div class="proj-body">
        <p class="kicker"><span class="dot"></span>{u("featured")}{f'<span class="live">{u("live")}</span>' if p.get("demo") else ""}</p>
        <h3 id="{e(p["id"])}-t">{e(t(p["title"], lang))}</h3>
        {f'<p class="badge"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-3 5 3-1.5-7"/></svg><span>{e(t(p["badge"], lang))}</span></p>' if p.get("badge") else ""}
        <p class="lead">{e(t(p.get("summary"), lang))}</p>
        <div class="ps-wrap" id="{e(p["id"])}-more">{blocks}</div>
        <button class="more-btn" type="button" aria-expanded="false" aria-controls="{e(p["id"])}-more" data-more="{u("read_more")}" data-less="{u("read_less")}"><span>{u("read_more")}</span><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
        {f'<ul class="chips" dir="ltr" aria-label="{u("tech")}">{chips}</ul>' if chips else ""}
        <div class="actions">{btns}</div>
      </div>
    </article>'''

    featured_html = "".join(project_card(p, i) for i, p in enumerate(featured))

    more_html = "".join(f'''
      <li class="mini reveal">
        <span class="mini-ico"><svg viewBox="0 0 24 24" aria-hidden="true">{MORE_ICONS.get(p["id"], '<circle cx="12" cy="12" r="8"/>')}</svg></span>
        <h4>{e(t(p["title"], lang))}</h4>
        {f'<p>{e(t(p.get("summary"), lang))}</p>' if t(p.get("summary"), lang) else ""}
        {f'<a href="{e(p["code"])}" target="_blank" rel="noopener">{u("code")}{new_tab}</a>' if p.get("code") else ""}
      </li>''' for p in more)

    skills_html = "".join(f'''
      <div class="skill reveal">
        <h3>{e(t(g["group"], lang))}</h3>
        <ul dir="ltr">{"".join(f"<li>{e(x)}</li>" for x in g["items"])}</ul>
      </div>''' for g in D["skills"])

    def tl_item(kind, tag, x):
        period = t(x.get("period"), lang)
        desc = t(x.get("description"), lang)
        return f'''
      <li class="reveal tl-{kind}">
        <span class="tl-dot" aria-hidden="true"></span>
        <p class="tl-tag">{u(tag)}{f'<span class="tl-when" dir="ltr">{e(period)}</span>' if period else ""}</p>
        <h3>{e(t(x["title"], lang))}</h3>
        <p class="tl-org">{e(t(x["org"], lang))}</p>
        {f'<p class="tl-desc">{e(desc)}</p>' if desc else ""}
      </li>'''

    edu_html = (
        "".join(tl_item("exp", "exp_tag", x) for x in D.get("experience", []))
        + "".join(tl_item("edu", "education", x) for x in D["education"])
        + "".join(tl_item("cert", "cert_tag", x) for x in D.get("certifications", []))
    )

    langs_html = "".join(f'''
          <li><span class="lg-name">{e(t(x["name"], lang))}</span><span class="lg-level">{e(t(x["level"], lang))}</span>
            <span class="lg-bar" aria-hidden="true"><i style="width:{int(x["pct"])}%"></i></span></li>''' for x in D.get("languages", []))

    cv = contact.get("cv")
    cv_html = f'''
        <div class="cv-card reveal" id="cv">
          <div class="cv-info">
            <p class="eyebrow">{u("cv_kicker")}</p>
            <h3>{u("cv_title")}</h3>
            <p>{u("cv_sub")}</p>
            <div class="cv-btns">
              <a class="btn-demo" href="{e(cv)}" download="Lara-Alothmani-CV.pdf">{DL_ICO}{u("cv_download")}</a>
              <a class="btn-ghost" href="{e(cv)}" target="_blank" rel="noopener">{EYE_ICO}{u("cv_view")}{new_tab}</a>
            </div>
          </div>
        </div>''' if cv else ""

    email = contact.get("email")
    contact_btns = ""
    if email:
        contact_btns += f'''
        <div class="mail">
          <a class="mail-link" href="mailto:{e(email)}">{MAIL_ICO}<span dir="ltr">{e(email)}</span></a>
          <button class="copy" type="button" data-copy="{e(email)}" data-done="{u("copied")}">{COPY_ICO}<span>{u("copy")}</span></button>
        </div>'''
    if cv:
        contact_btns += f'<a class="btn-ghost light" href="{e(cv)}" download="Lara-Alothmani-CV.pdf">{DL_ICO}{u("cv")}</a>'
    if contact.get("github"):
        contact_btns += f'<a class="btn-ghost light" href="{e(contact["github"])}" target="_blank" rel="noopener">{GH_ICO}{u("github")}{new_tab}</a>'

    contact_btns += (f'<button class="btn-demo collab-btn" type="button" aria-expanded="false" aria-controls="collab-form">'
                     f'{HANDS_ICO}{u("collab_btn")}</button>')
    collab_text = json.dumps({k: t(v, lang) for k, v in COLLAB_TEXT.items()}, ensure_ascii=False).replace("</", "<\\/")

    def field(key, label, control):
        return (f'<div class="collab-field"><label for="collab-{key}">{label}</label>{control}'
                f'<p class="collab-err" id="collab-{key}-err" hidden></p></div>')

    collab_html = f'''
        <form class="collab-form" id="collab-form" data-api="{e(contact.get("collab_api") or "")}" aria-labelledby="collab-t" novalidate hidden>
          <h3 id="collab-t">{u("collab_title")}</h3>
          <fieldset>
            <div class="collab-row">
              {field("name", u("collab_name"), '<input id="collab-name" name="name" type="text" autocomplete="name" maxlength="80" required aria-describedby="collab-name-err">')}
              {field("email", u("email"), '<input id="collab-email" name="email" type="email" dir="ltr" autocomplete="email" maxlength="254" required aria-describedby="collab-email-err">')}
            </div>
            {field("idea", u("collab_idea"), '<textarea id="collab-idea" name="idea" rows="5" maxlength="2000" required aria-describedby="collab-idea-err"></textarea>')}
            <div class="collab-field">
              <span class="collab-label">{u("collab_file")}</span>
              <div class="collab-file">
                <input class="sr-only" id="collab-file" name="file" type="file" accept="application/pdf,.pdf" required aria-describedby="collab-file-name collab-file-err collab-note">
                <label class="btn-ghost" for="collab-file">{FILE_ICO}{u("collab_pick")}</label>
                <span class="collab-file-name" id="collab-file-name" dir="auto">{e(t(COLLAB_TEXT["no_file"], lang))}</span>
              </div>
              <p class="collab-err" id="collab-file-err" hidden></p>
            </div>
            <p class="collab-note" id="collab-note">{u("collab_note")}</p>
          </fieldset>
          <progress class="collab-bar" max="1" value="0" hidden aria-label="{e(t(COLLAB_TEXT["uploading"], lang))}"></progress>
          <p class="collab-status" role="status" aria-live="polite" tabindex="-1"></p>
          <div class="collab-end">
            <button class="btn-demo" type="submit"><span>{u("collab_send")}</span></button>
            <button class="btn-ghost collab-cancel" type="button">{u("close")}</button>
          </div>
        </form>
        <script type="application/json" id="collab-text">{collab_text}</script>'''

    year = "2026"
    return f'''<!doctype html>
<html lang="{lang}" dir="{L["dir"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(t(site["title"], lang))}</title>
  <meta name="description" content="{e(t(site["description"], lang))}">
  <meta name="theme-color" content="#14213D">
  <link rel="canonical" href="{url}">
{alts}
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{e(t(site["title"], lang))}">
  <meta property="og:description" content="{e(t(site["description"], lang))}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/images/cosigning.jpg">
  <meta property="og:locale" content="{L["og"]}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{ld}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css?v={asset_v("style.css")}">
  <script>document.documentElement.classList.add("js")</script>
</head>
<body>
  <a class="skip" href="#main">{u("skip")}</a>

  <div class="bg" aria-hidden="true">
    <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
    <div class="pattern"></div>
  </div>

  <header class="top">
    <div class="brand">
      <a class="logo" href="#main" aria-label="{e(name)}"><span>{e(prof["initials"])}</span></a>
      <p class="hello"><span class="wave" aria-hidden="true">👋</span> {u("hero_hi")}</p>
    </div>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{u("menu")}"><svg class="ico i-open" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="ico i-close" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
    <nav class="nav" id="site-nav" aria-label="{u("menu")}">{nav}</nav>
    <div class="langs" role="group" aria-label="{u("language")}" dir="ltr">{langsw}</div>
  </header>

  <main id="main">
    <section class="hero">
      <div class="hero-text">
        <h1 class="name reveal">{e(name)}</h1>
        <p class="role reveal">{e(t(prof["title"], lang))} <span class="sep">·</span> {e(t(prof["location"], lang))}</p>
        <p class="tagline reveal">{tagline_html}</p>
        <div class="hero-cta reveal">
          <a class="btn-demo" href="#work">{u("cta_projects")}{ARROW}</a>
          <a class="btn-ghost" href="#contact">{u("cta_contact")}</a>
        </div>
      </div>
      <div class="hero-art reveal" aria-hidden="true">
        {code_card}
      </div>
    </section>

    <section class="band band-light stats-band" aria-label="{u("projects_count")}">
      <svg class="hero-wave" viewBox="0 0 1440 170" preserveAspectRatio="none" aria-hidden="true">
        <path class="w1" d="M0 46 C 140 52 260 94 420 122 C 560 148 760 166 980 170 L0 170 Z"/>
        <path class="w2" d="M0 138 C 280 112 540 124 830 110 C 1090 98 1290 76 1440 56 L1440 170 L0 170 Z"/>
      </svg>
      <dl class="facts reveal">
        <div><dt>{len(projects)}</dt><dd>{u("projects_count")}</dd></div>
        <div><dt>{len(live)}</dt><dd>{u("live_count")}</dd></div>
        <div><dt>3</dt><dd>{u("langs_count")}</dd></div>
      </dl>
      <div class="hero-art hero-art-m" aria-hidden="true">
        {code_card}
      </div>
    </section>

    <section id="work" class="section band band-light work-band" aria-labelledby="work-t">
      <div class="sec-head reveal">
        <p class="eyebrow">{u("work_kicker")}</p>
        <h2 id="work-t">{u("projects_title")}</h2>
      </div>
      <div class="projs">{featured_html}
      </div>
    </section>

    <section class="section band dark-band" aria-label="{u("more_projects")}">
      <h3 class="sub reveal">{u("more_projects")}</h3>
      <ul class="minis">{more_html}
      </ul>
    </section>

    <section id="about" class="section band band-light about-band about" aria-labelledby="about-t">
      <div class="sec-head reveal">
        <p class="eyebrow">{u("about_kicker")}</p>
        <h2 id="about-t">{u("about_title")}</h2>
      </div>
      <div class="about-grid">
        <div class="about-main">
          <p class="about-text reveal">{e(t(D["about"], lang))}</p>
          {f'''<div class="langs-box reveal"><h3>{u("langs_title")}</h3><ul class="lg">{langs_html}
          </ul></div>''' if langs_html else ""}
          {cv_html}
        </div>
        <ol class="timeline" aria-label="{u("timeline_title")}">{edu_html}
        </ol>
      </div>
    </section>

    <section id="skills" class="section band band-light skills-band" aria-labelledby="skills-t">
      <div class="sec-head reveal">
        <p class="eyebrow">{u("skills_kicker")}</p>
        <h2 id="skills-t">{u("skills_title")}</h2>
      </div>
      <div class="skills">{skills_html}
      </div>
    </section>

    <section id="contact" class="section" aria-labelledby="contact-t">
      <div class="contact reveal">
        <div class="contact-glow" aria-hidden="true"></div>
        <p class="eyebrow">{u("contact_kicker")}</p>
        <h2 id="contact-t">{u("contact_title")}</h2>
        <p class="contact-text">{u("contact_text")}</p>
        <div class="contact-actions">{contact_btns}
        </div>{collab_html}
      </div>
    </section>
  </main>

  <footer class="foot">
    <p>© {year} {e(name)}. {u("rights")}</p>
    <a href="#main">{u("back_to_top")} ↑</a>
  </footer>

  <dialog class="lightbox" aria-label="{u("zoom")}">
    <button class="lb-close" type="button" aria-label="{u("close")}">×</button>
    <img alt="">
  </dialog>

  <script src="main.js?v={asset_v("main.js")}" defer></script>
  <script src="collab.js?v={asset_v("collab.js")}" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    if not D["contact"].get("collab_api"):
        print('note: contact.collab_api in data.json is empty, so the collaboration form cannot send yet')
    for L in LANGS:
        html = build(L)
        if L["dir"] == "rtl":
            # keep "C#" readable inside Arabic sentences
            html = html.replace("C#", "C#\u200e")
        (HERE / L["file"]).write_text(html, encoding="utf-8")
        print("built", L["file"])

    # English is now the home page; keep old en.html links working
    (HERE / "en.html").write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8"><title>Lara Alothmani</title>'
        f'<link rel="canonical" href="{SITE}/"><meta name="robots" content="noindex">'
        '<meta http-equiv="refresh" content="0; url=./">'
        '<script>location.replace("./" + location.hash)</script>'
        '<a href="./">Lara Alothmani</a></html>\n', encoding="utf-8")
    print("built en.html (redirect to home)")
