import datetime
import random
import tempfile
import time
import tkinter
from tkinter import filedialog
from tkinter import ttk

from pdfdocument.document import *
from reportlab import *
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, TableStyle

root = tkinter.Tk()
inputValidFlag = False
noOfSets = 1
qcount = 0
colistflag = True
questionslist = []
colists = ""
colist = []
qstring = ""
currentsetno = 0
processingStarted = 0
mainframe = tkinter.Frame(root)
pdfmetrics.registerFont(TTFont('Times New Roman', 'Times New Roman.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman Italic', 'Times New Roman Italic.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman Bold', 'Times New Roman Bold.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman Bold Italic', 'Times New Roman Bold Italic.ttf'))
addMapping('Times New Roman', 0, 0, 'Times New Roman')
addMapping('Times New Roman', 0, 1, 'Times New Roman Italic')
addMapping('Times New Roman', 1, 0, 'Times New Roman Bold')
addMapping('Times New Roman', 1, 1, 'Times New Roman Bold Italic')


def filechooseronclick():  # File open dialog handler
    global filename
    filename = tkinter.filedialog.askopenfilename(parent=root, title="Choose Questions file",
                                                  filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if filename is not (None or ''):
        file = open(filename, 'r', encoding="utf-8")
        global qstring
        qstring = file.read()
        file.close()


def cofilechooseronclick():
    global cofilename
    cofilename = tkinter.filedialog.askopenfilename(parent=root, title="Choose CO file",
                                                    filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if cofilename is not (None or ''):
        file1 = open(cofilename, 'r', encoding="utf-8")
        global colists
        colists = file1.read()
        file1.close()
    else:
        global colistflag
        colistflag = False


def processcol():
    global colists
    global colist
    global colistflag
    tempstr = ""
    stillp = True
    i = 0

    while stillp:
        if i >= len(colists) - 1:
            stillp = False
            continue
        if colists[i] == "#":
            i += 3

            while colists[i] != "#":
                tempstr += colists[i]
                i += 1
            colist.append(tempstr)
            tempstr = ""
            i += 1
        else:
            i += 1

    if len(colist) == 0:
        colistflag = False


def randomgenerate(low, high):  # Random number generator function
    return random.randint(low, high)


def getnsets():
    if inputValidFlag:
        return noOfSets
    else:
        return 0


def getqpdata():
    return questionslist


def getqpdatacount():
    return qcount


def generatepdf2(a, filenamex):
    c = canvas.Canvas(filenamex)
    now = datetime.datetime.now()
    date = "Date: " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    styles = getSampleStyleSheet()
    c.setFont('Times New Roman Bold', 18)
    c.setFontSize(18)
    c.drawCentredString(298, 770, "DAYANANDA SAGAR COLLEGE OF ENGINEERING")
    c.setFont('Times New Roman', 12)
    c.setFontSize(12)
    c.drawString(72, 740, date)
    c.drawRightString(522, 740, "Marks: 50")
    c.drawRightString(525, 690, "Marks")
    c.drawRightString(545, 690, "LL")
    c.drawRightString(565, 690, "CO")
    data = []
    for i in range(0, len(a)):
        temp = str(i + 1) + ". " + a[i][0]
        p = Paragraph(temp, styles["Normal"])
        t1 = str(a[i][1])
        p1 = Paragraph(t1, styles["Normal"])
        p2 = Paragraph(str(a[i][2]), styles["Normal"])
        p3 = Paragraph(str(a[i][3]), styles["Normal"])
        d1list = [[p1, p2, p3]]
        table2 = Table(d1list)
        dlist = [p, table2]
        data.append(dlist)
    table = Table(data, colWidths=[420, 40], vAlign="TOP")
    table.wrap(524, 680)
    table.drawOn(c, 72, 420)
    c.showPage()
    d = []
    global colist
    if colistflag:
        pc = Paragraph("CO", styles["Normal"])
        pd = Paragraph("Statement", styles["Normal"])
        tx = [pc, pd]
        d.append(tx)
        for i in range(0, len(colist)):
            tempd = []
            tempstr = str(i + 1)
            pa = Paragraph(tempstr, styles["Normal"])
            tempd.append(pa)
            tempstr = colist[i]
            pb = Paragraph(tempstr, styles["Normal"])
            tempd.append(pb)
            d.append(tempd)
        t = Table(d, colWidths=[50, 400], hAlign="CENTER", vAlign="TOP")
        t.setStyle(TableStyle(
            [('LINEABOVE', (0, 0), (-1, 0), 2, colors.black), ('BOX', (0, 0), (1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
             ('LINEABOVE', (0, 1), (-1, -1), 0.25, colors.black), ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
             ('ALIGN', (1, 1), (-1, -1), 'RIGHT')]))
        t.wrap(450, 200)
        t.drawOn(c, 72, 500)
        c.showPage()
    c.save()


def reportinvalid():
    global inputValidFlag
    inputValidFlag = False
    popup = tkinter.Tk()
    popup.wm_title("Error!")
    label = tkinter.Label(popup, text="Invalid File!")
    label.pack(side="top", fill="x", pady=10)
    b1 = tkinter.Button(popup, text="Okay", command=popup.destroy)
    b1.pack()
    popup.mainloop()


def questionselector(qlist):
    marks = 0
    selected_questions = []
    used = []
    while marks != 50 and marks <= 50:
        r = randomgenerate(0, len(qlist) - 1)
        if r not in used:
            used.append(r)
            selected_questions.append(qlist[r])
            marks += qlist[r][1]
    else:
        if marks == 50:
            return selected_questions
        elif marks > 50:
            p = selected_questions.pop()
            marks -= p[1]
            rem = 50 - marks
            l1 = len(selected_questions) - 1
            if rem <= 3:
                for i in range(0, rem):
                    selected_questions[l1 - i][1] += 1
                return selected_questions
            else:
                tlist = []
                for i in range(0, len(qlist)):
                    if (qlist[i][1] == rem) and (i not in used):
                        tlist.append(qlist[i])
                if not tlist:
                    i = 0
                    while rem >= 2:
                        selected_questions[len(selected_questions) - 1 - i][1] += 2
                        i += 1
                        rem -= 2
                    if rem != 0:
                        selected_questions[len(selected_questions) - 1][1] += 1
                    return selected_questions
                else:
                    t = randomgenerate(0, len(tlist) - 1)
                    selected_questions.append(tlist[t])
                    return selected_questions


def generateop():
    global currentsetno
    f = tkinter.filedialog.askdirectory()
    if f is None:
        return

    tempdir = tempfile.mkdtemp()
    while currentsetno < noOfSets:
        fil = tempdir + '/file' + str(currentsetno) + ".pdf"
        generatepdf2(questionselector(questionslist), fil)
        currentsetno += 1
    now = datetime.datetime.now()
    date = str(now.day) + " " + str(now.month) + " " + str(now.year) + " " + str(now.hour) + str(now.minute) + str(
        now.second)
    os.rename(tempdir, (f + "/Question Papers" + "-" + date))

    def endprompt(promptx, ui):
        ui.destroy()
        promptx.destroy()

    prompt = tkinter.Tk()
    prompt.geometry("500x300")
    prompt.wm_title("Files Saved")
    lh = tkinter.Label(prompt, text="Files Saved", font=("Times", 20))
    lh.pack(side="top", fill='x', padx=10, pady=10, expand=True)
    global root
    bex = tkinter.Button(prompt, text="Done", command=lambda: endprompt(prompt, root), bg='green', fg='white')
    bex.pack(side="bottom", fill='x', padx=20, pady=10, ipadx=20, ipady=15, expand=True)
    prompt.mainloop()


def generateqp():
    global filename
    global processingStarted
    global inputValidFlag
    if filename is not (None or ""):
        inputValidFlag = True
        processfile()
        processcol()
        processingStarted = 1
        if processingStarted == 1:
            global button1
            global button3
            global dropdownMenu
            global mainframe
            button1.pack_forget()
            button3.pack_forget()
            dropdownMenu.pack_forget()
            dropdownMenu.destroy()
            mainframe.pack_forget()
            button3.destroy()
            button1.destroy()
            mainframe.destroy()
            button2.pack_forget()
            button2.destroy()
            progress1 = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
            progress1.pack()
            progress1.start()
            progress1["value"] = 1
            root.update()
            time.sleep(0.25)
            progress1["value"] = 30
            root.update()
            time.sleep(0.25)
            progress1["value"] = 50
            root.update()
            time.sleep(0.25)
            progress1["value"] = 80
            root.update()
            time.sleep(0.25)
            progress1["value"] = 98
            root.update()
            time.sleep(0.25)
            progress1.pack_forget()
            progress1.destroy()
            button3 = tkinter.Button(root, text="Save File", command=generateop)
            button3.pack(padx=50, pady=10)
            root.update()

    else:
        reportinvalid()


def processfile():
    global filename
    tvalcheck = 0
    if filename is not None or filename is not "":
        file = open(filename, 'r', encoding='utf-8')
        global qstring
        global questionslist
        global qcount
        global inputValidFlag
        qstring = file.read()
        file.close()
        counth = 0
        tempstring = ""
        a = 0
        co = 0
        ll = 0
        for i in range(0, len(qstring)):
            if qstring[i] == '#':
                counth += 1
                if counth == 3 and qstring[i + 1] != "#":
                    counth -= 1
                continue
            if counth == 2:
                tempstring = tempstring + qstring[i]
            elif counth == 4:
                a = a + int(qstring[i])
                if qstring[i + 1] != "#":
                    a = a * 10
            elif counth == 5:
                co = int(qstring[i])
            elif counth == 6:
                ll = int(qstring[i])
            if counth == 7:
                qcount += 1
                questionslist.append([tempstring, a, ll, co])
                counth = 0
                tempstring = ""
                co = 0
                ll = 0
                a = 0
            if counth > 7:
                reportinvalid()
                inputValidFlag = True
        for i in range(0, len(questionslist)):
            tvalcheck += questionslist[i][1]
        if tvalcheck < 50:
            popup = tkinter.Tk()
            popup.wm_title("Error!")
            label = tkinter.Label(popup, text="File doesn't contain questions amounting upto 50 marks.")
            label.pack(side="top", fill="x", pady=10)
            b1 = tkinter.Button(popup, text="Okay", command=popup.destroy)
            b1.pack()
            popup.mainloop()


root.wm_title("Question Paper Generator")
tkinter.Label(root, text='Question Paper Generator', font=("Arial", 20, "bold"), fg="black").pack(pady=20, padx=50)

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady=20, padx=50)
dropdown1 = tkinter.StringVar(root)
dropdownoptions1 = ("1", "2", "3", "4", "5")  # Current Max Sets is 5
dropdown1.set("1")
dropdownMenu = tkinter.OptionMenu(mainframe, dropdown1, *dropdownoptions1)
dropdownMenu["menu"].config(bg="white")
qtext = tkinter.Label(mainframe, text="Choose number of sets: ").grid(row=1, column=1)
dropdownMenu.grid(row=2, column=1)


def dropdownchange(*args):
    global noOfSets
    noOfSets = int(dropdown1.get())


def destroywindow1():
    root.destroy()


dropdown1.trace('w', dropdownchange)
button1 = tkinter.Button(text="Select questions file", command=filechooseronclick)
button2 = tkinter.Button(text="Select CO file", command=cofilechooseronclick)
button3 = tkinter.Button(text="Generate Paper(s)", command=generateqp)
button1.pack(pady=10, padx=50)
button2.pack(pady=10, padx=50)
button3.pack(pady=10, padx=50)

root.mainloop()
