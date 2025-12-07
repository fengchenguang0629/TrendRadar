#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendRadar Web管理界面 - Flask后端
支持Vue3前端
"""

import os
import json
import yaml
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder=None, static_url_path=None, template_folder='dist')
CORS(app)
app.config['SECRET_KEY'] = 'trendradar-secret-key-2025'

# 配置路径
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / 'config'
OUTPUT_DIR = BASE_DIR / 'output'
CONFIG_FILE = CONFIG_DIR / 'config.yaml'
FREQUENCY_WORDS_FILE = CONFIG_DIR / 'frequency_words.txt'
MAIN_PY = BASE_DIR / 'main.py'

# 爬虫运行状态
crawler_status = {
    'running': False,
    'last_run': None,
    'last_status': None,
    'process': None,
    'logs': []
}


def load_config():
    """加载配置文件"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {'error': str(e)}


def save_config(config_data):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, allow_unicode=True, default_flow_style=False)
        return True
    except Exception as e:
        return str(e)


def load_frequency_words():
    """加载频率词"""
    try:
        with open(FREQUENCY_WORDS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            groups = []
            current_group = []
            for line in content.split('\n'):
                line = line.strip()
                if line:
                    current_group.append(line)
                elif current_group:
                    groups.append(current_group)
                    current_group = []
            if current_group:
                groups.append(current_group)
            return groups
    except Exception as e:
        return []


def save_frequency_words(groups):
    """保存频率词"""
    try:
        content = '\n\n'.join(['\n'.join(group) for group in groups])
        with open(FREQUENCY_WORDS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        return str(e)


def get_news_dates():
    """获取所有新闻日期"""
    try:
        dates = []
        for item in OUTPUT_DIR.iterdir():
            if item.is_dir() and '年' in item.name:
                dates.append(item.name)
        return sorted(dates, reverse=True)
    except Exception as e:
        return []


def get_news_files(date):
    """获取指定日期的新闻文件（仅HTML）"""
    try:
        date_dir = OUTPUT_DIR / date
        files = []
        
        html_dir = date_dir / 'html'
        if html_dir.exists():
            files = sorted([f.name for f in html_dir.iterdir() if f.is_file()], reverse=True)
        
        return files
    except Exception as e:
        return []


def run_crawler():
    """在后台运行爬虫"""
    global crawler_status
    
    try:
        crawler_status['running'] = True
        crawler_status['last_run'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        crawler_status['logs'] = []
        
        process = subprocess.Popen(
            ['python3', str(MAIN_PY)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=str(BASE_DIR)
        )
        
        crawler_status['process'] = process
        
        for line in process.stdout:
            line = line.strip()
            if line:
                crawler_status['logs'].append({
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'message': line
                })
                if len(crawler_status['logs']) > 100:
                    crawler_status['logs'].pop(0)
        
        process.wait()
        
        if process.returncode == 0:
            crawler_status['last_status'] = 'success'
        else:
            crawler_status['last_status'] = 'failed'
            
    except Exception as e:
        crawler_status['last_status'] = 'error'
        crawler_status['logs'].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': f'错误: {str(e)}'
        })
    finally:
        crawler_status['running'] = False
        crawler_status['process'] = None


# ============ 路由 ============

@app.route('/')
def index():
    """主页 - 返回Vue应用"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置"""
    config = load_config()
    return jsonify(config)


@app.route('/api/config', methods=['POST'])
def update_config():
    """更新配置"""
    try:
        config_data = request.json
        result = save_config(config_data)
        if result is True:
            return jsonify({'success': True, 'message': '配置保存成功'})
        else:
            return jsonify({'success': False, 'message': f'保存失败: {result}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """获取关键词"""
    groups = load_frequency_words()
    return jsonify({'groups': groups})


@app.route('/api/keywords', methods=['POST'])
def update_keywords():
    """更新关键词"""
    try:
        data = request.json
        groups = data.get('groups', [])
        result = save_frequency_words(groups)
        if result is True:
            return jsonify({'success': True, 'message': '关键词保存成功'})
        else:
            return jsonify({'success': False, 'message': f'保存失败: {result}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/news/dates', methods=['GET'])
def get_dates():
    """获取新闻日期列表"""
    dates = get_news_dates()
    return jsonify({'dates': dates})


@app.route('/api/news/files/<date>', methods=['GET'])
def get_files(date):
    """获取指定日期的HTML文件列表"""
    files = get_news_files(date)
    return jsonify({'files': files})


@app.route('/api/news/content/<date>/<filename>')
def get_news_content(date, filename):
    """获取新闻内容"""
    try:
        file_path = OUTPUT_DIR / date / 'html' / filename
        if not file_path.exists():
            return jsonify({'error': '文件不存在'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({'content': content, 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/news/<date>/<filename>')
def serve_news_file(date, filename):
    """直接访问新闻文件"""
    try:
        directory = OUTPUT_DIR / date / 'html'
        return send_from_directory(directory, filename)
    except Exception as e:
        return f"Error: {str(e)}", 404


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        dates = get_news_dates()
        total_files = 0
        latest_date = None
        latest_count = 0
        
        if dates:
            latest_date = dates[0]
            files = get_news_files(latest_date)
            latest_count = len(files)
        
        for date in dates:
            files = get_news_files(date)
            total_files += len(files)
        
        return jsonify({
            'total_dates': len(dates),
            'total_files': total_files,
            'latest_date': latest_date,
            'latest_count': latest_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/crawler/start', methods=['POST'])
def start_crawler():
    """启动爬虫"""
    if crawler_status['running']:
        return jsonify({'success': False, 'message': '爬虫正在运行中'}), 400
    
    thread = threading.Thread(target=run_crawler, daemon=True)
    thread.start()
    
    return jsonify({'success': True, 'message': '爬虫已启动'})


@app.route('/api/crawler/stop', methods=['POST'])
def stop_crawler():
    """停止爬虫"""
    if not crawler_status['running']:
        return jsonify({'success': False, 'message': '爬虫未在运行'}), 400
    
    try:
        if crawler_status['process']:
            crawler_status['process'].terminate()
            crawler_status['process'].wait(timeout=5)
        crawler_status['running'] = False
        crawler_status['last_status'] = 'stopped'
        return jsonify({'success': True, 'message': '爬虫已停止'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'停止失败: {str(e)}'}), 500


@app.route('/api/crawler/status', methods=['GET'])
def get_crawler_status():
    """获取爬虫状态"""
    return jsonify({
        'running': crawler_status['running'],
        'last_run': crawler_status['last_run'],
        'last_status': crawler_status['last_status'],
        'log_count': len(crawler_status['logs'])
    })


@app.route('/api/crawler/logs', methods=['GET'])
def get_crawler_logs():
    """获取爬虫日志"""
    limit = request.args.get('limit', 50, type=int)
    logs = crawler_status['logs'][-limit:] if crawler_status['logs'] else []
    return jsonify({'logs': logs})


@app.route('/api/crawler/logs/stream')
def stream_crawler_logs():
    """实时流式传输爬虫日志"""
    def generate():
        last_count = 0
        while True:
            current_count = len(crawler_status['logs'])
            if current_count > last_count:
                new_logs = crawler_status['logs'][last_count:]
                for log in new_logs:
                    yield f"data: {json.dumps(log)}\n\n"
                last_count = current_count
            time.sleep(0.5)
    
    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/cron/info', methods=['GET'])
def get_cron_info():
    """获取定时任务信息"""
    try:
        cron_schedule = os.environ.get('CRON_SCHEDULE', '*/30 * * * *')
        run_mode = os.environ.get('RUN_MODE', 'manual')
        immediate_run = os.environ.get('IMMEDIATE_RUN', 'false')
        
        return jsonify({
            'cron_schedule': cron_schedule,
            'run_mode': run_mode,
            'immediate_run': immediate_run == 'true',
            'is_docker': os.path.exists('/.dockerenv')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ SPA 路由处理 ============
# 这个路由必须在所有 API 路由之后定义
# 用于处理所有非 API 的前端路由
@app.route('/<path:path>')
def spa_fallback(path):
    """处理所有非 API 的前端路由，返回 index.html"""
    # 如果是静态文件（有扩展名），尝试从 dist 目录返回
    if '.' in path:
        try:
            dist_folder = Path(__file__).parent / 'dist'
            return send_from_directory(dist_folder, path)
        except Exception as e:
            # 静态文件不存在，继续返回 index.html
            pass
    
    # 其他所有请求都返回 index.html（SPA 路由）
    return render_template('index.html')


if __name__ == '__main__':
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    port = int(os.environ.get('WEB_PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
