#!/usr/bin/env python3
"""Render entry.png (1024x1024) for make.fun news-image-20261122.
Dense one-image digest of world news from Sunday 22 November 2026.
Original code for this entry; renders with Pillow + DejaVu fonts.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 1024
BG = (13, 20, 32)
PANEL = (19, 28, 44)
INK = (238, 242, 247)
SUB = (168, 182, 200)
FAINT = (110, 124, 144)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

f_title   = F("DejaVuSans-Bold.ttf", 44)
f_kicker  = F("DejaVuSans-Bold.ttf", 15)
f_sub     = F("DejaVuSans.ttf", 14)
f_cat     = F("DejaVuSans-Bold.ttf", 14)
f_head    = F("DejaVuSans-Bold.ttf", 13)
f_ctx     = F("DejaVuSans.ttf", 11)
f_foot    = F("DejaVuSans.ttf", 10)

# (category, colour, [(headline, context), ...])
BLOCKS = [
    ("WORLD", (231, 76, 60), [
        ("COP31 ends without a climate deal in Antalya",
         "194 delegations reject the 'Antalya Pact'; fossil-fuel language blocked after 2 weeks"),
        ("Ukrainian sea drones hit Russian corvette in Libya",
         "Libya: 6 drones, 2 struck the Merkury at Benghazi naval base; serious damage reported"),
        ("Russian missile strike on Kryvyi Rih kills 2, wounds ~60",
         "A 7-year-old boy and a woman, 20, killed; six children among the injured, Kyiv says"),
        ("Russian cargo ship Sparta II burns in Finnish waters",
         "121 m military-logistics vessel drifted into Finnish waters after reported drone hit"),
        ("Bahrain says Iran struck civilian industrial site in Sitra",
         "Fire at the facility; UKMTO also reports a tanker incident in the Gulf of Oman"),
        ("ICJ rules Myanmar committed genocide against Rohingya",
         "Landmark Hague judgment; Myanmar challenges the ruling and regional rebuke"),
        ("Thousands march in Istanbul over seizure of Sozcu TV",
         "Protesters rally against the state takeover of the opposition broadcaster"),
        ("Fire at Indonesian candy factory: 3 dead, dozens missing",
         "Rescue teams search the wreckage as families wait for news of missing workers"),
    ]),
    ("POLITICS", (155, 89, 182), [
        ("World weighs Trump-Xi-Putin Shenzhen declaration",
         "First trilateral summit: nuclear-risk pledge and UN reform, but no word on Ukraine"),
        ("UK and EU strike post-Brexit reset deal",
         "Food trade, youth mobility and linked carbon markets; London sees up to GBP 17bn/yr"),
        ("Eisenkot condemns West Bank settler attacks",
         "Opposition leader calls violence 'Jewish terrorism' as coalition talks stall in Israel"),
        ("Israeli forces kill 2 in Gaza amid West Bank attacks",
         "Settlers torch vehicles and daub racist slogans across the occupied West Bank"),
        ("Nepal PM Balendra Shah starts first India visit",
         "Meets Modi on Monday; energy, trade and connectivity top the agenda in New Delhi"),
        ("Bangladesh arrests 773 in two Dhaka operations",
         "Crackdown follows nationwide political violence; 181 tied to banned Awami League"),
        ("Trump orders contractors to clear answers with White House",
         "Firms must consult before replying to Congress or risk losing federal contracts"),
        ("Spain poll: PP and Vox projected at 210 of 350 seats",
         "Survey a week before the 29 November general election puts the right far ahead"),
    ]),
    ("ECONOMY", (243, 156, 18), [
        ("AI-led selloff: Nasdaq -10% in worst week since 2020",
         "S&P 500 falls 8.6% into correction; Dow posts its worst week since March 2020"),
        ("$12 trillion wiped from global stocks since 6 Oct peak",
         "AJ Bell tally: selloff spreads from chips to commodities, banks and world markets"),
        ("Nvidia plunges on reported SEC accounting probe",
         "Shares -14% Friday, -23% on the week, days after strong earnings and CEO's exit"),
        ("VIX fear gauge jumps 26% to 35.89; sentiment 'extreme fear'",
         "CNN Fear & Greed index closes at 10 as forced selling hits shares, gold and crypto"),
        ("Gold slides 8.9% to about $3,540 an ounce",
         "Oil and bitcoin fall too: 'nowhere to hide' in a week of forced selling"),
        ("Taiwan stocks crash 17.5%, worst week since 1990",
         "Asia's AI supply-chain markets take the heaviest blows in the global rout"),
        ("US week ahead: confidence, PCE inflation, GDP revision",
         "Holiday-shortened week puts the Fed's December decision in the spotlight"),
    ]),
    ("TECH", (52, 152, 219), [
        ("UN talks on killer robots end without binding rules",
         "Geneva delegates extend autonomous-weapons discussions two more years, to 2028"),
        ("Signal moves to block AI assistants from private chats",
         "New safeguards restrict screenshots and screen access by on-device AI agents"),
        ("$44bn in notes to fund Nvidia chips for SpaceX",
         "Apollo and Goldman lead what they call the largest GPU financing executed to date"),
        ("Tencent open-sources 770B-parameter Hy4 model",
         "Downloadable weights released, with licence limits for large service providers"),
        ("Trump threatens tax on data centres built abroad",
         "US debate grows over an 'AI bailout' and a bill easing rules for data centres"),
        ("Kodak SlideTag: keychain photo frame and tracker",
         "1.54-inch colour E Ink display works with Apple Find My and Google Find Hub"),
        ("NASA tests onboard AI to aim satellites autonomously",
         "JPL's Dynamic Targeting on CogniSAT-6 picks clear-sky views without human input"),
    ]),
    ("SCIENCE", (26, 188, 156), [
        ("BepiColombo reaches Mercury after 8-year journey",
         "ESA-JAXA craft enters orbit; engineers check an engine burn that ended early"),
        ("Code-breaking maths finds a pulsar in 10 hours",
         "Lattice search spots PSR J1622-7204 spinning 261x/sec in 15 years of Fermi data"),
        ("SpaceX: two launches, one pad, 32 hours apart",
         "NROL-136 lifts off from Vandenberg just 32h 3m after the previous mission"),
        ("Sweetener study links erythritol to higher stroke risk",
         "Genetic analysis: ~25% higher odds of ischaemic stroke with higher levels"),
        ("GLP-1 drugs could free farmland the size of Italy",
         "Modelling study maps the land-use payoff if weight-loss drugs cut food demand"),
        ("OpenAI launches MedChemBench for drug research",
         "99 medicinal-chemistry problems; reconstruction beats selection in early tests"),
    ]),
    ("SPORT", (46, 204, 113), [
        ("Alcaraz beats Zverev to win first ATP Finals title",
         "6-2, 7-6 in Turin as the Spaniard dethrones the world number one"),
        ("Verstappen wins the Las Vegas Grand Prix",
         "Piastri takes a podium after a masterclass in overtaking under the lights"),
        ("Liverpool rout Man United 4-0 at Anfield",
         "Yoro's 8th-minute red card dooms Pochettino's United debut; Wirtz stars"),
        ("Marquez clinches eighth MotoGP crown in Portimao",
         "Ninth place seals a 10th world title after erasing a 102-point deficit"),
        ("Simeone sets La Liga wins record with Atletico",
         "3-0 at Getafe is his 345th league win, passing Luis Aragones at the top"),
        ("Werder Bremen thrash HSV 4-0 in the Nordderby",
         "Njinmah scores twice after the break at a jubilant Weserstadion"),
        ("Boca Juniors lift the Copa Sudamericana",
         "2-0 win over Atletico Mineiro seals the continental trophy for Boca"),
        ("Price wins Grand Slam of Darts in Wolverhampton",
         "Gerwyn Price beats Gian van Veen 16-11 for his fourth Grand Slam title"),
    ]),
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- header ----
d.rectangle([0, 0, W, 86], fill=(8, 13, 22))
d.rectangle([0, 86, W, 90], fill=(231, 76, 60))
d.text((18, 8), "THE WORLD IN ONE IMAGE  -  SUNDAY", font=f_kicker, fill=(243, 156, 18))
d.text((16, 22), "22 NOVEMBER 2026", font=f_title, fill=INK)
tw = d.textlength("44 STORIES  -  ONE DAY  -  SIX SECTIONS", font=f_kicker)
d.text((W - 18 - tw, 16), "44 STORIES  -  ONE DAY", font=f_kicker, fill=INK)
tw2 = d.textlength("SIX SECTIONS", font=f_kicker)
d.text((W - 18 - tw2, 38), "SIX SECTIONS", font=f_kicker, fill=SUB)
d.text((18, 68), "Climate talks collapse, drones strike in Libya, markets rout - the day the world made news.",
       font=f_sub, fill=SUB)

def wrap_px(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def fit_px(text, font, maxw):
    if d.textlength(text, font=font) <= maxw:
        return text
    while text and d.textlength(text + "...", font=font) > maxw:
        text = text[:-1]
    return text.rstrip(" .,;:") + "..."

def draw_block(x, y, col_w, name, colour, items):
    d.rounded_rectangle([x, y, x + col_w, y + 21], radius=4, fill=colour)
    d.text((x + 8, y + 3), name, font=f_cat, fill=(10, 14, 20))
    cnt = f"{len(items)} STORIES"
    cw = d.textlength(cnt, font=f_cat)
    d.text((x + col_w - 8 - cw, y + 3), cnt, font=f_cat, fill=(10, 14, 20))
    y += 27
    for head, ctx in items:
        for ln in wrap_px(head, f_head, col_w - 4)[:2]:
            d.text((x + 2, y), ln, font=f_head, fill=INK)
            y += 15
        d.text((x + 2, y), fit_px(ctx, f_ctx, col_w - 4), font=f_ctx, fill=SUB)
        y += 13
        y += 5
    return y

COL_W = 488
TOP = 100
left_blocks  = [BLOCKS[0], BLOCKS[1], BLOCKS[2]]
right_blocks = [BLOCKS[3], BLOCKS[4], BLOCKS[5]]

y = TOP
for name, colour, items in left_blocks:
    y = draw_block(16, y, COL_W, name, colour, items) + 8
left_end = y
y = TOP
for name, colour, items in right_blocks:
    y = draw_block(520, y, COL_W, name, colour, items) + 8
right_end = y

print("left_end", left_end, "right_end", right_end)
assert max(left_end, right_end) <= 990, "overflow!"

# ---- footer ----
fy = 992
d.rectangle([0, fy - 6, W, H], fill=(8, 13, 22))
d.text((18, fy + 4),
       "Sources: Le Monde - Reuters - AP - ESA - NASA - AJ Bell - SpaceNews - ATP - reports of 22 Nov 2026. Compiled 23 Nov 2026.",
       font=f_foot, fill=FAINT)
ft = "make.fun - news-image-20261122"
twf = d.textlength(ft, font=f_foot)
d.text((W - 18 - twf, fy + 4), ft, font=f_foot, fill=FAINT)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
