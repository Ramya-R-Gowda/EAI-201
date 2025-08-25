def grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"

print("AI Grading Assistant")
name = input("Student name: ")
count = int(input("Total subjects: "))

subjects = []
total_obtained = 0
total_max = 0

for i in range(count):
    subject = input(f"\nSubject {i+1} name: ")
    marks = int(input(f"Marks obtained in {subject}: "))
    # Default max marks = 100
    max_marks_input = input(f"Max marks for {subject} (press Enter for 100): ")
    max_marks = int(max_marks_input) if max_marks_input.strip() else 100  

    percentage = (marks / max_marks) * 100 if max_marks > 0 else 0
    subjects.append((subject, marks, max_marks, percentage, grade(percentage)))

    total_obtained += marks
    total_max += max_marks

overall_percentage = (total_obtained / total_max) * 100 if total_max > 0 else 0

print(f"\nReport Card for {name}\n" + "="*40)
for subject, marks, max_marks, pct, grd in subjects:
    print(f"{subject}: {marks}/{max_marks} -> {pct:.2f}%  Grade: {grd}")

print("-"*40)
print(f"Total: {total_obtained}/{total_max}")
print(f"Overall Percentage: {overall_percentage:.2f}%")
print(f"Overall Grade: {grade(overall_percentage)}")
print("="*40)
