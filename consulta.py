import requests
import csv
import time

API_KEY = "sk_4431.wxSoMIxB7lHceyoz50rhZbAmIMZcg8fM"
URL = "https://api.decolecta.com/v1/reniec/dni"

INPUT_FILE = "dnis.txt"               # archivo con los DNIs
OUTPUT_FILE = "resultados_dnis.csv"   # archivo de salida

def cargar_dnis():
    """Lee los DNIs desde un archivo .txt, uno por línea."""
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip().isdigit()]

def consultar_dni(numero):
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {"numero": numero}

    try:
        response = requests.get(URL, headers=headers, params=params)
        data = response.json()

        if "error" in data:
            print(f"❌ Error con DNI {numero}: {data['error']}")
            return None

        return data

    except Exception as e:
        print(f"⚠️ Error inesperado con DNI {numero}: {e}")
        return None


def main():
    dnis = cargar_dnis()

    print(f"📁 DNIs cargados desde {INPUT_FILE}: {len(dnis)} encontrados.\n")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["DNI", "Nombres", "Apellido Paterno", "Apellido Materno"])

        for dni in dnis:
            print(f"🔍 Consultando DNI: {dni}")

            data = consultar_dni(dni)

            if data:
                writer.writerow([
                    data.get("document_number", ""),
                    data.get("first_name", ""),
                    data.get("first_last_name", ""),
                    data.get("second_last_name", "")
                ])

            time.sleep(0.4)  # evita saturación del API

    print(f"\n✅ Archivo CSV generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
