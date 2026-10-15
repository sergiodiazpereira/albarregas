from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = next(
    (
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / 'data' / 'processed').is_dir()
    ),
    None,
)
if BASE_DIR is None:
    raise FileNotFoundError(
        'No se encontró la carpeta raíz del proyecto con data/processed.'
    )

DATA_DIR = BASE_DIR / 'data' / 'processed'
PHASE_DIR = Path(__file__).resolve().parent
CHARTS_DIR = PHASE_DIR / 'reports' / 'charts'
HUNTS_PATH = DATA_DIR / 'hunts.csv'
CHART_PATH = CHARTS_DIR / '05_hunts_by_prey.png'

if not HUNTS_PATH.is_file():
    raise FileNotFoundError(
        f'No existe {HUNTS_PATH}. Ejecuta primero la actividad 2 '
        'para generar hunts.csv.'
    )

hunts = pd.read_csv(HUNTS_PATH)

if 'prey_type' not in hunts.columns:
    raise ValueError(f'{HUNTS_PATH} no contiene la columna prey_type.')

if hunts.empty:
    print('No hay cacerías completadas registradas. No se generó gráfico.')
    if CHART_PATH.is_file():
        CHART_PATH.unlink()
        print('Se eliminó el gráfico anterior para no confundirlo con esta partida.')
else:
    prey_types = hunts['prey_type'].astype('string').str.strip()
    missing_prey = prey_types.isna() | prey_types.eq('')
    if missing_prey.any():
        raise ValueError(
            f'{int(missing_prey.sum())} cacería(s) no tienen prey_type informado.'
        )

    counts = prey_types.value_counts()
    print(f'Cacerías completadas registradas: {int(counts.sum())}')
    print('Cacerías por presa:')
    print(counts.to_string())

    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 4))
    counts.plot.bar(color='steelblue')
    plt.title('Cacerías completadas registradas por tipo de presa')
    plt.xlabel('Tipo de presa')
    plt.ylabel('Número de cacerías completadas')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(CHART_PATH)
    plt.close()