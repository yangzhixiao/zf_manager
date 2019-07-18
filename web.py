import datetime
import os
import zipfile
import _thread
from io import BytesIO

from flask import Flask, jsonify, send_file, session, request
import db
from send_post import publish_house
import redis

r = redis.Redis(host='yangzhixiao.top', port=6379)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'A0Zr981/3yX 6~XHH!j2N]LWX/,?R8'


@app.before_first_request
def beforerequest():
    db.connect()


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route('/api/login', methods=['POST'])
def zf_login():
    name = request.form['name']
    password = request.form['password']
    if name is None:
        return jsonify({'success': 400, 'msg': '账户不能为空'})
    if password is None:
        return jsonify({'success': 400, 'msg': '密码不能为空'})
    num = db.query_count('select count(*) from account where name=? and password=?', name, password)
    if num > 0:
        session['name'] = name
        return jsonify({'success': 200, 'msg': '登录成功'})
    return jsonify({'success': 400, 'msg': '账户不存在'})


@app.route('/api/list')
def zf_list():
    sql = 'select id, title, imgs, updatetime from house order by updatetime desc'
    ret = db.query(sql)
    return jsonify(ret)


@app.route('/api/publish/<fid>')
def zf_publish(fid):
    try:
        num = db.query_count('select count(*) from publish_record where fid=? and status!=?', fid, '待发布')
        if num > 0:
            return jsonify({'success': 400, 'msg': 'house is already published.'})

        db.execute('insert into publish_record (fid, addtime, status) values (?, ?, ?)',
                   fid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '待发布')
        r.publish('fid', fid)
        return jsonify({'success': 200, 'msg': '发布成功'})
    except Exception as ex:
        return jsonify({'success': 400, 'msg': ex.__str__()})


@app.route('/download/<fid>')
def zf_download(fid):
    if fid is None:
        return 'file not found'
    row = db.query_one('select imgs from house where id=?', fid)
    if row is None:
        return 'file not found'
    file_list = row['imgs'].split(',')
    dl_name = '{}.zip'.format(fid)

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        i = 1
        for _file in file_list:
            with open(os.path.join(os.getcwd(), 'data/images/', _file), 'rb') as fp:
                zf.writestr('{}.jpg'.format(i), fp.read())
            i = i + 1
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename=dl_name, as_attachment=True)


@app.route('/test/publish')
def zf_test():
    r.publish('action', 'do it!')
    return 'done'


def subcribe():
    ps = r.pubsub()
    ps.subscribe('fid')
    for item in ps.listen():
        if item['data'] == 1:
            continue
        fid = str(item['data'], encoding='utf-8')
        print('process item...', fid)
        publish_house(fid, '1')


if __name__ == '__main__':
    _thread.start_new_thread(subcribe)
    app.run()
    db.close()

