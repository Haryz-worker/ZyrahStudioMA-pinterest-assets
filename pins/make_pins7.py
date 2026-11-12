"""Batch 5 pin generator (12 Nov 2026): 30 pins for the 10 published 2027 printables (L01-L13).
Sources: listing images (hero / closeup / printed mockup, 2000x2000 JPG). Three layouts:
  A = headline band + hero image card, B = full-bleed mockup + headline band, C = closeup card + 3 ticks.
Run: python3 make_pins7.py SRC_DIR OUT_DIR   (SRC_DIR holds L01/L01_01_hero_ZyrahStudioMA.jpg ...)"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = sys.argv[2] if len(sys.argv) > 2 else "out"
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"
def F(n, s): return ImageFont.truetype(FD + n, s)
W, H = 1000, 1500
RAW = "https://raw.githubusercontent.com/Haryz-worker/ZyrahStudioMA-pinterest-assets/main/pins/"
B_CAL = "BOARD_CAL"   # replaced by build step with the real Pinterest board id
B_HOME = "BOARD_HOME"

# code: (listing id, slug url, board key, accent colour, source files)
P = {
 "L01": ("4615787913", "2027-weekly-home-planner-printable-pre", B_HOME, (22, 92, 82)),
 "L02": ("4615801748", "2027-monthly-calendar-printable", B_CAL, (60, 76, 110)),
 "L03": ("4615801804", "2027-monthly-planner-printable-portrait", B_CAL, (60, 76, 110)),
 "L04": ("4615788571", "2027-year-at-a-glance-printable-one-page", B_CAL, (60, 76, 110)),
 "L06": ("4615788663", "2027-weekly-planner-printable-inserts", B_CAL, (60, 76, 110)),
 "L08": ("4615803578", "2027-weekly-meal-planner-printable-with", B_HOME, (22, 92, 82)),
 "L09": ("4615803642", "2027-family-calendar-printable-family", B_HOME, (22, 92, 82)),
 "L10": ("4615803720", "2027-habit-tracker-printable-dated", B_HOME, (22, 92, 82)),
 "L11": ("4615790445", "2027-wall-planner-printable-full-year", B_CAL, (60, 76, 110)),
 "L13": ("4615804006", "2027-52-week-savings-challenge-printable", B_HOME, (22, 92, 82)),
}
SRCN = {"hero": "01_hero", "close": "03_closeup", "mock": None}
MOCK = {"L01": "07", "L02": "06", "L03": "06", "L04": "05", "L06": "06", "L08": "06", "L09": "07", "L10": "06", "L11": "06", "L13": "06"}

def img_path(code, kind):
    if kind == "hero": n = "01_hero"
    elif kind == "close": n = "03_closeup"
    else: n = MOCK[code] + "_printed_mockup"
    return f"{SRC}/{code}/{code}_{n}_ZyrahStudioMA.jpg"

# (pin id suffix, code, layout, source kind, kicker, headline lines, ticks, title, description)
PINS = [
 ("A", "L01", "A", "hero", "2027 home planner", ["Your whole year of", "home care, planned"], None,
  "2027 Weekly Home Planner Printable | Pre-Filled Home Maintenance and Cleaning Schedule",
  "A dated 2027 weekly planner that is already filled in: seasonal home maintenance jobs, a cleaning focus, US holidays and a weekly checklist for every week. Fillable PDF in US Letter and A4, Monday or Sunday start. Instant download."),
 ("B", "L01", "B", "mock", "Pre-filled weekly planner", ["Know what to do", "around the house", "this week"], None,
  "Home Maintenance Checklist 2027 | Weekly Cleaning Schedule Planner Printable PDF",
  "53 dated weekly pages with two seasonal home maintenance jobs and a cleaning zone already written in, plus alarm and HVAC filter reminders. Print it or type into the PDF. Home management planner for 2027."),
 ("C", "L01", "C", "close", "Every week is started", ["Seasonal jobs", "change weekly"], ["2 maintenance jobs a week", "A cleaning zone with 3 tasks", "Blank lines for your own tasks"],
  "Printable Home Management Planner 2027 | Fillable Weekly Home Care Pages",
  "Spring windows, fall gutters, monthly smoke alarm tests: each week of 2027 comes with seasonal home care jobs and a short cleaning list, with space for your own tasks. Fillable PDF planner, Letter and A4."),

 ("A", "L02", "A", "hero", "2027 calendar", ["Big boxes,", "clean look"], None,
  "2027 Monthly Calendar Printable | Landscape Lined or Unlined, Monday or Sunday Start",
  "A clean landscape 2027 monthly calendar, one month per page with big day boxes. Lined or unlined, Monday or Sunday start, with US holidays or none. 16 fillable PDFs in US Letter and A4. Instant download."),
 ("B", "L02", "B", "mock", "Print for the fridge or desk", ["Your 2027 month", "at a glance"], None,
  "Printable 2027 Calendar | Simple Monthly Wall or Desk Calendar PDF",
  "Print a month at a time for the fridge, desk or clipboard. 12 landscape monthly pages for 2027 with mini previous and next months and lightly shaded weekends. Fillable PDF, Letter and A4."),
 ("C", "L02", "C", "close", "Pick your version", ["16 versions in", "one download"], ["Lined or unlined boxes", "Monday or Sunday start", "US holidays or none"],
  "2027 Fillable Calendar PDF | Monthly Calendar with US Holidays, Letter and A4",
  "Choose the style that fits: lined or unlined day boxes, Monday or Sunday start, US federal holidays shown or hidden. Click a day and type, or print. 2027 monthly calendar printable."),

 ("A", "L03", "A", "hero", "2027 monthly planner", ["Plan the month", "on one page"], None,
  "2027 Monthly Planner Printable | Portrait Calendar with To Do List and Notes",
  "A portrait 2027 monthly planner: calendar on top, then top priorities, dates to remember, a to-do list and notes on the same page. Monday or Sunday start, Letter and A4, fillable PDF. Instant download."),
 ("B", "L03", "B", "mock", "Month on one page", ["Calendar, to-dos", "and notes together"], None,
  "Monthly Planner Printable 2027 | Month on One Page with Priorities and To Do List",
  "Run your month from one page: the calendar, five top priorities, dates to remember, 13 to-do checkboxes and a notes box. Printable and fillable 2027 monthly planner PDF for binders and clipboards."),
 ("C", "L03", "C", "close", "Plan, do, review", ["More than a", "calendar page"], ["5 top priorities", "13 checkbox to-do list", "Dates to remember and notes"],
  "Planner Inserts 2027 Monthly | Portrait Calendar with Goals and Checklist, PDF",
  "Type into the day boxes and lists or print and write by hand. 12 dated portrait pages for 2027 with holiday and no-holiday versions, US Letter and A4. Instant download."),

 ("A", "L04", "A", "hero", "2027 year at a glance", ["All 12 months", "on one sheet"], None,
  "2027 Year at a Glance Printable | One Page Yearly Calendar, Letter, A4, A3 and 11x17",
  "The whole of 2027 on one page, easy to read from a distance. Portrait and landscape, Monday or Sunday start, US holidays highlighted or plain. 32 PDFs in US Letter, A4, A3 and 11 x 17. Instant download."),
 ("B", "L04", "B", "mock", "Wall, fridge or desk", ["See the whole", "year at once"], None,
  "One Page 2027 Calendar | Year at a Glance Wall Calendar Printable PDF",
  "A one-page 2027 yearly calendar for the wall, fridge, desk mat or front of a binder. Print at home or at a copy shop in A3 or 11 x 17. Simple, clear and printable."),
 ("C", "L04", "C", "close", "Pick your size", ["Four paper sizes,", "one download"], ["US Letter and A4", "A3 and 11 x 17 for the wall", "Portrait or landscape"],
  "2027 Yearly Calendar Printable | Full Year on One Page with US Holidays",
  "US federal holidays highlighted and listed at the bottom, or a plain version with a notes line. Monday or Sunday start. A year-at-a-glance 2027 calendar you can print big."),

 ("A", "L06", "A", "hero", "2027 weekly planner", ["One clean page", "for every week"], None,
  "2027 Weekly Planner Printable Inserts | Dated Week on One Page, A5, Half Letter, A4, Letter",
  "A minimalist dated 2027 weekly planner: seven day boxes, top 3 priorities and notes on every page. 53 weeks, four paper sizes, Monday or Sunday start, fillable PDF. Instant download."),
 ("B", "L06", "B", "mock", "Planner inserts", ["Fill your", "binder for 2027"], None,
  "A5 Planner Inserts 2027 | Weekly Planner Refill Pages Printable, Half Letter and A4",
  "Print the size you need: US Letter, A4, A5 or Half Letter. One week on one page with space for work, study and everyday planning. Dated 2027 weekly pages for ring planners and binders."),
 ("C", "L06", "C", "close", "Week on one page", ["Simple, dated", "and fillable"], ["Seven lined day boxes", "Top 3 priorities each week", "53 pages, Monday or Sunday start"],
  "Minimalist Weekly Planner 2027 PDF | Dated Weekly Pages for Work and School",
  "Type straight into the PDF or print and write. US holidays are noted, and the first and last pages include a few days of the neighbouring years so no week is cut in half."),

 ("A", "L08", "A", "hero", "2027 meal planner", ["What's for dinner?", "Plan it by week"], None,
  "2027 Weekly Meal Planner Printable with Grocery List | Dated Menu Planner PDF",
  "A dated 2027 weekly meal planner with the grocery list on the same page: breakfast, lunch, dinner and snacks for seven days, then a shopping list sorted by store section. Fillable PDF, Letter and A4."),
 ("B", "L08", "B", "mock", "Meal plan + shopping list", ["Plan meals,", "then shop once"], None,
  "Meal Planner and Grocery List Printable 2027 | Weekly Menu Planner for Families",
  "The meal grid and a 29-line checkbox grocery list share one page. Includes a use-up-first box, prep-ahead box, a family favorites page and a freezer and pantry inventory."),
 ("C", "L08", "C", "close", "Grocery list inside", ["Shop by store", "section"], ["7-day meal grid", "Grocery list in 7 sections", "Use up first and prep ahead"],
  "Weekly Menu Planner 2027 | Fillable Meal Plan and Shopping List PDF, Letter and A4",
  "53 dated weekly pages, 55 pages per PDF, Sunday or Monday start. Major US holidays are noted on the day so you can plan the big meals. Printable 2027 family meal planner."),

 ("A", "L09", "A", "hero", "2027 family calendar", ["One place for", "the whole family"], None,
  "2027 Family Calendar Printable | Family Command Center, Monthly and Weekly Schedule",
  "A 2027 family command center: monthly pages with a color key for up to 6 people, plus dated weekly pages with a row per person, a dinner row and chores. A3 and 11 x 17 wall pages included."),
 ("B", "L09", "B", "mock", "Command center", ["Everyone knows", "who is where"], None,
  "Family Command Center 2027 | Printable Family Planner with Chore Chart and Contacts",
  "Monthly overview, 53 weekly family pages, a 12-chore chart and an important contacts page in one download. Fillable PDFs in US Letter and A4, Sunday or Monday start."),
 ("C", "L09", "C", "close", "Weekly family grid", ["A row for", "each person"], ["5 color-coded person rows", "Dinner and chores rows", "Appointments, bills and birthdays"],
  "Family Organizer 2027 Printable | Weekly Family Schedule for Busy Households",
  "Keep appointments, practices, dinners and chores in one place. Print for the fridge or wall (A3 and 11 x 17 included) or type into the PDF and print each week."),

 ("A", "L10", "A", "hero", "2027 habit tracker", ["Tick off your", "habits all year"], None,
  "2027 Habit Tracker Printable | Dated Monthly Habit Tracker with Year in Pixels, Fillable PDF",
  "Twelve dated monthly habit grids for 2027 with up to 12 habits a day, a monthly review and a year in pixels page. Click the checkboxes on your computer or print. US Letter and A4."),
 ("B", "L10", "B", "mock", "New year goals", ["Build one", "small habit", "at a time"], None,
  "Habit Tracker 2027 | Monthly Habit Chart and Goal Planner Printable PDF",
  "A new-year habit tracker with the correct days and weekday letters for every month. Weekends are shaded and each month has an intention line and three review boxes."),
 ("C", "L10", "C", "close", "Year in pixels", ["365 squares,", "one per day"], ["12 habit rows per month", "Monthly review boxes", "Habits and goals page"],
  "Year in Pixels 2027 Printable | Mood and Habit Tracker, Letter and A4",
  "Colour one square a day for a picture of your whole year. Includes a colour key, a habits and goals planning page and 12 monthly habit trackers. Fillable PDF."),

 ("A", "L11", "A", "hero", "2027 wall planner", ["The whole year", "on one big sheet"], None,
  "2027 Wall Planner Printable | Full Year Calendar Poster, A1, A2, A3, 24x36, 18x24, 11x17",
  "A large 2027 wall planner with a box to write in for every day. Two layouts, eight paper sizes from US Letter to A1 and 24 x 36 in, Monday or Sunday start. Vector PDFs that stay sharp when printed big."),
 ("B", "L11", "B", "mock", "Plan leave, terms and trips", ["See the year", "at a glance"], None,
  "Year Planner 2027 Wall Calendar Printable | Office and Family Annual Planner",
  "Plan leave, school terms, shifts, projects or trips on one sheet. Weekends are shaded and US federal holidays are in colour. Print at home or send to a copy shop for poster sizes."),
 ("C", "L11", "C", "close", "Two layouts", ["Pick the layout", "that suits you"], ["Weekday-aligned rows", "Date columns, days 1 to 31", "24 PDFs in one ZIP"],
  "Large Wall Planner 2027 PDF | Yearly Planner Poster Printable for Home and Office",
  "Weekday-aligned layout makes weekends form clear stripes; the date-columns layout lists days 1 to 31 down the page. Not fillable: made for writing by hand."),

 ("A", "L13", "A", "hero", "2027 savings challenge", ["Save money,", "one week at a time"], None,
  "2027 52 Week Savings Challenge Printable | Dated Money Saving Tracker, 1378, 5000 and 10000 Goals",
  "A dated 2027 52-week savings challenge with every deposit and running total filled in. Ten plans from the classic 1,378 dollar challenge to 10,000, plus biweekly paycheck versions. Fillable PDF in Letter and A4."),
 ("B", "L13", "B", "mock", "New year money goal", ["Build your", "emergency fund", "in 52 weeks"], None,
  "Savings Challenge Printable 2027 | Weekly Money Saving Chart for Emergency Fund or Vacation",
  "Tick a checkbox each week as you save. Classic, reverse, flat 50 a week, write-your-own and 26-paycheck challenges are all included. A tracker, not financial advice."),
 ("C", "L13", "C", "close", "Deposits already worked out", ["Every week is", "dated for 2027"], ["Classic, reverse and 10K plans", "Biweekly paycheck versions", "Running total column"],
  "52 Week Money Challenge 2027 | Printable Savings Tracker with Dates and Checkboxes",
  "Week 1 starts Friday, January 1, 2027 and week 52 starts December 24. Choose a plan, print it and tick off each deposit. Sinking fund and savings goal tracker, PDF."),
]

CHIPS = ["PRINTABLE PDF", "INSTANT DOWNLOAD"]

def fit(d, text, name, size, maxw):
    f = F(name, size)
    while d.textlength(text, font=f) > maxw: size -= 2; f = F(name, size)
    return f, size

def shadow(img, box, radius, blur=24, off=(0, 16), alpha=110):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(lay)
    sd.rounded_rectangle([box[0]+off[0], box[1]+off[1], box[2]+off[0], box[3]+off[1]], radius, fill=(0, 0, 0, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(blur)); img.paste(lay, (0, 0), lay)

def kicker(img, text, x, y, col):
    d = ImageDraw.Draw(img); f = F("Inter-Bold.otf", 28); t = text.upper(); w = d.textlength(t, font=f) + 44
    d.rounded_rectangle([x, y, x+w, y+52], 26, fill="white"); d.text((x+22, y+10), t, font=f, fill=col)
    return y + 52

def headline(img, lines, x, y, size, fill, maxw):
    d = ImageDraw.Draw(img)
    for ln in lines:
        f, s = fit(d, ln, "InterDisplay-Black.otf", size, maxw); d.text((x, y), ln, font=f, fill=fill); y += int(s * 1.08)
    return y

def chips(img, y, col):
    d = ImageDraw.Draw(img); f = F("Inter-Bold.otf", 30)
    ws = [d.textlength(t, font=f) + 56 for t in CHIPS]; x = 500 - (sum(ws) + 20) / 2
    for t, w_ in zip(CHIPS, ws):
        d.rounded_rectangle([x, y, x+w_, y+66], 33, fill="white"); d.text((x+28, y+15), t, font=f, fill=col); x += w_ + 20

def footer(img, col, note="Zyrah Studio · Dated for 2027"):
    d = ImageDraw.Draw(img); d.rectangle([0, H-170, W, H], fill=col)
    f = F("Inter-Medium.otf", 24); d.text(((W - d.textlength(note, font=f)) / 2, H-148), note, font=f, fill="white"); chips(img, H-95, col)

def card(img, im, cx, y, pad=14, radius=22):
    x = cx - (im.width + 2*pad)//2; box = (x, y, x+im.width+2*pad, y+im.height+2*pad)
    shadow(img, box, radius); d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius, fill="white", outline=(215, 215, 215), width=2); img.paste(im, (x+pad, y+pad))
    return box[3]

def square(code, kind, side):
    im = Image.open(img_path(code, kind)).convert("RGB")
    return im.resize((side, side), Image.LANCZOS)

def layout_A(p, col):
    img = Image.new("RGB", (W, H), col); k = kicker(img, p[4], 60, 60, col)
    y = headline(img, p[5], 60, k + 28, 112, "white", W - 120)
    top = y + 36; side = min(880, H - 170 - 28 - top - 28)
    yb = card(img, square(p[1], p[3], side), 500, top)
    footer(img, col); return img

def layout_B(p, col):
    img = Image.new("RGB", (W, H), col); k = kicker(img, p[4], 60, 60, col)
    y = headline(img, p[5], 60, k + 28, 108, "white", W - 120)
    top = max(y + 30, 480); vis = H - 170 - top
    im = square(p[1], p[3], 1000); off = max(0, 1000 - vis)
    img.paste(im.crop((0, off, 1000, off + vis)), (0, top))
    footer(img, col); return img

def layout_C(p, col):
    img = Image.new("RGB", (W, H), (247, 242, 233)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 16], fill=col)
    k = kicker(img, p[4], 60, 56, col); d.rounded_rectangle([60, 56, 60 + d.textlength(p[4].upper(), font=F("Inter-Bold.otf", 28)) + 44, 108], 26, fill=col)
    d.text((82, 66), p[4].upper(), font=F("Inter-Bold.otf", 28), fill="white")
    y = headline(img, p[5], 60, 140, 104, (28, 34, 44), W - 120)
    top = y + 24; side = min(760, H - 170 - 24 - top - 28 - 60 * len(p[6]) - 20)
    yb = card(img, square(p[1], p[3], side), 500, top)
    d = ImageDraw.Draw(img); yy = yb + 36
    for b in p[6]:
        d.ellipse([70, yy+4, 106, yy+40], fill=col); d.text((78, yy+4), "✓", font=F("Inter-Bold.otf", 30), fill="white")
        d.text((128, yy), b, font=F("Inter-SemiBold.otf", 36), fill=(28, 34, 44)); yy += 60
    footer(img, col); return img

LAY = {"A": layout_A, "B": layout_B, "C": layout_C}
queue = []
for p in PINS:
    pid = f"ZS-27{p[1]}-{p[0]}"
    code = p[1]; col = P[code][3]
    img = LAY[p[2]](p, col); img.save(f"{OUT}/{pid}.png", optimize=True)
    lid, slug, board, _ = P[code]
    queue.append(dict(id=pid, product=code, image=RAW + pid + ".png", title=p[7], desc=p[8],
                      url=f"https://www.etsy.com/listing/{lid}/{slug}", board=board))
json.dump(queue, open(f"{OUT}/queue_batch5.json", "w"), indent=1, ensure_ascii=False)
print(len(queue), "pins")
