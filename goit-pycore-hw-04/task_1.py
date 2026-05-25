
def total_salary(path):
    total_amount = 0
    developers_count = 0

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    name, salary = line.split(',')
                    total_amount += float(salary)
                    developers_count += 1
                except ValueError:
                    print(f"Warning: Invalid data format in line: {line}")
                    continue

        if developers_count == 0:
            return 0, 0

        average_salary = total_amount / developers_count
        return total_amount, average_salary

    except FileNotFoundError:
        print(f"Error: File at path '{path}' not found.")
        return 0, 0

#  CREATE FILE 
data = """Alex Korp,3000
Nikita Borisenko,2000
Sitarama Raju,1000"""

with open("salary_file.txt", "w", encoding="utf-8") as f:
    f.write(data)

#  CALL FUNCTION AND PRINT RESULT
total, average = total_salary("salary_file.txt")
print(f"Total salary: {total}, Average salary: {average}")