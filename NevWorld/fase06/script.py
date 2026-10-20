from pathlib import Path
from hashlib import sha256

# ---------------   ARCHIVOS ENVIADOS   ------------------
path_A = Path('data/intercambio/envio/partida_A.jsonl')
huella_A = sha256(path_A.read_bytes()).hexdigest()
path_B = Path('data/intercambio/envio/partida_B.jsonl')
huella_B = sha256(path_B.read_bytes()).hexdigest()
print(path_A.name, path_A.stat().st_size, huella_A)
print(path_B.name, path_B.stat().st_size, huella_B)
if huella_A == huella_B:
    print("Mismo hash")
else: print("Hash distinto")
if path_A.stat().st_size == path_B.stat().st_size:
    print("Mismo tamaño")
else: print("Tamaño distinto")
print("------------------------------------------")





# ---------------   ARCHIVOS RECIBIDOS   ------------------
path_RA = Path('data/intercambio/recibido/PartidaA.jsonl')
if not path_RA.exists():
    print("ARCHIVO 'A' NO RECIBIDO")
else:
    huella_RA = sha256(path_RA.read_bytes()).hexdigest()
    hesperada_RA = "acdbc071670ba6243b4ac36214f80d920517307ce229dc211ef25bf0b75a91d1"
    tesperado_RA = 1210784
    path_RB = Path('data/intercambio/recibido/PartidaB.jsonl')
    if not path_RB.exists():
        print("ARCHIVO 'B' NO RECIBIDO")
    else:
        huella_RB = sha256(path_RB.read_bytes()).hexdigest()
        hesperada_RB = "acdbc071670ba6243b4ac36214f80d920517307ce229dc211ef25bf0b75a91d1"
        tesperado_RB = 1210784
        print(path_RA.name, path_RA.stat().st_size)
        print("Esperada: ",hesperada_RA)
        print("Recibida: ",huella_RA)
        if hesperada_RA == huella_RA: print("Resultado hash: COINCIDE")
        else: print("Resultado hash: NO COINCIDE")
        if tesperado_RA == path_RA.stat().st_size: print("Resultado tamaño: COINCIDE")
        else: print("Resultado tamaño: NO COINCIDE")
        print(path_RB.name, path_RB.stat().st_size)
        print("Esperada: ",hesperada_RB)
        print("Recibida: ",huella_RB)
        if hesperada_RB == huella_RB: print("Resultado hash: COINCIDE")
        else: print("Resultado hash: NO COINCIDE")
        if tesperado_RB == path_RB.stat().st_size: print("Resultado tamaño: COINCIDE")
        else: print("Resultado tamaño: NO COINCIDE")