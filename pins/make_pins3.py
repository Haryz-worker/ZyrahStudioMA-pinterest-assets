import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SP = "/tmp/claude-0/-home-claude/dc18d2b8-82c1-5aec-ae1f-a02b12610ea9/scratchpad"
OUT = f"{SP}/pins3/out"; os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, s)
W, H = 1000, 1500
RAW = "https://raw.githubusercontent.com/Haryz-worker/ZyrahStudioMA-pinterest-assets/main/pins/"
B = dict(P01="1144195917770567138", P02="1144195917770583205", P03="1144195917770583210", R2="1144195917770583210",
         R3="1144195917770583210", P04="1144195917770567153", R7="1144195917770669627", P06="1144195917770669629")
U = dict(P01="https://www.etsy.com/listing/4573254943/contractor-job-costing-spreadsheet",
         P02="https://www.etsy.com/listing/4579324688/home-bakery-pricing-spreadsheet-recipe",
         P03="https://www.etsy.com/listing/4579770626/home-build-budget-spreadsheet-renovation",
         P04="https://www.etsy.com/listing/4579978345/embroidery-pricing-spreadsheet-machine",
         R2="https://www.etsy.com/listing/4598103933/home-renovation-planner-spreadsheet-room",
         R3="https://www.etsy.com/listing/4599376778/renovation-budget-tracker-spreadsheet",
         R7="https://www.etsy.com/listing/4602943564/moving-budget-planner-excel-google",
         P06="https://www.etsy.com/listing/4603656166/homeschool-transcript-template-and")
COL = dict(P01=(30, 58, 95), P02=(150, 72, 92), P03=(28, 110, 110), R2=(176, 102, 44), R3=(52, 96, 150),
           P04=(96, 62, 128), R7=(47, 75, 138), P06=(59, 91, 71))
# (key, product, style, src, crop, headline lines, bullets / answer, title, desc)
PINS = [
 ("ZS-P01-L1", "P01", "L", "p01h/ren/hi-02_t.png", (0, 0.02, 0.36, 0.55), ["Price a remodel", "job in minutes"],
  ["Materials, labor, subs, permits", "Target margin → quote price", "Prints a clean client quote"],
  "Contractor Estimate Template Excel | Remodel Job Pricing Spreadsheet",
  "Price a remodel job without guessing: list materials, loaded labor, subcontractors and permits, set your margin and get the quote price. Small contractor estimate template for Excel and Google Sheets with job costing, change orders and a client quote. Example data is fictional."),
 ("ZS-P01-Q1", "P01", "Q", "p01h/ren/hi-09_t.png", (0, 0.43, 0.40, 0.96), ["Is this job still", "making money?"],
  "Estimate vs actual, change orders and forecast profit on one summary.",
  "Job Costing Spreadsheet for Contractors | Estimate vs Actual Profit",
  "See if a job is still profitable while it runs: actual costs, approved change orders and forecast profit against your estimate. Job costing spreadsheet for small remodelers, handymen and general contractors. Excel and Google Sheets, instant download. Example data is fictional."),
 ("ZS-P02-L1", "P02", "L", "pins/ren/P02/pg-43.png", (0.04, 0.02, 0.80, 0.40), ["Your bakery", "price list, done"],
  ["Cost of every cake & cookie", "Suggested price for your margin", "Printable price list"],
  "Bakery Price List Template | Cake Pricing Spreadsheet for Home Bakers",
  "Know what to charge for every cake, cupcake and cookie: ingredient cost per item, your time, packaging and fees, then a suggested price and a printable price list. Bakery pricing spreadsheet for home and cottage bakers. Excel and Google Sheets. Example data is fictional."),
 ("ZS-P02-Q1", "P02", "Q", "pins/ren/P02/pg-44.png", (0.04, 0.02, 0.80, 0.78), ["How much should", "I charge for", "this cake?"],
  "Recipe cost + your time + fees → a price, and a custom order quote with deposit.",
  "How to Price Cakes | Cake Order Quote and Recipe Cost Calculator",
  "Stop guessing cake prices. Enter ingredients once, build recipes and products, and get a suggested price plus a custom order quote with deposit and balance. Recipe cost calculator for home bakeries in Excel and Google Sheets. Example data is fictional."),
 ("ZS-P03-L1", "P03", "L", "p03/render/dash-03.png", (0, 0.0, 0.66, 0.48), ["Build a house", "without budget", "surprises"],
  ["Forecast final cost", "Allowances vs real choices", "Builder bids compared"],
  "Home Build Budget Spreadsheet | New Construction Cost Tracker",
  "Keep your home build or major renovation on budget: forecast final cost, contingency left, allowances against your real selections and builder bids side by side. Homeowner budget spreadsheet for Excel and Google Sheets. Example data is fictional."),
 ("ZS-P03-Q1", "P03", "Q", "p03/render/coa3-09.png", (0, 0.07, 0.40, 0.31), ["What did that", "change order", "really cost?"],
  "Log every change order; only approved ones count in your forecast.",
  "Change Order Log for Homeowners | Home Renovation Budget Tracker",
  "Track change orders, draws and payments with your builder and see the forecast final cost update. Home renovation budget spreadsheet with allowances, bid comparison and a change order log. Excel and Google Sheets. Example data is fictional."),
 ("ZS-R2-L1", "R2", "L", "r2/pdf3/d-02_c.png", (0, 0, 1, 1), ["Plan your", "renovation", "room by room"],
  ["Tasks, dates & status", "Budget vs spent per room", "What to order next"],
  "Home Renovation Planner Spreadsheet | Room by Room Remodel Tracker",
  "Plan a kitchen, bathroom or whole-house renovation room by room: tasks with dates, budget vs spent per room, materials to order and a dashboard. Home renovation planner for Excel and Google Sheets. Example data is fictional."),
 ("ZS-R2-Q1", "R2", "Q", "r2/pdf3/t-07_c.png", (0, 0, 1, 1), ["When will my", "renovation be", "finished?"],
  "Your task dates build a 26-week timeline automatically.",
  "Renovation Timeline Template | Remodel Schedule Gantt Chart Spreadsheet",
  "See your renovation schedule at a glance: enter each task's dates and a 26-week Gantt-style timeline builds itself, with overdue tasks flagged. Renovation planner spreadsheet for Excel and Google Sheets. Example data is fictional."),
 ("ZS-R3-L1", "R3", "L", "r3/ren/after-2.png", (0.04, 0.12, 0.72, 0.52), ["Keep your", "remodel on", "budget"],
  ["Planned vs spent", "Over-plan turns orange", "One page, prints clean"],
  "Renovation Budget Tracker | Simple Remodel Expense Spreadsheet",
  "A simple renovation budget tracker: set a budget per category, log every payment and see planned vs spent, what is left and what is over plan. Kitchen or bathroom remodel expense spreadsheet for Excel and Google Sheets. Example data is fictional."),
 ("ZS-R3-Q1", "R3", "Q", "r3/ren/after-2.png", (0.04, 0.555, 0.72, 0.95), ["Where did the", "remodel money", "go?"],
  "Log each payment; the planned vs spent chart updates itself.",
  "Remodel Budget Tracker Spreadsheet | Planned vs Spent Chart",
  "See exactly where your renovation money went: 12 categories, an expense log and a planned vs spent chart that updates as you add payments. Renovation budget tracker for Excel and Google Sheets. Example data is fictional."),
 ("ZS-P04-L1", "P04", "L", "p04/render/hi-15.png", (0.47, 0.10, 1.0, 0.62), ["Price embroidery", "orders with", "confidence"],
  ["Cost-based or stitch rate", "Profit & margin per order", "Client quote with deposit"],
  "Machine Embroidery Pricing Calculator | Stitch Count Price Spreadsheet",
  "Work out what to charge for custom embroidery: price by your real costs or your stitch rate, compare the margin and print a client quote with deposit. Embroidery pricing spreadsheet for Excel and Google Sheets. Example rates are placeholders, not industry rates."),
 ("ZS-P04-Q1", "P04", "Q", "p04/render/hi-16.png", (0.55, 0.0, 1.0, 0.6), ["Am I charging", "enough for", "embroidery?"],
  "Compare two pricing methods and see the margin before you quote.",
  "How to Price Embroidery | Embroidery Business Profit Spreadsheet",
  "Not sure your embroidery prices cover your time and machine? Compare cost-based and stitch-rate pricing, add setup and rush fees and see profit per order. Embroidery business spreadsheet for Excel and Google Sheets. Example data is fictional."),
 ("ZS-R7-L1", "R7", "L", "r7/big/q2-02_t.png", (0, 0.0, 1.0, 0.62), ["Your whole", "move on one", "phone screen"],
  ["Days to move & budget left", "Selected mover & quote", "Tasks & boxes packed"],
  "Moving Budget Planner | Moving Cost Calculator Spreadsheet",
  "Know what your move will cost: compare mover quotes, plan 12 budget categories, log expenses and check it all on a phone summary. Moving budget planner for Excel and Google Sheets with checklist and box inventory. Example data is fictional."),
 ("ZS-R7-Q1", "R7", "Q", "r7/big/q5-05_t.png", (0, 0.02, 0.55, 0.38), ["How much does", "moving really", "cost?"],
  "Log every moving expense; spent and left update per category.",
  "Moving Expense Tracker | Relocation Budget Spreadsheet Excel",
  "Track every moving expense in one list: movers, deposits, first rent, utilities and more, with spent and left per category and net cost after deposits come back. Moving expense spreadsheet for Excel and Google Sheets. Example data is fictional."),
 ("ZS-P06-L1", "P06", "L", "p06/v2/ren/hi1_t.png", (0, 0.06, 0.6, 0.42), ["Homeschool", "records in", "one file"],
  ["Courses, credits & GPA", "Weighted gradebook", "One-page transcript"],
  "Homeschool Records Spreadsheet | High School Transcript and GPA",
  "Keep homeschool high school records in one spreadsheet: courses and credits, GPA and weighted GPA, a weighted gradebook, attendance and hours, and a one-page transcript. Excel and Google Sheets. Example student is fictional."),
 ("ZS-P06-Q1", "P06", "Q", "p06/v2/ren/hi21_t.png", (0, 0, 0.62, 0.50), ["Need course", "descriptions for", "college apps?"],
  "Your course list turns into a printable course descriptions page.",
  "Homeschool Course Descriptions Template | College Application Records",
  "Print homeschool course descriptions for college or dual-enrollment applications, next to a one-page transcript with weighted GPA. Homeschool transcript template and gradebook for Excel and Google Sheets. Example student is fictional."),
]

def fit(d, text, font_name, size, maxw):
    f = F(font_name, size)
    while d.textlength(text, font=f) > maxw: size -= 3; f = F(font_name, size)
    return f, size

def shot(src, crop, maxw, maxh):
    im = Image.open(f"{SP}/{src}").convert("RGB"); w0, h0 = im.size
    im = im.crop((int(crop[0]*w0), int(crop[1]*h0), int(crop[2]*w0), int(crop[3]*h0)))
    k = min(maxw / im.width, maxh / im.height)
    return im.resize((int(im.width*k), int(im.height*k)), Image.LANCZOS)

def card(img, im, x, y, pad=18, radius=22):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(lay)
    sd.rounded_rectangle([x+8, y+18, x+im.width+2*pad+8, y+im.height+2*pad+26], radius, fill=(0, 0, 0, 90))
    lay = lay.filter(ImageFilter.GaussianBlur(22)); img.paste(lay, (0, 0), lay)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x+im.width+2*pad, y+im.height+2*pad], radius, fill="white", outline=(215, 215, 215), width=2)
    img.paste(im, (x+pad, y+pad))
    return y + im.height + 2*pad

def style_L(p):
    key, prod, _, src, cr, lines, bullets = p[:7]
    c = COL[prod]; ink = (28, 34, 44)
    img = Image.new("RGB", (W, H), (247, 242, 233)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 16], fill=c)
    y = 70
    for ln in lines:
        f, s = fit(d, ln, "InterDisplay-Black.otf", 118, W - 140); d.text((70, y), ln, font=f, fill=ink); y += int(s * 1.08)
    d.rectangle([70, y + 14, 230, y + 24], fill=c)
    im = shot(src, cr, W - 140 - 36, (H - 150 - 3*66 - 50) - (y + 60) - 36)
    yb = card(img, im, (W - im.width - 36) // 2, y + 60)
    d = ImageDraw.Draw(img); fb = F("Inter-SemiBold.otf", 40); yy = yb + 50
    for b in bullets:
        d.ellipse([78, yy + 8, 112, yy + 42], fill=c); d.text((86, yy + 2), "✓", font=F("Inter-Bold.otf", 30), fill="white")
        d.text((134, yy), b, font=fb, fill=ink); yy += 66
    d.rectangle([0, H - 92, W, H], fill=c)
    ft = F("Inter-Bold.otf", 30); t = "EXCEL + GOOGLE SHEETS  ·  INSTANT DOWNLOAD"
    d.text(((W - d.textlength(t, font=ft)) / 2, H - 70), t, font=ft, fill="white")
    d.text((70, H - 132), "Example data is fictional · Zyrah Studio", font=F("Inter-Medium.otf", 24), fill=(110, 110, 110))
    return img

def style_Q(p):
    key, prod, _, src, cr, lines, answer = p[:7]
    c = COL[prod]
    img = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(img)
    top = 120 + len(lines) * 128
    d.rectangle([0, 0, W, top + 170], fill=c)
    y = 80
    for ln in lines:
        f, s = fit(d, ln, "InterDisplay-Black.otf", 120, W - 120)
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill="white"); y += int(s * 1.06)
    im = shot(src, cr, W - 120 - 36, H - y - 420)
    yb = card(img, im, (W - im.width - 36) // 2, y + 50)
    d = ImageDraw.Draw(img)
    fa = F("Inter-SemiBold.otf", 40); words = answer.split(); line = ""; yy = yb + 50; out = []
    for w_ in words:
        t = (line + " " + w_).strip()
        if d.textlength(t, font=fa) > W - 160: out.append(line); line = w_
        else: line = t
    out.append(line)
    for l in out: d.text(((W - d.textlength(l, font=fa)) / 2, yy), l, font=fa, fill=(28, 34, 44)); yy += 54
    f2 = F("Inter-Bold.otf", 32); chips = ["EXCEL + GOOGLE SHEETS", "INSTANT DOWNLOAD"]
    ws = [d.textlength(x, font=f2) + 56 for x in chips]; x = (W - sum(ws) - 20) / 2; cy = max(yy + 30, H - 190)
    for t, w_ in zip(chips, ws):
        d.rounded_rectangle([x, cy, x + w_, cy + 68], 34, fill=c); d.text((x + 28, cy + 16), t, font=f2, fill="white"); x += w_ + 20
    d.text((40, H - 50), "Example data is fictional · Zyrah Studio", font=F("Inter-Medium.otf", 24), fill=(120, 120, 120))
    return img, cy + 68

queue = []
for p in PINS:
    key, prod, st = p[:3]
    if st == "L": img = style_L(p); bottom = None
    else: img, bottom = style_Q(p)
    img.save(f"{OUT}/{key}.png", optimize=True)
    title, desc = p[7], p[8]
    assert len(title) <= 100 and len(desc) <= 500, key
    queue.append(dict(id=key, product=prod, image=RAW + key + ".png", title=title, desc=desc, url=U[prod], board=B[prod]))
    print(key, st, len(title), len(desc), bottom)
json.dump(queue, open(f"{OUT}/queue.json", "w"), indent=1, ensure_ascii=False)
