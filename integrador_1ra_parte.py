import time
import os

def pedir_str(mensaje):
    dato = input(mensaje)
    while dato == "":
        print("Por favor no dejar el campo vacio")
        dato = input(mensaje)
    return dato


def pedir_int(mensaje):
    dato = input(mensaje)
    while True:
        try:
            dato = int(dato)
            break
        except ValueError:
            print("Ingrese un numero")
        dato = input(mensaje)
    return dato


def pedir_float(mensaje):
    dato = input(mensaje)
    while True:
        try:
            dato = float(dato)
            break
        except ValueError:
            print("Ingrese un numero")
        dato = input(mensaje)
    return dato


def bienvenido_encargado():
    print("Bienvenido a MCV Burgers")
    nombre = pedir_str("Ingrese su nombre encargad@: ")
    return nombre


def menu(encargado):
    print("MCV Burgers")
    print(f"Encargad@ -> {encargado}")
    print("Recuerda siempre recibir al cliente con una sonrisa :)")
    print("\n")
    print("1 – Ingreso nuevo pedido")
    print("2 – Cambio de turno")
    print("3 – Apagar sistema")

def calcular_total(pedido, precios):
    total = 0
    total += pedido["combo_simple"] * precios["combo_simple"]
    total += pedido["combo_doble"] * precios["combo_doble"]
    total += pedido["combo_triple"] * precios["combo_triple"]
    total += pedido["postre"] * precios["postre"]
    return total


def confirmar_pedido():
    respuesta = input("¿Confirma pedido? Y/N  >>> ")
    if respuesta.lower() != "y" and respuesta.lower() != "n":
        print("Error. Elija una opcion correcta")
        respuesta = input("¿Confirma pedido? Y/N  >>> ")
    if respuesta == "y":
        return True
    else:
        return False


def guardar_venta(pedido):
    renglon = ""
    for n in pedido:
        if n == "total":
            renglon += str(pedido[n]) + "\n"
        else:
            renglon += str(pedido[n]) + "; "
    f = open("ventas.txt", "a")
    f.write(renglon)
    f.close()


def guardar_encargado(encargado):
    renglon_ingreso = f"IN, {encargado['ingreso']}, Encargad@ {encargado['nombre']}, Caja: $0\n"
    renglon_egreso = f"OUT, {encargado['egreso']}, Encargad@ {encargado['nombre']}, Caja: ${encargado['facturado']}\n"
    f = open("registro.txt", "a")
    f.write(renglon_ingreso)
    f.write(renglon_egreso)
    f.write("#"*50 + "\n")
    f.close() 

###############################################################
def limpiar_consola():
    if os.name == "nt":
        borrar = os.system("cls")
    else:
        borrar == os.system("clear")
    return borrar

precios = {"combo_simple":5, "combo_doble":6, "combo_triple":7, "postre":2}
salir = True

while salir:
    limpiar_consola()
    datos_encargado = {"nombre":"", "ingreso":"", "egreso":"", "facturado":""}
    datos_encargado["nombre"] = bienvenido_encargado()
    datos_encargado["ingreso"] = time.asctime()
    caja = 0
    print("\n"*2)
    while True:
        limpiar_consola()
        menu(datos_encargado["nombre"])
        opcion = pedir_int("Elija una opcion >>> ")
        print("\n")
        if opcion == 1:
            limpiar_consola()
            pedido = {"nombre":"", "fecha":"", "combo_simple":0, "combo_doble":0, "combo_triple":0, "postre":0, "total":0}
            pedido["nombre"] = pedir_str("Ingrese nombre del cliente: ")
            pedido["fecha"] = time.asctime()
            pedido["combo_simple"] = pedir_int("Ingrese cantidad de Combos Simples: ")
            pedido["combo_doble"] = pedir_int("Ingrese cantidad de Combos Dobles: ")
            pedido["combo_triple"] = pedir_int("Ingrese cantidad de Combos Triples: ")
            pedido["postre"] = pedir_int("Ingrese cantidad de Postres: ")
            total_pedido = calcular_total(pedido, precios)
            pedido["total"] = total_pedido
            print("\n")
            print(f"Total: ${total_pedido}")
            abona_con = pedir_float("Abona con $")
            while True:
                if total_pedido > abona_con:
                    print("No es suficiente. Ingrese un monto mayor...\n")
                    abona_con = pedir_float("Abona con $")
                else:
                    print(f"Vuelto: ${abona_con - total_pedido}\n")
                    break
            estado = confirmar_pedido()
            if estado:
                caja += total_pedido
                guardar_venta(pedido)
                input("Venta guardada con exito...")
            else:
                input("Pedido cancelado")

        elif opcion == 2:
            datos_encargado["egreso"] = time.asctime()
            datos_encargado["facturado"] = caja
            guardar_encargado(datos_encargado)
            break

        elif opcion == 3:
            datos_encargado["egreso"] = time.asctime()
            datos_encargado["facturado"] = caja
            guardar_encargado(datos_encargado)
            input("Gracias por utilizar nuestro programa...")
            salir = False
            limpiar_consola()
            break

        else:
            input("Error. Elija una opcion valida...")
            print("\n"*3)
