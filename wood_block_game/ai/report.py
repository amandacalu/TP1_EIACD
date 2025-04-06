import os
import csv
from datetime import datetime

def save_report(data):
    # Garante que os relatórios fiquem sempre na pasta correta
    base_path = os.path.join(os.path.dirname(__file__), "..", "relatorios")
    os.makedirs(base_path, exist_ok=True)

    with open(os.path.join(base_path, "relatorio_ia.txt"), "w") as f:
        f.write("RELATÓRIO DA IA\n\n")
        f.write(f"Algoritmo: {data['algoritmo']}\n")
        if "heuristicas" in data:
            f.write(f"Heurísticas: {', '.join(data['heuristicas'])}\n")
        f.write(f"Pontuação: {data['pontuacao']}\n")
        f.write(f"Passos: {data['passos']}\n")
        f.write(f"Tempo: {data.get('tempo_ms', round(data.get('tempo', 0), 2))} ms\n")
        f.write(f"Resultado: {'VITÓRIA' if data['venceu'] else 'DERROTA'}\n")

def save_summary(data):
    base_path = os.path.join(os.path.dirname(__file__), "..", "relatorios")
    os.makedirs(base_path, exist_ok=True)

    path = os.path.join(base_path, f"{data['algoritmo'].lower()}_resumo.csv")

    # Garante que o campo 'modo' está presente
    dificuldade = data.get("dificuldade", "--")
    data["modo"] = dificuldade

    # Adiciona o campo 'data' com data e hora (formato: YYYY-MM-DD HH:MM)
    data["data"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    campos = ["data", "modo", "venceu", "pontuacao", "passos", "tempo_ms"]

    escrever_cabecalho = not os.path.exists(path)
    with open(path, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if escrever_cabecalho:
            writer.writeheader()
        writer.writerow({campo: data.get(campo, "") for campo in campos})
