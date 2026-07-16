from datetime import date, timedelta

# Test 2026/08/16
d1 = date(2026, 8, 16)
print(f'2026/08/16 is {d1.strftime("%A")}')
print(f'29 days before: {(d1 - timedelta(days=29)).strftime("%Y/%m/%d %A")}')
print()

# Test 2026/08/02
d2 = date(2026, 8, 2)
print(f'2026/08/02 is {d2.strftime("%A")}')
print(f'29 days before: {(d2 - timedelta(days=29)).strftime("%Y/%m/%d %A")}')
print()

# From scenarios, the rule should adjust Sunday to Friday
# So 2026/07/18 (Monday) should adjust to 2026/07/17 (Friday)
d3 = date(2026, 7, 18)
print(f'2026/07/18 is {d3.strftime("%A")} - should adjust to 2026/07/17 (Friday)')

# And 2026/07/04 should adjust to 2026/07/03 (Friday)
d4 = date(2026, 7, 4)
print(f'2026/07/04 is {d4.strftime("%A")} - should adjust to 2026/07/03 (Friday)')
