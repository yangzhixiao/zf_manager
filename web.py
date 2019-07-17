import os
import zipfile
from io import BytesIO

from flask import Flask, jsonify, send_file
import db

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


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
