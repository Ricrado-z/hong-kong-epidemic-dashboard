#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香港各区疫情新增确诊人数对比可视化脚本
绘制香港各区新增确诊人数的变化趋势对比图
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
    # 确保日期格式正确
    df['报告日期'] = pd.to_datetime(df['报告日期'])
    
    # 按日期和地区排序
    df = df.sort_values(['报告日期', '地区名称'])
    
    print(f"数据处理完成！共{len(df)}条记录")
    return df

def plot_regional_comparison(df):
    """
    绘制香港各区新增确诊人数对比图表
    """
    print("正在绘制各区对比图表...")
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    
    # 获取所有地区
    regions = df['地区名称'].unique()
    
    # 设置颜色
    colors = plt.cm.Set3(np.linspace(0, 1, len(regions)))
    
    # 第一个子图：所有区域的趋势线
    for i, region in enumerate(regions):
        region_data = df[df['地区名称'] == region]
        ax1.plot(region_data['报告日期'], region_data['新增确诊'], 
                label=region, color=colors[i], linewidth=1.5, alpha=0.8)
    
    ax1.set_title('香港各区每日新增确诊人数变化趋势', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('日期', fontsize=12, fontweight='bold')
    ax1.set_ylabel('新增确诊人数', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    
    # 设置x轴日期格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # 第二个子图：总体趋势
    daily_total = df.groupby('报告日期')['新增确诊'].sum().reset_index()
    ax2.plot(daily_total['报告日期'], daily_total['新增确诊'], 
             linewidth=3, color='#e74c3c', marker='o', markersize=2)
    
    ax2.set_title('香港每日新增确诊人数总计', fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('日期', fontsize=12, fontweight='bold')
    ax2.set_ylabel('新增确诊人数', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # 设置x轴日期格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # 添加统计信息
    max_cases = daily_total['新增确诊'].max()
    max_date = daily_total[daily_total['新增确诊'] == max_cases]['报告日期'].iloc[0]
    avg_cases = daily_total['新增确诊'].mean()
    
    ax2.text(0.02, 0.98, f'最高单日新增: {max_cases}例 ({max_date.strftime("%m-%d")})\n平均每日新增: {avg_cases:.1f}例', 
             transform=ax2.transAxes, fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('香港各区疫情新增确诊对比.png', dpi=300, bbox_inches='tight')
    print("图表已保存为: 香港各区疫情新增确诊对比.png")
    
    # 显示图表
    plt.show()

def create_regional_summary(df):
    """
    创建各区疫情统计摘要
    """
    print("\n=== 香港各区疫情统计摘要 ===")
    
    # 按地区统计
    regional_stats = df.groupby('地区名称').agg({
        '新增确诊': ['sum', 'mean', 'max'],
        '人口': 'first'
    }).round(2)
    
    regional_stats.columns = ['总新增确诊', '平均每日新增', '最高单日新增', '人口']
    regional_stats = regional_stats.sort_values('总新增确诊', ascending=False)
    
    print("\n各区域疫情统计（按总新增确诊排序）:")
    print("-" * 80)
    print(f"{'地区名称':<10} {'总新增确诊':<10} {'平均每日新增':<12} {'最高单日新增':<12} {'人口':<10}")
    print("-" * 80)
    
    for region, row in regional_stats.iterrows():
        print(f"{region:<10} {row['总新增确诊']:<10} {row['平均每日新增']:<12} {row['最高单日新增']:<12} {row['人口']:<10}")

def main():
    """
    主函数
    """
    try:
        # 加载和处理数据
        df = load_and_process_data()
        
        # 绘制对比图表
        plot_regional_comparison(df)
        
        # 创建统计摘要
        create_regional_summary(df)
        
        print("\n✅ 区域对比图表生成完成！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
