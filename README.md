# salary-analytics

## Data Sources
* [Сайт Росстата](https://rosstat.gov.ru/)
* [Таблицы уровня инфляции в России](https://уровень-инфляции.рф/)
* [Динамика официального курса ЦБ](https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True)

Итоговый датасет salary_data был преобразован из data sources. Датасет содержит колонку года, и зарплаты: 
* номинальные
* с учётом инфляции
* с учётом инфляции и корректировкой
* зарплата в долларах

Ноутбуки:
* Преобразования можно посмотреть в data_pareparation.ipynb
* Jupyter Notebook с анализом данных: salary-analytics.ipynb
