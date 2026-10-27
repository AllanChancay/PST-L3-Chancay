from fastapi import APIRouter
from .schemas import LecturaEntrada, ComandoLED
from . import services

router = APIRouter()

@router.get("/salud")
def salud():
    return {"estado": "ok"}

@router.get("/lecturas")
def get_lecturas():
    return services.listar_lecturas()

@router.post("/lecturas", status_code=201)
def post_lectura(datos: LecturaEntrada):
    return services.guardar_lectura(datos)

@router.get("/led")
def get_led():
    return services.consultar_led()

@router.put("/led")
def put_led(comando: ComandoLED):
    return services.cambiar_led(comando)
