import csv
import sys
import os
def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")
    
    if len(data) == 0:
        print("Error: The file has no assignment rows. Nothing to evaluate.")
        return
    # a) Scores must be 0-100
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Error: '{item['assignment']}' has score {item['score']}, outside the 0-100 range.")
            return

    # b) Weights: total 100, Formative 60, Summative 40
    total_weight = 0
    formative_weight = 0
    summative_weight = 0
    for item in data:
        total_weight += item['weight']
        if item['group'].strip().lower() == 'formative':
            formative_weight += item['weight']
        elif item['group'].strip().lower() == 'summative':
            summative_weight += item['weight']

    valid = True
    if total_weight != 100:
        print(f"Error: Total weight is {total_weight}, it must be exactly 100.")
        valid = False
    if formative_weight != 60:
        print(f"Error: Formative weight is {formative_weight}, it must be exactly 60.")
        valid = False
    if summative_weight != 40:
        print(f"Error: Summative weight is {summative_weight}, it must be exactly 40.")
        valid = False
    if not valid:
        return

    # c) Final grade and GPA
    formative_earned = 0
    summative_earned = 0
    for item in data:
        points = item['score'] * item['weight'] / 100
        if item['group'].strip().lower() == 'formative':
            formative_earned += points
        else:
            summative_earned += points

    total_grade = formative_earned + summative_earned
    gpa = (total_grade / 100) * 5.0

    # d) Pass/Fail: at least 50% in BOTH categories
    formative_pct = formative_earned / 60 * 100
    summative_pct = summative_earned / 40 * 100
    if formative_pct >= 50 and summative_pct >= 50:
        status = "PASSED"
    else:
        status = "FAILED"

    # e) Failed formatives (< 50) and the highest weight among them
    failed = []
    for item in data:
        if item['group'].strip().lower() == 'formative' and item['score'] < 50:
            failed.append(item)

    resubmit = []
    if len(failed) > 0:
        highest = failed[0]['weight']
        for item in failed:
            if item['weight'] > highest:
                highest = item['weight']
        for item in failed:
            if item['weight'] == highest:
                resubmit.append(item)

    # f) Print the results
    print(f"Formative: {formative_earned:.2f}/60 ({formative_pct:.2f}%)")
    print(f"Summative: {summative_earned:.2f}/40 ({summative_pct:.2f}%)")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}")
    print(f"Final Status: {status}")

    if len(resubmit) > 0:
        print("\nEligible for resubmission (failed formative with highest weight):")
        for item in resubmit:
            print(f" - {item['assignment']} (score {item['score']:.0f}, weight {item['weight']:.0f})")
    else:
        print("\nNo failed formative assignments. No resubmission needed.")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)
