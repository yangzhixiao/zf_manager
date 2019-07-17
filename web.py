import os
import zipfile
from io import BytesIO

from flask import Flask, jsonify, send_file, url_for, Response
import db

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def root_dir():
    return os.path.abspath('./static/')


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/')
def zf_index():
    content = get_file('index.html')
    return Response(content, mimetype="text/html")


@app.route('/api/list')
def zf_list():
    sql = 'select id, title, imgs, updatetime from house order by updatetime desc'
    ret = db.query(sql)
    return jsonify(ret)


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


if __name__ == '__main__':
    app.run()
