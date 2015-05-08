from bottle import route, run, validate, static_file ,request, response, post, get, template, Bottle
import json
import urllib, urllib2

def requesttoRTB(req,exchange,locn):
  try:
    opener = urllib2.build_opener()
    data = json.load(open(req,'r'))

    if locn:
      lat = locn.split(',')[0]
      long = locn.split(',')[1]

    if 'device' in data:
      dev = data['device']
      if 'loc' in dev:
        dev['loc'] = locn
      elif 'geo' in dev:
        geo = dev['geo']
        if 'lat' in geo:
          geo['lat'] = lat
        if 'lon' in geo:
          geo['lon'] = long

    headers = {'Content-type':'application/json','exchange':exchange}
    url ="http://75.101.227.115:8080/auctions?"

    request = urllib2.Request(url, json.dumps(data), headers)

    try:
      result = opener.open(request)
    except Exception,ex:
      print repr(ex)

    result = result.read()
    #print "result : ",result

    if result:
      res = eval(result)

      if 'nurl' in res['seatbid'][0]['bid'][0]:
        winurl = (res['seatbid'][0]['bid'][0]['nurl']).replace('${AUCTION_PRICE}',str(res['seatbid'][0]['bid'][0]['price'])).replace('${AUCTION_CURRENCY}','USD')
        #print "winurl :",winurl

      return res['seatbid'][0]['bid'][0]['adm']
    else:
      return '<h1>No bid</h1>'

  except Exception, ex:
      #print repr(ex)
      return '<h1>Errorrrr!!!</h1>'


@route('/adhost/')
def serve_homepage():
  req = request.params.get('request','test.json')
  exchange = request.params.get('exchange','nexage')
  locn = request.params.get('locn',None)
  resp = requesttoRTB(req,exchange,locn)
  return template(resp,{})

run(host='localhost', port=85)
