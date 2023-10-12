# # # # ################## Proj Python With GUI ###################


# #สร้างdatabase
# import sqlite3
# conn = sqlite3.connect("proj.db")
# c = conn.cursor()
# c.execute('''CREATE TABLE firstusers(id integer PRIMARY KEY AUTOINCREMENT,
#           fname varcher(30) NOT NULL,
#           tel varcher(10) NOT NULL,
#           destination varcher(100) NOT NULL)''')
# c.execute('''CREATE TABLE secondusers(id integer PRIMARY KEY AUTOINCREMENT,
#           sname varcher(30) NOT NULL,
#           tel varcher(10) NOT NULL,
#           destination varcher(100) NOT NULL)''')
# c.execute('''CREATE TABLE post (id integer PRIMARY KEY AUTOINCREMENT,
#           date varcher(100) NOT NULL,
#           time varcher(100) NOT NULL,
#           weight varcher(100) NOT NULL,
#           prize varcher(100) NOT NULL,
#           status varcher(100) NOT NULL)''')
# c.execute('''CREATE TABLE history (id integer PRIMARY KEY AUTOINCREMENT,
#           fname varcher(30) NOT NULL,
#           tel1 varcher(10) NOT NULL,
#           destination1 varcher(100) NOT NULL,
#           sname varcher(30) NOT NULL,
#           tel2 varcher(10) NOT NULL,
#           destination2 varcher(100) NOT NULL,
#           date varcher(100) NOT NULL,
#           time varcher(100) NOT NULL,
#           weight varcher(100) NOT NULL,
#           prize varcher(100) NOT NULL,
#           status varcher(100) NOT NULL)''')

# conn.commit()
# conn.close()





#main program

#import โมดูลต่างๆ

from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
from PIL import ImageTk, Image
import sqlite3
from tkcalendar import*
import requests 
from io import BytesIO
import numpy as np
import cv2
from datetime import datetime
import re
import subprocess
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



#ฟังก์ชั่นติดตามพัสดุหน้าหลัก
def showinfo():
    data = id.get()
    conn = sqlite3.connect("proj.db")
    c = conn.cursor()
    
    c.execute('''SELECT id FROM firstusers WHERE id=?''',(data,))
    checkid = c.fetchall()
    if checkid:
        show = Toplevel(home)
        show.title("P&B EXPRESS")
        show.geometry("1080x720+200+50")
        imgshow = ImageTk.PhotoImage(Image.open("show.png"))
        bgshow = Label(show,image = imgshow)
        bgshow.pack()
        bgshow.image = imgshow
        Label(show,text=data,font="Arial 20",bg ="#ffffff",borderwidth=0).place(x=150 , y=320)
        
        c.execute('''SELECT fname FROM firstusers WHERE id=?''',(data,))
        result = c.fetchall()
        for x in result :
            Label(show,text=x,font="Arial 20",bg ="#ffffff",borderwidth=0).place(x=350 , y=320)


        c.execute('''SELECT sname FROM secondusers WHERE id=?''',(data,))
        result = c.fetchall()
        for x in result :
            Label(show,text=x,font="Arial 20",bg ="#ffffff",borderwidth=0).place(x=600 , y=320)

        c.execute('''SELECT status FROM post WHERE id=(?)''',(data,))
        result = c.fetchall()
        for x in result :
            Label(show,text=x,font="Arial 20",bg ="#ffffff",borderwidth=0).place(x=830 , y=320)
        
        conn.commit()
        c.close()
        myid.delete(0, END)
        Button(show,image = imghomeicon,width=86, height=56,borderwidth=0,command=show.destroy,cursor="hand2").place(x=10,y=20)
    
    else:
        messagebox.showerror("ไม่พบข้อมูลพัสดุ","โปรดกรอกเลข ID ของท่านให้ถูกต้อง")



#สำหรับเช็คข้อมูลผู้ส่งที่มากกว่า1ชิ้น
def showsong():
    checkidshowsong = Toplevel(home)
    checkidshowsong.title("P&B EXPRESS")
    checkidshowsong.geometry("720x500+390+150")
    Label(checkidshowsong,image = imgchecktelsong).pack()
    entl = Entry(checkidshowsong,textvariable=tl,width=12,borderwidth=0)
    entl.place(x=190 , y=280)
    entl.config(font = ("Arial", 30))
    


    def checktelshowsong():
        telf = str(tl.get())
        conn = sqlite3.connect("proj.db")
        c = conn.cursor()
        c.execute('''SELECT tel FROM firstusers WHERE tel=?''',(telf,))
        checktelsong = c.fetchall()
        if checktelsong:
            entl.delete(0,END)
            checkidshowsong.destroy()
            showsongmain = Toplevel(home)
            showsongmain.title("P&B EXPRESS")
            showsongmain.geometry("1080x720+200+50")
            Label(showsongmain,image = imgshowsongbg).pack()
            c.execute('''SELECT fname FROM history WHERE tel1=?''',(telf,))
            result = c.fetchone()
            namesong = Label(showsongmain,text=result,bg="#d40000",fg="#ffffff")
            namesong.place(x=700,y=30)
            namesong.config(font = ("Arial", 30))
            def on_vertical_scroll(*args):
                tree.yview(*args)

            frame = ttk.Frame(showsongmain)
            frame.place(x=130,y=200)


            tree = ttk.Treeview(frame,columns=("id","fname","sname","status"))
            tree.heading("id",text="เลขพัสดุ")
            tree.heading("fname",text="ชื่อผู้ส่ง")
            tree.heading("sname",text="ชื่อผู้รับ")
            tree.heading("status",text="สถานะพัสดุ")

            tree.column("id",anchor="center",width=200)
            tree.column("fname",anchor="center",width=200)
            tree.column("sname",anchor="center",width=200)
            tree.column("status",anchor="center",width=200)
            tree.column("#0",width=0,stretch=NO)
            style = ttk.Style()
            style.configure("Treeview.Heading",font = ("arial",15))
            style.configure("Treeview", font=("Arial", 15))
            

            conn = sqlite3.connect("proj.db")
            c = conn.cursor()

            c.execute('''SELECT id,fname,sname,status FROM history WHERE tel1=?''',(telf,))   
            result = c.fetchall()
            for x in result :
                tree.insert("","end",values=x)


            vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_vertical_scroll)
            vscrollbar.pack(side="right", fill="y")
            tree.config(yscrollcommand=vscrollbar.set)

            tree.pack(fill="both", expand=True)

            Button(showsongmain,image = imgbackicon,width=86, height=56,borderwidth=0,command=showsongmain.destroy,cursor="hand2").place(x=10,y=20)

        else:
            Label(checkidshowsong,text="ไม่พบข้อมูล",font=20,fg='white',bg='#d40000',width=20, height=1).place(x=240 , y=385)


    Button(checkidshowsong,image = imgsearchad,width=60, height=40,borderwidth=0,command=checktelshowsong,cursor="hand2").place(x=505 ,y=285)



#สำหรับเช็คข้อมูลผู้รับที่มากกว่า1ชิ้น
def showrub():
    checkidshowrub = Toplevel(home)
    checkidshowrub.title("P&B EXPRESS")
    checkidshowrub.geometry("720x500+390+150")
    Label(checkidshowrub,image = imgchecktelrub).pack()
    entl = Entry(checkidshowrub,textvariable=tl,width=12,borderwidth=0)
    entl.place(x=190 , y=280)
    entl.config(font = ("Arial", 30))



    def checktelshowrub():
        tel = str(tl.get())
        conn = sqlite3.connect("proj.db")
        c = conn.cursor()
        c.execute('''SELECT tel FROM secondusers WHERE tel=?''',(tel,))
        checktelsong = c.fetchall()
        if checktelsong:
            entl.delete(0,END)
            checkidshowrub.destroy()
            showsongmain = Toplevel(home)
            showsongmain.title("P&B EXPRESS")
            showsongmain.geometry("1080x720+200+50")
            Label(showsongmain,image = imgshowrubbg).pack()
            c.execute('''SELECT sname FROM history WHERE tel2=?''',(tel,))
            result = c.fetchone()
            namesong = Label(showsongmain,text=result,bg="#d40000",fg="#ffffff")
            namesong.place(x=660,y=30)
            namesong.config(font = ("Arial", 30))
            def on_vertical_scroll(*args):
                tree.yview(*args)

            frame = ttk.Frame(showsongmain)
            frame.place(x=130,y=200)


            tree = ttk.Treeview(frame,columns=("id","fname","sname","status"))
            tree.heading("id",text="เลขพัสดุ")
            tree.heading("fname",text="ชื่อผู้ส่ง")
            tree.heading("sname",text="ชื่อผู้รับ")
            tree.heading("status",text="สถานะพัสดุ")

            tree.column("id",anchor="center",width=200)
            tree.column("fname",anchor="center",width=200)
            tree.column("sname",anchor="center",width=200)
            tree.column("status",anchor="center",width=200)
            tree.column("#0",width=0,stretch=NO)
            style = ttk.Style()
            style.configure("Treeview.Heading",font = ("arial",15))
            style.configure("Treeview", font=("Arial", 15))
            

            conn = sqlite3.connect("proj.db")
            c = conn.cursor()

            c.execute('''SELECT id,fname,sname,status FROM history WHERE tel2=?''',(tel,))   
            result = c.fetchall()
            for x in result :
                tree.insert("","end",values=x)


            vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_vertical_scroll)
            vscrollbar.pack(side="right", fill="y")
            tree.config(yscrollcommand=vscrollbar.set)

            tree.pack(fill="both", expand=True)

            Button(showsongmain,image = imgbackicon,width=86, height=56,borderwidth=0,command=showsongmain.destroy,cursor="hand2").place(x=10,y=20)

        else:
            Label(checkidshowrub,text="ไม่พบข้อมูล",font=20,fg='white',bg='#d40000',width=20, height=1).place(x=240 , y=385)


    Button(checkidshowrub,image = imgsearchad,width=60, height=40,borderwidth=0,command=checktelshowrub,cursor="hand2").place(x=505 ,y=285)









#ฟังชั่นตรวจสอบรหัสผ่านADMIN
def chekad():
    chad = Toplevel(home)
    chad.title("P&B EXPRESS")
    chad.geometry("720x500+390+150")
    Label(chad,image = imgloginad).pack()
    mypw = Entry(chad,textvariable=pw1,width=12,borderwidth=0,show="*")   #รหัสADMIN1234
    mypw.place(x=190 , y=225)
    mypw.config(font = ("Arial", 30))
    
    

    #ฟังชั่นADMIN MODE
    def AD() :   
        mmypw = pw1.get()
        if(mmypw=='1234'):
            mypw.delete(0,END)
            chad.destroy()
            admin = Toplevel(home)
            admin.title("P&B EXPRESS")
            admin.geometry("1080x720+200+50")
            Label(admin,image = imgadminbg).pack()


            ##### ฟังชั่นก์เพิ่มข้อมูล ###########################################
            def add():
                addadmin = Toplevel(home)
                addadmin.title("P&B EXPRESS")
                addadmin.geometry("1080x720+200+50")
                Label(addadmin,image = imgaddbg).pack()
                enfn = Entry(addadmin,textvariable=fn,width = 13,borderwidth=0)
                enfn.place(x=210 ,y=247)
                enfn.config(font = ("Arial", 20))

                entlf = Entry(addadmin,textvariable=tlf,width = 13,borderwidth=0)
                entlf.place(x=210 ,y=320)
                entlf.config(font = ("Arial", 20))

                endesf = Entry(addadmin,textvariable=desf,width = 13,borderwidth=0)
                endesf.place(x=210 ,y=393)
                endesf.config(font = ("Arial", 20))

                ensn = Entry(addadmin,textvariable=sn,width = 13,borderwidth=0)
                ensn.place(x=810 ,y=247)
                ensn.config(font = ("Arial", 20))

                entl = Entry(addadmin,textvariable=tl,width = 13,borderwidth=0)
                entl.place(x=810 ,y=320)
                entl.config(font = ("Arial", 20))

                endes = Entry(addadmin,textvariable=des,width = 13,borderwidth=0)
                endes.place(x=810 ,y=393)
                endes.config(font = ("Arial", 20))
                
                enwe = Entry(addadmin,textvariable=we,width = 5,borderwidth=0)
                enwe.place(x=535 ,y=535)
                enwe.config(font = ("Arial", 18))


                
                day = datetime.now().strftime("%d")
                month = datetime.now().strftime("%m")
                year = datetime.now().strftime("%y")
                date = str(day + "/" + month + "/" + year)

                
                endmy = Entry(addadmin,textvariable=dmy,width = 10,borderwidth=0)
                endmy.place(x=180 ,y=535)
                endmy.config(font = ("Arial", 18))
                endmy.insert(0,date)
                
                

                combo = Entry(addadmin, textvariable=combo_var,borderwidth=0,width = 10)
                combo.place(x=895 ,y=533)
                combo.config(font = ("Arial", 18))
                combo.insert(0,"รับฝากพัสดุ")

                
                #ฟังชั่นตรวจสอบความถูกต้องของข้อมูล
                def total():
                    fn1 = str(fn.get())
                    tlf1 = str(tlf.get())
                    desf1 = str(desf.get())
                    sn1 = str(sn.get())
                    tl1 = str(tl.get())
                    des1 = str(des.get())
                    we1 = float(we.get())
                    dmy1 = str(dmy.get())
                    


                    if we1 <=1:
                        sum = 30
                    else:
                        sum = we1*50


                    #ฟังชั่นหน้าสรุปข้อมูลก่อนกดยืนยัน
                    def ctotal():
                        totaladmin = Toplevel(home)
                        totaladmin.title("P&B EXPRESS")
                        totaladmin.geometry("1080x720+200+50")
                        Label(totaladmin,image = imgtotaladmin).pack()
                        Label(totaladmin,text="%s"%fn1,font=20,bg='#eddecb').place(x=210 ,y=250)
                        Label(totaladmin,text="%s"%tlf1,font=20,bg='#eddecb').place(x=210 ,y=325)
                        Label(totaladmin,text="%s"%desf1,font=20,bg='#eddecb').place(x=210 ,y=400)

                        Label(totaladmin,text="%s"%sn1,font=20,bg='#eddecb').place(x=800 ,y=250)
                        Label(totaladmin,text="%s"%tl1,font=20,bg='#eddecb').place(x=800 ,y=325)
                        Label(totaladmin,text="%s"%des1,font=20,bg='#eddecb').place(x=800 ,y=400)
                        Label(totaladmin,text="%s"%we1,font=20,bg='#eddecb').place(x=210 ,y=595)
                        Label(totaladmin,text="%s"%dmy1,font=20,bg='#eddecb').place(x=210 ,y=535)

                        #dropstatus
                        selected_option = combo_var.get()
                        result_label = tk.Label(totaladmin, text="", font= 12,bg='#eddecb')
                        result_label.place(x=210 ,y=650)
                        result_label.config(text=f"{selected_option}")

                        Label(totaladmin,text='%d'%sum,font=20,bg='#eddecb').place(x=550 ,y=535)

                        
                        #สร้าง QR ล็อกเงิน
                        text = "https://promptpay.io/0902830599/" + str(sum) + ".png"
                        image_url = text

                        
                        response = requests.get(image_url)

                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content))
                            
                            
                            if image.mode != 'L':
                                image = image.convert('L')

                            img_np = np.array(image)
 
                            qr_decoder = cv2.QRCodeDetector()

                            
                            val, pts, qr_code = qr_decoder.detectAndDecode(img_np)
  
                            image = image.resize((int(image.width*0.5),int(image.height*0.5)))
                            img_tk = ImageTk.PhotoImage(image)
                            qr = Label(totaladmin, image=img_tk)
                            qr.image = img_tk  
                            qr.place(x = 845, y = 520)

                        else:
                            print("Failed to download the image. HTTP status code:", response.status_code)



                        #ฟังชั่นยืนยันการเพิ่มข้อมูลรับฝาก
                        def sub1():
                            conn = sqlite3.connect("proj.db")
                            c = conn.cursor()
                            fn1 = str(fn.get())
                            tlf1 = int(tlf.get())
                            desf1 = str(desf.get())
                            sn1 = str(sn.get())
                            tl1 = int(tl.get())
                            des1 = str(des.get())
                            we1 = float(we.get())
                            sx = combo_var.get()
                            dmy1 = str(dmy.get())

                            if we1 <=1:
                                sum = 30
                            else:
                                sum = we1*50
                            
                            timenow = datetime.now().strftime("%H:%M:%S")


                            data = (fn1,tlf1,desf1)
                            data1 = (sn1,tl1,des1)
                            data2 = (dmy1,timenow,we1,sum,sx)
                            data3 = (fn1,tlf1,desf1,sn1,tl1,des1,dmy1,timenow,we1,sum,sx)
                            
                            c.execute('INSERT INTO firstusers (fname,tel,destination)VALUES (?,?,?)',data)
                            c.execute('INSERT INTO secondusers (sname,tel,destination)VALUES (?,?,?)',data1)
                            c.execute('INSERT INTO post (date,time,weight,prize,status)VALUES (?,?,?,?,?)',data2)
                            c.execute('INSERT INTO history (fname,tel1,destination1,sname,tel2,destination2,date,time,weight,prize,status)VALUES (?,?,?,?,?,?,?,?,?,?,?)',data3)

                            showsub1  = Toplevel(home)
                            showsub1.title("P&B EXPRESS")
                            showsub1.geometry("720x500+390+150")
                            Label(showsub1,image = imgshowsub1).pack()
                            
                            c.execute("SELECT COUNT(id) FROM secondusers;")
                            count_all = c.fetchone()[0]
                            shsub1 = Label(showsub1,text=f"{count_all}",bg='#000000',fg='#ffffff')
                            shsub1.place(x=380 , y=265)
                            shsub1.config(font = ("Arial", 30))
                            
                            conn.commit()
                            c.close()
                            


                            #สร้างใบเสร็จ
                            pdfmetrics.registerFont(TTFont('THSarabun', r"C:\\Users\\phuri\AppData\\Local\\Microsoft\\Windows\\Fonts\\THSarabun.ttf"))

                            doc = SimpleDocTemplate("invoiceID%s.pdf"%f"{count_all}", pagesize=letter)

                            elements = []

                            
                            styles = getSampleStyleSheet()
                            normal_style_head = styles['Normal']
                            normal_style_head.fontName = 'THSarabun'  
                            normal_style_head.fontSize = 20


                            styles = getSampleStyleSheet()
                            normal_style1 = styles['Normal']
                            normal_style1.fontName = 'THSarabun'  
                            normal_style1.fontSize = 30

                            styles = getSampleStyleSheet()
                            normal_style2 = styles['Normal']
                            normal_style2.fontName = 'THSarabun'  
                            normal_style2.fontSize = 25


                            #สร้างคำในใบเสร็จ
                            head = Paragraph("ใบเสร็จรับเงิน", normal_style1)
                            head1 = Paragraph("บริษัทพีเอ็นบี เอ็กเพรส จำกัด (สำนักงานใหญ่)", normal_style_head)
                            head2 = Paragraph("999/9 หมู่ที่ 9 ต.ทุ่มเท อ.ทุ่มทิ้ง จ.ทุ่มครึ่ง 999999", normal_style_head)
                            datepdf = Paragraph("วันที่รับฝาก : %s"%date, normal_style_head)
                            time = Paragraph("เวลาที่รับฝาก : %s"%timenow, normal_style_head)
                            line = Paragraph("________________________________________________________________", normal_style_head)
                            postid = Paragraph("POST ID : %s"%f"{count_all}", normal_style2)
                            hu1 =  Paragraph("ผู้ส่ง : ", normal_style2)
                            un1 =  Paragraph("คุณ : %s"%fn1, normal_style_head)
                            telun1 =  Paragraph("เบอร์โทร : 0%s"%tlf1, normal_style_head)
                            desun1 =  Paragraph("ที่อยู่ผู้ส่ง : %s"%desf1, normal_style_head)
                            hu2 =  Paragraph("ผู้รับ : ", normal_style2)
                            un2 =  Paragraph("คุณ : %s"%sn1, normal_style_head)
                            telun2 =  Paragraph("เบอร์โทร : 0%s"%tl1, normal_style_head)
                            desun2 =  Paragraph("ที่อยู่ผู้รับ : %s"%des1, normal_style_head)
                            wun2 = Paragraph("น้ำหนักพัสดุ : %s KG"%we1, normal_style_head)
                            sumun2 = Paragraph("Total : %d บาท"%sum, normal_style1)


                            spacer = Spacer(1, 10)  
                            spacer1 = Spacer(1, 50)
                            spacer2 = Spacer(1, 20)


                            elements.append(head)
                            elements.append(spacer1)
                            elements.append(head1)
                            elements.append(spacer)
                            elements.append(head2)
                            elements.append(spacer1)
                            elements.append(datepdf)
                            elements.append(spacer)
                            elements.append(time)
                            elements.append(line)
                            elements.append(spacer2)
                            elements.append(postid)
                            elements.append(spacer1)
                            elements.append(hu1)
                            elements.append(spacer2)
                            elements.append(un1)
                            elements.append(spacer)
                            elements.append(telun1)
                            elements.append(spacer)
                            elements.append(desun1)
                            elements.append(spacer1)
                            elements.append(hu2)
                            elements.append(spacer2)
                            elements.append(un2)
                            elements.append(spacer)
                            elements.append(telun2)
                            elements.append(spacer)
                            elements.append(desun2)
                            elements.append(spacer1)
                            elements.append(wun2)
                            elements.append(spacer2)
                            elements.append(sumun2)
                            elements.append(spacer2)
                            elements.append(line)


                            doc.build(elements)

                            #เปิดสลิปpdf
                            subprocess.Popen(["start", "invoiceID%s.pdf"%f"{count_all}"], shell=True)

                            enfn.delete(0, END)
                            ensn.delete(0, END)
                            entl.delete(0, END)
                            endes.delete(0, END)
                            enwe.delete(0, END)
                            combo.delete(0, END)
                            entlf.delete(0, END)
                            endesf.delete(0, END)
                            endmy.delete(0,END)

                            addadmin.destroy()
                            totaladmin.destroy()

                            

                        btsubadd = Button(totaladmin,text="ยืนยัน",command=sub1,width=15,borderwidth=0,fg='#ffffff',bg='#0e7b46',activebackground="#0e7b46",cursor="hand2")
                        btsubadd.place(x=420 , y=650)
                        btsubadd.config(font = ("Arial", 20))

                        

                        Button(totaladmin,image = imgbackicon,width=86, height=56,borderwidth=0,command=totaladmin.destroy,cursor="hand2").place(x=10,y=20)
                        

                    #ตรวจสอบค่าที่กรอกให้ถูกต้อง 
                    if fn1 and sn1  and des1 and we1 and combo_var and desf1 and dmy1 :
                            if len(tl1) == 10 and len(tlf1) == 10:
                                if re.match("^[a-zA-Zก-๏เ-๙]+$", fn1) and re.match("^[a-zA-Zก-๏เ-๙]+$", sn1):
                                    if re.match("^[0-9]+$", tl1) and re.match("^[0-9]+$", tlf1):
                                        ctotal()
                                    else :
                                        messagebox.showerror("กรอกข้อมูล","กรุณากรอกเบอร์โทรให้ถูกต้อง")
                                        endmy.delete(0,END)
                                        combo.delete(0,END)
                                        add()

                                else :
                                    messagebox.showerror("กรอกข้อมูล","กรุณากรอกข้อมูลให้ถูกต้อง")
                                    endmy.delete(0,END)
                                    combo.delete(0,END)
                                    add()
                            else :
                                messagebox.showerror("กรอกข้อมูล","กรุณากรอกเบอร์โทรให้ครบ 10 ตัว")
                                endmy.delete(0,END)
                                combo.delete(0,END)
                                add()
                    else:
                        messagebox.showerror("กรอกข้อมูล","กรุณากรอกข้อมูลให้ครบถ้วน")
                        endmy.delete(0,END)
                        combo.delete(0,END)
                        add()
                        

                def adback():
                    enfn.delete(0, END)
                    ensn.delete(0, END)
                    entl.delete(0, END)
                    endes.delete(0, END)
                    enwe.delete(0, END)
                    combo.delete(0, END)
                    entlf.delete(0, END)
                    endesf.delete(0, END)
                    endmy.delete(0,END)
                    addadmin.destroy()

                btsarub = Button(addadmin,text="สรุปยอด",command=total,width=15,borderwidth=0,fg='#ffffff',bg='#0e7b46',activebackground="#0e7b45",cursor="hand2")
                btsarub.place(x=420 , y=638)
                btsarub.config(font = ("Arial", 20))
                Button(addadmin,image = imgbackicon,width=86, height=56,borderwidth=0,command=adback,cursor="hand2").place(x=10,y=20)
            Button(admin,image = imgaddadmin,width=250, height=50,borderwidth=0,command=add,cursor="hand2").place(x=418 ,y=168)





            ##### ฟังชั่นกรอกเลข ID แก้ไขข้อมูล #########################
            def idfix():
                cidfix  = Toplevel(home)
                cidfix.title("P&B EXPRESS")
                cidfix.geometry("720x500+390+150")
                Label(cidfix,image = imgidfix).pack()
                fixid = Entry(cidfix,textvariable=fid,width=14,borderwidth=0)
                fixid.place(x=180 , y=285)
                fixid.config(font = ("Arial", 28))


                #ฟังชั่นตรวจสอบเลขที่ต้องการแก้ไข
                def fix():
                    z = fid.get()
                    conn = sqlite3.connect("proj.db")
                    c = conn.cursor()
                    c.execute('''SELECT id FROM firstusers WHERE id=?''',(z,))
                    checkid = c.fetchall()
                    if checkid:
                        fixid.delete(0, END)
                        cidfix.destroy()
                        
                        fixmain = Toplevel(home)
                        fixmain.title("P&B EXPRESS")
                        fixmain.geometry("1080x720+200+50")
                        Label(fixmain,image = imgfixbg).pack()
                        shfid = Label(fixmain,text=z,fg='white',bg='#d40000')
                        shfid.place(x=670 , y=30)
                        shfid.config(font = ("Arial", 28))

                        conn = sqlite3.connect("proj.db")
                        c = conn.cursor()

                        c.execute('''SELECT fname FROM firstusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            enfn = Entry(fixmain,textvariable=fn,width = 13,borderwidth=0)
                            enfn.insert(0,x)
                            enfn.place(x=210 ,y=247)
                            enfn.config(font = ("Arial", 20))


                        c.execute('''SELECT tel FROM firstusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            entlf = Entry(fixmain,textvariable=tlf,width = 13,borderwidth=0)
                            entlf.place(x=210 ,y=320)
                            entlf.config(font = ("Arial", 20))
                            entlf.insert(0,"0%s"%x)
                        

                        c.execute('''SELECT destination FROM firstusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            endesf = Entry(fixmain,textvariable=desf,width = 13,borderwidth=0)
                            endesf.place(x=210 ,y=393)
                            endesf.config(font = ("Arial", 20))
                            endesf.insert(0,"%s"%x)


                        c.execute('''SELECT sname FROM secondusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            ensn = Entry(fixmain,textvariable=sn,width = 13,borderwidth=0)
                            ensn.place(x=810 ,y=247)
                            ensn.config(font = ("Arial", 20))
                            ensn.insert(0,x)


                        c.execute('''SELECT tel FROM secondusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            entl = Entry(fixmain,textvariable=tl,width = 13,borderwidth=0)
                            entl.place(x=810 ,y=320)
                            entl.config(font = ("Arial", 20))
                            entl.insert(0,"0%s"%x)


                        c.execute('''SELECT destination FROM secondusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            endes = Entry(fixmain,textvariable=des,width = 13,borderwidth=0)
                            endes.place(x=810 ,y=393)
                            endes.config(font = ("Arial", 20))
                            endes.insert(0,"%s"%x)


                        c.execute('''SELECT weight FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            enwe = Entry(fixmain,textvariable=we,width = 5,borderwidth=0)
                            enwe.place(x=535 ,y=535)
                            enwe.config(font = ("Arial", 18))
                            enwe.insert(0,x)


                        # #dropstatus
                        c.execute('''SELECT status FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            combo = ttk.Combobox(fixmain, textvariable=combo_var,width = 10)
                            combo['values'] = ('รับฝากพัสดุ', 'นำส่งพัสดุ', 'ส่งพัสดุสำเร็จ','พัสดุถูกตีกลับ')
                            combo.place(x=875 ,y=530)
                            combo.insert(0,x)
                            combo.config(font = ("Arial", 18))


                        c.execute('''SELECT date FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            def pick_date(event):
                                global cal,date_window

                                date_window = Toplevel()
                                date_window.grab_set()
                                date_window.title("DATE")
                                date_window.geometry("250x220+350+320")
                                cal = Calendar(date_window,selectmode="day",date_pattern="dd/mm/yy")
                                cal.place(x=0,y=0)

                                submit_btn = Button(date_window,text='Submit',command=grab_date,width=20,cursor="hand2")
                                submit_btn.place(x=50,y=190)

                            def grab_date():
                                endmy.delete(0,END)
                                endmy.insert(0,cal.get_date())
                                date_window.destroy()

                            endmy = Entry(fixmain,textvariable=dmy,width = 10,borderwidth=0)
                            endmy.place(x=180 ,y=535)
                            endmy.config(font = ("Arial", 18))
                            endmy.insert(0,x)
                            endmy.bind("<1>",pick_date)


                        #ฟังชั่นยืนยันการแก้ไขข้อมูล
                        def sub2 ():
                            showsub2  = Toplevel(home)
                            showsub2.title("P&B EXPRESS")
                            showsub2.geometry("720x500+390+150")
                            Label(showsub2,image = imgshowsub2).pack()

                            
                            fn1 = str(fn.get())
                            sn1 = str(sn.get())
                            tl1 = int(tl.get())
                            des1 = str(des.get())
                            we1 = float(we.get())
                            sx = combo_var.get()
                            tlf1 = str(tlf.get())
                            desf1 = str(desf.get())
                            dmy1 = str(dmy.get())
                            
                            if we1 <=1:
                                sum = 30
                            else:
                                sum = we1*50
                            

                            timenow = datetime.now().strftime("%H:%M:%S")


                            shsub2 = Label(showsub2,text=z,bg='#000000',fg='#ffffff')
                            shsub2.place(x=370 , y=230)
                            shsub2.config(font = ("Arial", 28))
                            conn = sqlite3.connect("proj.db")
                            c = conn.cursor()
                            c.execute('''UPDATE firstusers SET fname=?,tel=?,destination=? WHERE id=?''',(fn1,tlf1,desf1,z))
                            c.execute('''UPDATE secondusers SET sname=?,tel=?,destination=? WHERE id=?''',(sn1,tl1,des1,z))
                            c.execute('''UPDATE post SET date=?,weight=?,prize=?,status=? WHERE id=?''',(dmy1,we1,sum,sx,z))
                            c.execute('''UPDATE history SET fname=?,tel1=?,destination1=?,sname=?,tel2=?,destination2=?,date=?,weight=?,prize=?,status=? WHERE id=?''',(fn1,tlf1,desf1,sn1,tl1,des1,dmy1,we1,sum,sx,z,))
                            conn.commit()

                            
                            enfn.delete(0, END)
                            ensn.delete(0, END)
                            entl.delete(0, END)
                            endes.delete(0, END)
                            enwe.delete(0, END)
                            combo.delete(0, END)
                            entlf.delete(0, END)
                            endesf.delete(0, END)
                            endmy.delete(0, END)
                            fixmain.destroy()


                            #สร้างใบเสร็จ
                            pdfmetrics.registerFont(TTFont('THSarabun', r"C:\\Users\\phuri\AppData\\Local\\Microsoft\\Windows\\Fonts\\THSarabun.ttf"))

                            doc = SimpleDocTemplate("invoiceID%s.pdf"%z, pagesize=letter)

                            elements = []

                            
                            styles = getSampleStyleSheet()
                            normal_style_head = styles['Normal']
                            normal_style_head.fontName = 'THSarabun'  
                            normal_style_head.fontSize = 20


                            styles = getSampleStyleSheet()
                            normal_style1 = styles['Normal']
                            normal_style1.fontName = 'THSarabun'  
                            normal_style1.fontSize = 30

                            styles = getSampleStyleSheet()
                            normal_style2 = styles['Normal']
                            normal_style2.fontName = 'THSarabun'  
                            normal_style2.fontSize = 25



                            head = Paragraph("ใบเสร็จรับเงิน", normal_style1)
                            head1 = Paragraph("บริษัทพีเอ็นบี เอ็กเพรส จำกัด (สำนักงานใหญ่)", normal_style_head)
                            head2 = Paragraph("999/9 หมู่ที่ 9 ต.ทุ่มเท อ.ทุ่มทิ้ง จ.ทุ่มครึ่ง 999999", normal_style_head)
                            datepdf = Paragraph("วันที่รับฝาก : %s"%dmy1, normal_style_head)
                            time = Paragraph("เวลาที่แก้ไข : %s"%timenow, normal_style_head)
                            line = Paragraph("________________________________________________________________", normal_style_head)
                            postid = Paragraph("POST ID : %s"%z, normal_style2)
                            hu1 =  Paragraph("ผู้ส่ง : ", normal_style2)
                            un1 =  Paragraph("คุณ : %s"%fn1, normal_style_head)
                            telun1 =  Paragraph("เบอร์โทร : %s"%tlf1, normal_style_head)
                            desun1 =  Paragraph("ที่อยู่ผู้ส่ง : %s"%desf1, normal_style_head)
                            hu2 =  Paragraph("ผู้รับ : ", normal_style2)
                            un2 =  Paragraph("คุณ : %s"%sn1, normal_style_head)
                            telun2 =  Paragraph("เบอร์โทร : 0%s"%tl1, normal_style_head)
                            desun2 =  Paragraph("ที่อยู่ผู้รับ : %s"%des1, normal_style_head)
                            wun2 = Paragraph("น้ำหนักพัสดุ : %s KG"%we1, normal_style_head)
                            sumun2 = Paragraph("Total : %d บาท"%sum, normal_style1)


                            spacer = Spacer(1, 10)  
                            spacer1 = Spacer(1, 50)
                            spacer2 = Spacer(1, 20)


                            
                            elements.append(head)
                            elements.append(spacer1)
                            elements.append(head1)
                            elements.append(spacer)
                            elements.append(head2)
                            elements.append(spacer1)
                            elements.append(datepdf)
                            elements.append(spacer)
                            elements.append(time)
                            elements.append(line)
                            elements.append(spacer2)
                            elements.append(postid)
                            elements.append(spacer1)
                            elements.append(hu1)
                            elements.append(spacer2)
                            elements.append(un1)
                            elements.append(spacer)
                            elements.append(telun1)
                            elements.append(spacer)
                            elements.append(desun1)
                            elements.append(spacer1)
                            elements.append(hu2)
                            elements.append(spacer2)
                            elements.append(un2)
                            elements.append(spacer)
                            elements.append(telun2)
                            elements.append(spacer)
                            elements.append(desun2)
                            elements.append(spacer1)
                            elements.append(wun2)
                            elements.append(spacer2)
                            elements.append(sumun2)
                            elements.append(spacer2)
                            elements.append(line)


                            doc.build(elements)

                            subprocess.Popen(["start", "invoiceID%s.pdf"%z], shell=True)
                        

                        
                        #ฟังชั่นย้อนกลับ
                        def backfix():
                            enfn.delete(0, END)
                            ensn.delete(0, END)
                            entl.delete(0, END)
                            endes.delete(0, END)
                            enwe.delete(0, END)
                            combo.delete(0, END)
                            entlf.delete(0, END)
                            endesf.delete(0, END)
                            endmy.delete(0, END)
                            fixmain.destroy()


                        Button(fixmain,image = imgbackicon,width=86, height=56,borderwidth=0,command=backfix,cursor="hand2").place(x=10,y=20)
                        btfix = Button(fixmain,text="ยืนยัน",command=sub2,width=15,borderwidth=0,fg='#ffffff',bg='#0e7b46',activebackground='#0e7b46',cursor="hand2")
                        btfix.place(x=420 , y=638)
                        btfix.config(font = ("Arial", 20))


                    else:
                        Label(cidfix,text="โปรดกรอกเลข ID ให้ถูกต้อง",font=20,fg='white',bg='#d40000',width=20, height=1).place(x=240 , y=365)
                        
                Button(cidfix,image = imgsearchad,width=60, height=40,borderwidth=0,command=fix,cursor="hand2").place(x=510 ,y=285)
            Button(admin,image = imgfixadmin,width=250, height=50,borderwidth=0,command=idfix,cursor="hand2").place(x=418 ,y=275)






            #ฟังชั่นอัปเดตข้อมูล###########
            def up():
                cidup  = Toplevel(home)
                cidup.title("P&B EXPRESS")
                cidup.geometry("720x500+390+150")
                Label(cidup,image = imgidup).pack()
                upid = Entry(cidup,textvariable=uid,width=14,borderwidth=0)
                upid.place(x=180 , y=285)
                upid.config(font = ("Arial", 28))


                ##ฟังชั่นตรวจสอบเลข ID และแสดงหน้า อัปเดต
                def cupdate():
                    data = uid.get()
                    conn = sqlite3.connect("proj.db")
                    c = conn.cursor()
                    c.execute('''SELECT id FROM firstusers WHERE id=?''',(data,))
                    checkid = c.fetchall()
                    if checkid:
                        upid.delete(0, END)
                        cidup.destroy()
                        
                        upmain = Toplevel(home)
                        upmain.title("P&B EXPRESS")
                        upmain.geometry("1080x720+200+50")
                        Label(upmain,image = imgupbg).pack()
                        shuid = Label(upmain,text=data,fg='white',bg='#d40000')
                        shuid.place(x=680 , y=28)
                        shuid.config(font = ("Arial", 28))



                        Label(upmain,text=data,font="Arial 20",bg ="#ffffff",borderwidth=0).place(x=150 , y=320)
                        conn = sqlite3.connect("proj.db")
                        c = conn.cursor()
                        c.execute('''SELECT fname FROM firstusers WHERE id=?''',(data,))
                        result = c.fetchall()
                        for x in result :
                            Label(upmain,text=x,font="Arial 20",bg ="#ffffff",borderwidth=0).place(x=350 , y=320)
                            
                        
                        c.execute('''SELECT sname FROM secondusers WHERE id=?''',(data,))
                        result = c.fetchall()
                        for x in result :
                            Label(upmain,text=x,font="Arial 20",bg ="#ffffff",borderwidth=0).place(x=600 , y=320)
                            

                        #ดร็อปดาวอัพเดตสถานะ
                        c.execute('''SELECT status FROM post WHERE id=?''',(data,))
                        result = c.fetchall()
                        for x in result :
                            combo = ttk.Combobox(upmain,textvariable=combo_var,width=10)
                            combo.config(font="Arial 20")
                            combo['values'] = ('รับฝากพัสดุ', 'นำส่งพัสดุ', 'ส่งพัสดุสำเร็จ','พัสดุถูกตีกลับ')
                            combo.place(x=800 , y=320)
                            combo.insert(0,x)
                            
                        conn.commit()
                        c.close()


                        #ฟังชั่นยืนยันการอัปเดตข้อมูล
                        def sub3():
                            sx = combo_var.get()
                            showup  = Toplevel(home)
                            showup.title("P&B EXPRESS")
                            showup.geometry("720x500+390+150")
                            Label(showup,image = imgshowsub3).pack()
                            
                            
                            shsub3 = Label(showup,text=data,bg='#000000',fg='#ffffff')
                            shsub3.place(x=370 , y=230)
                            shsub3.config(font = ("Arial", 28))
                            conn = sqlite3.connect("proj.db")
                            c = conn.cursor()
                            c.execute('''UPDATE post SET status=? WHERE id=?''', (sx, data))
                            c.execute('''UPDATE history SET status=? WHERE id=?''', (sx, data))
                            conn.commit()
                            
                            combo.delete(0, END)
                            upmain.destroy()
                            

                        def backup():
                            combo.delete(0, END)
                            upmain.destroy()

                        Button(upmain,image = imgbackicon,width=86, height=56,borderwidth=0,command=backup,cursor="hand2").place(x=10,y=20)
                        btup = Button(upmain,text="ยืนยัน",command=sub3,width=15,borderwidth=0,fg='#ffffff',bg='#0e7b46',activebackground='#0e7b46',cursor="hand2")
                        btup.place(x=410 , y=455)
                        btup.config(font = ("Arial", 20))

                    else :
                        Label(cidup,text="โปรดกรอกเลข ID ให้ถูกต้อง",font=20,fg='white',bg='#d40000',width=20, height=1).place(x=240 , y=365)


                Button(cidup,image = imgsearchad,width=60, height=40,borderwidth=0,command=cupdate,cursor="hand2").place(x=510 ,y=285)
            Button(admin,image = imgupadmin,width=250, height=50,borderwidth=0,command=up,cursor="hand2").place(x=418 ,y=379)




            #ฟังชั่นโชว์ข้อมูล#########
            def cshowinfo():
                cidshow  = Toplevel(home)
                cidshow.title("P&B EXPRESS")
                cidshow.geometry("720x500+390+150")
                Label(cidshow,image = imgidshow).pack()
                showid = Entry(cidshow,textvariable=shid,width=14,borderwidth=0)
                showid.place(x=180 , y=285)
                showid.config(font = ("Arial", 28))


                def showinfo() :
                    z = shid.get()
                    conn = sqlite3.connect("proj.db")
                    c = conn.cursor()
                    c.execute('''SELECT id FROM firstusers WHERE id=?''',(z,))
                    checkid = c.fetchall()
                    if checkid:
                        showid.delete(0, END)
                        cidshow.destroy()
                        showmain = Toplevel(home)
                        showmain.title("P&B EXPRESS")
                        showmain.geometry("1080x720+200+50")
                        Label(showmain,image = imgshowinfobg).pack()
                        shinid = Label(showmain,text=z,fg='white',bg='#d40000')
                        shinid.place(x=680 , y=28)
                        shinid.config(font = ("Arial", 28))

                        conn = sqlite3.connect("proj.db")
                        c = conn.cursor()

                        c.execute('''SELECT fname FROM firstusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text=x,font=20,bg='#eddecb').place(x=210 ,y=265)
                            

                        c.execute('''SELECT tel FROM firstusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text="0%s"%x,font=20,bg='#eddecb').place(x=210 ,y=340)
                            

                        c.execute('''SELECT destination FROM firstusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text="%s"%x,font=20,bg='#eddecb').place(x=210 ,y=415)
                            

                        c.execute('''SELECT sname FROM secondusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text=x,font=20,bg='#eddecb').place(x=800 ,y=266)


                        c.execute('''SELECT tel FROM secondusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text="0%s"%x,font=20,bg='#eddecb').place(x=800 ,y=340)


                        c.execute('''SELECT destination FROM secondusers WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text="%s"%x,font=20,bg='#eddecb').place(x=800 ,y=415)
                            

                        c.execute('''SELECT weight FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text=x,font=20,bg='#eddecb').place(x=560 ,y=595)


                        c.execute('''SELECT status FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text=x,font=20,bg='#eddecb').place(x=910 ,y=595)


                        c.execute('''SELECT date FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text=x,font=20,bg='#eddecb').place(x=265 ,y=595)


                        c.execute('''SELECT time FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text=x,font=20,bg='#eddecb').place(x=265 ,y=650)


                        c.execute('''SELECT prize FROM post WHERE id=?''',(z,))
                        result = c.fetchall()
                        for x in result :
                            Label(showmain,text=x,font=20,bg='#eddecb').place(x=560 ,y=650)
                        

                        Button(showmain,image = imgbackicon,width=86, height=56,borderwidth=0,command=showmain.destroy,cursor="hand2").place(x=10,y=20)

                    else :
                        Label(cidshow,text="โปรดกรอกเลข ID ให้ถูกต้อง",font=20,fg='white',bg='#d40000',width=20, height=1).place(x=240 , y=365)

                Button(cidshow,image = imgsearchad,width=60, height=40,borderwidth=0,command=showinfo,cursor="hand2").place(x=510 ,y=285)

            Button(admin,image = imgshowinfoadmin,width=250, height=50,borderwidth=0,command=cshowinfo,cursor="hand2").place(x=418 ,y=483)



            def sumallday():
                
                winsum = Toplevel(home)
                winsum.title("P&B EXPRESS")
                winsum.geometry("720x500+390+150")
                Label(winsum,image = imgpickdate).pack()

                def pick_date(event):
                    global cal,date_window

                    date_window = Toplevel()
                    date_window.grab_set()
                    date_window.title("DATE")
                    date_window.geometry("250x220+350+320")
                    cal = Calendar(date_window,selectmode="day",date_pattern="dd/mm/yy")
                    cal.place(x=0,y=0)

                    submit_btn = Button(date_window,text='Submit',command=grab_date,width=20,cursor="hand2")
                    submit_btn.place(x=50,y=190)

                def grab_date():
                    endmy.delete(0,END)
                    endmy.insert(0,cal.get_date())
                    date_window.destroy()

                endmy = Entry(winsum,textvariable=dmy,width=14,borderwidth=0)
                endmy.place(x=180 , y=285)
                endmy.config(font = ("Arial", 28))
                endmy.bind("<1>",pick_date)
                

                def showsumall():
                    sumall = int()
                    numall = int()
                    
                    showsumallwin =  Toplevel(home)
                    showsumallwin.title("P&B EXPRESS")
                    showsumallwin.geometry("1080x720+200+50")
                    Label(showsumallwin,image = imgshowalldaybg).pack()

                    date = str(dmy.get())

                    conn = sqlite3.connect('proj.db')
                    cursor = conn.cursor()
                    cursor.execute('''SELECT date,prize FROM post''')

                    result = cursor.fetchall()
                    cursor.close()

                    for x in result:
                        if str(x[0]) == date:
                            sumall = sumall + int(x[1])
                    for x in result:
                        if str(x[0]) == date:
                            numall = numall + 1
                    
                    shsum = Label(showsumallwin,text=sumall,bg='#eddecb')
                    shsum.place(x=845 , y=265)
                    shsum.config(font = ("Arial", 28))


                    shnum = Label(showsumallwin,text=numall,bg='#eddecb')
                    shnum.place(x=275 , y=265)
                    shnum.config(font = ("Arial", 28))


                    shdate = Label(showsumallwin,text=date,bg='#d40000',fg='#ffffff')
                    shdate.place(x=580 , y=30)
                    shdate.config(font = ("Arial", 28))

                 
                    
                    def on_vertical_scroll(*args):
                        tree.yview(*args)


                    frame = ttk.Frame(showsumallwin)
                    frame.place(x=20,y=400)


                    #สร้างตารางคอลั่ม
                    tree = ttk.Treeview(frame,columns=("id","fname","tel1","destination1","sname","tel2","destination2","time","weight","prize","status"))

                    tree.heading("id",text="เลขพัสดุ")
                    tree.heading("fname",text="ชื่อผู้ส่ง")
                    tree.heading("tel1",text="เบอร์ผู้ส่ง")
                    tree.heading("destination1",text="ที่อยู่ผู้ส่ง")
                    tree.heading("sname",text="ชื่อผู้รับ")
                    tree.heading("tel2",text="เบอร์ผู้รับ")
                    tree.heading("destination2",text="ที่อยู่ผู้รับ")
                    tree.heading("time",text="เวลารับฝาก")
                    tree.heading("weight",text="น้ำหนักพัสดุ")
                    tree.heading("prize",text="ค่าบริการ")
                    tree.heading("status",text="สถานะพัสดุ")


                    tree.column("id",anchor="center",width=60)
                    tree.column("fname",anchor="center",width=80)
                    tree.column("tel1",anchor="center",width=100)
                    tree.column("destination1",anchor="center",width=130)
                    tree.column("sname",anchor="center",width=80)
                    tree.column("tel2",anchor="center",width=100)
                    tree.column("destination2",anchor="center",width=130)
                    tree.column("time",anchor="center",width=80)
                    tree.column("weight",anchor="center",width=90)
                    tree.column("prize",anchor="center",width=80)
                    tree.column("status",anchor="center",width=100)
                    tree.column("#0",width=0,stretch=NO)
                    style = ttk.Style()
                    style.configure("Treeview.Heading",font = ("arial",12))
                    style.configure("Treeview", font=("Arial", 12))

                    
                    #เพิ่มข้อมูลไปในตารางคอลั่ม

                    conn = sqlite3.connect("proj.db")
                    c = conn.cursor()

                    c.execute('''SELECT id,fname,tel1,destination1,sname,tel2,destination2,time,weight,prize,status FROM history WHERE date=? ''',(date,))
                    result = c.fetchall()
                    for x in result :
                        tree.insert("","end",values=x)



                    vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_vertical_scroll)
                    vscrollbar.pack(side="right", fill="y")
                    tree.config(yscrollcommand=vscrollbar.set)

                    
                    tree.pack(fill="both", expand=True)


                    endmy.delete(0, END)
                    winsum.destroy()



                    Button(showsumallwin,image = imgbackicon,width=86, height=56,borderwidth=0,command=showsumallwin.destroy,cursor="hand2").place(x=10,y=20)
                    
                
                Button(winsum,image = imgsearchad,width=60, height=40,borderwidth=0,command=showsumall,cursor="hand2").place(x=505 ,y=285)

            Button(admin,image = imgcheckadmin,width=250, height=50,borderwidth=0,command=sumallday,cursor="hand2").place(x=418 ,y=588)
            Button(admin,image = imglogoutadmin,width=86, height=56,borderwidth=0,command=admin.destroy,cursor="hand2").place(x=980 ,y=22)
                
                
        else :
            Label(chad,text="รหัสผ่านไม่ถูกต้อง",font=20,fg='white',bg='#d40000',width=20, height=1).place(x=240 , y=320)


    Button(chad,image = imgsearchad,width=60, height=40,borderwidth=0,command=AD,cursor="hand2").place(x=495 ,y=230)
        


#ฟังชั่นหน้า about เกี่ยวกับ
def about():
    aboutmain = Toplevel(home)
    aboutmain.title("P&B EXPRESS")
    aboutmain.geometry("720x500+390+150")
    Label(aboutmain,image = imgaboutshow).pack()
    
    #คิดอัตราค่าส่ง
    def autta():
        aboutautta= Toplevel(home)
        aboutautta.title("P&B EXPRESS")
        aboutautta.geometry("1080x720+200+50")
        Label(aboutautta,image = imgshowwebg).pack()
        enwe = Entry(aboutautta,textvariable=we,width = 5,borderwidth=0)
        enwe.place(x=200 ,y=370)
        enwe.config(font = ("Arial", 18))

        def showautta():
            Label(aboutautta,image = imgshowwe).place(x=200 ,y=500)
            we1 = float(we.get())
            if we1 <=1:
                sum = 30
            else:
                sum = we1*50

            Label(aboutautta,text="%s"%we1,font=20,bg="#ffffff").place(x=270,y=640)
            Label(aboutautta,text="%d"%sum,font=20,bg="#ffffff").place(x=430,y=640)
            Label(aboutautta,text="%d"%sum,font=20,bg="#ffffff").place(x=790,y=640)
            Label(aboutautta,text="0",font=20,bg="#ffffff").place(x=620,y=640)

        def abde():
            endesf.delete(0,END)
            endes.delete(0,END)
            enwe.delete(0,END)
            aboutautta.destroy()
            

        kon = Button(aboutautta,text="ตรวจสอบ",borderwidth=0,command=showautta,bg="#d40000",fg="#ffffff",activebackground="#d40000",cursor="hand2")
        kon.place(x=480,y=425)
        kon.config(font = ("Arial", 20))
        Button(aboutautta,image = imgbackicon,width=86, height=56,borderwidth=0,command=abde,cursor="hand2").place(x=10,y=20)


    #เกี่ยวกับผู้พัฒนา
    def aboutdev():
        aboutdev1= Toplevel(home)
        aboutdev1.title("P&B EXPRESS")
        aboutdev1.geometry("1080x720+200+50")
        Label(aboutdev1,image = imgaboutbg).pack()
        Button(aboutdev1,image = imgbackicon,width=86, height=56,borderwidth=0,command=aboutdev1.destroy,cursor="hand2").place(x=10,y=20)


    aut = Button(aboutmain,text="อัตราค่าส่ง",borderwidth=0,bg="#d40000",fg="white",width=10,command=autta,activebackground="#d40000",cursor="hand2")
    aut.place(x=200,y=205)
    aut.config(font = ("Arial", 30))
    ab = Button(aboutmain,text="เกี่ยวกับผู้พัฒนา",borderwidth=0,bg="#d40000",fg="white",width=12,command=aboutdev,activebackground="#d40000",cursor="hand2")
    ab.place(x=180,y=320)
    ab.config(font = ("Arial", 30))
                






##ฟังชั่นโชว์กล่องข้อความเพื่อถามปิดโปรแกรม
def close():
    status=messagebox.askyesno(title="ยืนยันการปิดโปรแกรม",message="คุณต้องการปิดโปรแกรมใช่หรือไม่")
    if status>0:
        sys.exit()



#ฟังชั่นสร้างหน้าหลัก
home = Tk()
home.title("P&B EXPRESS")
home.geometry("1080x720+200+50")
imghomebg = ImageTk.PhotoImage(Image.open("homebg1.png"))
Label(image = imghomebg).pack()



#กำหนดแปรต่างๆ
#กำหนดตัวแปรในการรับ ID ในการทำงานในแต่ละตัวเลือก

id = StringVar()
pw1 = StringVar()
fid = StringVar()
uid = StringVar()
shid = StringVar()
deid = StringVar()

#ตัวแปรเก็บค่า ชื่อ เบอร์ ปลายทาง สถานะ
fn = StringVar()
sn = StringVar()
tl = StringVar()
des = StringVar()
we = StringVar()
st = StringVar()
tlf = StringVar()
desf = StringVar()
dmy = StringVar()

# เก็บค่าบริการและ สถานะ
st1 = StringVar()
x = StringVar()  
sx = StringVar()
sum = IntVar()




#กำหนดตัวแปรเก็บค่าDropdown
combo_var = tk.StringVar()
combo = ttk.Combobox(textvariable=combo_var)


#กำหนดค่าให้ช่องรับข้อมูลต่างๆ
enfn = Entry(textvariable=fn)
entlf = Entry(textvariable=tlf)
endesf = Entry(textvariable=desf)
ensn = Entry(textvariable=sn)
entl = Entry(textvariable=tl)
endes = Entry(textvariable=des)
enwe = Entry(textvariable=we)
endmy = Entry(textvariable=dmy)
fixid = Entry(textvariable=fid)
upid = Entry(textvariable=uid)
showid = Entry(textvariable=shid)
delateid = Entry(textvariable=deid)
mypw = Entry(textvariable=pw1)
myid = Entry(home,textvariable=id, width = 22,borderwidth=0)
myid.place(x=245 , y=375)
myid.config(font = ("Arial", 30))


# import รูปต่างๆทั้งหมดในโปรแกรม
imgsearch = ImageTk.PhotoImage(Image.open("search.png"))
imghomeicon = ImageTk.PhotoImage(Image.open("homeicon.png"))
imgadminicon = ImageTk.PhotoImage(Image.open("adminicon.png"))
imgabouticon = ImageTk.PhotoImage(Image.open("abouticon.png"))
imgcloseicon = ImageTk.PhotoImage(Image.open("closeicon.png"))
imgloginad = ImageTk.PhotoImage(Image.open("loginad.png"))
imgsearchad = ImageTk.PhotoImage(Image.open("searchad.png"))
imgadminbg = ImageTk.PhotoImage(Image.open("adminbg.png"))
imgaddadmin = ImageTk.PhotoImage(Image.open("addadmin.png"))
imgfixadmin = ImageTk.PhotoImage(Image.open("fixadmin.png"))
imgupadmin = ImageTk.PhotoImage(Image.open("upadmin.png"))
imgshowinfoadmin = ImageTk.PhotoImage(Image.open("showinfoadmin.png"))
imglogoutadmin = ImageTk.PhotoImage(Image.open("logoutadmin.png"))
imgaddbg = ImageTk.PhotoImage(Image.open("addbg.png"))
imgbackicon = ImageTk.PhotoImage(Image.open("backicon.png"))
imgtotaladmin = ImageTk.PhotoImage(Image.open("totalbg.png"))
imgshowsub1 = ImageTk.PhotoImage(Image.open("showsub1.png"))
imgidfix = ImageTk.PhotoImage(Image.open("idfix.png"))
imgfixbg = ImageTk.PhotoImage(Image.open("fixbg.png"))
imgshowsub2 = ImageTk.PhotoImage(Image.open("showsub2.png"))
imgidup = ImageTk.PhotoImage(Image.open("idup.png"))
imgupbg = ImageTk.PhotoImage(Image.open("upbg.png"))
imgshowsub3 = ImageTk.PhotoImage(Image.open("showsub3.png"))
imgidshow = ImageTk.PhotoImage(Image.open("idshow.png"))
imgshowinfobg = ImageTk.PhotoImage(Image.open("showinfobg.png"))
imgaboutbg = ImageTk.PhotoImage(Image.open("aboutbg.png"))
imgpickdate = ImageTk.PhotoImage(Image.open("pickdate.png"))
imgcheckadmin = ImageTk.PhotoImage(Image.open("checkadmin.png"))
imgshowalldaybg = ImageTk.PhotoImage(Image.open("showalldaybg.png"))
imgaboutshow = ImageTk.PhotoImage(Image.open("aboutshow.png"))
imgshowwebg = ImageTk.PhotoImage(Image.open("showwebg.png"))
imgshowwe = ImageTk.PhotoImage(Image.open("showwe.png"))
imgsongicon = ImageTk.PhotoImage(Image.open("songicon.png"))
imgrubicon = ImageTk.PhotoImage(Image.open("rubicon.png"))
imgchecktelsong = ImageTk.PhotoImage(Image.open("checktelsong.png"))
imgchecktelrub = ImageTk.PhotoImage(Image.open("checktelrub.png"))
imgshowsongbg = ImageTk.PhotoImage(Image.open("showsongbg.png"))
imgshowrubbg = ImageTk.PhotoImage(Image.open("showrubbg.png"))



#ปุ่มต่างๆหน้าHOME
bt1 = Button(image = imgsearch,width=86, height=56,borderwidth=0,command=showinfo,cursor="hand2").place(x=748 ,y=370)
bt2 = Button(image = imgsongicon,width=44, height=44,borderwidth=0,command=showsong,cursor="hand2").place(x=430 ,y=610)
bt3 = Button(image = imgrubicon,width=44, height=44,borderwidth=0,command=showrub,cursor="hand2").place(x=575 ,y=610)
adminbt = Button(home,image = imgadminicon,width=86, height=56,borderwidth=0,command=chekad,cursor="hand2").place(x=840 ,y=15)
aboutbt = Button(home,image = imgabouticon,width=86, height=56,borderwidth=0,command=about,cursor="hand2").place(x=910 ,y=15)
closebt = Button(home,image = imgcloseicon,width=86, height=56,borderwidth=0,command=close,cursor="hand2").place(x=980 ,y=15)



home.mainloop()