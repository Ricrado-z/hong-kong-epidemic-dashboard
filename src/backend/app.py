#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香港疫情数据可视化大屏 - Flask后端应用
提供数据API接口
"""

from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd
import json
from datetime import datetime
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend')

def load_data():
    """加载疫情数据"""
    try:
        data_path = os.path.join(project_root, 'data', '香港各区疫情数据_20250322.xlsx')
        df = pd.read_excel(data_path)
        df['报告日期'] = pd.to_datetime(df['报告日期'])
        return df
    except Exception as e:
        print(f"数据加载错误: {e}")
        return None

@app.route('/')
def index():
    """主页面"""
    return render_template('dashboard.html')

@app.route('/favicon.ico')
def favicon():
    """网站图标"""
    return send_from_directory('../frontend/images', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/daily_trend')
def daily_trend():
    """每日趋势数据API"""
    df = load_data()
    if df is None:
        return jsonify({'error': '数据加载失败'})
    
    # 按日期汇总所有区域的新增确诊
    daily_data = df.groupby('报告日期')['新增确诊'].sum().reset_index()
    daily_data['报告日期'] = daily_data['报告日期'].dt.strftime('%Y-%m-%d')
    
    return jsonify({
        'dates': daily_data['报告日期'].tolist(),
        'cases': daily_data['新增确诊'].tolist()
    })

@app.route('/api/regional_comparison')
def regional_comparison():
    """区域对比数据API"""
    df = load_data()
    if df is None:
        return jsonify({'error': '数据加载失败'})
    
    # 按地区统计总新增确诊
    regional_data = df.groupby('地区名称')['新增确诊'].sum().reset_index()
    regional_data = regional_data.sort_values('新增确诊', ascending=True)
    
    return jsonify({
        'regions': regional_data['地区名称'].tolist(),
        'cases': regional_data['新增确诊'].tolist()
    })

@app.route('/api/risk_distribution')
def risk_distribution():
    """风险等级分布数据API"""
    df = load_data()
    if df is None:
        return jsonify({'error': '数据加载失败'})
    
    # 统计风险等级分布
    risk_data = df['风险等级'].value_counts().reset_index()
    risk_data.columns = ['risk_level', 'count']
    
    return jsonify({
        'risk_levels': risk_data['risk_level'].tolist(),
        'counts': risk_data['count'].tolist()
    })

@app.route('/api/monthly_statistics')
def monthly_statistics():
    """月度统计数据API"""
    df = load_data()
    if df is None:
        return jsonify({'error': '数据加载失败'})
    
    # 按月份统计
    df['月份'] = df['报告日期'].dt.to_period('M')
    monthly_data = df.groupby('月份').agg({
        '新增确诊': 'sum',
        '新增康复': 'sum',
        '新增死亡': 'sum'
    }).reset_index()
    
    monthly_data['月份'] = monthly_data['月份'].astype(str)
    
    return jsonify({
        'months': monthly_data['月份'].tolist(),
        'new_cases': monthly_data['新增确诊'].tolist(),
        'recovered': monthly_data['新增康复'].tolist(),
        'deaths': monthly_data['新增死亡'].tolist()
    })

@app.route('/api/summary_stats')
def summary_stats():
    """统计摘要数据API"""
    df = load_data()
    if df is None:
        return jsonify({'error': '数据加载失败'})
    
    # 计算关键统计指标
    total_cases = df['新增确诊'].sum()
    avg_daily = df.groupby('报告日期')['新增确诊'].sum().mean()
    max_daily = df.groupby('报告日期')['新增确诊'].sum().max()
    total_recovered = df['新增康复'].sum()
    total_deaths = df['新增死亡'].sum()
    
    # 找出疫情高峰日期
    daily_total = df.groupby('报告日期')['新增确诊'].sum().reset_index()
    peak_date = daily_total[daily_total['新增确诊'] == max_daily]['报告日期'].iloc[0]
    peak_date_str = peak_date.strftime('%Y-%m-%d')
    
    return jsonify({
        'total_cases': int(total_cases),
        'avg_daily': round(avg_daily, 1),
        'max_daily': int(max_daily),
        'peak_date': peak_date_str,
        'total_recovered': int(total_recovered),
        'total_deaths': int(total_deaths)
    })

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print("🚀 启动香港疫情数据可视化大屏...")
    print("📊 访问地址: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)
