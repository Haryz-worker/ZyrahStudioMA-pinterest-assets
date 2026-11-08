"""Batch 3 pin generator (8 Nov 2026): 20 pins, new angles, layouts and crops. Reuses the drawing code of make_pins4.py."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_pins4 as m
S, HERO, RAW, URL, BOARD, OUT = m.S, m.HERO, m.RAW, m.URL, m.BOARD, m.OUT
PINS = [
 dict(id="ZS-R7-E", prod="R7", lay="T4", kicker="Moving day budget", lines=["How much does a", "move really cost?"], ticks=["12 moving cost categories", "Compare up to 5 mover quotes", "Net cost after deposits"], shot=S("c_R7_3-03.png"),
      title="Moving Cost Calculator Spreadsheet | Mover Quote Comparison Excel & Google Sheets",
      desc="Add up what your move will really cost: movers or truck, packing, deposits, utility setup and cleaning. Compare up to 5 mover quotes and see the net cost after refundable deposits. Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R7-F", prod="R7", lay="T2", kicker="First apartment", lines=["First apartment", "budget and checklist"], ticks=["Deposits and first rent", "42-task moving checklist", "Box log by room"], shot=S("c_R7_4-04.png", (0, 0, 1, 0.8)),
      title="First Apartment Moving Budget Spreadsheet | Move Out Checklist and Costs",
      desc="Moving into a first apartment? Budget deposits, first rent, utility setup and furniture, follow a dated moving checklist and number your boxes by room. Spreadsheet for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R7-G", prod="R7", lay="T3", kicker="Moving checklist", lines=["Moving timeline", "8 weeks out"], items=["Set your move date and budget", "Get and compare mover quotes", "Book the truck or movers", "Pack and number your boxes", "Notify banks, mail and utilities"], shot=S("c_R7_13-13.png", (0, 0, 1, 0.5)),
      title="Moving Checklist Spreadsheet | Moving Timeline and Change of Address List",
      desc="Follow a moving timeline from 8 weeks before to the first week after, with due dates calculated from your move date and a who-to-notify list for your change of address. Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R2-E", prod="R2", lay="T2", kicker="Kitchen remodel", lines=["Kitchen remodel", "planner"], ticks=["Typical kitchen task list", "Materials to order", "Budget vs spent"], shot=S("c_R2_2-02.png", (0, 0, 1, 0.7)),
      title="Kitchen Remodel Planner Spreadsheet | Renovation Tasks, Materials and Budget",
      desc="Plan a kitchen remodel with a ready task list you can copy into your plan, materials to order, a timeline and budget vs spent. Renovation planner for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R2-F", prod="R2", lay="T3", kicker="Bathroom remodel", lines=["Bathroom remodel", "checklist"], items=["Set a budget for the room", "List every task with dates", "Order materials on time", "Track what you spend"], shot=S("c_R2_4-04.png", (0, 0, 1, 0.55)),
      title="Bathroom Remodel Checklist Spreadsheet | DIY Renovation Planner",
      desc="Plan a bathroom remodel step by step: tasks with dates, materials to order, budget for the room and what you have spent. DIY renovation planner for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R2-G", prod="R2", lay="T1", kicker="Renovation dashboard", lines=["See your whole", "renovation at a", "glance"], shot=S("c_R2_11-11.png"),
      title="Renovation Dashboard Spreadsheet | Home Project Tracker Excel & Google Sheets",
      desc="One dashboard shows tasks done, overdue tasks, planned finish date and budget vs spent per room. Home renovation project tracker for DIY renovators in Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R3-E", prod="R3", lay="T3", kicker="Kitchen remodel budget", lines=["Kitchen remodel", "budget categories"], items=["Demolition and haul-away", "Materials and fixtures", "Labour and trades", "Plumbing and electrical", "Contingency fund"], shot=S("c_R3_2-2.png", (0, 0, 1, 0.56)),
      title="Kitchen Remodel Budget Spreadsheet | Renovation Cost Categories Template",
      desc="Split a kitchen remodel budget into categories like demolition, materials, labour, plumbing, electrical and contingency, then see planned vs spent. Renovation budget tracker for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R3-F", prod="R3", lay="T1", kicker="Renovation contingency", lines=["Is your remodel", "over budget?"], shot=S("c_R3_3-3.png", (0, 0, 1, 0.5)),
      title="Renovation Contingency Budget Tracker | Remodel Cost Overrun Spreadsheet",
      desc="Set a contingency percentage, log every payment and see right away which category is over plan and how much contingency is left. Renovation budget tracker for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-R3-G", prod="R3", lay="T2", kicker="Bathroom remodel budget", lines=["Bathroom remodel", "cost tracker"], ticks=["Budget per category", "200-row expense log", "Print on one page"], shot=S("c_R3_2-2.png", (0, 0.55, 1, 1)),
      title="Bathroom Remodel Cost Tracker Spreadsheet | Home Improvement Budget Template",
      desc="Track a bathroom remodel: budget per category, a 200-row expense log and a planned vs spent chart, printable on one page. Home improvement budget template for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P06-E", prod="P06", lay="T2", kicker="Homeschool credits", lines=["Homeschool credit", "and GPA tracker"], ticks=["Courses and credits", "GPA and weighted GPA", "One-page transcript"], shot=S("c_P06_2-02.png", (0, 0, 1, 0.6)),
      title="High School Credit Tracker Spreadsheet | Homeschool Courses, GPA and Credits",
      desc="Track high school credits and GPA for a homeschool student: courses, credits, weighted GPA and a one-page transcript. Homeschool records spreadsheet for Excel and Google Sheets. Example student is fictional."),
 dict(id="ZS-P06-F", prod="P06", lay="T4", kicker="Homeschool attendance", lines=["Homeschool", "attendance and", "hours log"], ticks=["Days and hours per course", "Totals by month", "Printable record"], shot=S("c_P06_5-05.png", (0, 0, 1, 0.6)),
      title="Homeschool Attendance Log and Hours Tracker Spreadsheet | Excel & Google Sheets",
      desc="Log homeschool attendance days and course hours, see totals by month and print a record. Part of a homeschool transcript, gradebook and attendance spreadsheet for Excel and Google Sheets. Example student is fictional."),
 dict(id="ZS-P06-G", prod="P06", lay="T1", kicker="Homeschool transcript", lines=["College-ready", "homeschool records"], shot=S("c_P06_3-03.png", (0, 0.3, 1, 1)),
      title="Homeschool Course Descriptions Template | Transcript Records for College Applications",
      desc="Keep course descriptions, grades, credits and GPA together so a homeschool transcript is ready when college applications start. Excel and Google Sheets spreadsheet. Example student is fictional."),
 dict(id="ZS-P01-C", prod="P01", lay="T2", kicker="Handyman estimate", lines=["Handyman estimate", "and job costing"], ticks=["Materials and labor", "Markup and margin", "Client quote"], shot=HERO["P01"],
      title="Handyman Estimate Spreadsheet | Small Contractor Quote and Job Cost Template",
      desc="Build a handyman or small contractor estimate with materials, labor, subs and permits, set your markup and print a client quote, then compare estimate vs actual. Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P01-D", prod="P01", lay="T3", kicker="Contractor templates", lines=["Contractor job", "costing in 4 steps"], items=["Enter the estimate", "Add actual costs as you go", "Log change orders", "Check forecast profit"], shot=HERO["P01"],
      title="Contractor Bid and Change Order Tracker | Construction Job Costing Spreadsheet",
      desc="Job costing in four steps: enter the estimate, add actual costs, log approved change orders and check forecast profit. Construction bid and job cost spreadsheet for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P02-C", prod="P02", lay="T2", kicker="Cake pricing", lines=["How to price", "a custom cake"], ticks=["Ingredient cost per cake", "Time, packaging and fees", "Order quote"], shot=HERO["P02"],
      title="Cake Pricing Calculator Spreadsheet | Custom Cake Order Quote for Home Bakers",
      desc="Price a custom cake from its real ingredient cost, your time, packaging and fees, then create an order quote for the client. Cake pricing calculator for home bakers in Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P02-D", prod="P02", lay="T3", kicker="Cottage bakery", lines=["Cottage bakery", "pricing steps"], items=["List your ingredients once", "Build each recipe", "Add time and packaging", "Get a suggested price"], shot=HERO["P02"],
      title="Cottage Bakery Pricing Spreadsheet | Recipe Costing and Price List Template",
      desc="Cost every recipe in four steps: list ingredients once, build the recipe, add time and packaging and get a suggested price for your bakery price list. Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P03-C", prod="P03", lay="T2", kicker="Owner builder", lines=["Owner builder", "budget tracker"], ticks=["Forecast final cost", "Contingency left", "Bids side by side"], shot=HERO["P03"],
      title="Owner Builder Budget Spreadsheet | House Construction Cost Tracker",
      desc="Acting as your own general contractor? Track the budget by phase, compare builder and subcontractor bids and see contingency left. House construction cost tracker for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P03-D", prod="P03", lay="T3", kicker="Home build budget", lines=["Home build budget", "checklist"], items=["Set the total budget", "Add allowances per item", "Compare contractor bids", "Log change orders"], shot=HERO["P03"],
      title="Home Renovation Budget Spreadsheet | Allowance Tracker and Contractor Bid Comparison",
      desc="Set the total budget, add allowances per item, compare contractor bids and log change orders. Home renovation and home build budget spreadsheet for Excel and Google Sheets. Example data is fictional."),
 dict(id="ZS-P04-C", prod="P04", lay="T2", kicker="Embroidery quote", lines=["Embroidery quote", "with deposit"], ticks=["Price by stitch count", "Setup and rush fees", "Client quote"], shot=HERO["P04"],
      title="Embroidery Quote Template Spreadsheet | Custom Embroidery Price and Deposit Calculator",
      desc="Price a custom embroidery order by stitch count, add setup and rush fees and print a client quote with deposit. Embroidery pricing spreadsheet for Excel and Google Sheets. Example rates are placeholders, not industry rates."),
 dict(id="ZS-P04-D", prod="P04", lay="T3", kicker="Embroidery profit", lines=["Embroidery profit", "per order"], items=["Enter thread and stabilizer cost", "Add machine time", "Set your margin", "See profit per order"], shot=HERO["P04"],
      title="Machine Embroidery Profit Calculator | Stitch Count Cost Per Order Spreadsheet",
      desc="Work out profit per embroidery order: thread and stabilizer cost, machine time, setup and your margin. Machine embroidery profit calculator for Excel and Google Sheets. Example rates are placeholders, not industry rates."),
]
if __name__ == "__main__":
    queue = []
    for p in PINS:
        assert len(p["title"]) <= 100 and len(p["desc"]) <= 500, (p["id"], len(p["title"]), len(p["desc"]))
        img = m.LAY[p["lay"]](p); img.convert("RGB").save(f"{OUT}/{p['id']}.png", optimize=True)
        queue.append(dict(id=p["id"], product=p["prod"], image=RAW + p["id"] + ".png", title=p["title"], desc=p["desc"], url=URL[p["prod"]], board=BOARD[p["prod"]]))
        print(p["id"], p["lay"])
    json.dump(queue, open(f"{OUT}/queue_batch3.json", "w"), indent=1, ensure_ascii=False)
