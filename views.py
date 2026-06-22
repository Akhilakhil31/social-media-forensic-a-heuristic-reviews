from django.shortcuts import render
import Database
import base64

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'AdminApp/Login.html')

def LoginAction(request):
    uname = request.POST['username']
    pwd = request.POST['password']

    if uname == 'Admin' and pwd == 'Admin':
        return render(request, 'AdminApp/AdminHome.html')
    else:
        return render(request, 'AdminApp/Login.html')

def AdminHome(request):
    return render(request, 'AdminApp/AdminHome.html')

def AddFilter(request):
    return render(request, 'AdminApp/AddFilter.html')

def FilterAction(request):
    cat = request.POST['category']
    filter = request.POST['filter']

    con=Database.connect()
    cur=con.cursor()
    cur.execute("select * from filter where category='"+cat+"' and f_word='"+filter+"'")
    data=cur.fetchone()
    if data is None:
        cur.execute("insert into filter values(null,'"+cat+"','"+filter+"')")
        con.commit()
        context={'msg':'Filter word added successfully..!!'}
        return render(request, 'AdminApp/AddFilter.html',context)
    else:
        context = {'msg': 'Filter word is already Exist in this Category..!!'}
        return render(request, 'AdminApp/AddFilter.html', context)

def ViewAllUsers(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from user ")
    data = cur.fetchall()
    tdata="<table>"
    tdata+="<tr><th>FullName</th><th>Email</th><th>Mobile</th></tr>"
    for d in data:
        tdata+="<tr><td>"+d[1]+"</td>"
        tdata += "<td>" +d[2] + "</td>"
        tdata += "<td>" + d[3]+ "</td>"
        tdata += "</tr>"

    tdata+="<table>"

    context={'data':tdata}
    return render(request,'AdminApp/ViewUsers.html',context)


def fetch_post_image_blob(id):
    connection=Database.connect()
    with connection.cursor() as cursor:
        cursor.execute("SELECT image FROM post WHERE id=%s", [id])
        row = cursor.fetchone()
    return row[0] if row else None

def ViewAllPosts(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from post")
    data = cur.fetchall()
    tdata = "<table>"
    tdata += "<tr><th>UserID</th><th>Title</th><th>Content</th><th>Image</th></tr>"
    for d in data:
        iid = str(d[0])

        print(iid)
        image_blob = fetch_post_image_blob(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        tdata += "<tr><td>" + d[1] + "</td>"
        tdata += "<td>" + d[2] + "</td>"
        tdata += "<td>" + d[3] + "</td>"
        tdata+=f"<td><img src = 'data:images/png;base64,{image_base64}' width=200, height=200></td>"
        tdata += "</tr>"

    tdata += "<table>"

    context = {'data': tdata}
    return render(request, 'AdminApp/ViewAllUsersPost.html', context)

def fetch_image_blob(id):
    connection=Database.connect()
    with connection.cursor() as cursor:
        cursor.execute("SELECT image FROM blocked_post WHERE id=%s", [id])
        row = cursor.fetchone()
    return row[0] if row else None
def ViewForensicReviews(request):
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from blocked_post ")
    data = cur.fetchall()
    tdata = "<table>"
    tdata += "<tr><th>UserID</th><th>Title</th><th>Content</th><th>Image</th><th>Category</th><th>Word</th></tr>"
    for d in data:
        iid = str(d[0])

        print(iid)
        image_blob = fetch_image_blob(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        tdata += "<tr><td>" + d[1] + "</td>"
        tdata += "<td>" + d[2] + "</td>"
        tdata += "<td>" + d[3] + "</td>"
        tdata += f"<td><img src = 'data:images/png;base64,{image_base64}' width=200, height=200></td>"
        tdata += "<td style='color:orange'>" + d[5] + "</td>"
        tdata += "<td style='color:orange'>" + d[6] + "</td>"
        tdata += "</tr>"

    tdata += "<table>"

    context = {'data': tdata}
    return render(request, 'AdminApp/ViewAllForensicPost.html', context)
