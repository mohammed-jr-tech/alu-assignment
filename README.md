# ALU Transcript Generator

This project reads a student's grades from a CSV file. It works out the final grade and GPA, decides if the student passed or failed, and shows which assignments can be resubmitted. It also has a shell script that saves old grade files in an archive.

## Files

- `grade-evaluator.py` - the Python program that checks and calculates the grades.
- `organizer.sh` - the shell script that archives `grades.csv` and keeps a log.
- `grades.csv` - the grades data used by the program.

## CSV format

The CSV file has four columns:

    assignment,group,score,weight

- `assignment` is the name of the work.
- `group` is either Formative or Summative.
- `score` is the mark, from 0 to 100.
- `weight` is how much the work counts towards the final grade.

## How to run

Run the Python program:

    python grade-evaluator.py

When it asks for a file name, type `grades.csv`.

Run the shell script:

    bash organizer.sh

## Validation rules

The program checks the data before it calculates anything:

- Every score must be between 0 and 100.
- All the weights together must be exactly 100.
- The Formative weights must add up to exactly 60.
- The Summative weights must add up to exactly 40.

If something is wrong, the program prints a clear message and stops. It also shows a message if the file is missing, or if the file has no data.

## How the grades are worked out

1. Each assignment gives points: score x weight / 100.
2. Total grade = Formative points + Summative points (out of 100).
3. GPA = (Total grade / 100) x 5.0.
4. The student passes only if they get at least 50% in Formative AND at least 50% in Summative. If one category is below 50%, the student fails.

## Resubmission

A formative assignment with a score below 50 is a failed assignment. The student can only resubmit the failed formative assignment with the highest weight. If two or more failed assignments have the same highest weight, the program shows all of them.

## Example output

    --- Processing Grades ---
    Formative: 34.00/60 (56.67%)
    Summative: 26.00/40 (65.00%)
    Total Grade: 60.00/100
    GPA: 3.00
    Final Status: PASSED

    Eligible for resubmission (failed formative with highest weight):
     - Group Exercise (score 40, weight 20)
     - Functions and Debugging Lab (score 45, weight 20)

## The organizer script

When you run `organizer.sh`, it does these things:

1. Creates a folder called `archive` if it does not exist.
2. Renames `grades.csv` with the date and time, for example `grades_20261117-143012.csv`, and moves it into `archive`.
3. Creates a new empty `grades.csv`, ready for the next batch.
4. Adds a line to `organizer.log` with the time, the original file name and the new file name. The log keeps growing every time you run the script.