import string, random, os
from flask import Flask, request, redirect, abort
import redis

app = Flask(__name__)
r = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), decode_responses=True)

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.post('/shorten')
def shorten():
    url = request.get_data(as_text=True)
    if not url:
        return 'missing url', 400
    code = generate_code()
    r.set(code, url)
    return f'{request.host_url}r/{code}', 201

@app.route('/r/<code>')
def resolve(code):
    target = r.get(code)
    if target is None:
        abort(404)
    return redirect(target)
