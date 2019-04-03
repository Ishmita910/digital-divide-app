from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Greeting
from django.views.decorators.csrf import csrf_protect
import digitaldivide.src.digitaldivide as digitaldivide
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def get_result(request):
    # output_dump = digitaldivide.src.digitaldivideutil.digitaldividefunc()
    hset = digitaldivide.HouseholdSet('digitaldivide/dat/household-internet-data.csv').sample()
    (rowindex, h) = next(hset.iterrows())
    house = digitaldivide.Household(h)
    output_dump='<br>'
    output_dump +=   ''' Selected household ''' + str(house.unit_id) + ''' has the following characteristics: <br>
    Plan:  (Mbps down/up)'''+ str(house.advertised_rate_down)+" "+ str(house.advertised_rate_up)
    output_dump +='''<br>House ISP  '''+str(house.isp)
    output_dump += '''<br> House Technology '''+str(house.technology)
    output_dump += '''<br>House State '''+str(house.state)
    output_dump +='''<br>Estimated price per month: $'''+str(house.monthly_charge)

    output_dump+= '''<br>Upload rate (kbps)  '''+str(house.rate_up_kbps)
    output_dump+='''<br>Download rate (kbps) '''+ str(house.rate_down_kbps)

    output_dump += '''<br>Round-trip delay (ms)  '''+ str(house.latency_ms)
    output_dump +='''<br>Uplink jitter (ms)     '''+ str(house.jitter_up_ms)
    output_dump +='''<br>Downlink jitter (ms)   '''+ str(house.jitter_down_ms)
    output_dump +='''<br>Packet loss (%%)       '''+str(house.loss)
    output_dump += '<br><br><br>'
    # output_dump += str(house.netem_template_up("192.168.0.1")).split()

    return render(
        request,
        'houseset.html',
        {
            'output_dump': output_dump
        }
    )
@csrf_protect
def house_id(request):
    if request.method == 'POST':
        unit_id = request.POST['txtUnitId']
        unit_id = int(str(unit_id).strip())
        allcsv = pd.read_csv('digitaldivide/dat/household-internet-data.csv')
    # output_dump = digitaldivide.src.digitaldivideutil.digitaldividefunc()
    hset = digitaldivide.HouseholdSet('digitaldivide/dat/household-internet-data.csv').sample()
    (rowindex, h) = next(hset.iterrows())
    # unit_id = 243232
    # house = digitaldivide.Household(unit_id)
    house = allcsv[allcsv.unit_id == unit_id].tail(1)

    
    # house = digitaldivide.Household(unit_id)
    # print("new house")
    # print(house)
    output_dump='<br>'
    # output_dump +=   ''' Selected household ''' + str(unit_id) + ''' has the following characteristics: <br>
    # Plan:  (Mbps down/up)'''+ str(house.advertised_rate_down)+" "+ str(house.advertised_rate_up)
    # output_dump +='''<br>House ISP  '''+str(house.isp)
    # output_dump += '''<br> House Technology '''+str(house.technology)
    # output_dump += '''<br>House State '''+str(house.state)
    # output_dump +='''<br>Estimated price per month: $'''+str(house.monthly_charge)
    #
    # output_dump+= '''<br>Upload rate (kbps)  '''+str(house.rate_up_kbps)
    # output_dump+='''<br>Download rate (kbps) '''+ str(house.rate_down_kbps)
    #
    # output_dump += '''<br>Round-trip delay (ms)  '''+ str(house.latency_ms)
    # output_dump +='''<br>Uplink jitter (ms)     '''+ str(house.jitter_up_ms)
    # output_dump +='''<br>Downlink jitter (ms)   '''+ str(house.jitter_down_ms)
    # output_dump +='''<br>Packet loss (%%)       '''+str(house.loss)
    output_dump += '<br><br><br>'+str(house)

    # output_dump += str(house.netem_template_up("192.168.0.1")).split()

    return render(
        request,
        'houseset.html',
        {
            'output_dump': output_dump
        }
    )