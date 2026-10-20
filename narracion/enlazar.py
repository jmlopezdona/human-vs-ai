import os, sys
from pathlib import Path
origen, destino = Path(sys.argv[1]), Path(sys.argv[2])
for raiz, dirs, ficheros in os.walk(origen):
    for f in ficheros:
        p = Path(raiz) / f
        rel = p.relative_to(origen)
        blob = p
        while blob.is_symlink():  # se sigue a mano: resolve() choca con la guarda de Windows
            blob = Path(os.path.normpath(blob.parent / os.readlink(blob)))
        d = destino / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        if not d.exists():
            os.link(blob, d)
        print(rel, d.stat().st_size)
