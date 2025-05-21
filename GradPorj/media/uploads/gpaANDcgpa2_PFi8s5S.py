def calculate_gpa(grades, credits):

    # Multiply each grade by the corresponding credits, sum them up, and divide by the total credits.
    total_quality_points = sum(grade * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_quality_points / total_credits if total_credits else 0

def calculate_cgpa(all_grades, all_credits):
    # Flatten the list of grades and credits, since we need the total sum for CGPA calculation.
    flat_grades = [grade for semester in all_grades for grade in semester]
    flat_credits = [credit for semester in all_credits for credit in semester]

    return calculate_gpa(flat_grades, flat_credits)
