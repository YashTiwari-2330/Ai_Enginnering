# Remove duplicates from list

items = [1, 2, 3, 4, 5, 6, 1, 2, 3, "hello", "Hello"]

uniq_item = []

for item in items:
    if isinstance(item , str):
        item = item.lower()

    if item not in uniq_item:
        uniq_item.append(item)

print(uniq_item)
