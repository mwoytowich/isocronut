import os
import sys
import signal
import json
import time
from datetime import datetime

import flask

import isocronut
 
# Instantiate Flask app.
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
  return "pong"


'''
     origin : Either street address or lat,lon. e.g.: '
              "350 5th Avenue, New York, NY 10118" or '
              "40.74844,-73.985664"                   '
    duration: drive time in minutes'
      angles: how many bearings to calculate this contour for (think of this like resolution)'
   tolerance: how many minutes within the exact answer for the contour is good enough'

"40.74844,-73.985664" 20 12 0.1

    curl http://localhost:8080/isochrone?origin=40.74844,-73.985664&duration=10&angles=12&tolerance=0.1    

'''
@app.route('/isochrone', methods=['GET'])
def api_isochrone():
    start_time = time.time()
    request = flask.request

    #if origin is a point, parse it
    origin_x=request.values.get('origin',None)
    if origin_x is not None:
      parts = origin_x.split(",")
      if len(parts) == 2 and isfloat(parts[0]) and isfloat(parts[1]):
        origin = [float(parts[0]),float(parts[1])]        
      else:
        origin = origin_x

    duration=int(request.values.get('duration',10))
    angles=int(request.values.get('angles',12))
    tolerance=float(request.values.get('tolerance',0.1))

    now = datetime.now()
    print '{} <<< Incoming get_isochrone request received for origin {}, duration {}, number_of_angles {}, tolerance  {}'.format(now, origin, duration, angles, tolerance)

    isochrone = generate_isochrone(origin,duration,angles,tolerance)
    json_string = json.dumps(isochrone)


    elapsed_time = time.time() - start_time

    now = datetime.now()
    print '{} >>> returning response (elapsed time: {}):\n{}'.format(now, elapsed_time, json_string)

    return json_string
 
def isfloat(value):
    try:
      float(value)
      return True
    except ValueError:
      return False

def generate_isochrone(origin='',
                       duration='',
                       number_of_angles=12,
                       tolerance=0.1,
                       access_type='personal',
                       config_path='config/'):
    """
    Call the get_isochrone function 
    """
    if origin == '':
        raise Exception('origin cannot be blank')
    if duration == '':
        raise Exception('duration cannot be blank')
    if not isinstance(number_of_angles, int):
        raise Exception('number_of_angles must be an int')

    if isinstance(origin, str):
        origin_geocode = geocode_address(origin, access_type, config_path)
    elif isinstance(origin, list) and len(origin) == 2:
        origin_geocode = origin
    else:
        raise Exception('origin should be a list [lat, lng] or a string address.')

    iso = isocronut.get_isochrone(origin, duration, number_of_angles, tolerance, access_type, config_path)

    return iso


# Graceful exit of ctrl-c
def signal_handler(signal, frame):
    print 'Exiting...\n'
    # for p in jobs:
    #     p.terminate()
    sys.exit(0) 

# Boiler plate to make the app run when executing: python application.py
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.debug = True
    app.run(host='0.0.0.0', port=port, threaded=True)

