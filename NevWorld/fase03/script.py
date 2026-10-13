from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[4]
DATA_DIR = BASE_DIR / 'data' / 'processed'
REPORTS_DIR = BASE_DIR / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)

hunts = pd.read_csv(DATA_DIR / 'hunts.csv')
resources = pd.read_csv(DATA_DIR / 'resources.csv')

required_columns = {
    'hunts.csv': ['run_id', 'event_index', 'prey_type', 'simulation_day'],
    'resources.csv': ['run_id', 'event_index', 'resource_type', 'amount_delta'],
}
tables = {
    'hunts.csv': hunts,
    'resources.csv': resources,
}

for table_name, table in tables.items():
    missing_columns = [
        column for column in required_columns[table_name]
        if column not in table.columns
    ]
    if missing_columns:
        raise ValueError(
            f'{table_name}: faltan las columnas requeridas: '
            f'{", ".join(missing_columns)}'
        )

    missing_values = table[required_columns[table_name]].isna().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        details = ', '.join(
            f'{column}: {count}'
            for column, count in missing_values.items()
        )
        raise ValueError(
            f'{table_name}: hay valores ausentes en campos usados: {details}'
        )

    duplicate_keys = table.duplicated(
        subset=['run_id', 'event_index'],
        keep=False,
    )
    if duplicate_keys.any():
        duplicate_count = int(duplicate_keys.sum())
        raise ValueError(
            f'{table_name}: hay {duplicate_count} filas con la clave '
            '(run_id, event_index) repetida.'
        )

    run_ids = table['run_id'].unique()
    if len(run_ids) > 1:
        raise ValueError(
            f'{table_name}: se esperaba como máximo una partida, pero hay '
            f'{len(run_ids)} valores distintos de run_id.'
        )

if (
    not hunts.empty
    and not resources.empty
    and hunts['run_id'].iloc[0] != resources['run_id'].iloc[0]
):
    raise ValueError(
        'hunts.csv y resources.csv pertenecen a partidas distintas '
        '(run_id no coincide).'
    )

hunt_count = len(hunts)
prey_counts = hunts['prey_type'].value_counts()
prey_proportions = hunts['prey_type'].value_counts(normalize=True)
day_counts = hunts['simulation_day'].value_counts().sort_index()

print('\nCACERIAS COMPLETADAS')
print('Total registradas:', hunt_count)

if hunts.empty:
    print('No hay cacerias completadas registradas.')

print('\nCACERIAS DE CADA PRESA')
print(prey_counts)

print('\nPORCENTAJE DE CADA PRESA')
print((prey_proportions * 100).round(1))

print('\nCACERIAS REGISTRADAS EN CADA DIA OBSERVADO')
print(day_counts)

assert prey_counts.sum() == hunt_count
assert day_counts.sum() == hunt_count
print('Comprobaciones de recuentos: correctas.')

if hunt_count > 0:
    assert abs(prey_proportions.sum() * 100 - 100) < 0.000001
    print('Comprobacion de porcentajes: correcta.')

food_events = resources[resources['resource_type'] == 'food']
food_gains = food_events[food_events['amount_delta'] > 0]['amount_delta'].sum()
food_reductions = food_events[food_events['amount_delta'] < 0]['amount_delta'].abs().sum()
food_net_change = food_events['amount_delta'].sum()

print('\nCAMBIOS DE COMIDA')
if food_events.empty:
    print('No hay eventos de cambio de comida registrados.')
print('Aumentos registrados:', food_gains)
print('Disminuciones registradas:', food_reductions)
print('Balance neto:', food_net_change)

assert abs(food_gains - food_reductions - food_net_change) < 0.000001
print('Comprobacion del balance de comida: correcta.')

summary = pd.DataFrame([
    {'metric': 'hunt_events', 'value': hunt_count},
    {'metric': 'food_change_events', 'value': len(food_events)},
    {'metric': 'food_gains', 'value': food_gains},
    {'metric': 'food_reductions', 'value': food_reductions},
    {'metric': 'food_net_change', 'value': food_net_change},
])

summary.to_csv(REPORTS_DIR / 'hunting_summary.csv', index=False)