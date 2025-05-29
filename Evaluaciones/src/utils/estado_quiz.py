from datetime import datetime

def determinar_estado(fecha_inicio, fecha_fin) -> str:
    ahora = datetime.now()
    if ahora < fecha_inicio:
        return "programado"
    elif fecha_inicio <= ahora <= fecha_fin:
        return "activo"
    else:
        return "finalizado"
