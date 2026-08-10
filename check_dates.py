import csv
rows = list(csv.reader(open('pins.csv', encoding='utf-8-sig'), delimiter=';'))
head = rows[0]; col = {n:i for i,n in enumerate(head)}
for label, date in [('MA (2026.06.21)', '2026.06.21'), ('HOLNAP (2026.06.22)', '2026.06.22')]:
    print(f'\n=== {label} ===')
    for r in rows[1:]:
        if len(r) > col['Datum'] and r[col['Datum']] == date:
            slug = r[col['URL']].replace('https://milesandflavors.com/','').strip('/')
            pin_no = r[col['Pin #']]
            bold = r[col['Pin bold (vastag)']][:55]
            t = r[col['Idopont']]
            print(f"  {t}  pin{pin_no}  |  {bold}  |  {slug}")
