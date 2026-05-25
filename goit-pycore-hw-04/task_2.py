def get_cats_info(path):
    cats_list = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    cat_id, name, age = line.split(',')
                    cats_list.append({"id": cat_id, "name": name, "age": age})
                except ValueError:
                    print(f"Error: Line has incorrect format: '{line}'")
                    continue
    except FileNotFoundError:
        print(f"Error: File at path '{path}' not found.")
        return []
    return cats_list
cats_info = get_cats_info("cats_info.txt")

# Pretty print each cat separately
for cat in cats_info:
    print(f"ID: {cat['id']} | Name: {cat['name']} | Age: {cat['age']}")


