def calculate_gpa(grades, credits):
    """
    Calculate the GPA for a single semester.
    
    Parameters:
    grades (list): A list of grades received, each grade being a number (e.g., A=4, B=3).
    credits (list): A list of credits for each course corresponding to the grades list.

    Returns:
    float: The GPA for the semester.
    """
    # Multiply each grade by the corresponding credits, sum them up, and divide by the total credits.
    total_quality_points = sum(grade * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_quality_points / total_credits if total_credits else 0

def calculate_cgpa(all_grades, all_credits):
    """
    Calculate the CGPA across multiple semesters.

    Parameters:
    all_grades (list of lists): A list containing lists of grades for each semester.
    all_credits (list of lists): A list containing lists of credits for each semester.

    Returns:
    float: The CGPA for all semesters.
    """
    # Flatten the list of grades and credits, since we need the total sum for CGPA calculation.
    flat_grades = [grade for semester in all_grades for grade in semester]
    flat_credits = [credit for semester in all_credits for credit in semester]

    return calculate_gpa(flat_grades, flat_credits)

# Example usage:
# Let's say we have grades for two semesters. For simplicity, grades are on a scale from 0 to 4.
# First semester grades and credits
grades_semester_1 = [4, 3, 3.7]  # A, B, A-
credits_semester_1 = [3, 3, 4]    # 3 credit course, 3 credit course, 4 credit course

# Second semester grades and credits
grades_semester_2 = [3.3, 3.7, 4]  # B+, A-, A
credits_semester_2 = [4, 3, 2]     # 4 credit course, 3 credit course, 2 credit course

# Calculate GPA for each semester
gpa_semester_1 = calculate_gpa(grades_semester_1, credits_semester_1)
gpa_semester_2 = calculate_gpa(grades_semester_2, credits_semester_2)

# Calculate CGPA for all completed semesters
cgpa = calculate_cgpa([grades_semester_1, grades_semester_2], [credits_semester_1, credits_semester_2])

gpa_semester_1, gpa_semester_2, cgpa
