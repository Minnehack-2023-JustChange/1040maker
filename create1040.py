# Adapted from https://akdux.com/python/2020/10/31/python-fill-pdf-files/

import fillpdf
from fillpdf import fillpdfs
import pdfrw

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


# Creates an f1040sa PDF file in the current directory with given name and donation total (as a string)
def output_pdf(name, donation_total):
    fields = fillpdfs.get_form_fields('orig_f1040sa.pdf')
    
    fields['FEFF00660031005F0031005B0030005D'] = name  # Name Line 
    fields['FEFF00660031005F00320035005B0030005D'] = donation_total  # Line 11
    fields['FEFF00660031005F00320038005B0030005D'] = donation_total  # Line 14

    fill_pdf('orig_f1040sa.pdf', 'f1040sa.pdf', fields)

def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        if type(data_dict[key]) == bool:
                            if data_dict[key] == True:
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


# For testing
# if __name__ == '__main__':
#     output_pdf('Benjamin Lindeen', '100.00')