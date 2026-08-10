import csv
rows = list(csv.reader(open('pins.csv', encoding='utf-8-sig'), delimiter=';'))
head = rows[0]; col = {n:i for i,n in enumerate(head)}
no_date = [r for r in rows[1:] if len(r) > col['Datum'] and not r[col['Datum']].strip()]
print(f'Dátum nélküli pinek: {len(no_date)}')
for r in no_date:
    slug = r[col['URL']].replace('https://milesandflavors.com/','').strip('/')
    print(f"  pin{r[col['Pin #']]}  |  {r[col['Pin bold (vastag)']][:55]}  |  {slug}")
