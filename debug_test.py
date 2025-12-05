import sys
sys.path.append('.')
from model.model_window import EMTApi

print("=== Verificando obtención de líneas ===")
api = EMTApi()
stops = api.get_all_stops()

if stops and len(stops) > 0:
    print(f'Encontradas {len(stops)} líneas')
    print('Primeras 3 líneas:')
    for i, stop in enumerate(stops[:3]):
        print(f'  {i+1}: ID="{stop.get("id")}", lineId="{stop.get("lineId")}", name="{stop.get("name")}"')
else:
    print('No se obtuvieron líneas')

print("\n=== Probando sublíneas para línea A1 ===")
if stops and len(stops) > 0:
    first_line = stops[0]
    line_id = first_line.get('lineId')
    print(f'Probando con lineId: {line_id}')
    sublines = api.get_line_sublines(line_id)
    print(f'Resultado: {sublines}')
