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
    password='shreya#2305',
    database='project1')
cur = conn.cursor()
def generate_flight_ticket_pdf(reservationid):
    reservationid=str(reservationid)
    cur.execute('select * from reservation where reservation_id=%s',(reservationid,));
    records=cur.fetchall()
    passengers=[]
    seat_d=[]
    seat_a=[]
    for i in records:
        passengers.append(i[0])
        pnr_d=i[1]
        flight_d=i[2]
        flight_a=i[3]
        seat_d.append(i[4])
        seat_a.append(i[5])
        date_d=i[6]
        date_a=i[7]
        pnr_a=i[8]
    tripdata=[pnr_d,flight_d,flight_a,seat_d,seat_a,date_d,date_a,pnr_a]
    passengerdata=[]
    for i in passengers:
        cur.execute('select* from passenger where passenger_id=%s',(str(i),))
        passengerdata.append(cur.fetchone())
    mail=passengerdata[0][4]

    pdf_file=pnr_d+"_flight_ticket.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)

    c.setFont("Helvetica-Bold", size=15)
    c.drawString(30, 760, 'Your ZenAir Itinerary - '+pnr_d)

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
    c.setStrokeColorRGB(17 / 255, 23 / 255, 43 / 255)
    c.line(30, line_y_position, 600, line_y_position)

    font_name = "Helvetica-Bold"
    font_size = 30
    font_color = '#11172b'  # You can also use RGB tuples or hexadecimal values
    c.setFont(font_name, font_size)
    c.setFillColor(font_color)
    c.drawString(30, 660, "ZenAir")

    c.setFont(font_name, 18)
    c.setFillColor(font_color)
    c.drawString(440, 665, "Reservation ID: "+reservationid)

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
    page_width, _ = letter
    num_cols = len(data[0])
    col_width = (page_width-50) / num_cols
    col_widths = [col_width] * num_cols
    table = Table(data, colWidths=col_widths)
    table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to the center
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Data row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.wrapOn(c, 100, 600)
    table.drawOn(c, 30, 590)
    t1='Booking date reflects in UST (Universal Standard Time), all other timings mentioned are as per local time'
    style = getSampleStyleSheet()
    italic_style = style['Italic']
    c.setFont(italic_style.fontName, italic_style.fontSize)
    c.drawString(30, 575, t1)

    c.setFont("Helvetica-Bold", 24)
    c.drawString(30, 540, 'Passenger Details')

    data = [['Name','Age','Gender']]
    for i in passengerdata:
        if i[6]=='female':
            val='Ms. '+i[1]+' '+i[2]
        else:
            val='Mr. '+i[1]+' '+i[2]
        l=[val,i[3],i[6].upper()]
        data.append(l)
    page_width, _ = letter
    num_cols = len(data[0])
    col_width = (page_width-50) / num_cols
    col_widths = [col_width] * num_cols
    # Create the table with the calculated column widths
    table = Table(data, colWidths=col_widths)
    table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to the center
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Data row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.wrapOn(c,600,100)
    table.drawOn(c, 30, 460)

    c.setFont("Helvetica-Bold", 24)
    c.drawString(30, 410, 'Trip Details')

    if pnr_a!=None:
        sql = "SELECT departure,destination,departure_time,arrival_time FROM flightdata WHERE flight_no=%s"
        cur.execute(sql, (flight_d,))
        departure,destination,departure_time,arrival_time  = cur.fetchone()
        code1=departure
        code2=destination
        sql = "SELECT code FROM airports WHERE name=%s"
        cur.execute(sql, (code1,))
        c1=cur.fetchone()
        sql = "SELECT code FROM airports WHERE name=%s"
        cur.execute(sql, (code2,))
        c2=cur.fetchone()
        c.setFont('Helvetica-Bold',18)
        c.drawString(30, 365, c1[0])
        x_mid = (30 + 140) / 2
        y_mid = 375
        image_path = r"C:\Users\VBALA\Downloads\round.png"
        c.drawImage(image_path, 84,361, width=30, height=30)  # Adjust width and height as needed
        c.setFont('Helvetica-Bold',18)
        c.drawString(130, 365, c2[0])


        '''
        Departure- PNR_D, FLIGHT_D, DATE_D, DEPT_TIME, ARRIVAL_TIME, SEAT_D (CSV)
        Arrival- PNR_A, FLIGHT_A, DATE_A, DEPT_TIME, ARRIVAL_TIME (to be extracted), SEAT_A (CSV)
        '''
        seats_d=''
        seats_a=''
        for i in seat_d:
            seats_d+=i
            seats_d+=' '
        for i in seat_a:
            seats_a+=i
            seats_a+=' '
        head=['PNR','Flight','From','To','Date','Departure','Arrival','Seat']
        data1=[pnr_d,flight_d,c1[0],c2[0],date_d,departure_time,arrival_time,seats_d]
        data=[head,data1]
        num_cols = len(data[0])
        col_width = (page_width-50) / num_cols
        col_widths = [col_width] * num_cols
        table = Table(data, colWidths=col_widths)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to the center
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Data row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
        ])
        table.wrapOn(c,600,100)
        table.drawOn(c, 30,310)

        sql = "SELECT departure,destination,departure_time,arrival_time FROM flightdata WHERE flight_no=%s"
        cur.execute(sql, (flight_a,))
        departure,destination,departure_time,arrival_time  = cur.fetchone()
        code1=departure
        code2=destination
        sql = "SELECT code FROM airports WHERE name=%s"
        cur.execute(sql, (code1,))
        c1=cur.fetchone()
        sql = "SELECT code FROM airports WHERE name=%s"
        cur.execute(sql, (code2,))
        c2=cur.fetchone()

        data2=[pnr_a,flight_a,c1[0],c2[0],date_a,departure_time,arrival_time,seats_a]
        data=[head,data2]
        num_cols = len(data[0])
        col_width = (page_width-50) / num_cols
        col_widths = [col_width] * num_cols
        table = Table(data, colWidths=col_widths)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to the center
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Data row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
        ])
        table.wrapOn(c,600,100)
        table.drawOn(c, 30, 245)
    else:
        sql = "SELECT departure,destination,departure_time,arrival_time FROM flightdata WHERE flight_no=%s"
        cur.execute(sql, (flight_d,))
        departure,destination,departure_time,arrival_time  = cur.fetchone()
        code1=departure
        code2=destination
        sql = "SELECT code FROM airports WHERE name=%s"
        cur.execute(sql, (code1,))
        c1=cur.fetchone()
        sql = "SELECT code FROM airports WHERE name=%s"
        cur.execute(sql, (code2,))
        c2=cur.fetchone()
        c.setFont('Helvetica-Bold',18)
        c.drawString(30, 375, c1[0])
        image_path = r"C:\Users\VBALA\Downloads\oneway.jpg"
        c.drawImage(image_path, 88,367, width=30, height=30)  # Adjust width and height as needed
        c.setFont('Helvetica-Bold',18)
        c.drawString(130, 375, c2[0])
        seats_d=''
        for i in seat_d:
            seats_d+=i
            seats_d+=' '
        head=['PNR','Flight','From','To','Date','Departure','Arrival','Seat']
        data1=[pnr_d,flight_d,c1[0],c2[0],date_d,departure_time,arrival_time,seats_d]
        data=[head,data1]
        num_cols = len(data[0])
        col_width = (page_width-50) / num_cols
        col_widths = [col_width] * num_cols
        table = Table(data, colWidths=col_widths)
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align all cells to the center
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Font name for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header row
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Data row background color
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
        ])
        table.wrapOn(c,600,100)
        table.drawOn(c, 30,310)

    c.save()
    try:
        subprocess.Popen(["start", "", pnr_d+"_flight_ticket.pdf"], shell=True)
    except OSError:
        print("Unable to open the PDF. Please open 'flight_ticket.pdf' manually.")

generate_flight_ticket_pdf(1)
cur.close()
conn.close()
