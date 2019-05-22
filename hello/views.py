from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
# from django import jsonify
import os
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


def options_landing(request):
    return render(request, "options_landing.html")


def get_result(request):
    # output_dump = digitaldivide.src.digitaldivideutil.digitaldividefunc()
    global data
    path = 'digitaldivide/dat/household-internet-data.csv'
    data = pd.read_csv(path)
    # filter here
    hset = digitaldivide.HouseholdSet(data).sample()

    global h

    # print(hset)
    (rowindex, h) = next(hset.iterrows())
    print('>>')
    # print(h)
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
    output_dump = ''
    if request.method == 'POST':

        houseSet = request.POST['txtHouseSetQty']
        state = request.POST['txtState']
        tech = request.POST['txtTechnology']
        isp = request.POST['txtIsp']
        pricemin = request.POST['txtPriceMin']
        pricemax = request.POST['txtPriceMax']
        houseSet = int(houseSet)
        if state == 'Any':
            state = ['IL', 'NY', 'CA', 'KS', 'OH', 'CO', 'PA', 'NJ', 'OK', 'TX', 'AZ',
                     'GA', 'MA', 'KY', 'MD', 'NC', 'TN', 'WI', 'IA', 'NH', 'UT', 'IN',
                     'MI', 'HI', 'WV', 'FL', 'OR', 'WA', 'AR', 'DE', 'MN', 'VT', 'VA',
                     'ME', 'MT', 'CT', 'DC', 'MO', 'AL', 'NV', 'NE', 'SC', 'RI', 'LA',
                     'MS', 'NM', 'ID', 'WY', 'SD', 'ND']
        else:
            state = [state]
        if tech == 'Any':
            tech = ['CABLE', 'DSL', 'FIBER', 'SATELLITE']
        else:
            tech=[tech]
        if isp == 'Any':
            isp = ['Comcast', 'Time Warner Cable', 'Cox', 'Mediacom', 'Brighthouse',
                   'Charter', 'Cablevision', 'CenturyLink', 'AT&T', 'Windstream',
                   'Frontier', 'Verizon', 'Wildblue/ViaSat', 'Hughes']
        else:
            isp=[isp]

        pricemin = float(pricemin)
        pricemax = float(pricemax)

    else:
        houseSet = "1"
        state = ['IL', 'NY', 'CA', 'KS', 'OH', 'CO', 'PA', 'NJ', 'OK', 'TX', 'AZ',
            'GA', 'MA', 'KY', 'MD', 'NC', 'TN', 'WI', 'IA', 'NH', 'UT', 'IN',
            'MI', 'HI', 'WV', 'FL', 'OR', 'WA', 'AR', 'DE', 'MN', 'VT', 'VA',
            'ME', 'MT', 'CT', 'DC', 'MO', 'AL', 'NV', 'NE', 'SC', 'RI', 'LA',
            'MS', 'NM', 'ID', 'WY', 'SD', 'ND']
        tech = ['CABLE', 'DSL', 'FIBER', 'SATELLITE']
        isp = ['Comcast', 'Time Warner Cable', 'Cox', 'Mediacom', 'Brighthouse',
                'Charter', 'Cablevision', 'CenturyLink', 'AT&T', 'Windstream',
                'Frontier', 'Verizon', 'Wildblue/ViaSat', 'Hughes']
        pricemin = "0"
        pricemax = "300"

    path = 'digitaldivide/dat/household-internet-data.csv'
    # data = pd.read_csv("household-internet-data.csv")
    global data
    data = pd.read_csv(path)
    # print("size of data")
    # print(data.shape)
    # print(tech)
    data = data.loc[data['technology'].isin(tech)]
    # print("size of sieved data")
    # print(data.shape)
    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE , change technology'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )
    data = data.loc[data['isp'].isin(isp)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE , change ISP'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )

    data = data.loc[data['state'].isin(state)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE , change State'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )

    data = data.loc[data['monthly.charge'] > float(pricemin)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE, change monthly minimum price'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )
    data = data.loc[data['monthly.charge'] < float(pricemax)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE, change maximum monthly price'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )


    # filter here
    for i in range(int(houseSet)):

        if i > 0:
            data = data.loc[data['unit_id'] != str(unit_id)]
        if data.shape == (0, 0):
            output_dump = 'NO RELEVANT SAMPLE, less samples for these specs'
            return render(
                request,
                'houseset.html',
                {
                    'output_dump': output_dump
                }
            )
        try:
            print(data.shape)
            # hset = digitaldivide.HouseholdSet(data).sample()
            hset = digitaldivide.HouseholdSet(data).sample()
        except:
            output_dump = 'NO RELEVANT SAMPLE'
            return render(
                request,
                'houseset.html',
                {
                    'output_dump': output_dump
                }
            )

        print(hset)
        global h
        (rowindex, h) = next(hset.iterrows())

        house = digitaldivide.Household(h)

        output_dump+='<br>'
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
        output_dump += '<br><br><br>'+str(house)

    # output_dump += str(house.netem_template_up("192.168.0.1")).split()

    return render(
        request,
        'houseset.html',
        {
            'output_dump': output_dump
        }
    )


def get_json(request):
    global h
    global hset
    global data
    hset = digitaldivide.HouseholdSet(data).sample()
    (rowindex, h) = next(hset.iterrows())
    house = digitaldivide.Household(h)
    j_response_house = digitaldivide.Household.json_template(house)
    # return HttpResponse(json.dumps(j_response_house), content_type="application/json", )
    response = HttpResponse(j_response_house, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="foo.json"'
    return response
    # return jsonify(name='j_dump.json', data=j_response_house)

def get_rspec(request):
    global h
    global hset
    global data
    # hset = digitaldivide.HouseholdSet(data).sample()
    # star = digitaldivide.Star()
    # star.add_household(h)
    # (rowindex, h) = next(hset.iterrows())
    house = digitaldivide.Household(h)
    output_dir = os.getcwd()
    print(output_dir)
    rspec = os.path.join(output_dir, "houses.xml")
    # star.rspec_write(rspec)
    rspec_response = Star.rspec_write(rspec)
    return HttpResponse(rspec_response,content_type="application/text" )


def get_netem(request):
    global h
    global hset
    global data
    house = digitaldivide.Household(h)

    output_dump =  ''' Netem template down <br>'''
    output_dump += str(house.netem_template_down("0.0.0.0"))
    # output_dump += digitaldivide.Household.netem_template_down('192.168.0.1')
    output_dump += ''' Netem template up <br>'''
    output_dump += str(house.netem_template_up("0.0.0.0"))
    # output_dump += digitaldivide.Household.netem_template_up('192.168.0.1')

    output_dump = '<br><br><br>'
    output_dump += ''' Selected household ''' + str(house.unit_id) + ''' has the following characteristics: <br>
        Plan:  (Mbps down/up)''' + str(house.advertised_rate_down) + " " + str(house.advertised_rate_up)
    output_dump += '''<br>House ISP  ''' + str(house.isp)
    output_dump += '''<br> House Technology ''' + str(house.technology)
    output_dump += '''<br>House State ''' + str(house.state)
    output_dump += '''<br>Estimated price per month: $''' + str(house.monthly_charge)

    output_dump += '''<br>Upload rate (kbps)  ''' + str(house.rate_up_kbps)
    output_dump += '''<br>Download rate (kbps) ''' + str(house.rate_down_kbps)

    output_dump += '''<br>Round-trip delay (ms)  ''' + str(house.latency_ms)
    output_dump += '''<br>Uplink jitter (ms)     ''' + str(house.jitter_up_ms)
    output_dump += '''<br>Downlink jitter (ms)   ''' + str(house.jitter_down_ms)
    output_dump += '''<br>Packet loss (%%)       ''' + str(house.loss)
    output_dump += '<br><br><br>'

    return render(
        request,
        'houseset.html',
        {
            'output_dump': output_dump
        }
    )