from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/app', defaults={'path': ''})
@app.route('/api/app/<path:path>', methods=['POST', 'GET', 'OPTIONS'])
@app.route('/download', methods=['POST', 'OPTIONS'])
def get_video_data():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json(silent=True) or {}
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'format': 'best[ext=mp4]/bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            download_url = info.get('url')
            if not download_url and 'requested_formats' in info:
                download_url = info['requested_formats'][0].get('url')

            return jsonify({
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': download_url,
                'ext': info.get('ext', 'mp4')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
