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


def options_landing(request):
    return render(request, "options_landing.html")


def get_result(request):
    # output_dump = digitaldivide.src.digitaldivideutil.digitaldividefunc()
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

        # TEST
        # print("-- -- --")
        # print("house no --")
        # print(houseSet)
        # print("state --")
        # print(state)
        # print("tech --")
        # print(tech)
        # print("isp --")
        # print(isp)
        # print("price min --")
        # print(pricemin)
        # print("pricemax --")
        # print(pricemax)
        # print("-- -- --")

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
    data = pd.read_csv(path)
    # print("size of data")
    # print(data.shape)
    # print(tech)
    data = data.loc[data['technology'].isin(tech)]
    # print("size of sieved data")
    # print(data.shape)
    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE 1'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )
    data = data.loc[data['isp'].isin(isp)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE 2'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )

    data = data.loc[data['state'].isin(state)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE 3'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )

    data = data.loc[data['monthly.charge'] > float(pricemin)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE'
        return render(
            request,
            'houseset.html',
            {
                'output_dump': output_dump
            }
        )
    data = data.loc[data['monthly.charge'] < float(pricemax)]

    if data.shape == (0, 0):
        output_dump = 'NO RELEVANT SAMPLE'
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
            output_dump = 'NO RELEVANT SAMPLE'
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
        # print(hset)
        (rowindex, h) = next(hset.iterrows())
        # print('>>')
        # print(h)
        # print(h)
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
    j_response_house = digitaldivide.Household.json_template(h)
    return HttpResponse(j_response_house, mimetype="application/json", headers={"Content-disposition": "attachment; filename=damlevels.json"})


def get_rspec():
    global h
    rspec_response = digitaldivide.Star.rspec_write(h)
    return HttpResponse(rspec_response, mimetype="text/xml",
                        headers={"Content-disposition": "attachment; filename=damlevels.xml"})


def get_netem():
    global h
    output_dump =  ''' Netem template down <br>'''
    output_dump += digitaldivide.Star.netem_template_down(h)
    output_dump += ''' Netem template up <br>'''
    output_dump += digitaldivide.Star.netem_template_up(h)

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