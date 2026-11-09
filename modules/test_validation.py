from modules.patients import (
    validate_name,
    validate_age,
    validate_gender,
    validate_phone
)

print("\n===== TEST INPUT VALIDATION =====")

name = validate_name(input("Enter patient name: "))
age = validate_age()
gender = validate_gender()
phone = validate_phone()

print("\n===== VALIDATED DETAILS =====")
print("Name:", name)
print("Age:", age)
print("Gender:", gender)
print("Phone:", phone)