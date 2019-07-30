from django.shortcuts import render
from django.conf import settings
from django.utils import timezone

# Create your views here.

def show_index(request):

    context = {}
    return render(request, 'webcam/index.html', context)


def upload_snapshot(request):
    upload_file = request.FILES['image_file']
    ret = {}
    if upload_file:
        target_folder = settings.MEDIA_ROOT
        if not os.path.exists(target_folder): os.mkdir(target_folder)
        rtime = str(int(time.time()))
        #filename = request.POST['filename']
        filename = "snapshot_{}.png".format(rtime)
        target = os.path.join(target_folder, filename)
        with open(target, 'wb+') as dest:
            for c in upload_file.chunks():
                dest.write(c)
        ret['file_remote_path'] = target
    else:
        return HttpResponse(status=500)
    return HttpResponse(json.dumps(ret), mimetype="application/json")