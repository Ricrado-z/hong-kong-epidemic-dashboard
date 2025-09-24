#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香港各区疫情数据详细分析脚本
深入分析香港各区疫情数据_20250322.xlsx文件
"""

import pandas as pd
import numpy as np
from datetime import datetime

def detailed_data_analysis():
    """
    详细数据分析函数
    """
    # 读取数据
    df = pd.read_excel("香港各区疫情数据_20250322.xlsx")
    
    print("=" * 60)
    print("香港各区疫情数据详细分析报告")
    print("=" * 60)
    
    # 1. 基本信息
    print("\n1. 数据基本信息:")
    print(f"   - 数据形状: {df.shape}")
    print(f"   - 时间范围: {df['报告日期'].min()} 至 {df['报告日期'].max()}")
    print(f"   - 包含地区数: {df['地区名称'].nunique()}")
    print(f"   - 数据天数: {df['报告日期'].nunique()}")
    
    # 2. 地区信息
    print("\n2. 香港各区信息:")
    regions = df['地区名称'].unique()
    for i, region in enumerate(regions, 1):
        print(f"   {i:2d}. {region}")
    
    # 3. 前20行数据详细分析
    print("\n3. 前20行数据详细分析:")
    print("-" * 40)
    
    first_20 = df.head(20)
    for idx, row in first_20.iterrows():
        print(f"\n第{idx+1}行数据:")
        print(f"  报告日期: {row['报告日期']}")
        print(f"  地区名称: {row['地区名称']}")
        print(f"  新增确诊: {row['新增确诊']} 例")
        print(f"  累计确诊: {row['累计确诊']} 例")
        print(f"  现存确诊: {row['现存确诊']} 例")
        print(f"  新增康复: {row['新增康复']} 例")
        print(f"  累计康复: {row['累计康复']} 例")
        print(f"  新增死亡: {row['新增死亡']} 例")
        print(f"  累计死亡: {row['累计死亡']} 例")
        print(f"  发病率: {row['发病率(每10万人)']:.2f} (每10万人)")
        print(f"  人口: {row['人口']:,} 人")
        print(f"  风险等级: {row['风险等级']}")
    
    # 4. 数据特征分析
    print("\n4. 数据特征分析:")
    print("-" * 40)
    
    # 统计各列的基本信息
    numeric_cols = ['新增确诊', '累计确诊', '现存确诊', '新增康复', '累计康复', 
                   '新增死亡', '累计死亡', '发病率(每10万人)', '人口']
    
    for col in numeric_cols:
        print(f"\n{col}统计:")
        print(f"  平均值: {df[col].mean():.2f}")
        print(f"  中位数: {df[col].median():.2f}")
        print(f"  最大值: {df[col].max()}")
        print(f"  最小值: {df[col].min()}")
        print(f"  标准差: {df[col].std():.2f}")
    
    # 5. 风险等级分布
    print("\n5. 风险等级分布:")
    print("-" * 40)
    risk_distribution = df['风险等级'].value_counts()
    for risk_level, count in risk_distribution.items():
        percentage = (count / len(df)) * 100
        print(f"  {risk_level}: {count} 条记录 ({percentage:.1f}%)")
    
    # 6. 地区人口分析
    print("\n6. 各地区人口分析:")
    print("-" * 40)
    region_population = df.groupby('地区名称')['人口'].first().sort_values(ascending=False)
    for region, population in region_population.items():
        print(f"  {region}: {population:,} 人")
    
    # 7. 疫情初期情况分析（前20行）
    print("\n7. 疫情初期情况分析（基于前20行数据）:")
    print("-" * 40)
    
    early_data = df.head(20)
    total_new_cases = early_data['新增确诊'].sum()
    total_cumulative_cases = early_data['累计确诊'].sum()
    regions_with_cases = early_data[early_data['新增确诊'] > 0]['地区名称'].unique()
    
    print(f"  前20条记录中:")
    print(f"  - 新增确诊总数: {total_new_cases} 例")
    print(f"  - 累计确诊总数: {total_cumulative_cases} 例")
    print(f"  - 有新增病例的地区: {', '.join(regions_with_cases)}")
    print(f"  - 所有地区风险等级均为: {early_data['风险等级'].unique()[0]}")
    
    return df

if __name__ == "__main__":
    df = detailed_data_analysis()
