from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas


def exportar_ticket_pdf(ticket_text, filename="ticket.pdf", ancho=58):
    page_width = ancho * mm
    lineas = ticket_text.splitlines()
    espacio_por_linea = 15
    margen_superior = 20
    margen_inferior = 20
    page_height = (len(lineas) * espacio_por_linea) + margen_superior + margen_inferior

    c = canvas.Canvas(filename, pagesize=(page_width, page_height))

    y = page_height - margen_superior
    c.setFont("Helvetica", 10)

    for linea in lineas:
        c.drawCentredString(page_width / 2, y, linea)
        y -= espacio_por_linea

    c.showPage()
    c.save()
