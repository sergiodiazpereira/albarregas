from pathlib import Path
import pandas as pd

DATASET = Path('data/raw/nevworld_614258720572051651_20261005_182715.jsonl')
OUTPUT_DIR = Path('data/processed')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_json(DATASET, lines=True)

def event_table_hunts(df, event_type='hunt_completed', custom_columns=None):
    if custom_columns is None:
        custom_columns = ['villager_id', 'prey_type']
    
    base_columns = ['run_id', 'event_index', 'tick']
    mandatory_fields = base_columns + custom_columns
    final_output_columns = mandatory_fields + ['simulation_day']

    if 'type' in df.columns:
        filtered_df = df[df['type'] == event_type].copy()
    else:
        filtered_df = pd.DataFrame()

    if not filtered_df.empty:
        missing_fields = [col for col in mandatory_fields if col not in filtered_df.columns]
        if missing_fields:
            raise ValueError(f" Error: Se encontraron cacerías pero faltan los campos obligatorios: {missing_fields}")

    table = filtered_df.reindex(columns=mandatory_fields).copy()

    if not table.empty and 'tick' in table.columns:
        table['simulation_day'] = table['tick'] // 12000
    else:
        table['simulation_day'] = pd.Series(dtype='int64')

    return table[final_output_columns]

hunts_df = event_table_hunts(df)

EVENT_TYPE = 'hunt_completed'
REQUIRED_FIELDS = ['run_id', 'event_index', 'tick', 'villager_id', 'prey_type', 'simulation_day']

expected_count = (df['type'] == EVENT_TYPE).sum() if 'type' in df.columns else 0
assert len(hunts_df) == expected_count, f"Esperadas {expected_count} filas, se obtuvieron {len(hunts_df)}"

assert not hunts_df.duplicated(subset=['run_id', 'event_index']).any(), "Existen parejas (run_id, event_index) duplicadas"

if len(hunts_df) > 0:
    assert hunts_df[REQUIRED_FIELDS].notna().all().all(), "Hay valores ausentes en campos obligatorios"
    assert (hunts_df['simulation_day'] == hunts_df['tick'] // 12000).all(), "Cálculo incorrecto de simulation_day"

output_path = OUTPUT_DIR / 'hunts.csv'
hunts_df.to_csv(output_path, index=False)

print(output_path, '->', len(hunts_df), 'filas')