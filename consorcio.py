# Simulador de Comparação: Consórcio x Financiamento

# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Função para formatar valores em estilo brasileiro
def formatar_brasileiro(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

# Entradas do usuário
valor_bem = float(input("Digite o valor do bem (R$): "))
prazo_meses = int(input("Digite o prazo (em meses): "))
taxa_juros_financiamento_ano = float(input("Digite a taxa de juros do financiamento (% ao ano): "))
taxa_adm_consorcio_total = float(input("Digite a taxa de administração do consórcio (% sobre o valor do bem): "))
valor_entrada = float(input("Digite o valor da entrada no financiamento (R$) [coloque 0 se não houver]: "))
reajuste_anual_consorcio = float(input("Digite o percentual de reajuste anual do consórcio (%): "))

# Conversões
valor_financiado = valor_bem - valor_entrada
taxa_juros_mensal = (1 + taxa_juros_financiamento_ano / 100) ** (1/12) - 1

# Financiamento: cálculo da parcela pela Tabela Price
parcela_price = valor_financiado * (taxa_juros_mensal * (1 + taxa_juros_mensal)**prazo_meses) / ((1 + taxa_juros_mensal)**prazo_meses - 1)
custo_total_price = parcela_price * prazo_meses + valor_entrada

# Financiamento: cálculo da parcela pela Tabela SAC
amortizacao_sac = valor_financiado / prazo_meses
parcelas_sac = []
for mes in range(1, prazo_meses + 1):
    saldo_devedor = valor_financiado - amortizacao_sac * (mes - 1)
    parcela_mes = amortizacao_sac + saldo_devedor * taxa_juros_mensal
    parcelas_sac.append(parcela_mes)
custo_total_sac = sum(parcelas_sac) + valor_entrada

# Consórcio: parcela sem contemplação, com taxa de administração diluída
valor_total_consorcio = valor_bem * (1 + taxa_adm_consorcio_total / 100)
parcela_inicial_consorcio = valor_total_consorcio / prazo_meses

# Aplicar reajuste anual no consórcio
parcelas_consorcio = []
parcela_atual = parcela_inicial_consorcio
for mes in range(1, prazo_meses + 1):
    parcelas_consorcio.append(parcela_atual)
    if mes % 12 == 0:
        parcela_atual *= (1 + reajuste_anual_consorcio / 100)

custo_total_consorcio = sum(parcelas_consorcio)

# Resultado
print("\n------ Resultado ------")
print(f"Custo total do financiamento (Tabela Price): {formatar_brasileiro(custo_total_price)}")
print(f"Custo total do financiamento (Tabela SAC): {formatar_brasileiro(custo_total_sac)}")
print(f"Custo total do consórcio: {formatar_brasileiro(custo_total_consorcio)}")

# Comparativo de custos
print("\n------ Comparativo de Menor Custo ------")
menor_custo = min(custo_total_price, custo_total_sac, custo_total_consorcio)

if menor_custo == custo_total_price:
    diferenca = min(custo_total_sac, custo_total_consorcio) - custo_total_price
    print(f"O financiamento (Tabela Price) é {formatar_brasileiro(diferenca)} mais barato que a segunda melhor opção.")
elif menor_custo == custo_total_sac:
    diferenca = min(custo_total_price, custo_total_consorcio) - custo_total_sac
    print(f"O financiamento (Tabela SAC) é {formatar_brasileiro(diferenca)} mais barato que a segunda melhor opção.")
else:
    diferenca = min(custo_total_price, custo_total_sac) - custo_total_consorcio
    print(f"O consórcio é {formatar_brasileiro(diferenca)} mais barato que a segunda melhor opção.")

# Aproximação das parcelas
parcelas_price_mensal = [parcela_price] * prazo_meses
meses = np.arange(1, prazo_meses + 1)

print("\n------ Aproximação das Parcelas ------")

# Price vs Consórcio
diferencas_price = np.abs(np.array(parcelas_consorcio) - np.array(parcelas_price_mensal))
indice_min_diferenca_price = np.argmin(diferencas_price)
ano_price = indice_min_diferenca_price // 12 + 1
mes_price = indice_min_diferenca_price % 12 + 1
valor_price = parcelas_price_mensal[indice_min_diferenca_price]
valor_consorcio_price = parcelas_consorcio[indice_min_diferenca_price]
print(f"- Price x Consórcio: Ano {ano_price}, Mês {mes_price} | Price: {formatar_brasileiro(valor_price)}, Consórcio: {formatar_brasileiro(valor_consorcio_price)}")

# SAC vs Consórcio
diferencas_sac = np.abs(np.array(parcelas_consorcio) - np.array(parcelas_sac))
indice_min_diferenca_sac = np.argmin(diferencas_sac)
ano_sac = indice_min_diferenca_sac // 12 + 1
mes_sac = indice_min_diferenca_sac % 12 + 1
valor_sac = parcelas_sac[indice_min_diferenca_sac]
valor_consorcio_sac = parcelas_consorcio[indice_min_diferenca_sac]
print(f"- SAC x Consórcio: Ano {ano_sac}, Mês {mes_sac} | SAC: {formatar_brasileiro(valor_sac)}, Consórcio: {formatar_brasileiro(valor_consorcio_sac)}")

# Valores pagos até o momento de aproximação
valor_pago_price = sum(parcelas_price_mensal[:indice_min_diferenca_price + 1]) + valor_entrada
valor_pago_sac = sum(parcelas_sac[:indice_min_diferenca_sac + 1]) + valor_entrada
valor_pago_consorcio_price = sum(parcelas_consorcio[:indice_min_diferenca_price + 1])
valor_pago_consorcio_sac = sum(parcelas_consorcio[:indice_min_diferenca_sac + 1])

print("\n------ Valores Pagos até o Momento de Aproximação ------")
print(f"- Até Ano {ano_price}, Mês {mes_price}:")
print(f"  Financiamento Price: {formatar_brasileiro(valor_pago_price)}")
print(f"  Consórcio (vs Price): {formatar_brasileiro(valor_pago_consorcio_price)}")
print(f"\n- Até Ano {ano_sac}, Mês {mes_sac}:")
print(f"  Financiamento SAC: {formatar_brasileiro(valor_pago_sac)}")
print(f"  Consórcio (vs SAC): {formatar_brasileiro(valor_pago_consorcio_sac)}")

# Análise de aproximação dos valores pagos acumulados
valores_acumulados_price = np.cumsum(parcelas_price_mensal) + valor_entrada
valores_acumulados_sac = np.cumsum(parcelas_sac) + valor_entrada
valores_acumulados_consorcio = np.cumsum(parcelas_consorcio)

# Price vs Consórcio
diferenca_acumulada_price = np.abs(valores_acumulados_price - valores_acumulados_consorcio)
indice_min_diferenca_acumulada_price = np.argmin(diferenca_acumulada_price)
ano_acumulado_price = indice_min_diferenca_acumulada_price // 12 + 1
mes_acumulado_price = indice_min_diferenca_acumulada_price % 12 + 1

# SAC vs Consórcio
diferenca_acumulada_sac = np.abs(valores_acumulados_sac - valores_acumulados_consorcio)
indice_min_diferenca_acumulada_sac = np.argmin(diferenca_acumulada_sac)
ano_acumulado_sac = indice_min_diferenca_acumulada_sac // 12 + 1
mes_acumulado_sac = indice_min_diferenca_acumulada_sac % 12 + 1

print("\n------ Momento de Aproximação dos Valores Pagos Totais ------")
print(f"- Price x Consórcio: Ano {ano_acumulado_price}, Mês {mes_acumulado_price}")
print(f"  Valor pago Financiamento Price: {formatar_brasileiro(valores_acumulados_price[indice_min_diferenca_acumulada_price])}")
print(f"  Valor pago Consórcio: {formatar_brasileiro(valores_acumulados_consorcio[indice_min_diferenca_acumulada_price])}")

print(f"\n- SAC x Consórcio: Ano {ano_acumulado_sac}, Mês {mes_acumulado_sac}")
print(f"  Valor pago Financiamento SAC: {formatar_brasileiro(valores_acumulados_sac[indice_min_diferenca_acumulada_sac])}")
print(f"  Valor pago Consórcio: {formatar_brasileiro(valores_acumulados_consorcio[indice_min_diferenca_acumulada_sac])}")


# --- INÍCIO: Tabela Comparativa - Média Anual das Parcelas até o Ano 5 ---
print("\n------ Quadro Comparativo: Média Anual até o Ano 5 ------")
anos = [1, 2, 3, 4, 5]
media_parcelas_price = [parcela_price] * 5
media_parcelas_sac = []
media_parcelas_consorcio = []

for ano in anos:
    inicio = (ano - 1) * 12
    fim = ano * 12
    media_ano_sac = np.mean(parcelas_sac[inicio:fim])
    media_ano_consorcio = np.mean(parcelas_consorcio[inicio:fim])
    media_parcelas_sac.append(media_ano_sac)
    media_parcelas_consorcio.append(media_ano_consorcio)

dados_resumo = {
    'Ano': anos,
    'Média Parcela Financiamento (Price) (R$)': [formatar_brasileiro(valor) for valor in media_parcelas_price],
    'Média Parcela Financiamento (SAC) (R$)': [formatar_brasileiro(valor) for valor in media_parcelas_sac],
    'Média Parcela Consórcio (R$)': [formatar_brasileiro(valor) for valor in media_parcelas_consorcio]
}

df_resumo = pd.DataFrame(dados_resumo)
print(df_resumo.to_string(index=False))
# --- FIM: Tabela Comparativa ---

# Gráfico comparativo de custo total
plt.figure(figsize=(10,6))
plt.bar(['Financiamento Price', 'Financiamento SAC', 'Consórcio'], [custo_total_price, custo_total_sac, custo_total_consorcio], color=['blue', 'orange', 'green'])
plt.title('Comparativo de Custo Total')
plt.ylabel('Valor (R$)')
plt.grid(axis='y')
plt.show()

# Gráfico de evolução anual das parcelas
anos_plot = meses / 12

plt.figure(figsize=(12,6))
plt.plot(anos_plot, parcelas_price_mensal, label='Financiamento Price')
plt.plot(anos_plot, parcelas_sac, label='Financiamento SAC')
plt.plot(anos_plot, parcelas_consorcio, label='Consórcio')
plt.title('Evolução Anual das Parcelas')
plt.xlabel('Ano')
plt.ylabel('Valor da Parcela (R$)')
plt.legend()
plt.grid(True)
plt.show()
