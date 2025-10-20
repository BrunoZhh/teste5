import streamlit as st
import pandas as pd

st.title('Empresa de Manufaturas')
dados = st.file_uploader('Carregar Arquivo da Empresa', type=['csv']) #arquivo
if dados is not None:
    df = pd.read_csv(dados)
else:
    df = pd.DataFrame(columns=[
        'Data', 'Turno', 'Máquina',
        'Peças Produzidas', 'Peças Defeituosas'])
#editar
st.subheader('Produção')
df = st.data_editor(df, num_rows='dynamic')
#formuulario
st.sidebar.header('Adicionar novo registro')
data = st.sidebar.date_input('Data')
turno = st.sidebar.selectbox('Turno', ['Manhã', 'Tarde', 'Noite'])
maquina = st.sidebar.selectbox('Máquina', ['Manual', 'Semiautomática', 'Automática'])
pecas_produzidas = st.sidebar.number_input('Peças Produzidas', min_value=0)
pecas_defeituosas = st.sidebar.number_input('Peças Defeituosas', min_value=0)

if st.sidebar.button('Adicionar'):
    novo = pd.DataFrame({
        'Data': [data],
        'Turno': [turno],
        'Máquina': [maquina],
        'Peças Produzidas': [pecas_produzidas],
        'Peças Defeituosas': [pecas_defeituosas]})
    df = pd.concat([df, novo], ignore_index=True)
    st.success('Registro adicionado')
if not df.empty:
    df['Data'] = pd.to_datetime(df['Data'])
    df['Total'] = df['Peças Produzidas']-df['Peças Defeituosas']#calculo1
    df['Eficiência (%)'] = (df['Total']/df['Peças Produzidas']*100).round(1)#calcuulo2
    df['Taxa de Defeitos (%)'] = (df['Peças Defeituosas']/df['Peças Produzidas']*100).round(1)#calculo3
#escolhas
    escolha = st.radio(
        'Qual?',
        ('Cálculos e Alertas', 'Gráficos'))
    if escolha == 'Cálculos e Alertas':
        st.subheader('Tabela')
        st.dataframe(df)
        #produçao
        producao = df[df['Peças Produzidas'] < 80]
        if not producao.empty:
            st.warning('A produção caiu abaixo de 80 peças nestes dias:')
            st.dataframe(producao[['Data','Turno','Máquina','Peças Produzidas']])
            #eficiencia
            eficiencia = df.groupby('Data').sum().reset_index()
            eficiencia['Eficiência por dia (%)'] = (eficiencia['Total'] / eficiencia['Peças Produzidas'] * 100).round(1)
            st.subheader('Eficiência por dia (%)')
            erro = eficiencia[eficiencia['Eficiência por dia (%)'] < 90]
        if not erro.empty:
         st.warning('Alguns dias tiveram eficiência por dia menor que 90%')
         st.dataframe(eficiencia[['Data','Peças Produzidas','Total','Eficiência por dia (%)']])
#graficos
    if escolha == 'Gráficos':
        st.subheader('Produção diária por máquina')
        graf1 = df.groupby(['Data', 'Máquina'])['Peças Produzidas'].sum().unstack(fill_value=0)
        st.bar_chart(graf1)

        st.subheader('Eficiência média por máquina')
        graf2 = df.groupby('Máquina')['Eficiência (%)'].mean()
        st.bar_chart(graf2)
        
        st.subheader('Taxa média de defeitos por dia')
        graf3 = df.groupby('Data')['Taxa de Defeitos (%)'].mean()
        st.line_chart(graf3)
#salvar
    if st.button('Salvar'):
        df.to_csv('C:\Senai\Empresa.csv', index=False)
        st.success('Dados Salvos')