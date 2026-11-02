"""Batch 2 pin generator (2 Nov 2026). Four layouts: T1 photo+laptop, T2 zoom card, T3 list, T4 photo+panel.
Sources: Example workbooks rendered with LibreOffice (c_*.png), Runware lifestyle photos (bg/*.jpg), existing listing hero images.
Run from any folder; set WORK to the folder that holds r/ (cropped sheets) and bg/ (photos)."""
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORK = "/tmp/w"
OUT = f"{WORK}/out"; os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, s)
W, H = 1000, 1500
RAW = "https://raw.githubusercontent.com/Haryz-worker/ZyrahStudioMA-pinterest-assets/main/pins/"
UP = "/mnt/user-data/uploads/zyrah_studio/"
BOARD = dict(P01="1144195917770567138", P02="1144195917770583205", P03="1144195917770583210", R2="1144195917770583210",
             R3="1144195917770583210", P04="1144195917770567153", R7="1144195917770669627", P06="1144195917770669629")
URL = dict(P01="https://www.etsy.com/listing/4573254943/contractor-job-costing-spreadsheet",
           P02="https://www.etsy.com/listing/4579324688/home-bakery-pricing-spreadsheet-recipe",
           P03="https://www.etsy.com/listing/4579770626/home-build-budget-spreadsheet-renovation",
           P04="https://www.etsy.com/listing/4579978345/embroidery-pricing-spreadsheet-machine",
           R2="https://www.etsy.com/listing/4598103933/home-renovation-planner-spreadsheet-room",
           R3="https://www.etsy.com/listing/4599376778/renovation-budget-tracker-spreadsheet",
           R7="https://www.etsy.com/listing/4602943564/moving-budget-planner-excel-google",
           P06="https://www.etsy.com/listing/4603656166/homeschool-transcript-template-and")
COL = dict(P01=(30, 58, 95), P02=(150, 72, 92), P03=(28, 110, 110), R2=(176, 102, 44), R3=(52, 96, 150),
           P04=(96, 62, 128), R7=(47, 75, 138), P06=(59, 91, 71))
PHOTO = dict(P01="contr", P02="bake", P03="reno", R2="reno", R3="reno", P04="emb", R7="move", P06="home")
CHIPS = ["EXCEL + GOOGLE SHEETS", "INSTANT DOWNLOAD"]

def sheet(name, crop=(0, 0, 1, 1)):
    p = name if name.startswith("/") else f"{WORK}/r/{name}"
    im = Image.open(p).convert("RGB"); w, h = im.size
    return im.crop((int(crop[0]*w), int(crop[1]*h), int(crop[2]*w), int(crop[3]*h)))

def photo(key, w, h):
    im = Image.open(f"{WORK}/bg/{PHOTO[key]}.jpg").convert("RGB"); k = max(w / im.width, h / im.height)
    im = im.resize((int(im.width*k)+1, int(im.height*k)+1), Image.LANCZOS)
    x, y = (im.width - w)//2, (im.height - h)//2
    return im.crop((x, y, x+w, y+h))

def fit(d, text, name, size, maxw):
    f = F(name, size)
    while d.textlength(text, font=f) > maxw: size -= 2; f = F(name, size)
    return f, size

def fitim(im, maxw, maxh):
    k = min(maxw / im.width, maxh / im.height)
    return im.resize((max(1, int(im.width*k)), max(1, int(im.height*k))), Image.LANCZOS)

def shadow(img, box, radius, blur=24, off=(0, 16), alpha=110):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(lay)
    sd.rounded_rectangle([box[0]+off[0], box[1]+off[1], box[2]+off[0], box[3]+off[1]], radius, fill=(0, 0, 0, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(blur)); img.paste(lay, (0, 0), lay)

def card(img, im, cx, y, pad=16, radius=22):
    x = cx - (im.width + 2*pad)//2; box = (x, y, x+im.width+2*pad, y+im.height+2*pad)
    shadow(img, box, radius); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius, fill="white", outline=(215, 215, 215), width=2); img.paste(im, (x+pad, y+pad))
    return box[3]

def laptop(img, scr, cx, y, width):
    """Draw a laptop around the screenshot; returns bottom y."""
    bez = 18; inner_w = width - 2*bez
    s = fitim(scr, inner_w, int(inner_w * 0.66)); sw, sh = s.size
    bw, bh = sw + 2*bez, sh + 2*bez + 6; x0 = cx - bw//2
    shadow(img, (x0, y, x0+bw, y+bh+30), 26, blur=30, off=(0, 26), alpha=130)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y, x0+bw, y+bh], 26, fill=(24, 26, 32))
    d.ellipse([cx-4, y+7, cx+4, y+15], fill=(70, 74, 84))
    img.paste(s, (x0+bez, y+bez+4))
    by = y + bh
    d.polygon([(x0-34, by), (x0+bw+34, by), (x0+bw+14, by+22), (x0-14, by+22)], fill=(188, 191, 198))
    d.rounded_rectangle([cx-70, by, cx+70, by+9], 4, fill=(150, 153, 160))
    return by + 22

def chips(img, y, col, center=500, dark=False):
    d = ImageDraw.Draw(img); f = F("Inter-Bold.otf", 30)
    ws = [d.textlength(t, font=f) + 56 for t in CHIPS]; x = center - (sum(ws) + 20)/2
    for t, w_ in zip(CHIPS, ws):
        d.rounded_rectangle([x, y, x+w_, y+66], 33, fill="white" if dark else col)
        d.text((x+28, y+15), t, font=f, fill=col if dark else "white"); x += w_ + 20

def kicker(img, text, x, y, col, fg="white", bg=None):
    d = ImageDraw.Draw(img); f = F("Inter-Bold.otf", 28); t = text.upper()
    w = d.textlength(t, font=f) + 44
    d.rounded_rectangle([x, y, x+w, y+52], 26, fill=bg or col); d.text((x+22, y+10), t, font=f, fill=fg)
    return y + 52

def headline(img, lines, x, y, size, fill, maxw, center=False, shade=False):
    d = ImageDraw.Draw(img)
    for ln in lines:
        f, s = fit(d, ln, "InterDisplay-Black.otf", size, maxw)
        xx = (W - d.textlength(ln, font=f))/2 if center else x
        if shade: d.text((xx+3, y+4), ln, font=f, fill=(0, 0, 0, 90))
        d.text((xx, y), ln, font=f, fill=fill); y += int(s*1.07)
    return y

def gradient_top(img, col, h, a0=240):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); px = lay.load()
    for yy in range(h):
        a = int(a0 * (1 - yy/h)**1.4)
        for xx in range(W): px[xx, yy] = col + (a,)
    img.paste(lay, (0, 0), lay)

def note(img, text, y, col=(255, 255, 255), x=None):
    d = ImageDraw.Draw(img); f = F("Inter-Medium.otf", 24)
    d.text(((W - d.textlength(text, font=f))/2 if x is None else x, y), text, font=f, fill=col)

def ticks(img, items, x, y, col, ink, size=40, gap=64, badge=None):
    d = ImageDraw.Draw(img)
    for b in items:
        d.ellipse([x, y+4, x+36, y+40], fill=badge or col); d.text((x+8, y+4), "✓", font=F("Inter-Bold.otf", 30), fill="white" if badge is None else col)
        d.text((x+58, y), b, font=F("Inter-SemiBold.otf", size), fill=ink); y += gap
    return y

# ---------- layouts ----------
def T1(p):
    c = COL[p["prod"]]; img = photo(p["prod"], W, H); img = img.filter(ImageFilter.GaussianBlur(1.2))
    gradient_top(img, c, 820, 245)
    k = kicker(img, p["kicker"], 60, 60, c, fg=c, bg=(255, 255, 255))
    y = headline(img, p["lines"], 60, k + 28, 118, "white", W - 120, shade=True)
    by = laptop(img, sheet(*p["shot"]), 500, max(y + 40, 600), 900)
    d = ImageDraw.Draw(img); d.rectangle([0, H-170, W, H], fill=c); chips(img, H-95, c, dark=True)
    note(img, "Example data is fictional · Zyrah Studio", H-148, (255, 255, 255))
    return img

def T4(p):
    c = COL[p["prod"]]; img = Image.new("RGB", (W, H), c); img.paste(photo(p["prod"], W, 660), (0, 0))
    d = ImageDraw.Draw(img); d.rounded_rectangle([0, 560, W, H+80], 70, fill=c)
    kicker(img, p["kicker"], 60, 56, c, fg=c, bg="white")
    n = len(p["lines"]); hs = 92 if n < 3 else 82
    s = fitim(sheet(*p["shot"]), 840, 400 + (60 if n < 3 else 0))
    yb = card(img, s, 500, 330, pad=14)
    need = int(hs*1.07)*n + 26 + 64*len(p["ticks"])
    extra = max(0, (H - 170) - yb - need - 40)
    y = headline(img, p["lines"], 60, yb + 34 + int(extra*0.45), hs, "white", W - 120)
    ticks(img, p["ticks"], 60, y + 26 + int(extra*0.2), c, "white", size=34, gap=64, badge="white")
    d = ImageDraw.Draw(img); d.rectangle([0, H-170, W, H], fill=c); chips(img, H-95, c, dark=True)
    note(img, "Example data is fictional · Zyrah Studio", H-148, (255, 255, 255))
    return img

def T2(p):
    c = COL[p["prod"]]; img = Image.new("RGB", (W, H), c)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    ld.ellipse([380, -260, 1180, 540], fill=(255, 255, 255, 26)); ld.ellipse([-320, 900, 380, 1600], fill=(255, 255, 255, 18)); img.paste(lay, (0, 0), lay)
    k = kicker(img, p["kicker"], 60, 60, c, fg=c, bg="white")
    y = headline(img, p["lines"], 60, k + 26, 112, "white", W - 120)
    nt = len(p["ticks"]); avail = (H - 190) - (y + 30) - (nt*62 + 70)
    s = fitim(sheet(*p["shot"]), 860, min(avail, 760))
    used = s.height + 32 + 44 + nt*62; extra = max(0, (H - 190) - (y + 30) - used)
    yb = card(img, s, 500, y + 30 + extra//3, pad=16)
    ticks(img, p["ticks"], 90, yb + 44, c, "white", size=38, gap=62, badge="white")
    d = ImageDraw.Draw(img); d.rectangle([0, H-170, W, H], fill=(0, 0, 0, 0)) if False else None
    chips(img, H-95, c, dark=True)
    note(img, "Example data is fictional · Zyrah Studio", H-148, (255, 255, 255))
    return img

def T3(p):
    c = COL[p["prod"]]; img = Image.new("RGB", (W, H), (248, 243, 235)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 18], fill=c)
    k = kicker(img, p["kicker"], 60, 56, c)
    y = headline(img, p["lines"], 60, k + 24, 108, (28, 34, 44), W - 120)
    d = ImageDraw.Draw(img); yy = y + 24
    for i, it in enumerate(p["items"], 1):
        d.ellipse([60, yy, 116, yy+56], fill=c); f = F("Inter-Black.otf", 32)
        d.text((88 - d.textlength(str(i), font=f)/2, yy+8), str(i), font=f, fill="white")
        fi, _ = fit(d, it, "Inter-SemiBold.otf", 40, W - 220); d.text((140, yy+4), it, font=fi, fill=(28, 34, 44)); yy += 82
    s = fitim(sheet(*p["shot"]), 860, H - 210 - (yy + 30) - 36)
    card(img, s, 500, yy + 30 + max(0, (H - 210 - (yy + 30) - s.height - 28)//2), pad=14)
    d = ImageDraw.Draw(img); d.rectangle([0, H-120, W, H], fill=c); chips(img, H-95, c, dark=True)
    note(img, "Example data is fictional · Zyrah Studio", H-148, (110, 110, 110))
    return img

LAY = dict(T1=T1, T2=T2, T3=T3, T4=T4)
# shots: (file, crop)
S = lambda f, c=(0, 0, 1, 1): (f, c)
HERO = dict(P03=(UP+"_etsy_upload/P03-HERO-teal.jpg", (0.19, 0.335, 0.81, 0.80)),
            P04=(UP+"_etsy_upload/P04/P04-HERO-A-plum.jpg", (0.19, 0.335, 0.81, 0.80)),
            P01=(UP+"_etsy_upload/p01_rework/P01-HERO-A.png", (0.17, 0.28, 0.83, 0.80)),
            P02=(UP+"products/P02_Home_Bakery_Pricing/images/P02-PIN5.png", (0.095, 0.465, 0.90, 0.80)))
PINS = [
 dict(id="ZS-R7-A", prod="R7", lay="T1", kicker="Moving budget planner", lines=["Know what your", "move will cost"], shot=S("c_R7_4-04.png", (0, 0, 1, 0.6)),
      title="Moving Budget Planner Spreadsheet | Moving Cost Calculator Excel & Google Sheets",
      desc="Plan your moving budget by category, compare mover quotes and see spent vs left before moving day. This moving budget planner works in Excel and Google Sheets and includes an expense log, a moving checklist and a box log. Example data is fictional."),
 dict(id="ZS-R7-B", prod="R7", lay="T3", kicker="Moving checklist", lines=["5 moving costs", "people forget"], items=["Deposits and first month's rent", "Utility setup and connection fees", "Packing supplies and tape", "Cleaning before you hand back keys", "Truck fuel and parking"],
      shot=S("c_R7_13-13.png", (0, 0, 1, 0.4)),
      title="Moving Costs Checklist | Hidden Moving Expenses to Budget For",
      desc="Moving costs add up fast: deposits, utility connection fees, packing supplies, cleaning and fuel. Track every one in a moving budget spreadsheet with a checklist and an expense log, for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R7-C", prod="R7", lay="T2", kicker="Moving planner", lines=["Your move on", "one phone screen"], ticks=["Days to move and budget left", "Selected mover and quote", "Tasks done and boxes packed"], shot=S("c_R7_2-02.png", (0, 0, 1, 0.72)),
      title="Moving Planner Spreadsheet | Moving Checklist, Budget and Box Tracker",
      desc="One summary page shows days to move, budget left, your selected mover and how many tasks and boxes are done. Moving planner spreadsheet with checklist, expense log and box log for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R7-D", prod="R7", lay="T4", kicker="Moving cost compare", lines=["Will the new place", "cost more a month?"], ticks=["Current vs new rent", "Utilities, parking, transport", "See the yearly difference"], shot=S("c_R7_12-12.png"),
      title="Moving Cost Comparison Spreadsheet | New Home Monthly Budget Calculator",
      desc="Compare what you pay now with what the new home will cost each month: rent, utilities, internet, parking and transport, with the yearly difference. Part of a moving budget planner for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R2-A", prod="R2", lay="T1", kicker="Home renovation planner", lines=["Plan your whole", "renovation in", "one spreadsheet"], shot=S("c_R2_2-02.png"),
      title="Home Renovation Planner Spreadsheet | Remodel Budget and Task Tracker Google Sheets",
      desc="Plan a kitchen, bathroom or whole-house renovation room by room: tasks with dates, budget vs spent per room, materials to order and a dashboard. Home renovation planner for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R2-B", prod="R2", lay="T4", kicker="Renovation timeline", lines=["When will your", "renovation be", "finished?"], ticks=["Dates build the timeline", "26-week Gantt-style view", "Overdue tasks flagged"], shot=S("c_R2_7-07.png", (0, 0, 1, 0.62)),
      title="Renovation Timeline Template | Remodel Schedule Gantt Chart Spreadsheet",
      desc="Enter each task's dates and a 26-week Gantt-style timeline builds itself, with overdue tasks flagged. Renovation schedule template inside a home renovation planner for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R2-C", prod="R2", lay="T2", kicker="Renovation task list", lines=["Every renovation", "task in one list"], ticks=["Tasks, dates and status", "Budget vs spent per room", "What to order next"], shot=S("c_R2_4-04.png", (0, 0, 1, 0.5)),
      title="Renovation Task List Spreadsheet | Room by Room Remodel Checklist Template",
      desc="Keep every renovation task in one list with dates and status, then see budget vs spent per room and what materials to order next. Remodel checklist and planner for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R2-D", prod="R2", lay="T3", kicker="Renovation budget", lines=["Renovation budget", "by room"], items=["Set a budget for every room", "Add tasks with dates", "List the materials to order", "See budget vs spent per room"], shot=S("c_R2_3-03.png"),
      title="Room by Room Renovation Budget Spreadsheet | Kitchen and Bathroom Remodel Planner",
      desc="Split your remodel budget by room, add tasks with dates, list materials to order and watch budget vs spent per room. Kitchen and bathroom renovation planner for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R3-A", prod="R3", lay="T1", kicker="Renovation budget tracker", lines=["Keep your remodel", "on budget"], shot=S("c_R3_2-2.png", (0, 0, 1, 0.56)),
      title="Renovation Budget Tracker | Simple Remodel Expense Spreadsheet Excel & Google Sheets",
      desc="Set a budget per category, log every payment and see planned vs spent, what is left and what is over plan. A simple renovation budget tracker for kitchen or bathroom remodels in Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R3-B", prod="R3", lay="T2", kicker="Remodel budget", lines=["Where did the", "renovation money go?"], ticks=["12 budget categories", "Expense log with payments", "Planned vs spent chart"], shot=S("c_R3_2-2.png", (0, 0.60, 1, 0.99)),
      title="Remodel Budget Spreadsheet | Planned vs Spent Chart for Home Renovation",
      desc="See where your renovation money went with 12 categories, an expense log and a planned vs spent chart that updates as you add payments. Remodel budget spreadsheet for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R3-C", prod="R3", lay="T3", kicker="Renovation budget", lines=["Remodel budget", "mistakes to avoid"], items=["No contingency set aside", "Forgetting permits and fees", "Not logging small purchases", "Mixing up planned and spent", "Ignoring a category going over"], shot=S("c_R3_3-3.png", (0, 0, 1, 0.42)),
      title="Renovation Budget Mistakes | How to Track Remodel Costs in a Spreadsheet",
      desc="Common remodel budget mistakes: no contingency, forgotten permits and fees, small purchases never logged and categories quietly going over. Track it all in a renovation budget tracker for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R3-D", prod="R3", lay="T4", kicker="Renovation expense log", lines=["Log every payment,", "see what is left"], ticks=["Date, vendor and amount", "Receipt kept: yes or no", "Over plan turns orange"], shot=S("c_R3_3-3.png", (0, 0, 1, 0.45)),
      title="Home Renovation Expense Log | Remodel Payment Tracker Spreadsheet",
      desc="Log each renovation payment with date, vendor, amount and whether you kept the receipt. The tracker adds it up by category and flags what is over plan. Remodel expense spreadsheet for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P06-A", prod="P06", lay="T1", kicker="Homeschool transcript", lines=["Homeschool records", "made simple"], shot=S("c_P06_3-03.png", (0, 0, 1, 0.62)),
      title="Homeschool Transcript Template | High School Records, GPA and Gradebook Spreadsheet",
      desc="Keep homeschool high school records in one spreadsheet: courses and credits, GPA and weighted GPA, a weighted gradebook, attendance and hours, and a one-page transcript. Excel and Google Sheets. Example student is fictional."),
 dict(id="ZS-P06-B", prod="P06", lay="T4", kicker="Homeschool transcript", lines=["A one-page", "homeschool", "transcript"], ticks=["Courses, credits and GPA", "Weighted GPA", "Ready to print"], shot=S("c_P06_2-02.png", (0, 0, 1, 0.52)),
      title="Homeschool High School Transcript Template | Weighted GPA and Credits, Printable",
      desc="Turn your course list into a clean one-page homeschool transcript with credits, GPA and weighted GPA, ready to print. Homeschool transcript template and gradebook for Excel and Google Sheets. Example student is fictional."),
 dict(id="ZS-P06-C", prod="P06", lay="T2", kicker="Homeschool gradebook", lines=["Gradebook with", "weighted grades"], ticks=["Set category weights", "Log every assignment", "Course grade updates"], shot=S("c_P06_5-05.png", (0, 0, 1, 0.62)),
      title="Homeschool Gradebook Spreadsheet | Weighted Grades for High School Courses",
      desc="Set category weights for each course, log every assignment and see the course grade update. Homeschool gradebook inside a transcript and GPA spreadsheet for Excel and Google Sheets. Example student is fictional."),
 dict(id="ZS-P06-D", prod="P06", lay="T3", kicker="Homeschool high school", lines=["Records to keep", "for high school"], items=["Transcript with credits and GPA", "Course descriptions", "Grades and gradebook", "Attendance and hours", "Test scores and activities"], shot=S("c_P06_3-03.png", (0, 0, 1, 0.4)),
      title="Homeschool Records Checklist | What to Keep for High School and College Applications",
      desc="Homeschool high school records worth keeping: transcript with credits and GPA, course descriptions, grades, attendance hours, test scores and activities. Keep them in one homeschool transcript spreadsheet for Excel and Google Sheets. Example student is fictional."),
 dict(id="ZS-P01-A", prod="P01", lay="T1", kicker="Contractor estimate template", lines=["Quote every job", "with confidence"], shot=HERO["P01"],
      title="Contractor Estimate Spreadsheet | Job Costing Template for Remodelers Excel & Google Sheets",
      desc="Price a remodel job: materials, loaded labor, subcontractors and permits, then set your margin to get the quote price. Contractor estimate and job costing spreadsheet for small contractors and handymen. Example data is fictional."),
 dict(id="ZS-P01-B", prod="P01", lay="T4", kicker="Job costing", lines=["Estimate vs actual", "on every job"], ticks=["Materials, labor, subs, permits", "Change orders tracked", "Forecast profit"], shot=HERO["P01"],
      title="Job Cost Tracker for Small Contractors | Estimate vs Actual Spreadsheet",
      desc="See whether a job is still profitable while it runs: actual costs, approved change orders and forecast profit against your estimate. Job cost tracker for small remodelers and general contractors. Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P02-A", prod="P02", lay="T1", kicker="Bakery pricing", lines=["Price every bake", "for profit"], shot=HERO["P02"],
      title="Bakery Pricing Spreadsheet | Cake and Cookie Price Calculator for Home Bakers",
      desc="Know what to charge for every cake, cupcake and cookie: ingredient cost per item, your time, packaging and fees, then a suggested price. Bakery pricing spreadsheet for home bakers in Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P02-B", prod="P02", lay="T4", kicker="Home bakery", lines=["What should a", "cupcake cost?"], ticks=["Ingredient cost per recipe", "Time, packaging and fees", "Printable price list"], shot=HERO["P02"],
      title="Home Bakery Price List Template | Recipe Cost and Cupcake Pricing Calculator",
      desc="Enter ingredients once, build recipes and get a suggested price for every item plus a printable bakery price list. Recipe cost calculator for cottage and home bakeries in Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P03-A", prod="P03", lay="T1", kicker="Home build budget", lines=["Home build budget", "without surprises"], shot=HERO["P03"],
      title="Home Build Budget Spreadsheet | New Construction Cost Tracker Excel & Google Sheets",
      desc="Keep your home build or major renovation on budget: forecast final cost, contingency left, allowances against real selections and builder bids side by side. Homeowner budget spreadsheet. Example data is fictional."),
 dict(id="ZS-P03-B", prod="P03", lay="T4", kicker="Home construction", lines=["Track change orders", "and builder draws"], ticks=["Forecast final cost", "Allowances vs real choices", "Builder bids compared"], shot=HERO["P03"],
      title="Home Construction Budget Tracker | Change Order and Builder Bid Spreadsheet",
      desc="Log change orders, draws and payments with your builder and see the forecast final cost update. Home construction budget tracker with allowances and bid comparison for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P04-A", prod="P04", lay="T1", kicker="Embroidery pricing", lines=["Price embroidery", "orders right"], shot=HERO["P04"],
      title="Embroidery Pricing Calculator Spreadsheet | Stitch Rate and Cost Quote Template",
      desc="Work out what to charge for custom embroidery: price by your real costs or your stitch rate, compare the margin and print a client quote with deposit. Excel and Google Sheets. Example rates are placeholders, not industry rates."),
 dict(id="ZS-P04-B", prod="P04", lay="T4", kicker="Embroidery business", lines=["Are you charging", "enough for", "embroidery?"], ticks=["Cost-based or stitch rate", "Profit and margin per order", "Client quote with deposit"], shot=HERO["P04"],
      title="Embroidery Business Pricing Spreadsheet | Machine Embroidery Profit Calculator",
      desc="Not sure your embroidery prices cover your time and machine? Compare cost-based and stitch-rate pricing, add setup and rush fees and see profit per order. Excel and Google Sheets. Example rates are placeholders, not industry rates."),
]

if __name__ == "__main__":
    queue = []
    for p in PINS:
        assert len(p["title"]) <= 100 and len(p["desc"]) <= 500, (p["id"], len(p["title"]), len(p["desc"]))
        img = LAY[p["lay"]](p); img.convert("RGB").save(f"{OUT}/{p['id']}.png", optimize=True)
        queue.append(dict(id=p["id"], product=p["prod"], image=RAW + p["id"] + ".png", title=p["title"], desc=p["desc"], url=URL[p["prod"]], board=BOARD[p["prod"]]))
        print(p["id"], p["lay"], len(p["title"]), len(p["desc"]))
    json.dump(queue, open(f"{OUT}/queue_batch2.json", "w"), indent=1, ensure_ascii=False)
