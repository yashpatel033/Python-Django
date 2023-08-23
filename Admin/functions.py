def handle_uploaded_file(f):
    with open('Admin/static/assets/images/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

