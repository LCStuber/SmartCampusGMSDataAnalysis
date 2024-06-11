import streamlit as st
import hidrometer
import watertank_level
import artesian_well

# Mapeamento entre nomes amigáveis e funções dos scripts
script_mapping = {
    "Hidrômetro": hidrometer.main,
    "Nível do Tanque de Água": watertank_level.main,
    "Poço Artesiano": artesian_well.main
}

# Streamlit UI
st.title("Análise de Dados dos Sensores")

# Seleção do script com nomes amigáveis
script_selected = st.selectbox("Selecione um sensor para visualizar o panorama", list(script_mapping.keys()))

if st.button(f"Visualizar {script_selected}"):
    script_func = script_mapping[script_selected]
    st.write(f"Visualizando {script_selected}...")
    try:
        # Redireciona a saída padrão para capturar o output
        from io import StringIO
        import sys

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        script_func()

        sys.stdout = old_stdout
        st.write(mystdout.getvalue())
    except Exception as e:
        st.write("Errors:\n", str(e))
