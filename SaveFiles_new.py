import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class CompleteProductionDataGenerator:
    def __init__(self, start_date='2024-01-01', end_date='2025-06-30'):  # Увеличил период до июня 2025
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Расширенный список линий с названиями
        self.lines = [
            {'id': 'LINE_A', 'name': 'Автоматическая линия розлива А'},
            {'id': 'LINE_B', 'name': 'Полуавтоматическая линия фасовки B'},
            {'id': 'LINE_C', 'name': 'Высокоскоростная линия упаковки C'},
            {'id': 'LINE_D', 'name': 'Линия смешивания компонентов D'},
            {'id': 'LINE_E', 'name': 'Линия контроля качества E'},
            {'id': 'LINE_F', 'name': 'Экспериментальная линия F'}
        ]
        
        # Список цехов
        self.workshops = [
            {'id': 'WSH_01', 'name': 'Основной производственный цех'},
            {'id': 'WSH_02', 'name': 'Цех предварительной подготовки'},
            {'id': 'WSH_03', 'name': 'Цех финальной обработки'},
            {'id': 'WSH_04', 'name': 'Экспериментальный цех'}
        ]
        
        # Список складов
        self.warehouses = [
            {'id': 'WH_01', 'name': 'Основной склад готовой продукции'},
            {'id': 'WH_02', 'name': 'Склад сырья и материалов'},
            {'id': 'WH_03', 'name': 'Склад сезонного хранения'},
            {'id': 'WH_04', 'name': 'Региональный распределительный склад'}
        ]
        
        # Категории товаров
        self.categories = [
            'Уход за лицом',
            'Уход за телом', 
            'Солнцезащитные средства',
            'Антивозрастная косметика',
            'Натуральная косметика',
            'Профессиональная серия'
        ]
    
    def generate_products(self):
        """Генерация таблицы products с требуемыми полями"""
        print("Генерация продуктов...")
        products_data = []
        
        product_types = {
            'Кремы': ['Крем дневной увлажняющий', 'Крем ночной восстанавливающий', 'Крем SPF30'],
            'Сыворотки': ['Сыворотка витамин C', 'Сыворотка гиалуроновая', 'Сыворотка ретинол'],
            'Лосьоны': ['Лосьон для тела', 'Тонизирующий лосьон', 'Увлажняющий лосьон'],
            'Эмульсии': ['Легкая эмульсия', 'Питательная эмульсия', 'Матирующая эмульсия'],
            'Тоники': ['Очищающий тоник', 'Увлажняющий тоник', 'Восстанавливающий тоник']
        }
        
        sku_id = 1
        for prod_type, items in product_types.items():
            for item in items:
                line = random.choice(self.lines)
                workshop = random.choice(self.workshops)
                category = random.choice(self.categories)
                
                products_data.append({
                    'sku': f'SKU{sku_id:03d}',
                    'type': prod_type,
                    'тип_продукции': 'Готовая продукция',
                    'volume': round(np.random.uniform(0.05, 0.5), 2),
                    'min_batch': np.random.randint(100, 500),
                    'time_per_unit': round(np.random.uniform(0.5, 2.5), 2),
                    'line_id': line['id'],
                    'line_name': line['name'],
                    'WorkshopID': workshop['id'],
                    'WorkshopName': workshop['name'],
                    'Category_name': category,
                    'Product_ID': sku_id,
                    'Product_Name': item,
                    'Product_Group': 'Косметика',
                    'Cost_Price': round(np.random.uniform(50, 300), 2),
                    'Selling_Price': round(np.random.uniform(100, 600), 2)
                })
                sku_id += 1
                
        self.products = pd.DataFrame(products_data)
        return self.products
    
    def generate_dim_time(self):
        """Генерация таблицы времени"""
        print("Генерация временной размерности...")
        dates = pd.date_range(start=self.start_date, end=self.end_date, freq='D')
        
        time_data = []
        for date in dates:
            time_data.append({
                'Date_ID': date.strftime('%Y%m%d'),
                'Date': date,
                'Year': date.year,
                'Month': date.month,
                'Day': date.day,
                'Day_of_Week': date.weekday() + 1,
                'Is_Weekend': date.weekday() >= 5
            })
            
        self.time_df = pd.DataFrame(time_data)
        return self.time_df
    
    def generate_dim_customers(self):
        """Справочник клиентов"""
        print("Генерация клиентов...")
        customers = []
        for i in range(1, 21):  # Уменьшил количество клиентов
            customers.append({
                'Customer_ID': i,
                'Customer_Code': f'CUST{i:03d}',
                'Customer_Name': f'Клиент {i}',
                'Region': random.choice(['Центр', 'Север', 'Юг', 'Восток', 'Запад']),
                'Customer_Type': random.choice(['Оптовый', 'Розничный', 'Дилер'])
            })
        return pd.DataFrame(customers)
    
    def generate_dim_channels(self):
        """Справочник каналов продаж"""
        channels = [
            {'Channel_ID': 1, 'Channel_Code': 'DIRECT', 'Channel_Name': 'Прямые продажи'},
            {'Channel_ID': 2, 'Channel_Code': 'RETAIL', 'Channel_Name': 'Розничная сеть'},
            {'Channel_ID': 3, 'Channel_Code': 'ONLINE', 'Channel_Name': 'Интернет-магазин'},
            {'Channel_ID': 4, 'Channel_Code': 'WHOLESALE', 'Channel_Name': 'Оптовые поставки'},
            {'Channel_ID': 5, 'Channel_Code': 'EXPORT', 'Channel_Name': 'Экспортные поставки'}
        ]
        return pd.DataFrame(channels)
    
    def generate_dim_scenarios(self):
        """Справочник сценариев"""
        scenarios = [
            {'Scenario_ID': 1, 'Code': 'optimal', 'Name': 'Оптимальный'},
            {'Scenario_ID': 2, 'Code': 'positive', 'Name': 'Позитивный'},
            {'Scenario_ID': 3, 'Code': 'negative', 'Name': 'Негативный'},
            {'Scenario_ID': 4, 'Code': 'conservative', 'Name': 'Консервативный'},
            {'Scenario_ID': 5, 'Code': 'aggressive', 'Name': 'Агрессивный'}
        ]
        return pd.DataFrame(scenarios)

    def generate_demand_forecast(self):
        """Генерация прогноза спроса D_i"""
        print("Генерация прогноза спроса...")
        if self.products.empty:
            self.products = self.generate_products()
        if not hasattr(self, 'time_df'):
            self.time_df = self.generate_dim_time()
            
        forecast_data = []
        
        for _, time_row in self.time_df.iterrows():
            for _, product in self.products.iterrows():
                # Базовый спрос
                base_demand = np.random.randint(20, 100)
                
                # Сезонность
                month = time_row['Month']
                if month in [6, 7, 8] and 'SPF' in product['Product_Name']:
                    season_factor = 1.5
                elif month in [12, 1, 2] and 'ночной' in product['Product_Name']:
                    season_factor = 1.3
                else:
                    season_factor = 1.0
                
                D_i = max(10, int(base_demand * season_factor))
                
                forecast_data.append({
                    'date': time_row['Date'],
                    'sku': product['sku'],
                    'D_i': D_i,
                    'Date_ID': time_row['Date_ID'],
                    'Product_ID': product['Product_ID']
                })
                
        return pd.DataFrame(forecast_data)
    
    def generate_stock(self):
        """Генерация текущих остатков s_current_i"""
        print("Генерация остатков...")
        if self.products.empty:
            self.products = self.generate_products()
        if not hasattr(self, 'time_df'):
            self.time_df = self.generate_dim_time()
            
        stock_data = []
        
        for _, time_row in self.time_df.iterrows():
            for _, product in self.products.iterrows():
                warehouse = random.choice(self.warehouses)
                
                # Динамика остатков
                base_stock = np.random.randint(200, 1000)
                day_factor = 1.0 if time_row['Is_Weekend'] else 0.8
                
                s_current_i = max(0, int(base_stock * day_factor))
                
                stock_data.append({
                    'date': time_row['Date'],
                    'sku': product['sku'],
                    's_current_i': s_current_i,
                    'warehouse_id': warehouse['id'],
                    'warehouse_name': warehouse['name'],
                    'Date_ID': time_row['Date_ID'],
                    'Product_ID': product['Product_ID']
                })
                
        return pd.DataFrame(stock_data)
    
    def generate_production_calendar(self):
        """Генерация календаря простоя линий"""
        print("Генерация производственного календаря...")
        if not hasattr(self, 'time_df'):
            self.time_df = self.generate_dim_time()
            
        calendar_data = []
        
        for _, time_row in self.time_df.iterrows():
            for line in self.lines:
                is_working = not time_row['Is_Weekend']
                reason = 'Рабочий день' if is_working else 'Выходной'
                
                # Случайные простои
                if is_working and random.random() < 0.05:  # 5% chance простоя
                    is_working = False
                    reason = 'Техническое обслуживание'
                
                calendar_data.append({
                    'date': time_row['Date'],
                    'line_id': line['id'],
                    'line_name': line['name'],
                    'is_working': is_working,
                    'downtime_reason': reason,
                    'Date_ID': time_row['Date_ID']
                })
                    
        return pd.DataFrame(calendar_data)
    
    def generate_safety_stock_norms(self):
        """Генерация нормативов страхового запаса"""
        print("Генерация нормативов запаса...")
        if self.products.empty:
            self.products = self.generate_products()
            
        norms_data = []
        
        for _, product in self.products.iterrows():
            s_target_i = np.random.randint(100, 300)
            
            norms_data.append({
                'sku': product['sku'],
                's_target_i': s_target_i,
                'Product_ID': product['Product_ID']
            })
            
        return pd.DataFrame(norms_data)

    def generate_sales_actual(self):
        """Генерация ФАКТИЧЕСКИХ продаж - ЦЕНТРАЛЬНАЯ ТАБЛИЦА"""
        print("Генерация фактических продаж...")
        if self.products.empty:
            self.products = self.generate_products()
        if not hasattr(self, 'time_df'):
            self.time_df = self.generate_dim_time()
            
        sales_data = []
        sales_id = 1
        
        # Берем только каждый 3-й день чтобы уменьшить объем данных
        # sample_dates = self.time_df[self.time_df['Date'].dt.day % 3 == 0]
        sample_dates = self.time_df.copy() # убрал данную обрезку по каждому третьему дню, так как
        # приоритет на корректность прогноза

        for _, time_row in sample_dates.iterrows():
            for _, product in self.products.iterrows():
                # Фактические продажи
                actual_qty = np.random.randint(10, 50)
                
                if actual_qty > 0:
                    sales_data.append({
                        'Sales_ID': sales_id,
                        'Date_ID': time_row['Date_ID'],
                        'Product_ID': product['Product_ID'],
                        'Customer_ID': np.random.randint(1, 21),
                        'Channel_ID': np.random.randint(1, 6),
                        'Actual_Qty': actual_qty,
                        'Actual_Revenue': round(actual_qty * product['Selling_Price'], 2),
                        'Discount_Perc': round(np.random.uniform(0, 15), 1),
                        'Return_Qty': max(0, int(actual_qty * 0.02)),
                        'Sales_Status': 'completed',
                        'sku': product['sku'],
                        'date': time_row['Date'],
                        'Distribution_Point': f"Торговая точка {np.random.randint(1, 6)}",
                        'is_Promotion': np.random.randint(0, 2)
                    })
                    sales_id += 1
                
        print(f"Сгенерировано {len(sales_data)} записей продаж")
        return pd.DataFrame(sales_data)
    
    def generate_sales_forecast(self):
        """Генерация прогнозов продаж"""
        print("Генерация прогноза продаж...")
        if self.products.empty:
            self.products = self.generate_products()
        if not hasattr(self, 'time_df'):
            self.time_df = self.generate_dim_time()
            
        forecast_data = []
        forecast_id = 1
        
        scenarios = self.generate_dim_scenarios()
        
        for _, scenario in scenarios.iterrows():
            for _, time_row in self.time_df.iterrows():
                for _, product in self.products.iterrows():
                    # Базовый прогноз
                    base_forecast = np.random.randint(15, 60)
                    
                    # Корректировка по сценарию
                    if scenario['Code'] == 'positive':
                        forecast_qty = base_forecast * 1.2
                    elif scenario['Code'] == 'negative':
                        forecast_qty = base_forecast * 0.8
                    elif scenario['Code'] == 'aggressive':
                        forecast_qty = base_forecast * 1.4
                    elif scenario['Code'] == 'conservative':
                        forecast_qty = base_forecast * 0.7
                    else:
                        forecast_qty = base_forecast
                    
                    forecast_data.append({
                        'Forecast_ID': forecast_id,
                        'Date_ID': time_row['Date_ID'],
                        'Product_ID': product['Product_ID'],
                        'Scenario_ID': scenario['Scenario_ID'],
                        'Final_Forecast_Qty': round(forecast_qty),
                        'sku': product['sku'],
                        'date': time_row['Date'],
                        'прогноз': round(forecast_qty)
                    })
                    forecast_id += 1
                    
        return pd.DataFrame(forecast_data)
    
    def generate_inventory_balances(self):
        """Генерация остатков на складах"""
        print("Генерация балансов запасов...")
        if self.products.empty:
            self.products = self.generate_products()
        if not hasattr(self, 'time_df'):
            self.time_df = self.generate_dim_time()
            
        inventory_data = []
        balance_id = 1
        
        for _, time_row in self.time_df.iterrows():
            for _, product in self.products.iterrows():
                warehouse = random.choice(self.warehouses)
                
                inventory_data.append({
                    'Balance_ID': balance_id,
                    'Date_ID': time_row['Date_ID'],
                    'Product_ID': product['Product_ID'],
                    'warehouse_id': warehouse['id'],
                    'warehouse_name': warehouse['name'],
                    'Opening_Balance_Gp': np.random.randint(100, 800),
                    'Closing_Balance_Gp': np.random.randint(50, 750),
                    'Available_Gp': np.random.randint(40, 700),
                    'sku': product['sku'],
                    'date': time_row['Date'],
                    's_current_i': np.random.randint(50, 700)
                })
                balance_id += 1
                
        return pd.DataFrame(inventory_data)
    
    def generate_production_plans(self):
        """Генерация планов производства"""
        print("Генерация планов производства...")
        if self.products.empty:
            self.products = self.generate_products()
        if not hasattr(self, 'time_df'):
            self.time_df = self.generate_dim_time()
            
        plans_data = []
        plan_id = 1
        
        for _, time_row in self.time_df.iterrows():
            if not time_row['Is_Weekend']:  # Только рабочие дни
                for _, product in self.products.iterrows():
                    plans_data.append({
                        'Plan_ID': plan_id,
                        'Date_ID': time_row['Date_ID'],
                        'Product_ID': product['Product_ID'],
                        'Planned_Qty': np.random.randint(100, 400),
                        'Batch_Size': product['min_batch'],
                        'line_id': product['line_id'],
                        'line_name': product['line_name'],
                        'WorkshopID': product['WorkshopID'],
                        'WorkshopName': product['WorkshopName'],
                        'sku': product['sku'],
                        'date': time_row['Date']
                    })
                    plan_id += 1
                
        return pd.DataFrame(plans_data)
    
    def generate_all_data(self):
        """Генерация ВСЕХ данных"""
        print(" Начало генерации полного набора данных...")
        
        # Генерируем все таблицы
        products = self.generate_products()
        dim_time = self.generate_dim_time()
        dim_customers = self.generate_dim_customers()
        dim_channels = self.generate_dim_channels()
        dim_scenarios = self.generate_dim_scenarios()
        
        # Новые таблицы по вашим требованиям
        demand_forecast = self.generate_demand_forecast()
        stock = self.generate_stock()
        production_calendar = self.generate_production_calendar()
        safety_stock_norms = self.generate_safety_stock_norms()
        
        # Основные таблицы фактов
        sales_actual = self.generate_sales_actual()
        sales_forecast = self.generate_sales_forecast()
        inventory_balances = self.generate_inventory_balances()
        production_plans = self.generate_production_plans()
        
        # Сохранение в Excel
        print("Сохранение в Excel...")
        with pd.ExcelWriter('production_complete_model.xlsx') as writer:
            # Новые таблицы
            products.to_excel(writer, sheet_name='products', index=False)
            demand_forecast.to_excel(writer, sheet_name='demand_forecast', index=False)
            stock.to_excel(writer, sheet_name='stock', index=False)
            production_calendar.to_excel(writer, sheet_name='production_calendar', index=False)
            safety_stock_norms.to_excel(writer, sheet_name='safety_stock_norms', index=False)
            
            # Вчерашние таблицы
            sales_actual.to_excel(writer, sheet_name='Fact_Sales_Actual', index=False)
            sales_forecast.to_excel(writer, sheet_name='Fact_Sales_Forecast', index=False)
            inventory_balances.to_excel(writer, sheet_name='Fact_Inventory_Balances', index=False)
            production_plans.to_excel(writer, sheet_name='Fact_Production_Plans', index=False)
            
            # Справочники
            dim_time.to_excel(writer, sheet_name='Dim_Time', index=False)
            dim_customers.to_excel(writer, sheet_name='Dim_Customers', index=False)
            dim_channels.to_excel(writer, sheet_name='Dim_Channels', index=False)
            dim_scenarios.to_excel(writer, sheet_name='Dim_Scenarios', index=False)
            
            # Расширенный справочник продуктов
            products[['Product_ID', 'sku', 'Product_Name', 'Product_Group', 'Category_name', 
                     'WorkshopID', 'WorkshopName', 'line_id', 'line_name', 
                     'Cost_Price', 'Selling_Price']].to_excel(writer, sheet_name='Dim_Products', index=False)
        
        print(" Генерация завершена! Файл 'production_complete_model.xlsx' создан.")
        
        # Статистика
        all_data = {
            'products': products,
            'demand_forecast': demand_forecast,
            'stock': stock,
            'production_calendar': production_calendar,
            'safety_stock_norms': safety_stock_norms,
            'sales_actual': sales_actual,
            'sales_forecast': sales_forecast,
            'inventory_balances': inventory_balances,
            'production_plans': production_plans
        }
        
        print("\n Статистика генерации:")
        for name, df in all_data.items():
            print(f"{name}: {len(df)} записей")
            
        return all_data

# Запуск генерации
if __name__ == "__main__":
    print("Запуск генератора данных...")
    generator = CompleteProductionDataGenerator()
    all_data = generator.generate_all_data()
    print("Готово! Файл production_complete_model.xlsx создан успешно.")