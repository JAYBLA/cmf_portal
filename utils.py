from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template

from PyPDF2 import PdfReader, PdfWriter
from weasyprint import HTML
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# =====================================================
# CREATE A4 BACKGROUND PDF
# =====================================================


def create_background_pdf(image_uri):

    html = f"""
    <!doctype html>

    <html>

    <head>

        <meta charset="utf-8">


        <style>


            @page {{

                size: A4 portrait;

                margin: 0;

            }}


            html,
            body {{

                margin: 0;

                padding: 0;

                width: 210mm;

                height: 297mm;

            }}


            img {{

                display: block;

                width: 210mm;

                height: 297mm;

            }}


        </style>

    </head>


    <body>


        <img src="{image_uri}">


    </body>

    </html>
    """


    return HTML(
        string=html,
    ).write_pdf()

# =====================================================
# APPLY PAGE BACKGROUNDS
# =====================================================


def apply_document_backgrounds(
    content_pdf,
    header_bg,
    footer_bg,
    single_bg,
):

    # =========================================
    # READ CONTENT PDF
    # =========================================

    content_reader = PdfReader(
        BytesIO(content_pdf)
    )


    page_count = len(
        content_reader.pages
    )


    # =========================================
    # CREATE BACKGROUND PDFS
    # =========================================

    header_pdf = create_background_pdf(
        header_bg
    )


    footer_pdf = create_background_pdf(
        footer_bg
    )


    single_pdf = create_background_pdf(
        single_bg
    )


    # =========================================
    # READ BACKGROUND PDFS
    # =========================================

    header_reader = PdfReader(
        BytesIO(header_pdf)
    )


    footer_reader = PdfReader(
        BytesIO(footer_pdf)
    )


    single_reader = PdfReader(
        BytesIO(single_pdf)
    )


    # =========================================
    # PDF WRITER
    # =========================================

    writer = PdfWriter()


    # =========================================
    # PROCESS EACH PAGE
    # =========================================

    for index, content_page in enumerate(
        content_reader.pages
    ):

        # =====================================
        # SINGLE PAGE
        # =====================================

        if page_count == 1:

            background_page = (
                single_reader.pages[0]
            )


        # =====================================
        # FIRST PAGE
        # =====================================

        elif index == 0:

            background_page = (
                header_reader.pages[0]
            )


        # =====================================
        # LAST PAGE
        # =====================================

        elif index == page_count - 1:

            background_page = (
                footer_reader.pages[0]
            )


        # =====================================
        # MIDDLE PAGE
        # =====================================

        else:

            writer.add_page(
                content_page
            )

            continue


        # =====================================
        # BACKGROUND FIRST
        # CONTENT SECOND
        # =====================================

        background_page.merge_page(
            content_page
        )


        writer.add_page(
            background_page
        )


    # =========================================
    # WRITE FINAL PDF
    # =========================================

    output = BytesIO()


    writer.write(
        output
    )


    output.seek(0)


    return output.getvalue()