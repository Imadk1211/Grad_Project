from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import staff, Secretary, Student, Advisor, UploadedFile, Chairman, Vicechairman, secnotification, stdnotification, staffnotification
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.conf import settings
import os
from IPython.display import display
from .barcodetest import generate_barcode, documentType
from datetime import datetime
# Create your views here.
def index(request):
    ID = request.session.get('ID')
    return HttpResponse('<h1> Hey how are you? </h1>')
def get_ddmmyy_date():
    # Get current date and time
    current_date = datetime.now()
    # Format the date as ddmmyy
    formatted_date = current_date.strftime('%d%m%y')
    return formatted_date

def track(request):
    ID = request.session.get('ID')
    try:    
        name = Secretary.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login")
        return redirect('login')
    files = []
    if request.method != 'POST':

        for i in UploadedFile.objects.all():
            files.append(i)
    elif request.method == 'POST': 
        stdid = request.POST['id']
        choice = request.POST['choose']
        if stdid != "":
            if choice == "":
                for i in UploadedFile.objects.all():
                    if i.stdid == stdid:
                        files.append(i)
            elif choice == "seen":
                for i in UploadedFile.objects.all():
                    if i.stdid == stdid and (i.vicestatus == "received" or i.chairstatus == "received" or i.Advisorstatus == "received"):
                        files.append(i)
            elif choice == "Unseen":
                for i in UploadedFile.objects.all():
                    if i.stdid == stdid and (i.vicestatus == "sent" or i.chairstatus == "sent" or i.Advisorstatus == "sent"):
                        files.append(i)
        elif stdid =="":
            for i in UploadedFile.objects.all():
                if choice == "":
                    for i in UploadedFile.objects.all():
                            files.append(i)
                elif choice == "seen":
                    for i in UploadedFile.objects.all():
                        if (i.vicestatus == "received" or i.chairstatus == "received" or i.Advisorstatus == "received"):
                            files.append(i)
                elif choice == "Unseen":
                    for i in UploadedFile.objects.all():
                        if (i.vicestatus == "sent" or i.chairstatus == "sent" or i.Advisorstatus == "sent"):
                            files.append(i)

    context = {

        "name": name,
        "files":files
    }

    return render(request, 'tracking.html', context)

def Req(request):
    ID = request.session.get('ID')
    try:
        name = Student.objects.get(stdid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as a Student to acess this page")
        return redirect("login")
    if request.method =='POST':
        type = request.POST['choice1']
        language = request.POST['choice2']
        g = type+language
        if type == "transcript" and language == "english":
            x = generate_barcode(ID, documentType[g], get_ddmmyy_date())
            for i in UploadedFile.objects.all():
                if i.barcode == x and (i.status != "Denied" and i.status != "Approved"):
                    messages.info(request, "The student has a pending request for this specific document")
                    return redirect("Req")
            mes = "The student "+ name + " with ID =" + ID + " Is requesting an " + language +  " "+type
            secnotification.objects.create(text = mes, stdid = ID, type= type)      
            UploadedFile.objects.create(file = None, stdid = ID, type = type, status = "Pending", location = "Secretary", history = "No history yet", barcode = x, vicestatus = "Not received", chairstatus= "Not received", Advisorstatus = "Not received", flag = "0")
            return redirect("Req")
        elif type == "transcript" and language == "turkish":
            x = generate_barcode(ID, documentType[g], get_ddmmyy_date())
            for i in UploadedFile.objects.all():
                if i.barcode == x and (i.status != "Denied" or i.status != "Approved"):
                    messages.info(request, "The student has a pending request for this specific document")
                    return redirect("Req")
            mes = "The student "+ name + " with ID =" + ID + " Is requesting a " + language + " "+type
            secnotification.objects.create(text = mes, stdid = ID, type= type)
                    
            UploadedFile.objects.create(file = None, stdid = ID, type = type, status = "Pending", location = "Secretary", history = "No history yet", barcode = x, vicestatus = "Not received", chairstatus= "Not received", Advisorstatus = "Not received", flag = "0")
            return redirect("Req")
        elif type == "education-certificate" and language == "english":
            x = generate_barcode(ID, documentType[g], get_ddmmyy_date())
            for i in UploadedFile.objects.all():
                if i.barcode == x and (i.status != "Denied" or i.status != "Approved"):
                    messages.info(request, "The student has a pending request for this specific document")
                    return redirect("Req")
            mes = "The student "+ name + " with ID =" + ID + " Is requesting an " + language + " "+type
            secnotification.objects.create(text = mes, stdid = ID, type= type)
                    
            UploadedFile.objects.create(file = None, stdid = ID, type = type, status = "Pending", location = "Secretary", history = "No history yet", barcode = x ,vicestatus = "Not received", chairstatus= "Not received", Advisorstatus = "Not received", flag = "0")
            return redirect("Req")
        elif type == "education-certificate" and language == "turkish":
            x = generate_barcode(ID, documentType[g], get_ddmmyy_date())
            for i in UploadedFile.objects.all():
                if i.barcode == x and (i.status != "Denied" or i.status != "Approved"):
                    messages.info(request, "The student has a pending request for this specific document")
                    return redirect("Req")
            mes = "The student "+ name + " with ID =" + ID + " Is requesting a " + language + " "+type
            secnotification.objects.create(text = mes, stdid = ID, type= type)       
            UploadedFile.objects.create(file = None, stdid = ID, type = type, status = "Pending", location = "Secretary", history = "No history yet", barcode = x, vicestatus = "Not received", chairstatus= "Not received", Advisorstatus = "Not received", flag = "0")
            return redirect("Req")
    files = []
    for o in UploadedFile.objects.all():
        if (o.type =="transcript" or o.type == "education-certificate")and o.stdid ==ID and o.status == "Approved" and o.file:
            files.append(o)

    context = {
        "name": name,
        "files":files
    }
    
    return render(request, 'Request.html', context)

def stddash(request):
    ID = request.session.get('ID')
    try:
        name = Student.objects.get(stdid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as a Student to acess this page")
        return redirect("login")
    Advisorr = Advisor.objects.get(stdid = ID).Name
    messa = []
    for a in stdnotification.objects.all():
        if ID == a.stdid:
            messa.append(a)
    files = []
    for x in UploadedFile.objects.all():
        if x.status != "Approved" and x.status != "Denied" and x.type == "transcript" or x.type == "education-certificate":
            files.append(x)
    context = {
        "name": name,
        "Advisor": Advisorr,
        "messa":messa,
        "files":files
    }


    
    return render(request, 'student-dashboard.html', context)

def staffdash(request):
    ID = request.session.get('ID')
    try:
        name = staff.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as a staff to access this page")
        return redirect("login")
    files=[]
    flag = False
    for chair in Chairman.objects.all():
        if ID == chair.staf.secid:
            flag =True
            for f in UploadedFile.objects.all():
                    if f.chairstatus == "sent" or f.chairstatus == "received":
                        files.append(f)
                    else:
                        flag = False
            for file in files:
                for student in Student.objects.all():
                    if file.stdid == student.stdid:
                        file.stdid= file.stdid + "------"+student.Name
    for vice in Vicechairman.objects.all():
        if ID == vice.staf.secid:
            flag = True
            for f in UploadedFile.objects.all():
                    if f.vicestatus == "sent" or f.vicestatus == "received":
                        files.append(f)
                    else:
                        flag = False
            for file in files:
                for student in Student.objects.all():
                    if file.stdid == student.stdid:
                        file.stdid= file.stdid + "------"+student.Name
    if flag == False:
        for advise in Advisor.objects.all():
            if ID == advise.secid:
                for f in UploadedFile.objects.all():
                    if f.stdid == advise.stdid and (f.Advisorstatus == "sent" or f.Advisorstatus == "received"):
                        files.append(f)
                for file in files:
                    for student in Student.objects.all():
                        if file.stdid == student.stdid:
                            file.stdid= file.stdid + "------"+student.Name
    messa = []
    for m in staffnotification.objects.all():
        if ID == m.secid:
            messa.append(m)
    context = {
        "name": name,
        "files": files,
        "messa":messa
    }
    return render(request, 'staff-dashboard.html', context)

def secdash(request):
    ID = request.session.get('ID')
    try:
        name = Secretary.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as a Secretary to access this page")
        return redirect("login")
    files =[]
    for f in UploadedFile.objects.all():
        if f.status != "Approved" and f.status != "Denied":
            files.append(f)

    messa=secnotification.objects.all()
    context = {
        "name": name,
        "messa": messa,
        "files": files
    }
    return render(request, 'secretary-dashboard.html', context)

def staffupload(request):
    if request.method == 'POST':
        idd = request.POST['stdid']
        choice = request.POST['dropdown']
        if Student.objects.filter(stdid =idd).exists():
            if request.FILES:
                uploaded_file = request.FILES['file']
        else:
            messages.info(request, "No such student exists in the database.")
            return redirect('staffupload')
            
        UploadedFile.objects.create(file = uploaded_file, stdid = idd, type = choice)
    ID = request.session.get('ID')
    try:
        name = staff.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login")
        return redirect('login')
    messa = staffnotification.objects.all();
    context = {
        "name": name,
        "messa":messa
    }
    return render(request, 'staff-upload.html', context)
def login(request):
    auth.logout(request)
    if request.method == "POST":
        Id = request.POST['id']
        password = request.POST['password']
        user = auth.authenticate(username= Id, password = password)
        request.session['ID'] = Id
        if user is not None and Id[0] == 'S':
            auth.login(request, user)
            return redirect('stddash')
        elif user is not None and Id[0] == 'A':
            request.session['ID'] = Id
            auth.login(request, user)
            return redirect('staffdash')
        elif user is not None and Id[0] == 'T':
            auth.login(request, user)
            return redirect('secdash')
        else:
            messages.info(request, "Invalid ID or password")
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('login')

def upload_file(request):
    uploaded_file = None
    if request.method == 'POST':
        idd = request.POST['stdid']
        choice = request.POST['dropdown']
        if Student.objects.filter(stdid =idd).exists():
            if request.FILES:
                uploaded_file = request.FILES['file']
        else:
            messages.info(request, "No such student exists in the database.")
            return redirect('upload_file')
        if choice == "transcript":
            flag = False
            count = 0
            for uploads in UploadedFile.objects.all():
                count+=1
                x = generate_barcode(idd, documentType[choice], get_ddmmyy_date())
                if uploads.stdid == idd and uploads.type == "transcript" and uploads.vicestatus == "approve" and uploads.Advisorstatus == "approve" and uploads.chairstatus == "approve" and uploads.file:
                        flag = True
                        messages.info(request, "A transcript was already sent today. Or there was no request made for a transcript")
                        return redirect('upload_file')
                elif uploads.stdid == idd and uploads.type == "transcript" and uploads.vicestatus != "approve" and uploads.Advisorstatus != "approve" and uploads.chairstatus != "approve":
                    flag = True
                    messages.info(request, "No acceptance has been received for this student's transcript.")
                    return redirect('upload_file')
                elif uploads.stdid == idd and uploads.type == "transcript" and uploads.vicestatus == "approve" and uploads.Advisorstatus == "approve" and uploads.chairstatus == "approve" and not uploads.file:
                    flag = True
                    UploadedFile.objects.create(file = uploaded_file, stdid = uploads.stdid, type = uploads.type, status = uploads.status, location = uploads.location, history = uploads.history, barcode = uploads.barcode, vicestatus = uploads.vicestatus, chairstatus= uploads.chairstatus, Advisorstatus = uploads.Advisorstatus, flag =0)
                    UploadedFile.objects.filter(id = uploads.id).delete()
                    mes = "Transcript request was approved, Your transcript Can be found in the Request page"
                    stdnotification.objects.create(text = mes, stdid =idd)
                    secnotification.objects.filter(stdid = idd, type = choice).delete()       
            if flag == False:
                messages.info(request, "There was no accepted request made for this document. The request was either denied or not finished.")
                return redirect('upload_file')
        elif choice == "education-certificate":
            flag = False
            count = 0
            for uploads in UploadedFile.objects.all():
                count+=1
                if uploads.stdid == idd and uploads.type == "education-certificate" and uploads.vicestatus == "approve" and uploads.Advisorstatus == "approve" and uploads.chairstatus == "approve" and uploads.file:
                    flag = True
                    messages.info(request, "An education certificate was already sent today.. Or there was no request made for an education certificate")
                    return redirect('upload_file')
                elif uploads.stdid == idd and uploads.type == "education-certificate" and uploads.vicestatus != "approve" and uploads.Advisorstatus != "approve" and uploads.chairstatus != "approve":
                    flag = True
                    messages.info(request, "No acceptance has been received for this student's education-certificate.")
                    return redirect('upload_file')
                elif uploads.stdid == idd and uploads.type == "education-certificate" and uploads.vicestatus == "approve" and uploads.Advisorstatus == "approve" and uploads.chairstatus == "approve" and not uploads.file:
                    flag = True
                    UploadedFile.objects.create(file = uploaded_file, stdid = uploads.stdid, type = uploads.type, status = uploads.status, location = uploads.location, history = uploads.history, barcode = uploads.barcode, vicestatus = uploads.vicestatus, chairstatus= uploads.chairstatus, Advisorstatus = uploads.Advisorstatus, flag =0)
                    UploadedFile.objects.filter(id = uploads.id).delete()
                    mes = "Education certifcate request was approved, Your Education certificate Can be found in the Request page"
                    stdnotification.objects.create(text = mes, stdid =idd)
                    secnotification.objects.filter(stdid = idd, type = choice).delete()
            if flag == False:
                    messages.info(request, "There was no request made for this document")
                    return redirect('upload_file')
            
        else:
            x = generate_barcode(idd, documentType[choice], get_ddmmyy_date())
            UploadedFile.objects.create(file = uploaded_file, stdid = idd, type = choice, status = "Pending", location = "Secretary", history = "No history yet", barcode = x, vicestatus = "Not received", chairstatus= "Not received", Advisorstatus = "Not received", flag=0)
    ID = request.session.get('ID')
    try:
        name = Secretary.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login")
        return redirect('login')
    context = {
        "name": name
    }
    return render(request, 'upload.html', context)

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id= file_id)
    response = HttpResponse(uploaded_file.file, content_type ='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename ="{uploaded_file.file.name}"'
    return response
def download_file2(request, file_id):
    file_obj = get_object_or_404(UploadedFile, pk=file_id)
    file_path = file_obj.file.path
    return FileResponse(open(file_path, 'rb'))

def tracking_complete(request, pk):
    files = UploadedFile.objects.get(id=pk)
    if files.flag == "0" and files.location == "Sent to secretary" and (files.type != "transcript" and files.type != "education-certificate"):
        messages.info(request, "Please input the barcode befor accessing the approval page")
        return redirect('authenticatie', pk = files.id)  
    if files.location == "Sent to secretary" or files.location == "Secretary":
        files.location = "Secretary's office"
        if files.history == "No history yet":
            files.history = "Received By secretary"
            files.save()
            mes = "One of the documents has been updated by secretary"
            stdnotification.objects.create(text = mes, stdid =files.stdid)
        else:
            files.history = files.history + "--Received By secretary"
            files.save()
            mes = "One of the documents has been updated by secretary"
            stdnotification.objects.create(text = mes, stdid =files.stdid)
        
    if files.type != "transcript" and files.type != "education-certificate":

        for i in UploadedFile.objects.all():
            if i.Date == files.Date:
                x = i
        ID = request.session.get('ID')
        try:
            name = Secretary.objects.get(secid=ID).Name
        except ObjectDoesNotExist:
            messages.info(request, "Please login")
            return redirect('login')
        
        context = {
            "name": name,
            "files": files,
            "x": x,
        }
        if request.method == "POST":
            Decision = request.POST['choice1']
            sentto = request.POST['choice2']
            if Decision != "" and (files.vicestatus != "approve" and files.vicestatus != "delay") and (files.chairstatus != "approve" and files.chairstatus != "delay") and (files.Advisorstatus != "approve" and files.Advisorstatus != "delay"):
                messages.info(request, "A decision hasnt been made clear yet")
            elif Decision == "Denied" and (files.vicestatus == "delay" or files.chairstatus == "delay" or files.Advisorstatus == "delay"):
                files.status = "Denied" 
                files.history = files.history+ "--- Request or documents Denied"
                files.save()
                mes = "Your document has been Denied " + files.type
                stdnotification.objects.create(text = mes, stdid =files.stdid)
            elif Decision == "approve" and (files.vicestatus == "approve" and files.chairstatus == "approve" and files.Advisorstatus == "approve"):
                files.status = "Approved"
                files.history = files.history+ "--- Request or documents Approved"
                files.save()
                mes = "Your document has been approved " + files.type
                stdnotification.objects.create(text = mes, stdid =files.stdid)
            elif Decision == "approve" and (files.vicestatus != "approve" and files.chairstatus != "approve" and files.Advisorstatus != "approve"):
                messages.info(request, "The staff has not completely approved the request")
            elif Decision == "" and sentto == "Advisor" and files.Advisorstatus == "Not received" or files.Advisorstatus == "received":
                if files.location != "Secretary" and files.location !="Sent to secretary" and files.location != "Secretary's office":
                    messages.info(request, "The documents/request hasn't been approved or denied yet in its curent location.")
                    return redirect('tracking_complete', pk = files.id)
                else:
                    files.Advisorstatus = "sent"
                    if files.history == "No history yet":
                        files.history ="Sent to Advisor"
                        files.save()
                        files.location = "Sent to Advisor"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Advisor.objects.all():
                            if files.stdid == x.stdid:
                                staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.secid)
                    else:
                        files.history = files.history +"--Sent to Advsior"
                        files.save()
                        files.location = "Sent to Advisor"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Advisor.objects.all():
                            if files.stdid == x.stdid:
                                staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.secid)
            elif Decision == "" and sentto == "Chairman" and files.chairstatus == "Not received" or files.chairstatus == "received":
                if files.location != "Secretary" and files.location !="Sent to secretary" and files.location != "Secretary's office":
                    messages.info(request, "The documents/request hasn't been approved or denied yet in its curent location.")
                    return redirect('tracking_complete', pk = files.id)
                else:
                    files.chairstatus = "sent"
                    files.save()
                    if files.history == "No history yet":
                        files.history ="Sent to Chairman"
                        files.save()
                        files.location = "Sent to Chairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Chairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
                    else:
                        files.history = files.history +"--Sent to Chairman"
                        files.save()
                        files.location = "Sent to Chairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Chairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
            elif Decision == "" and sentto == "Vice-Chairman" and files.vicestatus == "Not received" or files.vicestatus == "received":
                if files.location != "Secretary" and files.location !="Sent to secretary" and files.location != "Secretary's office":
                    messages.info(request, "The documents/request hasn't been approved or denied yet in its curent location.")
                    return redirect('tracking_complete', pk = files.id)
                else:
                    files.vicestatus = "sent"
                    files.save()
                    if files.history == "No history yet":
                        files.history ="Sent to Vice-Chairman"
                        files.save()
                        files.location = "Sent to Vicechairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Vicechairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
                    else:
                        files.history = files.history +"--Sent to Vice Chairman"
                        files.save()
                        files.location = "Sent to Vicechairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Vicechairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
            elif Decision == "" and sentto == "Advisor" and files.Advisorstatus != "Not received":
                messages.info(request, "The file has already been sent to the advisor")
            elif Decision == "" and sentto == "Advisor" and files.chairstatus != "Not received":
                messages.info(request, "The file has already been sent to the Chairman")
            elif Decision == "" and sentto == "Advisor" and files.vicestatus != "Not received":
                messages.info(request, "The file has already been sent to the Vice-chairman")
            else:
                messages.info(request, "Please make a decision or send the documents/request to someone.")

        return render(request, 'tracking-complete.html', context)
    else:
        for i in UploadedFile.objects.all():
            if i.Date == files.Date:
                x = i
        ID = request.session.get('ID')
        try:
            name = Secretary.objects.get(secid=ID).Name
        except ObjectDoesNotExist:
            messages.info(request, "Please login")
            return redirect('login')
        context = {
            "name": name,
            "files": files,
            "x": x,
        }
        if request.method == "POST":
            Decision = request.POST['choice1']
            sentto = request.POST['choice2']
            if Decision != "" and (files.vicestatus != "approve" and files.vicestatus != "delay") and (files.chairstatus != "approve" and files.chairstatus != "delay") and (files.Advisorstatus != "approve" and files.Advisorstatus != "delay"):
                messages.info(request, "A decision hasnt been made clear yet")
            elif Decision == "Denied" and (files.vicestatus == "delay" or files.chairstatus == "delay" or files.Advisorstatus == "delay"):
                files.status = "Denied" 
                files.history = files.history+ "--- Request or documents Denied"
                files.save()
                mes = "Your document was Denied"
                stdnotification.objects.create(text = mes, stdid =files.stdid)
            elif Decision == "approve" and (files.vicestatus == "approve" and files.chairstatus == "approve" and files.Advisorstatus == "approve"):
                files.status = "Approved"
                files.history = files.history+ "--- Request or documents Approved"
                files.save()
                mes = "Your document was Approved sucessfully"
                stdnotification.objects.create(text = mes, stdid =files.stdid)
            elif Decision == "Denied" and (files.vicestatus == "approve" and files.chairstatus == "approve" and files.Advisorstatus == "approve"):
                messages.info(request, "The file was not denied by any of the staff")
                return redirect('tracking_complete', pk = files.id)
            elif Decision == "approve" and (files.vicestatus != "approve" or files.chairstatus != "approve" or files.Advisorstatus != "approve"):
                messages.info(request, "The staff has not completely approved the request")
            elif Decision == "" and sentto == "Advisor" and files.Advisorstatus == "Not received":
                if files.location != "Secretary" and files.location !="Sent to secretary" and files.location != "Secretary's office":
                    messages.info(request, "The documents/request hasn't been approved or denied yet in its curent location.")
                    return redirect('tracking_complete', pk = files.id)
                else:
                    files.Advisorstatus = "sent"
                    files.save()
                    if files.history == "No history yet":
                        files.history ="Sent to Advisor"
                        files.save()
                        files.location = "Sent to Advisor"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Advisor.objects.all():
                            if files.stdid == x.stdid:
                                staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.secid)
                    else:
                        files.history = files.history +"--Sent to Advsior"
                        files.save()
                        files.location = "Sent to Advisor"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Advisor.objects.all():
                            if files.stdid == x.stdid:
                                staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.secid)
            elif Decision == "" and sentto == "Chairman" and files.chairstatus == "Not received":
                if files.location != "Secretary" and files.location !="Sent to secretary" and files.location != "Secretary's office":
                    messages.info(request, "The documents/request hasn't been approved or denied yet in its curent location.")
                    return redirect('tracking_complete', pk = files.id)
                else:
                    files.chairstatus = "sent"
                    if files.history == "No history yet":
                        files.history ="Sent to Chairman"
                        files.save()
                        files.location = "Sent to Chairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Chairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
                        
                    else:
                        files.history = files.history +"--Sent to Chairman"
                        files.save()
                        files.location = "Sent to Chairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Chairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
            elif Decision == "" and sentto == "Vice-Chairman" and files.vicestatus == "Not received":
                if files.location != "Secretary" and files.location !="Sent to secretary" and files.location != "Secretary's office":
                    messages.info(request, "The documents/request hasn't been approved or denied yet in its curent location.")
                    return redirect('tracking_complete', pk = files.id)
                else:
                    files.vicestatus = "sent"
                    if files.history == "No history yet":
                        files.history ="Sent to Vice-Chairman"
                        files.save()
                        files.location = "Sent to Vicechairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Vicechairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
                    else:
                        files.history = files.history +"--Sent to Vice Chairman"
                        files.save()
                        files.location = "Sent to Vicechairman"
                        files.save()
                        mes = "One of the documents has been updated by secretary"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document is expected to arrive from the secretary " + files.type 
                        for x in Vicechairman.objects.all():
                            staffnotification.objects.create(text = messa, stdid = files.stdid, secid = x.staf.secid)
            elif Decision == "" and sentto == "Advisor" and files.Advisorstatus != "Not received":
                messages.info(request, "The file has already been sent to the advisor")
            elif Decision == "" and sentto == "Chairman" and files.chairstatus != "Not received":
                messages.info(request, "The file has already been sent to the Chairman")
            elif Decision == "" and sentto == "Vice-Chairman" and files.vicestatus != "Not received":
                messages.info(request, "The file has already been sent to the Vice-chairman")
            else:
                messages.info(request, "Please make a decision or send the documents/request to someone.")

        return render(request, 'tracking-complete-transcript.html', context)
def popup(request):
    return render(request, 'popup.html')

def staff_tracking(request):
    ID = request.session.get('ID')
    try:    
        name = staff.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login")
        return redirect('login')
    if request.method != "POST":

        files=[]
        flag = False
        for chair in Chairman.objects.all():
            if ID == chair.staf.secid:
                flag =True
                for f in UploadedFile.objects.all():
                    if f.chairstatus == "sent" or f.chairstatus == "received":
                        files.append(f)
                    else:
                        flag = False
                for file in files:
                    for student in Student.objects.all():
                        if file.stdid == student.stdid:
                            file.stdid= file.stdid + "------"+student.Name
        for vice in Vicechairman.objects.all():
            if ID == vice.staf.secid:
                flag = True
                for f in UploadedFile.objects.all():
                    if f.vicestatus == "sent" or f.vicestatus == "received":
                        files.append(f)
                    else:
                        flag = False
                for file in files:
                    for student in Student.objects.all():
                        if file.stdid == student.stdid:
                            file.stdid= file.stdid + "------"+student.Name
        if flag == False:
            for advise in Advisor.objects.all():
                if ID == advise.secid:
                    for f in UploadedFile.objects.all():
                        if f.stdid == advise.stdid and (f.Advisorstatus == "sent" or f.Advisorstatus == "received"):
                            files.append(f)
                    for file in files:
                        for student in Student.objects.all():
                            if file.stdid == student.stdid:
                                file.stdid= file.stdid + "------"+student.Name
    elif request.method == 'POST':
        files=[]
        flag = False
        filter = request.POST['filter']
        for chair in Chairman.objects.all():
            if ID == chair.staf.secid:
                flag =True
                for f in UploadedFile.objects.all():
                    if f.stdid == filter and (f.chairstatus == "sent" or f.chairstatus == "received"):
                        files.append(f)
                for file in files:
                    for student in Student.objects.all():
                        if file.stdid == student.stdid:
                            file.stdid= file.stdid + "------"+student.Name
        for vice in Vicechairman.objects.all():
            if ID == vice.staf.secid:
                flag = True
                for f in UploadedFile.objects.all():
                    if f.stdid == filter and (f.vicestatus == "sent" or f.vicestatus == "received"):
                        files.append(f)
                for file in files:
                    for student in Student.objects.all():
                        if file.stdid == student.stdid:
                            file.stdid= file.stdid + "------"+student.Name
        if flag == False:
            for advise in Advisor.objects.all():
                if ID == advise.secid:
                    for f in UploadedFile.objects.all():
                        if f.stdid == advise.stdid:
                            if f.stdid == filter and (f.Advisorstatus == "sent" or f.Advisorstatus == "received"):
                                files.append(f)
                    for file in files:
                        for student in Student.objects.all():
                            if file.stdid == student.stdid:
                                file.stdid= file.stdid + "------"+student.Name

    context = {
        "name": name,
        "files":files
    }
    #count = UploadedFile.objects.count()
    #if request.method == 'POST':
    #    print(count)
    #    stdid = request.POST['search']
    #    choice = request.POST['selection']
    #    c=1
    #    for std in UploadedFile.objects.all():    
    #        if stdid != std.stdid:
    #            messages.info(request,"There is no such student in the system")
    #            return redirect('staff_tracking')
    #        elif stdid == std.stdid and choice == std.type:
    #            c = c+1
    #            return redirect('staff_tracking_complete')
    #        elif stdid == std.stdid and choice != std.type and c != count:
    #            c=c+1
    #            pass
    #        elif stdid == std.stdid and choice == std.type and c == count:
    #            messages.info(request, "This student has no such file")
    #            return redirect('staff_tracking')
    #        elif stdid == std.stdid and choice != std.type and c == count:
    #            messages.info(request, "This student has no such file")
    #            return redirect('staff_tracking')
#
    return render(request, 'staff_tracking.html', context)

def staff_tracking_complete(request,pk):
    files = UploadedFile.objects.get(id=pk)
    ID = request.session.get('ID')
    try:
        name = staff.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as staff")
        return redirect('login')
    if files.flag == "0" and (files.location == "Sent to Vicechairman" or files.location == "Sent to Chairman" or files.location == "Sent to Advisor") and (files.type != "transcript" and files.type != "education-certificate"):
        print("hello")
        messages.info(request, "Please input the barcode befor accessing the approval page")
        return redirect('authenticatie_staff', pk = files.id)  
    
    
    if files.type != "transcript" and files.type != "education-certificate":
        files.flag = "0"
        files.save()
        for vice in Vicechairman.objects.all():
            if ID == vice.staf.secid:
                files.vicestatus = "received"
                if files.location !="Vicechairman's office":
                    files.history = files.history + "--In Vicechairman's office"
                files.location = "Vicechairman's office"
                files.save()
                mes = "One of the documents has been updated by Vice-Chairman"
                stdnotification.objects.create(text = mes, stdid =files.stdid)
                secnotification.objects.create(text = mes, stdid = files.stdid, type = files.type)
        for chair in Chairman.objects.all():
            if ID == chair.staf.secid:
                files.chairstatus = "received"
                if files.location !="Chairman's office":
                    files.history = files.history+ "--In Chairman's office"
                files.location = "Chairman's office"
                files.save()
                mes = "One of the documents has been updated by Chairman"
                stdnotification.objects.create(text = mes, stdid =files.stdid)
                secnotification.objects.create(text = mes, stdid =files.stdid, type = files.type)
        for advisor in Advisor.objects.all():
            if ID == advisor.secid:
                if files.stdid == advisor.stdid:
                    if files.location == "Vicechairman's office" or files.location == "Chairman's office":
                        if files.Advisorstatus != "received":
                            files.history = files.history + "--In advisor's office"
                        files.Advisorstatus = "received"
                        files.save()
                        mes = "One of the documents has been updated by Advisor"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        secnotification.objects.create(text = mes, stdid = files.stdid, type = files.type)
                    else:
                        files.Advisorstatus = "received"
                        if files.location !="Advisor's office":
                            files.history = files.history+ "--In Advisors's office"
                        files.location = "Advisor's office"
                        files.save()
                        mes = "One of the documents has been updated by Advisor"
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        secnotification.objects.create(text = mes, stdid = files.stdid, type = files.type)

        for std in Student.objects.all():
            if files.stdid == std.stdid:
                naaaaame = std.Name
        if request.method == 'POST':
            choice = request.POST['choice']
            barcode = request.POST['barcode']
            if files.barcode == barcode and choice == "approve":
                for vice in Vicechairman.objects.all():
                    if ID == vice.staf.secid:
                        files.vicestatus = choice
                        files.history =files.history + "--Approved by vice chairman\n"
                        files.flag= "0"
                        files.save()
                        mes = "A document has been approved by the vice-chairman " + files.type
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document has been approved by the vice-chairman and is expected to arrive soon"
                        secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for chair in Chairman.objects.all():
                    if ID == chair.staf.secid:
                        files.chairstatus = choice
                        files.history = files.history + "-- Approved by chairman\n"
                        files.flag= "0"
                        files.save()
                        mes = "A document has been approved by the chairman " + files.type
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document has been approved by the chairman and is expected to arrive soon"
                        secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for advisor in Advisor.objects.all():
                    if ID == advisor.secid:
                        if files.stdid == advisor.stdid:
                            files.Advisorstatus = choice
                            files.history = files.history + "--Approved by advisor\n"
                            files.flag= "0"
                            files.save()
                            mes = "A document has been approved by the Advisor " + files.type
                            stdnotification.objects.create(text = mes, stdid =files.stdid)
                            messa = "A document has been approved by the advisor and is expected to arrive soon"
                            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
            #if files.stdid == barcode and choice == "pending":
            #    for vice in Vicechairman.objects.all():
            #        files.vicestatus = choice
            #        if ID == vice.staf.secid:
            #                files.history = files.history + "\nReceived By Vicechairman\n"
            #                files.save()
            #    for chair in Chairman.objects.all():
            #        files.chairstatus = choice
            #        if ID == chair.staf.secid:
            #                files.history = files.history + "\nReceived By chairman\n" 
            #                files.save()
            #    for advisor in Advisor.objects.all():
            #        files.Advisorstatus = choice
            #        if ID == advisor.secid:
            #                files.history = files.history + "\nReceived By advisor\n"
            #                files.save()
            elif files.barcode == barcode and choice == "delay":
                for vice in Vicechairman.objects.all():
                    if ID == vice.staf.secid:
                            files.vicestatus = choice
                            files.history = files.history + "--Delayed by vice chairman-"
                            files.flag= "0"
                            files.save()
                            mes = "A document has been denied by the vice-chairman " + files.type
                            stdnotification.objects.create(text = mes, stdid =files.stdid)
                            messa = "A document has been denied by the vice-chairman and is expected to arrive soon"
                            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for chair in Chairman.objects.all():
                    if ID == chair.staf.secid:
                            files.chairstatus = choice
                            files.history = files.history + "--Delayed by chairman-"
                            files.flag= "0"
                            files.save()
                            mes = "A document has been denied by the chairman " + files.type
                            stdnotification.objects.create(text = mes, stdid =files.stdid)
                            messa = "A document has been denied by the chairman and is expected to arrive soon"
                            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for advisor in Advisor.objects.all():
                    if ID == advisor.secid:
                            if files.stdid == advisor.stdid:

                                files.Advisorstatus = choice
                                files.history = files.history + "--Delayed by advisor-"
                                files.flag= "0"
                                files.save()
                                mes = "A document has been denied by the advisor " + files.type
                                stdnotification.objects.create(text = mes, stdid =files.stdid)
                                messa = "A document has been denied by the advisor and is expected to arrive soon"
                                secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
            else:
                messages.info(request, "Input a correct barcode")
                return redirect('staff_tracking_complete', pk = files.id)
            files.history =files.history + "--Sent to secretary"
            files.location="Sent to secretary"
            files.save()
            mes = "The documents location has been updated " + files.type
            stdnotification.objects.create(text = mes, stdid =files.stdid)
            messa = "A document is expected to arrive soon"
            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
            return redirect('staff_tracking')
        
        context = {
            "name": name,
            "file": files,
            "naaame":naaaaame
        }
        return render(request, 'staff_tracking_complete.html', context)
    else:
        files.flag = "0"
        files.save()
        for vice in Vicechairman.objects.all():
            if ID == vice.staf.secid:
                files.vicestatus = "received"
                if files.location !="Vicechairman's office":
                    files.history = files.history + "--In Vicechairman's office"
                files.location = "Vicechairman's office"
                files.save()
                mes = "A document has been updated by the vice-chairman " + files.type
                stdnotification.objects.create(text = mes, stdid =files.stdid)
                secnotification.objects.create(text = mes, stdid = files.stdid, type = files.type)
        for chair in Chairman.objects.all():
            if ID == chair.staf.secid:
                files.chairstatus = "received"
                if files.location !="Chairman's office":
                    files.history = files.history+ "--In Chairman's office"
                files.location = "Chairman's office"
                files.save()
                mes = "A document has been updated by the chairman " + files.type
                stdnotification.objects.create(text = mes, stdid =files.stdid)
                secnotification.objects.create(text = mes, stdid = files.stdid, type = files.type)
        for advisor in Advisor.objects.all():
            if ID == advisor.secid:
                if files.stdid == advisor.stdid:
                    if files.location == "Vicechairman's office" or files.location == "Chairman's office":
                        if files.Advisorstatus != "received":
                            files.history = files.history + "--In advisor's office"
                        files.Advisorstatus = "received"
                        files.save()
                        mes = "A document has been updated by the advisor " + files.type
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        secnotification.objects.create(text = mes, stdid = files.stdid, type = files.type)
                    else:
                        files.Advisorstatus = "received"
                        if files.location !="Advisor's office":
                            files.history = files.history+ "--In Advisor's office"
                        files.location = "Advisor's office"
                        files.save()
                        mes = "A document has been updated by the advisor " + files.type
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        secnotification.objects.create(text = mes, stdid = files.stdid, type = files.type)

        for std in Student.objects.all():
            if files.stdid == std.stdid:
                naaaaame = std.Name
        if request.method == 'POST':
            choice = request.POST['choice']
            if choice == "approve":
                for vice in Vicechairman.objects.all():
                    if ID == vice.staf.secid:
                        files.vicestatus = choice
                        files.history =files.history + "--Approved by vice chairman\n"
                        files.save()
                        mes = "A document has been approved by the vice-chairman " + files.type
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document has been approved by the vice-chairman and is expected to arrive soon"
                        secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for chair in Chairman.objects.all():
                    if ID == chair.staf.secid:
                        files.chairstatus = choice
                        files.history = files.history + "-- Approved by chairman\n"
                        files.save()
                        mes = "A document has been approved by the chairman " + files.type
                        stdnotification.objects.create(text = mes, stdid =files.stdid)
                        messa = "A document has been approved by the chairman and is expected to arrive soon"
                        secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for advisor in Advisor.objects.all():
                    if ID == advisor.secid:
                        if files.stdid == advisor.stdid:
                            files.Advisorstatus = choice
                            files.history = files.history + "--Approved by advisor\n"
                            files.save()
                            mes = "A document has been approved by the advisor " + files.type
                            stdnotification.objects.create(text = mes, stdid =files.stdid)
                            messa = "A document has been approved by the advisor and is expected to arrive soon"
                            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
            elif choice == "delay":
                for vice in Vicechairman.objects.all():
                    if ID == vice.staf.secid:
                            files.vicestatus = choice
                            files.history = files.history + "--Delayed by vice chairman-"
                            files.save()
                            mes = "A document has been denied by the vice-chairman " + files.type
                            stdnotification.objects.create(text = mes, stdid =files.stdid)
                            messa = "A document has been denied by the vice-chairman and is expected to arrive soon"
                            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for chair in Chairman.objects.all():
                    if ID == chair.staf.secid:
                            files.chairstatus = choice
                            files.history = files.history + "--Delayed by chairman-"
                            files.save()
                            mes = "A document has been denied by the chairman " + files.type
                            stdnotification.objects.create(text = mes, stdid =files.stdid)
                            messa = "A document has been denied by the vice-chairman and is expected to arrive soon"
                            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
                for advisor in Advisor.objects.all():
                    if ID == advisor.secid:
                            if files.stdid == advisor.stdid:

                                files.Advisorstatus = choice
                                files.history = files.history + "--Delayed by advisor-"
                                files.save()
                                mes = "A document has been denied by the advisor " + files.type
                                stdnotification.objects.create(text = mes, stdid =files.stdid)
                                messa = "A document has been denied by the vice-chairman and is expected to arrive soon"
                                secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
            else:
                messages.info(request, "Input correct barcode or choose one of the valid options")
                return redirect("staff_tracking_complete", pk = files.id)
            files.history =files.history + "--Sent to secretary"
            files.location="Sent to secretary"
            files.save()
            mes = "The documents location has been updated" + files.type
            stdnotification.objects.create(text = mes, stdid =files.stdid)
            messa = "A document is expected to arrive soon"
            secnotification.objects.create(text = messa, stdid = files.stdid, type = files.type)
            return redirect('staff_tracking')
        
        context = {
            "name": name,
            "file": files,
            "naaame":naaaaame
        }
        return render(request, 'staff_tracking_complete_transcript.html', context)


def student_tracking(request):
    ID = request.session.get('ID')
    try:    
        name = Student.objects.get(stdid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login")
        return redirect('login')
    files = []
    if request.method != "POST":

        for i in UploadedFile.objects.all():
            if i.stdid == ID:
                files.append(i)
    else:
        choice = request.POST["choice"]
        for i in UploadedFile.objects.all():
            if i.stdid == ID and i.type == choice:
                files.append(i)
            elif i.stdid == ID and choice == "":
                files.append(i)
    context = {
        "name": name,
        "files":files
    }
    #count = UploadedFile.objects.count()
    #if request.method == 'POST':
    #    print(count)
    #    stdid = request.POST['search']
    #    choice = request.POST['selection']
    #    c=1
    #    for std in UploadedFile.objects.all():    
    #        if stdid != std.stdid:
    #            messages.info(request,"There is no such student in the system")
    #            return redirect('student_tracking')
    #        elif stdid == std.stdid and choice == std.type:
    #            c = c+1
    #            return redirect('student_tracking_complete')
    #        elif stdid == std.stdid and choice != std.type and c != count:
    #            c=c+1
    #            pass
    #        elif stdid == std.stdid and choice == std.type and c == count:
    #            messages.info(request, "This student has no such file")
    #            return redirect('student_tracking')
    #        elif stdid == std.stdid and choice != std.type and c == count:
    #            messages.info(request, "This student has no such file")
    #            return redirect('student_tracking')
#
    return render(request, 'student_tracking.html', context)

def student_tracking_complete(request):
    ID = request.session.get('ID')
    try:
        name = Student.objects.get(stdid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as staff")
        return redirect('login')
    context = {
        "name": name
    }
    return render(request, 'student_tracking_complete.html', context)

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})
#
#def tracking(request, pk):
#   
#    files = UploadedFile.objects.get(id=pk)
#
#    for i in UploadedFile.objects.all():
#        if i.Date == files.Date:
#            x = i
#    ID = request.session.get('ID')
#    try:
#        name = Secretary.objects.get(secid=ID).Name
#    except ObjectDoesNotExist:
#        messages.info(request, "Please login")
#        return redirect('login')
#    context = {
#        "name": name,
#        "files": files,
#        "x": x,
#        "pk": pk 
#    }
#    return render(request, 'tracking-complete.html', context)
#
def authenticatie(request, pk):
    files = UploadedFile.objects.get(id = pk)
    request.session['pk'] = pk
    ID = request.session.get('ID')
    try:
        name = Secretary.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as staff")
        return redirect('login')
    if files.location != "Sent to secretary" or (files.type == "transcript" or files.type == "education-certificate"):
        return redirect('tracking_complete', pk =files.id)
    context = {
        'name':name
    }
    if request.method == 'POST':
        barcode = request.POST['barcode']
        request.session['barcode'] =barcode
        if barcode == files.barcode and (files.type == "transcript" or files.type == "education-certificate"):
            files.flag = 1
            files.save()
            return redirect('tracking_complete', pk = files.id)
        elif barcode == files.barcode and (files.type != "transcript" or files.type != "education-certificate"):
            files.flag = 1
            files.save()
            return redirect('tracking_complete', pk = files.id)
        else:
            messages.info(request, "Input the correct barcode for this file")
            return render(request, 'authenticate.html',context)
    return render(request, 'authenticate.html', context)

def authenticatie_staff(request, pk):
    files = UploadedFile.objects.get(id = pk)
    print(files.id)
    request.session['pk'] = pk
    ID = request.session.get('ID')
    try:
        name = staff.objects.get(secid = ID).Name
    except ObjectDoesNotExist:
        messages.info(request, "Please login as staff")
        return redirect('login')
    flag = 0
    chairid = ""
    viceid =""
    for i in Chairman.objects.all():
        if i.staf.secid == ID:
            if files.chairstatus == "received" or (files.type == "transcript" or files.type == "education-certificate"):
                request.session['ID']= ID
                return redirect('staff_tracking_complete', pk = files.id)
        else:
            break
    for i in Vicechairman.objects.all():
        if i.staf.secid == ID:
             if files.vicestatus == "received" or (files.type == "transcript" or files.type == "education-certificate"):
                request.session['ID']= ID
                return redirect('staff_tracking_complete', pk = files.id)
        else:
            break
    for i in Advisor.objects.all():
        if i.secid == ID:
                if files.Advisorstatus == "received" or (files.type == "transcript" or files.type == "education-certificate"):
                    request.session['ID']= ID
                    return redirect('staff_tracking_complete', pk = files.id)
    context = {
        'name':name,
    }
    if request.method == 'POST':
        barcode = request.POST['barcode']
        request.session['barcode'] = barcode
        if barcode == files.barcode and (files.type == "transcript" or files.type == "education-certificate"):
            request.session['ID']= ID
            files.flag = "1"
            files.save()
            return redirect('staff_tracking_complete', pk = files.id)
        elif barcode == files.barcode and (files.type != "transcript" or files.type != "education-certificate"):
            request.session['ID']= ID
            files.flag = "1"
            files.save()
            return redirect('staff_tracking_complete', pk = files.id)
        else:
            messages.info(request, "Input the correct barcode for this file")
            return redirect('authenticatie_staff',pk = files.id)
    return render(request, 'authenticate_staff.html', context)
        