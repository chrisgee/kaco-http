# A fake Kaco Inverter with static responses
# Useful for reverse engineering the behavior
# of the Kaco NX Setup App
#
# Copyright 2022 by Jan Dittmer <jdi@l4x.org>
#
#
from flask import Flask, Response, jsonify
from flask import request
import json


app = Flask(__name__)


@app.route('/setting.cgi', methods=['POST'])
def setting():
    return jsonify({'dat': 'ok'})


@app.route('/getdevdata.cgi', methods=['GET'])
def getdevdata(device=2, sn="1234"):
  content = '{"flg":1,"tim":"20241124112956","tmp":284,"fac":4999,"pac":1026,"sac":1026,"qac":0,"eto":23634,"etd":17,"hto":1526,"pf":100,"wan":0,"err":0,"vac":[2236,2254,2267],"iac":[16,15,16],"vpv":[7619,0],"ipv":[132,0],"str":[]}'
  return Response(content, mimetype='application/json')


@app.route('/getdev.cgi', methods=['GET'])
def getdev(device=0):
    if request.args.get('device', 0) == "2":
        content = '{"inv":[{"isn":"8.0NX312064373","add":3,"safety":70,"rate":8000,"msw":"V610-03043-05 ","ssw":"V610-60009-00 ","tsw":"V610-11009-02 ","pac":1026,"etd":17,"eto":23634,"err":0,"cmv":"V2.1.2      ","mty":51,"psb_eb":1}],"num":1}'
    else:
        content = '{"psn":"B3278A2C2448","key":"EFM4VBWVVXRKXMPG","typ":5,"nam":"Wi-Fi Stick","mod":"B32078-10","muf":"KACO","brd":"KACO","hw":"M11","sw":"21618-006R","wsw":"ESP32-WROOM-32U","tim":"2024-11-24 11:32:06","pdk":"","ser":"","protocol":"V1.0","host":"cn-shanghai","port":1883,"status":-1}'
    return Response(content, mimetype='application/json')

@app.route('/wlanget.cgi')
def wlanget():
   return Response('{"mode":"STATION","sid":"Gohle","srh":-70,"ip":"192.168.178.182","gtw":"192.168.178.1","msk":"255.255.255.0"}', mimetype='application/json')

@app.route('/fdbg.cgi', methods=['POST', 'GET'])
def fdbg(path=None):
    print(path)
    print(request.args, request.data, request.path, request.method)
    if request.data == b'{"data":"03030fb8000106d9"}': #read shadow management status
        content =  '{"dat":"ok","data":"0303020000c184"}' #off case
        content =  '{"dat":"ok","data":"03030200010044"}' #on case  
    elif request.data == b'{"data":"03060fb80001cad9"}': #turn shadow management on
        content = '{"dat":"ok","data":"03060fb80001cad9"}'
    elif request.data == b'{"data":"03060fb800000b19"}': #turn shadow management off
        content = '{"dat":"ok","data":"03060fb800000b19"}'
    elif request.data == b'{"data":"03030fba0001a719"}': #read external write access status
        content =  '{"dat":"ok","data":"0303020000c184"}' #off case
        content =  '{"dat":"ok","data":"03030200010044"}' #on case  
    elif request.data == b'{"data":"03060fba00016b19"}': #turn external write on
        content = '{"dat":"ok","data":"03060fba00016b19"}'
    elif request.data == b'{"data":"03060fba0000aad9"}': #turn shadow management off
        content = '{"dat":"ok","data":"03060fba0000aad9"}'
    else:
        content = 'fdbg.cgi: Not implemented data: %s'%request.data
    print(content)
    return Response(content, mimetype='application/jsoon')


@app.route('/<path:path>', methods=['POST', 'GET'])
def catch_all(path):
    print("DEBUG: Before crash", path, request.data)
    app.logger.info('Catch-All %s: %s', (path, request.data))
    return 'Not implemented path: %s' % path

@app.route('/readme')
def readme():
   import markdown
   content = markdown.markdown(open('README.md').read())
   return '<html><body>' + content + '</body></html>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8484)
