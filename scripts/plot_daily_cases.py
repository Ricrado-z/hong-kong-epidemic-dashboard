#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香港每日疫情新增确诊人数可视化脚本
绘制香港每日所有区域新增确诊人数的变化趋势图
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

def load_and_process_data():
    """
    加载并处理疫情数据
    """
    print("正在加载数据...")
    df = pd.read_excel("香港各区疫情数据_20250322.xlsx")
    
    print("正在处理数据...")
    # 按日期汇总所有区域的新增确诊人数
    daily_cases = df.groupby('报告日期')['新增确诊'].sum().reset_index()
    
    # 确保日期格式正确
    daily_cases['报告日期'] = pd.to_datetime(daily_cases['报告日期'])
    
    # 按日期排序
    daily_cases = daily_cases.sort_values('报告日期')
    
    print(f"数据处理完成！共{len(daily_cases)}天的数据")
    return daily_cases

def plot_daily_cases(daily_cases):
    """
    绘制香港每日新增确诊人数图表
    """
    print("正在绘制图表...")
    
    # 创建图表
    plt.figure(figsize=(15, 8))
    
    # 绘制折线图
    plt.plot(daily_cases['报告日期'], daily_cases['新增确诊'], 
             linewidth=2, color='#e74c3c', marker='o', markersize=3)
    
    # 设置图表标题和标签
    plt.title('香港每日疫情新增确诊人数变化趋势', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('日期', fontsize=14, fontweight='bold')
    plt.ylabel('新增确诊人数', fontsize=14, fontweight='bold')
    
    # 设置x轴日期格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    
    # 旋转x轴标签
    plt.xticks(rotation=45)
    
    # 设置网格
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # 设置y轴从0开始
    plt.ylim(bottom=0)
    
    # 添加数据统计信息
    max_cases = daily_cases['新增确诊'].max()
    max_date = daily_cases[daily_cases['新增确诊'] == max_cases]['报告日期'].iloc[0]
    avg_cases = daily_cases['新增确诊'].mean()
    
    # 在图表上添加统计信息
    plt.text(0.02, 0.98, f'最高单日新增: {max_cases}例 ({max_date.strftime("%Y-%m-%d")})\n平均每日新增: {avg_cases:.1f}例', 
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('香港每日疫情新增确诊人数.png', dpi=300, bbox_inches='tight')
    print("图表已保存为: 香港每日疫情新增确诊人数.png")
    
    # 显示图表
    plt.show()

def create_detailed_analysis(daily_cases):
    """
    创建详细的数据分析
    """
    print("\n=== 香港每日疫情数据分析 ===")
    print(f"数据时间范围: {daily_cases['报告日期'].min().strftime('%Y-%m-%d')} 至 {daily_cases['报告日期'].max().strftime('%Y-%m-%d')}")
    print(f"总天数: {len(daily_cases)} 天")
    print(f"总新增确诊: {daily_cases['新增确诊'].sum():,} 例")
    print(f"平均每日新增: {daily_cases['新增确诊'].mean():.1f} 例")
    print(f"最高单日新增: {daily_cases['新增确诊'].max()} 例")
    print(f"最低单日新增: {daily_cases['新增确诊'].min()} 例")
    
    # 找出疫情高峰日期
    top_5_days = daily_cases.nlargest(5, '新增确诊')
    print(f"\n疫情高峰前5天:")
    for idx, row in top_5_days.iterrows():
        print(f"  {row['报告日期'].strftime('%Y-%m-%d')}: {row['新增确诊']} 例")

def main():
    """
    主函数
    """
    try:
        # 加载和处理数据
        daily_cases = load_and_process_data()
        
        # 绘制图表
        plot_daily_cases(daily_cases)
        
        # 创建详细分析
        create_detailed_analysis(daily_cases)
        
        print("\n✅ 图表生成完成！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
