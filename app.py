import hashlib, string, random, os
from flask import Flask, request, redirect, abort, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), decode_responses=True)

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return False
    stored = r.get(f'user:{auth.username}')
    if stored is None:
        return False
    return stored == hash_password(auth.password)

@app.post('/register')
def register():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if not username or not password:
        return 'username and password required', 400
    if r.exists(f'user:{username}'):
        return 'username already taken', 409
    r.set(f'user:{username}', hash_password(password))
    return 'user created', 201

@app.post('/urls')
def create_url():
    if not authenticate():
        return 'authentication required', 401
    url = request.get_data(as_text=True)
    if not url:
        return 'missing url', 400
    code = generate_code()
    r.set(code, url)
    r.sadd(f'user:{request.authorization.username}:urls', code)
    return f'{request.host_url}r/{code}', 201

@app.get('/urls')
def list_urls():
    if not authenticate():
        return 'authentication required', 401
    codes = r.smembers(f'user:{request.authorization.username}:urls')
    urls = [{
        'short_url': request.host_url + code,
        'original_url': r.get(code),
    } for code in sorted(codes)]
    return jsonify(urls)

@app.route('/r/<code>')
def resolve(code):
    target = r.get(code)
    if target is None:
        abort(404)
    return redirect(target)
