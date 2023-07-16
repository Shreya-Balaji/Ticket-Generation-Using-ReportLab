import reportlab
import pymysql
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess
from datetime import datetime
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table
from reportlab.lib import colors
import pytz
from reportlab.lib import styles
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

conn = pymysql.connect(
    user='root',
    password='123',
    database='project1'
)
cur = conn.cursor()

#generates ticket for whatever passengerid we pass
def generate_flight_ticket_pdf(passengerid):
    strpass=str(passengerid)
    sql='select pnr from reservation where passenger_id='+strpass
    cur.execute(sql)
    pnr=cur.fetchone()[0]
    pdf_file=pnr+"_flight_ticket.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.setFont("Helvetica-Bold", size=15)
    c.drawString(30, 760, 'Your ZenAir Itinerary - '+pnr)

    width, height = letter
    line_y_position = height - 40  # You can adjust this value as per your requirement
    c.setStrokeColorRGB(0, 0, 0)  # Set line color (black in this case)
    c.line(30, line_y_position, width - 10, line_y_position)  # Draw line from left to right

    width, height = letter
    line_y_position = height - 10
    c.setStrokeColorRGB(0, 0, 0)
    c.line(30, line_y_position, width-10, line_y_position)

    c.setFont("Helvetica", 10)
    c.drawString(30, 735, 'ZenAir <reservations@customer.zenair.in')
    c.drawString(30, 720, 'Reply to: ZenAir <no-reply@customer.zenair.in')

    sql1=cur.execute('select email from passenger where passenger_id='+str(1))
    mail=cur.fetchone()[0]
    c.setFont("Helvetica", 10)
    c.drawString(30, 705, 'To: '+mail)

    now=datetime.now()
    day = now.strftime("%A")  # Full weekday name (e.g., Monday)
    date = now.strftime("%d")  # Day of the month (e.g., 01 to 31)
    month = now.strftime("%B")  # Full month name (e.g., January)
    time = now.strftime("%H:%M")  # 24-hour time format (e.g., 13:45)
    year = now.strftime("%Y")
    fdate=day+', '+date+' '+month+' '+year+' at '+time

    c.setFont("Helvetica", 10)
    c.drawString(463, 735, fdate)

    line_y_position = 690
    line_width = 3
    c.setLineWidth(line_width)
    c.setStrokeColorRGB(0.5, 0, 0.5)
    c.line(30, line_y_position, 600, line_y_position)

    font_name = "Helvetica-Bold"
    font_size = 30
    font_color = (0.5, 0, 0.5)  # You can also use RGB tuples or hexadecimal values
    c.setFont(font_name, font_size)
    c.setFillColor(font_color)
    c.drawString(30, 660, "ZenAir")


    c.setFont('Helvetica-Bold',15)
    c.setFillColor("black")
    c.drawString(310, 667, "PNR/Booking Ref.:"+pnr)

    image_path = r"C:\Users\VBALA\Downloads\barcode.png"  # Replace with the path to your image
    image = ImageReader(image_path)
    c.drawImage(image, 520, 660, width=80, height=25)
    local_time = datetime.now()
    ust_tz = pytz.timezone('UTC')
    current_time_ust = local_time.astimezone(ust_tz)
    ust_date = current_time_ust.strftime('%d')
    ust_month = current_time_ust.strftime('%B')
    ust_year = current_time_ust.strftime('%Y')
    ust_time = current_time_ust.strftime('%H:%M')
    f1date=ust_date+' '+ust_month+', '+ust_year+' '+ust_time+' (UST)'
    data = [
        ['Status', 'Date of Booking', 'Payment Status'],
        ['Confirmed',f1date, 'Approved'],
    ]
    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to the center
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.wrapOn(c, 100, 600)
    table.drawOn(c, 30, 600)
    t1='Booking date reflects in UST (Universal Standard Time), all other timings mentioned are as per local time'
    style = getSampleStyleSheet()
    italic_style = style['Italic']
    c.setFont(italic_style.fontName, italic_style.fontSize)
    c.drawString(30, 587, t1)


    data = [["ZenAir Passenger(s)"]]
    sql='select first_name,last_name,gender from passenger where passenger_id='+strpass
    cur.execute(sql)
    record=cur.fetchone()
    if record[2]=='female':
        val='Ms. '+record[0]+' '+record[1]
    else:
        val='Mr. '+record[0]+' '+record[1]
    data.append([val])
    table = Table(data)
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to the center
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.wrapOn(c, 400, 600)
    table.drawOn(c, 30, 530)

    light_purple = (0.8, 0.6, 0.8)
    c.setStrokeColorRGB(0, 0, 0)  # Set stroke color (black)
    c.setFillColorRGB(*light_purple)  # Set fill color (light purple)
    c.rect(400, 540, 70, 25, stroke=0, fill=1)
    text = "CHECK-IN"
    c.setFillColorRGB(0, 0, 0)  # Set text color (black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(403, 547, text)

    light_purple = (0.8, 0.6, 0.8)
    c.setStrokeColorRGB(0, 0, 0)  # Set stroke color (black)
    c.setFillColorRGB(*light_purple)  # Set fill color (light purple)
    c.rect(480, 540, 110, 25, stroke=0, fill=1)
    text = "FLIGHT STATUS"
    c.setFillColorRGB(0, 0, 0)  # Set text color (black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(487, 547, text)

    cur.execute('select * from reservation where passenger_id='+str(1))
    record=cur.fetchall()
    record=record[0]
    dept_f=record[3]
    arr_f=record[4]
    seat_d=record[5]
    seat_a=record[6]
    dept_d=record[7]
    arr_d=record[8]
    sql = "SELECT departure,destination,departure_time,arrival_time FROM flightdata WHERE flight_no=%s"
    cur.execute(sql, (dept_f,))
    departure,destination,departure_time,arrival_time  = cur.fetchone()
    code1=departure
    code2=destination
    l1=[dept_d,departure,departure_time,dept_f,destination,arrival_time]
    sql = "SELECT departure,destination,departure_time,arrival_time FROM flightdata WHERE flight_no=%s"
    cur.execute(sql, (arr_f,))
    departure,destination,departure_time,arrival_time  = cur.fetchone()
    l2=[arr_d,departure,departure_time,arr_f,destination,arrival_time]
    data = [['Date', 'From (Terminal)','Departs','Flight Number','To (Terminal)','Arrives'],l1,l2]
    table = Table(data)
    table.setStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Title row background color (grey)
                        ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),  # Title row text color (white)
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Title row font (bold)
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
                        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Data row background color
                        ('GRID', (0, 0), (-1, -1), 1, (0.5, 0.5, 0.5))])  # Add grid lines

    table.wrapOn(c, 30, 400)
    x, y = 30, 420
    table.drawOn(c, x, y)
    title_x, title_y = x, y + table._height + 20  # Position the title below the table
    title_width = table._width  # Set the title width to match the table width
    title_height = 30  # Set the title height (adjust as needed)
    c.setFillColorRGB(0.8, 0.8, 0.8)  # Grey background color
    c.rect(title_x, title_y, title_width, title_height, stroke=0, fill=1)  # Draw the title background
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0, 0)  # White text color
    c.drawString(40, 500, "ZenAir Flight Details")  # Title text

    sql = "SELECT code FROM airports WHERE name=%s"
    cur.execute(sql, (code1,))
    c1=cur.fetchone()
    sql = "SELECT code FROM airports WHERE name=%s"
    cur.execute(sql, (code2,))
    c2=cur.fetchone()
    c.setFont('Helvetica-Bold',18)
    c.drawString(40, 375, c1[0])

    x_mid = (40 + 140) / 2
    y_mid = 375
    image_path = r"C:\Users\VBALA\Downloads\round.png"
    c.drawImage(image_path, 95,367, width=30, height=30)  # Adjust width and height as needed

    c.setFont('Helvetica-Bold',18)
    c.drawString(140, 375, c2[0])

    l1=[dept_d,dept_f,val,seat_d]
    l2=[arr_d,arr_f,val,seat_a]
    data = [['Date','Flight Number','Passenger Name', 'Seat','Additional Services Purchased'],l1,l2]
    table = Table(data)
    table.setStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Title row background color (grey)
                        ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),  # Title row text color (white)
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Title row font (bold)
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
                        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Data row background color
                        ('GRID', (0, 0), (-1, -1), 1, (0.5, 0.5, 0.5))])  # Add grid lines
    table.wrapOn(c, 30, 300)
    x, y = 30, 250
    table.drawOn(c, x, y)
    title_x, title_y = x, y + table._height + 20  # Position the title below the table
    title_width = table._width  # Set the title width to match the table width
    title_height = 30  # Set the title height (adjust as needed)
    c.setFillColorRGB(0.8, 0.8, 0.8)  # Grey background color
    c.rect(title_x, title_y, title_width, title_height, stroke=0, fill=1)  # Draw the title background
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0, 0)  # White text color
    c.drawString(40, 335, "Seats and Additional Services")  # Title text


    c.save()
    try:
        subprocess.Popen(["start", "", pnr+"_flight_ticket.pdf"], shell=True)
    except OSError:
        print("Unable to open the PDF. Please open 'flight_ticket.pdf' manually.")
generate_flight_ticket_pdf(1)


cur.close()
conn.close()
