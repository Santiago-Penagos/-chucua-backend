from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
REPOS = ("chucua-backend", "chucua-api", "chucua-frontend")
EXTENSIONES = {".py", ".js", ".html", ".css"}
EXCLUIR = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
}
LIMITE = 100


def _archivos(raiz: Path):
    for ruta in raiz.rglob("*"):
        if not ruta.is_file() or ruta.suffix not in EXTENSIONES:
            continue
        if any(parte in EXCLUIR for parte in ruta.parts):
            continue
        yield ruta


def _lineas(ruta: Path) -> int:
    return len(ruta.read_text(encoding="utf-8", errors="replace").splitlines())


def infractores(raiz: Path) -> list[tuple[str, int]]:
    resultado = []
    for ruta in _archivos(raiz):
        total = _lineas(ruta)
        if total > LIMITE:
            resultado.append((str(ruta), total))
    return resultado


def test_tres_repositorios_sin_infracciones():
    resultado = []
    for repo in REPOS:
        carpeta = RAIZ / repo
        if carpeta.exists():
            resultado.extend(infractores(carpeta))
    assert resultado == [], f"Archivos con más de {LIMITE} líneas: {resultado}"


def test_detecta_un_archivo_de_101_lineas(tmp_path):
    repo = tmp_path / "chucua-frontend" / "js"
    repo.mkdir(parents=True)
    (repo / "largo.js").write_text("linea\n" * 101, encoding="utf-8")
    (repo / "corto.js").write_text("linea\n" * 100, encoding="utf-8")
    hallados = infractores(tmp_path)
    assert len(hallados) == 1
    assert hallados[0][0].endswith("largo.js")
    assert hallados[0][1] == 101
