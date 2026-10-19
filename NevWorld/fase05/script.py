from pathlib import Path

import duckdb
import pandas as pd


BASE_DIR = next(
    (
        parent
        for parent in Path(__file__).resolve().parents
        if (parent / 'data' / 'processed' / 'hunts.csv').is_file()
    ),
    None,
)
if BASE_DIR is None:
    raise FileNotFoundError(
        'No se encontró la raíz del proyecto con data/processed/hunts.csv.'
    )

DATA_DIR = BASE_DIR / 'data' / 'processed'
PARQUET_DIR = DATA_DIR / 'parquet'
HUNTS_CSV_PATH = DATA_DIR / 'hunts.csv'
HUNTS_PARQUET_PATH = PARQUET_DIR / 'hunts.parquet'
REPORTS_DIR = BASE_DIR / 'reports'
REPORT_PATH = REPORTS_DIR / 'hunts_by_prey_sql.csv'

if not HUNTS_CSV_PATH.is_file():
    raise FileNotFoundError(
        f'No existe {HUNTS_CSV_PATH}. Ejecuta primero la actividad 2 '
        'para generar hunts.csv.'
    )

hunts = pd.read_csv(HUNTS_CSV_PATH)
if 'prey_type' not in hunts.columns:
    raise ValueError(f'{HUNTS_CSV_PATH} no contiene la columna prey_type.')

prey_types = hunts['prey_type'].astype('string').str.strip()
missing_prey = prey_types.isna() | prey_types.eq('')
if missing_prey.any():
    raise ValueError(
        f'{int(missing_prey.sum())} cacería(s) no tienen prey_type informado.'
    )

PARQUET_DIR.mkdir(parents=True, exist_ok=True)
hunts.to_parquet(HUNTS_PARQUET_PATH, engine='pyarrow', index=False)

print(f'Tamaño CSV: {HUNTS_CSV_PATH.stat().st_size} bytes')
print(f'Tamaño Parquet: {HUNTS_PARQUET_PATH.stat().st_size} bytes')

run_ids = (
    hunts['run_id'].dropna().astype(str).unique().tolist()
    if 'run_id' in hunts.columns
    else []
)
if run_ids:
    print('Partida:', ', '.join(run_ids))

if hunts.empty:
    print('Aviso: hunts.csv no contiene cacerías completadas.')

parquet_sql_path = str(HUNTS_PARQUET_PATH).replace('\\', '/').replace("'", "''")
hunt_query = f"""
    SELECT
        prey_type,
        COUNT(*) AS hunt_count
    FROM read_parquet('{parquet_sql_path}')
    GROUP BY prey_type
    ORDER BY hunt_count DESC
"""

connection = duckdb.connect()
try:
    hunt_summary = connection.execute(hunt_query).fetchdf()
finally:
    connection.close()

print('\nCACERÍAS POR PRESA CONSULTADAS CON SQL')
print(hunt_summary)

total_hunts = int(hunt_summary['hunt_count'].sum())
if total_hunts != len(hunts):
    raise AssertionError(
        f'La suma de hunt_count ({total_hunts}) no coincide con '
        f'las filas del CSV ({len(hunts)}).'
    )

print(f'\nTotal de cacerías: {total_hunts}')
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
hunt_summary.to_csv(REPORT_PATH, index=False)
print(f'Resumen guardado en {REPORT_PATH}')