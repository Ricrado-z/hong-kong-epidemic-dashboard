#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香港各区疫情数据分析脚本
读取并分析香港各区疫情数据_20250322.xlsx文件
"""

import pandas as pd
import numpy as np
import os

def read_epidemic_data(file_path):
    """
    读取香港各区疫情数据Excel文件
    
    Args:
        file_path (str): Excel文件路径
        
    Returns:
        pandas.DataFrame: 疫情数据
    """
    try:
        # 读取Excel文件
        print(f"正在读取文件: {file_path}")
        df = pd.read_excel(file_path)
        print(f"数据读取成功！数据形状: {df.shape}")
        return df
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def analyze_data_structure(df):
    """
    分析数据结构
    
    Args:
        df (pandas.DataFrame): 数据框
    """
    print("\n=== 数据结构分析 ===")
    print(f"数据形状: {df.shape}")
    print(f"列数: {df.shape[1]}")
    print(f"行数: {df.shape[0]}")
    
    print("\n=== 列名信息 ===")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    print("\n=== 数据类型 ===")
    print(df.dtypes)
    
    print("\n=== 缺失值统计 ===")
    missing_data = df.isnull().sum()
    print(missing_data[missing_data > 0])

def display_first_20_rows(df):
    """
    显示前20行数据
    
    Args:
        df (pandas.DataFrame): 数据框
    """
    print("\n=== 前20行数据 ===")
    print(df.head(20))
    
    print("\n=== 前20行数据详细信息 ===")
    print(df.head(20).to_string())

def main():
    """
    主函数
    """
    # 文件路径
    file_path = "香港各区疫情数据_20250322.xlsx"
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在！")
        return
    
    # 读取数据
    df = read_epidemic_data(file_path)
    
    if df is not None:
        # 分析数据结构
        analyze_data_structure(df)
        
        # 显示前20行数据
        display_first_20_rows(df)
        
        print("\n=== 数据概览 ===")
        print(df.describe())

if __name__ == "__main__":
    main()
