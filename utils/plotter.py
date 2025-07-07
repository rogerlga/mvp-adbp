import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from typing import Callable, Literal


def _with_gaps(
    data: pd.DataFrame,
    time_column: str,
    value_column: str,
    gap_threshold: pd.Timedelta,
) -> pd.DataFrame:
    """
    Retorna um dataset temporário contendo valores nulos em intervalos de tempo maiores que `gap_threshold`,
    de forma que o plotly desconecte linhas que seriam traçadas nesses intervalos.
    """

    time_deltas = data[time_column].diff()
    gap_rows = np.flatnonzero(time_deltas.values > gap_threshold)

    # Retorna o próprio dataframe se não há gaps
    if len(gap_rows) == 0:
        return data
    
    # Insere de forma ordenada as linhas que representam os gaps
    row_list = []
    for i, j in zip(np.insert(gap_rows, 0, 0), gap_rows):
        gap = data.iloc[[j]].drop(columns=value_column)
        gap[time_column] -= pd.to_timedelta("1ns")
        row_list += [data.iloc[i:j], gap]
    row_list.append(data.iloc[j:])
    return pd.concat(row_list, axis=0, ignore_index=True)

    # row_condition = time_deltas.values > gap_threshold
    # gaps = data.loc[row_condition].drop(columns=value_column)
    # gaps[time_column] -= pd.to_timedelta("1ns")
    # return pd.merge(data, gaps, how="outer", sort=True)


def _sync_axes(
    fig: go.Figure,
    sync_xaxes: Literal["all", "by_row", "by_col"] | None,
    sync_yaxes: Literal["all", "by_row", "by_col"] | None,
) -> None:
    """
    Configura a sincronia entre eixos, conforme definido na documentação da função `line`.
    """
    
    # Obtém índices das linhas e colunas
    n = fig._get_subplot_rows_columns()
    ncols = len(n[1])
    
    # Ajusta os eixos x
    if sync_xaxes is None:
        fig.update_xaxes(matches=None)
    elif sync_xaxes == "by_row":
        for i in n[0]:
            fig.update_xaxes(matches=f'x{ncols*(i - 1) + 1}', row=i)
    elif sync_xaxes == "by_col":
        for j in n[1]:
            fig.update_xaxes(matches=f'x{j}', col=j)
    
    # Ajusta os eixos y
    if sync_yaxes is None:
        fig.update_yaxes(matches=None)
    elif sync_yaxes == "by_row":
        for i in n[0]:
            fig.update_yaxes(matches=f'y{ncols*(i - 1) + 1}', row=i)
    elif sync_yaxes == "by_col":
        for j in n[1]:
            fig.update_yaxes(matches=f'y{j}', col=j)


def prepare_timeseries_data(
    data: pd.DataFrame,
    selectors: Callable[[pd.DataFrame], dict],
) -> go.Figure:
    """
    Prepara dataframe para o plot, incluindo filtragem e criação dos atributos auxiliares `time` e `class`.
    """

    # Filtra os dados com base no seletor
    plot_data = pd.concat([data.loc[v] for v in selectors(data).values()], axis=0, ignore_index=True)

    # Cria atributos auxiliares
    plot_data["time"] = pd.to_timedelta(plot_data["offset_seconds"], "s")
    for k, v in selectors(plot_data).items():
        plot_data.loc[v, "class"] = k
    
    return plot_data


def timeseries(
    data: pd.DataFrame,
    time_column: str,
    value_column: str,
    gap_threshold: pd.Timedelta,
    sync_xaxes: Literal["all", "by_row", "by_col"] | None = "all",
    sync_yaxes: Literal["all", "by_row", "by_col"] | None = "all",
    **kwargs,
) -> go.Figure:
    """
    Constrói um gráfico de linhas, desconectando os pontos em intervalos de tempo maiores que `gap_threshold`.

    A sincronização entre eixos em gráficos facetados pode ser contralado através dos argumentos `sync_xaxes`
    e `sync_yaxes`, onde:
    - `"all"`: todos os subplots possuem eixos sincronizados;
    - `"by_row"`: eixos de subplots da mesma linha são sincronizados;
    - `"by_col"`: eixos de subplots da mesma coluna são sincronizados;
    - `None`: cada subplot possui eixo independente.
    """

    # Trata os gaps e constrói o gráfico
    data_with_gaps = _with_gaps(data, time_column, value_column, gap_threshold)
    fig = px.line(data_with_gaps, x=time_column, y=value_column, **kwargs)

    # Ajusta a sincronização entre eixos dos subplots
    _sync_axes(fig, sync_xaxes, sync_yaxes)

    # Configura os intervalos e rótulos do eixo x
    xmin = pd.to_timedelta(fig.data[0].x.min())
    xmax = pd.to_timedelta(fig.data[0].x.max())
    ticks = pd.timedelta_range(xmin, xmax, freq=f'{max(int((xmax - xmin) / pd.to_timedelta("20d")), 1)}d')
    fig.update_xaxes(tickvals=ticks, ticktext=ticks.astype(str))

    # Personaliza a hover box
    for j in fig._get_subplot_rows_columns()[1]:
        fig.update_traces(hovertemplate=None, hoverinfo="name+text+y", hovertext=pd.to_timedelta(fig.data[j-1].x).astype(str), col=j)

    return fig
