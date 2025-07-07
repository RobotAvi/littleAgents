"""
Утилита для мониторинга инфраструктуры
Анализ логов Grafana, метрик системы и уведомления о проблемах.
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.llm_client import llm_client
from shared.config import Config
from shared.utils import (
    create_streamlit_header, display_metrics, 
    display_data_table, send_notification, 
    validate_config, async_to_sync
)
from datetime import datetime, timedelta
import random

def main():
    create_streamlit_header(
        "Мониторинг инфраструктуры", 
        "Анализ логов Grafana и метрик системы"
    )
    
    # Конфигурация
    config = Config.get_utility_config('infrastructure_monitor')
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Источники данных
        data_sources = st.multiselect(
            "Источники мониторинга:",
            ["Grafana", "Prometheus", "Логи приложений", "Системные метрики"],
            default=["Grafana", "Системные метрики"]
        )
        
        # Временной интервал
        time_range = st.selectbox(
            "Временной интервал:",
            ["Последний час", "Последние 6 часов", "Сутки", "Неделя"],
            index=1
        )
        
        # Уровень алертов
        alert_level = st.selectbox(
            "Минимальный уровень алертов:",
            ["Все", "Warning", "Error", "Critical"],
            index=1
        )
        
        if st.button("🔄 Обновить метрики", type="primary"):
            st.rerun()
    
    # Основное содержимое
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Дашборд", "🚨 Алерты", "📈 Метрики", "🤖 ИИ Анализ"
    ])
    
    with tab1:
        st.subheader("📊 Обзор инфраструктуры")
        
        with st.spinner("Загрузка метрик..."):
            # Симуляция данных мониторинга
            system_metrics = {
                "CPU Usage": random.uniform(20, 80),
                "Memory Usage": random.uniform(30, 70), 
                "Disk Usage": random.uniform(40, 85),
                "Network I/O": random.uniform(10, 90)
            }
            
            # Статус сервисов
            services_status = [
                {"name": "Web Server", "status": "healthy", "uptime": "99.9%"},
                {"name": "Database", "status": "healthy", "uptime": "99.8%"},
                {"name": "Cache", "status": "warning", "uptime": "98.5%"},
                {"name": "API Gateway", "status": "healthy", "uptime": "99.7%"}
            ]
            
            # Метрики системы
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("CPU", f"{system_metrics['CPU Usage']:.1f}%", "2.3%")
            with col2:
                st.metric("Memory", f"{system_metrics['Memory Usage']:.1f}%", "-1.2%")
            with col3:
                st.metric("Disk", f"{system_metrics['Disk Usage']:.1f}%", "0.5%")
            with col4:
                st.metric("Network", f"{system_metrics['Network I/O']:.1f}%", "5.1%")
            
            # Статус сервисов
            st.subheader("🖥️ Статус сервисов")
            
            for service in services_status:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{service['name']}**")
                
                with col2:
                    if service['status'] == 'healthy':
                        st.success("✅ Healthy")
                    elif service['status'] == 'warning':
                        st.warning("⚠️ Warning")
                    else:
                        st.error("❌ Error")
                
                with col3:
                    st.write(f"Uptime: {service['uptime']}")
            
            # График загрузки системы
            st.subheader("📈 Загрузка системы")
            
            import pandas as pd
            import plotly.express as px
            
            # Генерация данных для графика
            hours = list(range(24))
            cpu_data = [random.uniform(20, 80) for _ in hours]
            memory_data = [random.uniform(30, 70) for _ in hours]
            
            df = pd.DataFrame({
                'hour': hours * 2,
                'value': cpu_data + memory_data,
                'metric': ['CPU'] * 24 + ['Memory'] * 24
            })
            
            fig = px.line(
                df,
                x='hour',
                y='value',
                color='metric',
                title="Загрузка CPU и Memory за 24 часа"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🚨 Алерты и уведомления")
        
        # Симуляция алертов
        alerts = [
            {
                "timestamp": datetime.now() - timedelta(minutes=15),
                "level": "warning",
                "source": "Grafana",
                "message": "High memory usage on server-01",
                "value": "75%"
            },
            {
                "timestamp": datetime.now() - timedelta(hours=1),
                "level": "error", 
                "source": "Application",
                "message": "Database connection timeout",
                "value": "5s"
            },
            {
                "timestamp": datetime.now() - timedelta(hours=2),
                "level": "critical",
                "source": "System",
                "message": "Disk space critically low",
                "value": "95%"
            }
        ]
        
        # Фильтрация алертов
        if alert_level != "Все":
            filtered_alerts = [a for a in alerts if a['level'] == alert_level.lower()]
        else:
            filtered_alerts = alerts
        
        for alert in filtered_alerts:
            level_color = {
                'warning': 'warning',
                'error': 'error', 
                'critical': 'error'
            }
            
            level_icon = {
                'warning': '⚠️',
                'error': '🔴',
                'critical': '🚨'
            }
            
            with st.expander(
                f"{level_icon[alert['level']]} {alert['message']} | "
                f"{alert['timestamp'].strftime('%H:%M')}"
            ):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Источник:** {alert['source']}")
                    st.markdown(f"**Время:** {alert['timestamp']}")
                    st.markdown(f"**Сообщение:** {alert['message']}")
                    st.markdown(f"**Значение:** {alert['value']}")
                
                with col2:
                    if st.button(f"Исправить", key=f"fix_{id(alert)}"):
                        st.success("Команда исправления отправлена!")
                    
                    if st.button(f"Игнорировать", key=f"ignore_{id(alert)}"):
                        st.info("Алерт проигнорирован")
    
    with tab3:
        st.subheader("📈 Детальные метрики")
        
        # Выбор метрик для отображения
        selected_metrics = st.multiselect(
            "Выберите метрики:",
            ["CPU Usage", "Memory Usage", "Disk I/O", "Network Traffic", "Response Time"],
            default=["CPU Usage", "Memory Usage"]
        )
        
        if selected_metrics:
            import pandas as pd
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            # Генерация данных
            time_points = pd.date_range(
                start=datetime.now() - timedelta(hours=6),
                end=datetime.now(),
                freq='5T'
            )
            
            fig = make_subplots(
                rows=len(selected_metrics),
                cols=1,
                subplot_titles=selected_metrics,
                shared_xaxes=True
            )
            
            for i, metric in enumerate(selected_metrics):
                values = [random.uniform(20, 80) for _ in time_points]
                
                fig.add_trace(
                    go.Scatter(
                        x=time_points,
                        y=values,
                        name=metric,
                        mode='lines'
                    ),
                    row=i+1,
                    col=1
                )
            
            fig.update_layout(height=400 * len(selected_metrics))
            st.plotly_chart(fig, use_container_width=True)
        
        # Таблица с детальной информацией
        st.subheader("📋 Подробная информация")
        
        metrics_data = []
        for metric in selected_metrics:
            metrics_data.append({
                "Метрика": metric,
                "Текущее значение": f"{random.uniform(30, 70):.1f}%",
                "Среднее за час": f"{random.uniform(25, 65):.1f}%",
                "Максимум": f"{random.uniform(70, 90):.1f}%",
                "Статус": "Норма" if random.random() > 0.3 else "Внимание"
            })
        
        if metrics_data:
            display_data_table(pd.DataFrame(metrics_data))
    
    with tab4:
        st.subheader("🤖 ИИ Анализ инфраструктуры")
        
        if st.button("🔍 Анализировать состояние системы", type="primary"):
            with st.spinner("Анализ метрик и логов..."):
                # Подготовка данных для анализа
                analysis_data = f"""
                Метрики системы:
                - CPU: {system_metrics['CPU Usage']:.1f}%
                - Memory: {system_metrics['Memory Usage']:.1f}%
                - Disk: {system_metrics['Disk Usage']:.1f}%
                - Network: {system_metrics['Network I/O']:.1f}%
                
                Статус сервисов:
                {chr(10).join([f"- {s['name']}: {s['status']} ({s['uptime']})" for s in services_status])}
                
                Активные алерты: {len(alerts)}
                """
                
                @async_to_sync
                async def analyze_infrastructure():
                    return await llm_client.analyze_text(
                        analysis_data,
                        "Проанализируй состояние инфраструктуры. "
                        "Выдели проблемы, риски, рекомендации по оптимизации. "
                        "Предложи действия для улучшения производительности и надежности."
                    )
                
                analysis = analyze_infrastructure()
                
                st.subheader("📝 Результат анализа")
                st.markdown(analysis)
                
                # Рекомендации
                st.subheader("💡 Автоматические рекомендации")
                
                recommendations = []
                if system_metrics['CPU Usage'] > 70:
                    recommendations.append("🔧 Высокая загрузка CPU - рассмотрите масштабирование")
                if system_metrics['Memory Usage'] > 80:
                    recommendations.append("💾 Критичное использование памяти - освободите ресурсы")
                if any(s['status'] != 'healthy' for s in services_status):
                    recommendations.append("⚠️ Обнаружены проблемы с сервисами - требуется вмешательство")
                
                for rec in recommendations:
                    st.warning(rec)

if __name__ == "__main__":
    main()