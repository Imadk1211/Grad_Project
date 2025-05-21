import barcode
from PIL import Image
from IPython.display import display

def generate_barcode(student_number, document_id, date):
    # Format inputs
    student_number = str(student_number).zfill(7)  # Ensure 7 characters
    document_id = str(document_id).zfill(2)  # Ensure 2 characters
    date = str(date).zfill(6)  # Ensure 6 characters

    # Concatenate inputs
    barcode_data = student_number + document_id + date

    # Generate barcode
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(barcode_data)
    barcode_instance.save('barcode22')

    # Display the barcode image in Colab
    #display(Image.open('/barcode.png'))

# Example usage
generate_barcode('S123456', 10, 220101)