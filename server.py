import subprocess
import time
import sys
# sys.path.append("/usr/local/lib/python3.9/dist-packages/")
# sys.path.append("/usr/lib/python3/dist-packages/")
# sys.path.append("/home/vish182/.local/lib/python3.9/site-packages")
from flask import Flask
from flask import jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

filename = "/home/vishu/tab-backend/handlers/audio/music/temp.wav"
output = "/home/vishu/tab-backend/handlers/audio/music/temp2.wav"
other = "./separated/htdemucs/temp2/other.wav"
final = "/home/vishu/tab-backend/handlers/audio/music/temp.wav"

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return int(float(result.stdout))


@app.route('/seperate', methods=["POST"])
def separate():
    result = subprocess.run(["ffmpeg -i {} -acodec pcm_s16le -ac 1 -ar 16000 {}".format(filename, output)], shell=True, capture_output=True, text=True)
    print(result.stdout)

    print("converting to wav")
    time.sleep(0.1)


    result = subprocess.run(["demucs --two-stems=other {}".format(output)], shell=True, capture_output=True, text=True)
    print(result.stdout)

    print("demucs")
    time.sleep(0.1)

    result = subprocess.run(["rm {}".format(filename)], shell=True, capture_output=True, text=True)
    result = subprocess.run(["rm {}".format(output)], shell=True, capture_output=True, text=True)

    print(result.stdout)

    print("delete originals")

    time.sleep(0.1)

    result = subprocess.run(["cp {} {}".format(other, final)], shell=True, capture_output=True, text=True)
    print(result.stdout)
    # "demucs --two-stems=other {}".format(filename)
    return jsonify(get_length(final))

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5555, debug=True)

