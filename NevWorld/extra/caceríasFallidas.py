from pathlib import Path
import pandas as pd

DATASET = Path('data/raw/nevworld_614258720572051651_20261005_182715.jsonl')
OUTPUT_DIR = Path('data/processed')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TICKS_PER_DAY = 12000
HUNT_TIMEOUT = 50          # ticks tras iniciar la caza para considerar que falló
ONLY_HUNTERS = False       # True -> solo aldeanos con al menos un hunt_completed

df = pd.read_json(DATASET, lines=True)


def event_table_failed_hunts(df, timeout=HUNT_TIMEOUT, only_hunters=ONLY_HUNTERS):
    base_columns = ['run_id', 'event_index', 'tick', 'villager_id']
    final_output_columns = base_columns + [
        'simulation_day', 'next_activity', 'ticks_to_next_activity', 'villager_has_hunts'
    ]

    required = ['type', 'run_id', 'event_index', 'tick', 'villager_id', 'activity', 'resource_type']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Error: faltan columnas necesarias en el dataset: {missing}")

    activity = df[df['type'] == 'villager_activity_changed']
    starts = activity[(activity['activity'] == 'working') &
                      (activity['resource_type'] == 'food')].copy()
    hunts = df[df['type'] == 'hunt_completed']

    if starts.empty:
        return pd.DataFrame(columns=final_output_columns)

    # Un inicio de caza tiene éxito si hay un hunt_completed del mismo aldeano
    # en (inicio, inicio + timeout] dentro de la misma run.
    hunt_ticks = hunts.groupby(['run_id', 'villager_id'])['tick'].apply(sorted).to_dict()

    def succeeded(row):
        ticks = hunt_ticks.get((row['run_id'], row['villager_id']), [])
        return any(row['tick'] <= t <= row['tick'] + timeout for t in ticks)

    starts['success'] = starts.apply(succeeded, axis=1)
    failed = starts[~starts['success']].copy()

    # Descartar inicios "censurados": la simulación terminó antes de poder
    # observar la ventana completa de 50 ticks.
    last_tick = df.groupby('run_id')['tick'].transform('max')
    last_tick = last_tick.groupby(df['run_id']).first()
    failed = failed[failed['tick'] + timeout <= failed['run_id'].map(last_tick)]

    # Siguiente cambio de actividad del mismo aldeano (contexto del fallo)
    activity_sorted = activity.sort_values(['run_id', 'villager_id', 'event_index'])
    nxt = activity_sorted.groupby(['run_id', 'villager_id'])[['activity', 'tick']].shift(-1)
    activity_sorted['next_activity'] = nxt['activity']
    activity_sorted['next_tick'] = nxt['tick']
    failed = failed.merge(
        activity_sorted[['run_id', 'event_index', 'next_activity', 'next_tick']],
        on=['run_id', 'event_index'], how='left'
    )
    failed['ticks_to_next_activity'] = failed['next_tick'] - failed['tick']

    hunter_ids = set(hunts['villager_id'].dropna())
    failed['villager_has_hunts'] = failed['villager_id'].isin(hunter_ids)
    if only_hunters:
        failed = failed[failed['villager_has_hunts']]

    failed['simulation_day'] = failed['tick'] // TICKS_PER_DAY
    failed['villager_id'] = failed['villager_id'].astype('int64')
    return failed[final_output_columns].reset_index(drop=True)


failed_hunts_df = event_table_failed_hunts(df)

# ---------- Validaciones ----------
assert not failed_hunts_df.duplicated(subset=['run_id', 'event_index']).any(), \
    "Existen parejas (run_id, event_index) duplicadas"
base_required = ['run_id', 'event_index', 'tick', 'villager_id', 'simulation_day']
if len(failed_hunts_df) > 0:
    assert failed_hunts_df[base_required].notna().all().all(), "Hay valores ausentes en campos obligatorios"
    assert (failed_hunts_df['simulation_day'] == failed_hunts_df['tick'] // TICKS_PER_DAY).all(), \
        "Cálculo incorrecto de simulation_day"

# Cuadre: inicios = exitosos + fallidos + censurados (descartados al final)
activity = df[df['type'] == 'villager_activity_changed']
n_starts = ((activity['activity'] == 'working') & (activity['resource_type'] == 'food')).sum()
n_hunts = (df['type'] == 'hunt_completed').sum()
print(f"Inicios working/food: {n_starts} | hunt_completed: {n_hunts} | fallidos: {len(failed_hunts_df)}")

output_path = OUTPUT_DIR / 'failed_hunts.csv'
failed_hunts_df.to_csv(output_path, index=False)
print(output_path, '->', len(failed_hunts_df), 'filas')