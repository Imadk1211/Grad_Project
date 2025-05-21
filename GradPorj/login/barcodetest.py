import barcode
from IPython.display import display
from barcode.writer import ImageWriter
documentType = {
    "summertraining":10,
    "transcript":20,
    "transcriptenglish":21,
    "transcriptturkish":22,
    "education-certificateenglish":23,
    "education-certificateturkish":24,
    "healthreport":30,
    "graduationform":40,
    "courseenrollment":50,
    "leaveofabsence":60,
    "education-certificate":70,

}


def generate_barcode(student_number, document_id, date):
    # Format inputs
    student_number = str(student_number).zfill(7)  # Ensure 7 characters
    document_id = str(document_id).zfill(2)  # Ensure 2 characters
    date = str(date).zfill(6)  # Ensure 6 characters

    # Concatenate inputs
    barcode_data = student_number + document_id + date

    # Generate barcode
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(barcode_data, writer=ImageWriter())
    barcode_instance.save('barcode')  # Save barcode as PNG file

    return student_number + str(document_id) + str(date)

#def generate_barcode(student_number, document_id, date):
#    # Format inputs
#    student_number = str(student_number).zfill(7)  # Ensure 7 characters
#    document_id = str(document_id).zfill(2)  # Ensure 2 characters
#    date = str(date).zfill(6)  # Ensure 6 characters
#
#    # Concatenate inputs
#    barcode_data = student_number + document_id + date
#
#    # Generate barcode
#    code128 = barcode.get_barcode_class('code128')
#    barcode_instance = code128(barcode_data)
#    barcode_instance.save('barcode')
#
#    # Display the barcode image in Colab
#    display(barcode_instance.render())
#    return student_number + str(document_id) + str(date)
#
## Example usage
generate_barcode('S123456', 10, 220101)

