import threading

from chucua_backend.db.conexion import conectar


def test_conexion_se_usa_y_cierra_desde_otro_hilo(tmp_path):
    base = conectar(tmp_path / "hilos.db")
    errores = []

    def trabajar():
        try:
            base.execute("SELECT 1").fetchone()
            base.close()
        except Exception as exc:  # noqa: BLE001 - se reporta en el hilo principal
            errores.append(exc)

    hilo = threading.Thread(target=trabajar)
    hilo.start()
    hilo.join()
    assert errores == []


def test_permite_lecturas_concurrentes(tmp_path):
    ruta = tmp_path / "concurrente.db"
    conexion = conectar(ruta)
    conexion.execute(
        "INSERT INTO escenarios (nombre, sector, geometria, tipo_escenario)"
        " VALUES (?,?,?,?)",
        ("Cancha", "I", '{"type": "Point", "coordinates": [-74.16, 4.62]}', "cancha"),
    )
    conexion.commit()
    conexion.close()

    resultados = []

    def leer():
        otra = conectar(ruta)
        resultados.append(len(otra.execute("SELECT * FROM escenarios").fetchall()))
        otra.close()

    hilos = [threading.Thread(target=leer) for _ in range(4)]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()
    assert resultados == [1, 1, 1, 1]
