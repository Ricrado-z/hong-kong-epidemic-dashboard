// 香港疫情数据可视化大屏 - JavaScript

// 全局变量
let charts = {};
let updateInterval;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 初始化香港疫情数据可视化大屏...');
    initializeDashboard();
    startAutoUpdate();
});

// 初始化大屏
function initializeDashboard() {
    try {
        // 更新当前时间
        updateCurrentTime();
        
        // 初始化所有图表
        initializeCharts();
        
        // 加载所有数据
        loadAllData();
        
        console.log('✅ 大屏初始化完成');
    } catch (error) {
        console.error('❌ 大屏初始化失败:', error);
        showError('大屏初始化失败，请刷新页面重试');
    }
}

// 更新当前时间
function updateCurrentTime() {
    try {
        const now = new Date();
        const timeString = now.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        const updateTimeElement = document.getElementById('updateTime');
        if (updateTimeElement) {
            updateTimeElement.textContent = timeString;
        }
    } catch (error) {
        console.error('时间更新失败:', error);
    }
}

// 加载所有数据
async function loadAllData() {
    try {
        console.log('📊 开始加载数据...');
        
        // 并行加载所有数据
        const [summaryData, dailyData, regionalData, riskData, monthlyData] = await Promise.all([
            fetchData('/api/summary_stats'),
            fetchData('/api/daily_trend'),
            fetchData('/api/regional_comparison'),
            fetchData('/api/risk_distribution'),
            fetchData('/api/monthly_statistics')
        ]);
        
        // 更新统计卡片
        if (summaryData && !summaryData.error) {
            updateSummaryCards(summaryData);
        }
        
        // 更新图表数据
        if (dailyData && !dailyData.error) {
            updateChartData('dailyTrend', dailyData);
        }
        if (regionalData && !regionalData.error) {
            updateChartData('regional', regionalData);
        }
        if (riskData && !riskData.error) {
            updateChartData('risk', riskData);
        }
        if (monthlyData && !monthlyData.error) {
            updateChartData('monthly', monthlyData);
        }
        
        console.log('✅ 所有数据加载完成');
    } catch (error) {
        console.error('❌ 数据加载失败:', error);
        showError('数据加载失败，请检查网络连接');
    }
}

// 获取数据的通用函数
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`获取数据失败 ${url}:`, error);
        return { error: error.message };
    }
}

// 更新统计卡片
function updateSummaryCards(data) {
    try {
        animateNumber('totalCases', data.total_cases);
        animateNumber('avgDaily', data.avg_daily);
        animateNumber('maxDaily', data.max_daily);
        animateNumber('totalRecovered', data.total_recovered);
        animateNumber('totalDeaths', data.total_deaths);
    } catch (error) {
        console.error('统计卡片更新失败:', error);
    }
}

// 数字动画效果
function animateNumber(elementId, targetValue) {
    try {
        const element = document.getElementById(elementId);
        if (!element) {
            console.warn(`元素 ${elementId} 不存在`);
            return;
        }
        
        const startValue = 0;
        const duration = 2000;
        const startTime = performance.now();
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // 使用缓动函数
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = startValue + (targetValue - startValue) * easeOutQuart;
            
            element.textContent = Math.floor(currentValue).toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        }
        
        requestAnimationFrame(updateNumber);
    } catch (error) {
        console.error(`数字动画失败 ${elementId}:`, error);
    }
}

// 初始化所有图表
function initializeCharts() {
    try {
        // 每日趋势图
        const dailyTrendElement = document.getElementById('dailyTrendChart');
        if (dailyTrendElement) {
            charts.dailyTrend = echarts.init(dailyTrendElement);
        }
        
        // 区域对比图
        const regionalElement = document.getElementById('regionalChart');
        if (regionalElement) {
            charts.regional = echarts.init(regionalElement);
        }
        
        // 风险等级分布图
        const riskElement = document.getElementById('riskChart');
        if (riskElement) {
            charts.risk = echarts.init(riskElement);
        }
        
        // 月度统计图
        const monthlyElement = document.getElementById('monthlyChart');
        if (monthlyElement) {
            charts.monthly = echarts.init(monthlyElement);
        }
        
        // 设置默认配置
        setDefaultChartOptions();
        
        console.log('✅ 所有图表初始化完成');
    } catch (error) {
        console.error('❌ 图表初始化失败:', error);
    }
}

// 设置默认图表配置
function setDefaultChartOptions() {
    try {
        // 每日趋势图配置
        if (charts.dailyTrend) {
            charts.dailyTrend.setOption({
                title: {
                    text: '每日新增确诊趋势',
                    left: 'center',
                    textStyle: { color: '#2c3e50', fontSize: 16 }
                },
                tooltip: {
                    trigger: 'axis',
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    textStyle: { color: '#fff' }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    axisLine: { lineStyle: { color: '#ddd' } }
                },
                yAxis: {
                    type: 'value',
                    axisLine: { lineStyle: { color: '#ddd' } }
                },
                series: [{
                    name: '新增确诊',
                    type: 'line',
                    smooth: true,
                    lineStyle: { color: '#e74c3c', width: 3 },
                    areaStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 0, y2: 1,
                            colorStops: [
                                { offset: 0, color: 'rgba(231, 76, 60, 0.3)' },
                                { offset: 1, color: 'rgba(231, 76, 60, 0.05)' }
                            ]
                        }
                    },
                    emphasis: {
                        focus: 'series',
                        itemStyle: { borderWidth: 2, borderColor: '#fff' }
                    }
                }],
                animation: true,
                animationDuration: 2000
            });
        }
        
        // 区域对比图配置
        if (charts.regional) {
            charts.regional.setOption({
                title: {
                    text: '各区域确诊对比',
                    left: 'center',
                    textStyle: { color: '#2c3e50', fontSize: 16 }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'shadow' },
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    textStyle: { color: '#fff' }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    axisLine: { lineStyle: { color: '#ddd' } }
                },
                yAxis: {
                    type: 'category',
                    axisLine: { lineStyle: { color: '#ddd' } }
                },
                series: [{
                    name: '新增确诊',
                    type: 'bar',
                    itemStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 1, y2: 0,
                            colorStops: [
                                { offset: 0, color: '#3498db' },
                                { offset: 1, color: '#2980b9' }
                            ]
                        }
                    },
                    emphasis: {
                        itemStyle: { color: '#e74c3c' }
                    }
                }],
                animation: true,
                animationDuration: 2000
            });
        }
        
        // 风险等级分布图配置
        if (charts.risk) {
            charts.risk.setOption({
                title: {
                    text: '风险等级分布',
                    left: 'center',
                    textStyle: { color: '#2c3e50', fontSize: 16 }
                },
                tooltip: {
                    trigger: 'item',
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    textStyle: { color: '#fff' },
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    top: 'middle'
                },
                series: [{
                    name: '风险等级',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    center: ['60%', '50%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '18',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: []
                }],
                animation: true,
                animationDuration: 2000
            });
        }
        
        // 月度统计图配置
        if (charts.monthly) {
            charts.monthly.setOption({
                title: {
                    text: '月度疫情统计',
                    left: 'center',
                    textStyle: { color: '#2c3e50', fontSize: 16 }
                },
                tooltip: {
                    trigger: 'axis',
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    textStyle: { color: '#fff' }
                },
                legend: {
                    data: ['新增确诊', '新增康复', '新增死亡'],
                    top: 'bottom'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '15%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    axisLine: { lineStyle: { color: '#ddd' } }
                },
                yAxis: {
                    type: 'value',
                    axisLine: { lineStyle: { color: '#ddd' } }
                },
                series: [
                    {
                        name: '新增确诊',
                        type: 'line',
                        smooth: true,
                        lineStyle: { color: '#e74c3c', width: 3 },
                        areaStyle: { color: 'rgba(231, 76, 60, 0.3)' }
                    },
                    {
                        name: '新增康复',
                        type: 'line',
                        smooth: true,
                        lineStyle: { color: '#27ae60', width: 3 },
                        areaStyle: { color: 'rgba(39, 174, 96, 0.3)' }
                    },
                    {
                        name: '新增死亡',
                        type: 'line',
                        smooth: true,
                        lineStyle: { color: '#8e44ad', width: 3 },
                        areaStyle: { color: 'rgba(142, 68, 173, 0.3)' }
                    }
                ],
                animation: true,
                animationDuration: 2000
            });
        }
    } catch (error) {
        console.error('图表配置失败:', error);
    }
}

// 更新图表数据
function updateChartData(chartName, data) {
    try {
        if (!charts[chartName] || !data) return;
        
        switch(chartName) {
            case 'dailyTrend':
                charts.dailyTrend.setOption({
                    xAxis: { data: data.dates },
                    series: [{ data: data.cases }]
                });
                break;
                
            case 'regional':
                charts.regional.setOption({
                    yAxis: { data: data.regions },
                    series: [{ data: data.cases }]
                });
                break;
                
            case 'risk':
                const riskColors = {
                    '低风险': '#27ae60',
                    '中风险': '#f39c12',
                    '高风险': '#e74c3c'
                };
                charts.risk.setOption({
                    series: [{
                        data: data.risk_levels.map((level, index) => ({
                            value: data.counts[index],
                            name: level,
                            itemStyle: { color: riskColors[level] || '#95a5a6' }
                        }))
                    }]
                });
                break;
                
            case 'monthly':
                charts.monthly.setOption({
                    xAxis: { data: data.months },
                    series: [
                        { data: data.new_cases },
                        { data: data.recovered },
                        { data: data.deaths }
                    ]
                });
                break;
        }
    } catch (error) {
        console.error(`图表数据更新失败 ${chartName}:`, error);
    }
}

// 开始自动更新
function startAutoUpdate() {
    try {
        // 每30秒更新一次时间
        setInterval(updateCurrentTime, 30000);
        
        // 每5分钟重新加载数据
        updateInterval = setInterval(loadAllData, 300000);
        
        console.log('✅ 自动更新已启动');
    } catch (error) {
        console.error('自动更新启动失败:', error);
    }
}

// 显示错误信息
function showError(message) {
    console.error(message);
    // 可以在这里添加错误提示UI
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #e74c3c;
        color: white;
        padding: 15px;
        border-radius: 5px;
        z-index: 9999;
        font-size: 14px;
    `;
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    // 5秒后自动移除
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
}

// 窗口大小改变时重新调整图表
window.addEventListener('resize', function() {
    try {
        Object.values(charts).forEach(chart => {
            if (chart) chart.resize();
        });
    } catch (error) {
        console.error('图表调整失败:', error);
    }
});

// 页面卸载时清理
window.addEventListener('beforeunload', function() {
    try {
        if (updateInterval) {
            clearInterval(updateInterval);
        }
    } catch (error) {
        console.error('清理失败:', error);
    }
});
