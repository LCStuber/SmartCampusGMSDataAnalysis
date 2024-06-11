
def main():

    import pandas as pd
    import seaborn as sns
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from statsmodels.formula.api import ols
    import streamlit as st

    data_fields = [
        "applicationID", "applicationName", "data_boardVoltage", "data_distance", 
        "devEUI", "fCnt", "fPort", "host", "nodeName", "rxInfo_altitude_0", 
        "rxInfo_altitude_1", "rxInfo_latitude_0", "rxInfo_latitude_1", 
        "rxInfo_loRaSNR_0", "rxInfo_loRaSNR_1", "rxInfo_longitude_0", 
        "rxInfo_longitude_1", "rxInfo_mac_0", "rxInfo_mac_1", "rxInfo_name_0", 
        "rxInfo_name_1", "rxInfo_rssi_0", "rxInfo_rssi_1", "time", "txInfo_adr", 
        "txInfo_codeRate", "txInfo_dataRate_bandwidth", "txInfo_dataRate_modulation", 
        "txInfo_dataRate_spreadFactor", "txInfo_frequency"
    ]

    df_water_tank = pd.read_csv(r'data/WaterTankLevel.csv', header=3, usecols=data_fields)
    df_water_tank["time"] = pd.to_datetime(df_water_tank["time"])
    df_water_tank["data_distance"] /= 1000

    dfs_water_tank_per_node = {app_id: df_node for app_id, df_node in df_water_tank.groupby("devEUI")}
    ids = list(dfs_water_tank_per_node.keys())

    RADIUS = 5
    for id in ids:
        dfs_water_tank_per_node[id]["Volume"] = RADIUS**2 * np.pi * (dfs_water_tank_per_node[id]["data_distance"])
        dfs_water_tank_per_node[id]["time_diff"] = dfs_water_tank_per_node[id]["time"].diff().dt.seconds
        dfs_water_tank_per_node[id]["Vazao"] = dfs_water_tank_per_node[id]["Volume"].diff() / dfs_water_tank_per_node[id]["time_diff"]

    st.title("Estatistica sobre o volume no tanque de água")
    data_volume = []
    for id in ids:
        max_volume = dfs_water_tank_per_node[id]["Volume"].max()
        min_volume = dfs_water_tank_per_node[id]["Volume"].min()
        mean_volume = dfs_water_tank_per_node[id]["Volume"].mean()
        std_volume = dfs_water_tank_per_node[id]["Volume"].std()

        data_volume.append([id, max_volume, min_volume, mean_volume, std_volume])

    df_estatisticas = pd.DataFrame(data_volume, columns=["Device ID", "Max Volume", "Min Volume", "Mean Volume", "Std Volume"])
    st.table(df_estatisticas)

    st.title("Estatistica sobre a vazão no tanque de água")
    data_vazao = []
    for id in ids:
        max_vazao = dfs_water_tank_per_node[id]["Vazao"].max()
        min_vazao = dfs_water_tank_per_node[id]["Vazao"].min()
        mean_vazao = dfs_water_tank_per_node[id]["Vazao"].mean()
        std_vazao = dfs_water_tank_per_node[id]["Vazao"].std()

        data_vazao.append([id, max_vazao, min_vazao, mean_vazao, std_vazao])

    df_estatisticas_vazao = pd.DataFrame(data_vazao, columns=["Device ID", "Max Vazao", "Min Vazao", "Mean Vazao", "Std Vazao"])
    st.table(df_estatisticas_vazao)

    colors = sns.color_palette("husl", len(ids))

    ncols = 3
    nrows = (len(ids) + ncols - 1) // ncols

    st.title("Análise do volume no tanque de água")
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(20, nrows*5))
    axes = axes.flatten()
    for ax, id in zip(axes,ids):
        df_water_tank_id = dfs_water_tank_per_node[id]
        sns.lineplot(ax=ax, x="time", y="Volume", data=df_water_tank_id, label=id, color=colors.pop(0))
        ax.set_xlabel("Tempo (h)")
        ax.set_ylabel("Volume (L)")
        ax.set_title("Volume do tanque de água ao longo do tempo") 
        ax.legend(loc='upper left')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.grid(True)
    st.pyplot(plt.gcf())

    colors = sns.color_palette("husl", len(ids))

    ncols = 3
    nrows = (len(ids) + ncols - 1) // ncols

    st.title("Análise da vazão no tanque de água")
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(20, nrows*5))
    axes = axes.flatten()
    for ax, id in zip(axes,ids):
        df_water_tank_id = dfs_water_tank_per_node[id]
        sns.lineplot(ax=ax, x="time", y="Vazao", data=df_water_tank_id, label=id, color=colors.pop(0))
        ax.set_xlabel("Tempo (h)")
        ax.set_ylabel("Vazao (L/s)")
        ax.set_title("Vazao do tanque de água ao longo do tempo") 
        ax.legend(loc='upper left')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.grid(True)
    st.pyplot(plt.gcf())

    colors = sns.color_palette("husl", len(ids))

    st.title("Correlação entre Voltagem da placa e Volume para cada tanque de água")
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(20, nrows*5))
    axes = axes.flatten()
    for ax, id in zip(axes,ids):
        df_water_tank_id = dfs_water_tank_per_node[id]
        sns.regplot(ax=ax, x="data_boardVoltage", y="Volume", data=df_water_tank_id, label=id, color=colors.pop(0))
        ax.set_xlabel("Voltagem da placa (V)")
        ax.set_ylabel("Volume (L)")
        ax.set_title("Volume do tanque de água x Voltagem da placa") 
        ax.legend(loc='upper left')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.grid(True)
    st.pyplot(plt.gcf())

    lista_correlacoes = []
    for id in ids:
        corr_variable = dfs_water_tank_per_node[id][["data_boardVoltage", "Volume"]].corr()
        lista_correlacoes.append(corr_variable.iloc[0,1])
    
    st.write("Valor de Correlação entre Voltagem da placa e Volume para cada tanque de água")
    st.table(pd.DataFrame(lista_correlacoes, columns=["Correlação"], index=ids))



if __name__ == "__main__":
    main()