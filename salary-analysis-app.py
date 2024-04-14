import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv("salary_data.csv")
salary_data = load_data()


def plot_one_linear(x, y, caps=None, size=(12, 5)):
    fig, ax = plt.subplots(figsize=size)

    sns.lineplot(
        x=x,
        y=y,
        color="#334e70",
        linewidth=2,
        marker='o'
    )

    if caps is not None:
        assert isinstance(caps, (list, tuple)), "TypeError: must be list or tuple"
        assert len(caps) == 3, "IndexError"
        assert type(caps[0]) == type(caps[1]) == type(caps[1]) == str, "TypeError"
        plt.title(caps[0])
        plt.xlabel(caps[1])
        plt.ylabel(caps[2])

    plt.ylim(bottom=0)  # min of vertical axis in 0

    return fig


def multiple_linear(df, caps=None, palette=None, size=(12, 5)):
    fig, ax = plt.subplots(figsize=size)

    if palette is None:
        palette = "rocket_r"

    sns.lineplot(
        data=df,
        linewidth=1.5,
        marker='o',
        markersize=5,
        palette=palette,
        dashes=False,  # off auto line style variability
        alpha=0.85
    )

    # replace legend out of graph
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

    if caps is not None:
        assert isinstance(caps, (list, tuple)), "TypeError: must be list or tuple"
        assert len(caps) == 3, "IndexError"
        assert type(caps[0]) == type(caps[1]) == type(caps[1]) == str, "TypeError"
        plt.title(caps[0])
        plt.xlabel(caps[1])
        plt.ylabel(caps[2])

    plt.ylim(bottom=0)  # min of vertical axis in 0
    return fig

def get_new_df(df, pattern=None, overall_col=True):
    df = df.copy()
    df.set_index("year", inplace=True)

    if pattern is None:
        return df
    if pattern == "":  # nominal salary
        new_df = df.iloc[:, :8]  # we need first eight cols
    else:
        new_df = df.filter(like=pattern)  # filter cols
        new_df.columns = [col[:-len(pattern)] for col in new_df.columns]  # get beatiful name (for caption)

    if not overall_col:
        new_df = new_df.drop("overall", axis=1, inplace=False)

    return new_df


# App content
st.title("Анализ динамики заработных плат с 2000 по 2023 годы")
st.markdown("В ноутбуке больше словесной аналитики :)")

# Nominal salary
st.markdown("")
st.header("Анализ динамики номинальной зарплаты", anchor=None)
st.markdown("Номинальные зарплаты в целом по экономике явно **растут**")
plot_1 = plot_one_linear(
    x = salary_data.year,
    y=salary_data.overall,
    caps = ["По всей экономике", "Год", "Номинальная зарплата"]
)
st.markdown("")
st.pyplot(plot_1)


data = get_new_df(salary_data, "", overall_col=False)
captions = ["Номинальные заработные платы (по сферам)", "Год", "Номинальная зарплата"]
st.markdown("")
st.pyplot(multiple_linear(data, caps=captions))

st.markdown("* Номинальные зарплаты по избранным категориям тоже явственно растут")
st.markdown("* Добыча и финансы выгодно выделяются")
st.markdown('**Общий вывод по блоку**: зарплаты растут, всё выглядит замечательно ')

# Real salary
st.markdown("")
st.header("Анализ динамики заработной платы с учётом инфляции", anchor=None)

data = get_new_df(salary_data, "_inf_adj", overall_col=True)
plot_3 = multiple_linear(
    data,
    caps=["Заработная плата с учётом инфляции (c overall)", "Год", "Зарплата"],
    palette="crest"
)
st.markdown("")
st.pyplot(plot_3)
st.markdown('* В среднем по экономике рост уже не так впечатляет')
st.markdown('* Рост по всему периоду не такой большой, как было на графике номинальной зп')
st.markdown('* По некоторым годам наблюдается снижение')

st.markdown("")
st.markdown("Возьмём самые низкие зарплаты по 2023. Увидим, что зарплаты демонстрируют **небольшой рост**.")
data = get_new_df(salary_data, "_inf_adj", overall_col=False).iloc[:, :5]
captions = ["Заработная плата с учётом инфляции", "Год", "Зарплата"]
st.markdown("")
st.pyplot(multiple_linear(data, caps=captions, palette="viridis"))

st.markdown("**Общий вывод по блоку** с учётом инфляции:")
st.markdown("* зарплаты в общепите и гостиничном бизнесе после 2008 в реальном выражении почти не растут")
st.markdown("* самый скромный рост в сфере образования")
st.markdown("* зарплаты с учётом инфляции растут не сильно")
st.markdown("* зарплаты в финансах растут с учётом инфляции быстрее, чем прочие")

# Salary in USD
st.markdown("")
st.header("Анализ динамики зарплат с учётом курса доллара", anchor=None)
st.markdown("")
plot_5 = plot_one_linear(x = salary_data.year, y=salary_data.overall_in_dollars, caps = ["По всей экономике", "Год", "Зарплата в USD"])
st.pyplot(plot_5)
st.markdown("**В среднем по экономике зарплата в USD**:")
st.markdown("* зп явно растёт по 2008, рост похож визуально на экспоненциальный")
st.markdown("* рост с 2008 по 2023 незначительный")

data = get_new_df(salary_data, "_in_dollars", overall_col=True)
captions = ["Заработная плата в USD", "Год", "Зарплата"]
plot_6 = multiple_linear(data, caps=captions)
st.markdown("")
st.pyplot(plot_6)
st.markdown("Из графика видно, что все заработные платы **повторяют динамику** со средним по экономике, т.к. курс для всех одинаковый")

# Summarization
st.markdown("")
st.header("Обобщающие выводы", anchor=None)
st.markdown("* Номинальные зарплаты растут")
st.markdown("* Зарплаты в реальном выражениии растут демонстрируют меннее окрыляющий рост")
st.markdown("* Заработная плата в долларх более явно показывает последствия значимых событий")
st.markdown("* С 2000 по 2008 был значительный рост заработка граждан")
st.markdown("* С 2008 по 2023 рост скромный")

if __name__ == '__main__':
    pass


