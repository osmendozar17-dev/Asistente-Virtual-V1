import speech_recognition as sr
import pyttsx3
import subprocess
import psutil

def escuchar():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Reconocer en ambos idiomas (español e inglés)
        texto = recognizer.recognize_google(audio, language="es-ES")  # Intentar español primero
        print(f"Usuario (español): {texto}")
        return texto.lower()
    except sr.UnknownValueError:
        try:
            # Intentar inglés si el español no tiene resultados
            texto = recognizer.recognize_google(audio, language="en-US")
            print(f"User (English): {texto}")
            return texto.lower()
        except sr.UnknownValueError:
            print("Couldn't understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"Error making request to Google (English): {e}")
            return ""
    except sr.RequestError as e:
        print(f"Error haciendo la solicitud a Google (español): {e}")
        return ""

def hablar(mensaje):
    engine = pyttsx3.init()
    engine.say(mensaje)
    engine.runAndWait()

def abrir_aplicacion(nombre_aplicacion):
    try:
        # Puedes agregar más aplicaciones o sitios web según tus necesidades
        if nombre_aplicacion == "navegador" or nombre_aplicacion == "browser":
            subprocess.Popen(["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"])
        elif nombre_aplicacion == "editor de texto" or nombre_aplicacion == "text editor":
            subprocess.Popen(["C:\\Windows\\System32\\notepad.exe"])
        elif nombre_aplicacion == "explorador de archivos" or nombre_aplicacion == "file explorer":
            subprocess.Popen(["C:\\Windows\\explorer.exe"])
        elif nombre_aplicacion == "youtube":
            # Aquí puedes abrir el navegador y el sitio web de YouTube
            subprocess.Popen(["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe", "https://www.youtube.com"])
        else:
            hablar(f"Lo siento, no tengo información sobre cómo abrir {nombre_aplicacion}.")
            return

        hablar(f"Abriendo... Opening {nombre_aplicacion}.")
    except Exception as e:
        hablar(f"No pude abrir... I couldn't open {nombre_aplicacion}. {e}")

def cerrar_aplicacion(nombre_proceso):
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if nombre_proceso.lower() in process.info['name'].lower():
                pid = process.info['pid']
                subprocess.Popen(["taskkill", "/F", "/PID", str(pid)])
                hablar(f"Cerrando... Closing {nombre_proceso}.")
                return

        hablar(f"No se encontró {nombre_proceso} en ejecución... {nombre_proceso} not found running.")
    except Exception as e:
        hablar(f"No pude cerrar... I can't close {nombre_proceso}. {e}")

def asistente():
    hablar("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?... Hi, I'm your virtual assistant. How I could help you?")

    while True:
        comando = escuchar()

        if "adiós" in comando or "bye" in comando:
            hablar("Hasta luego. ¡Que tengas un buen día!... Bye bye. Have a nice day!")
            break
        elif "abrir" in comando or "open" in comando:
            # Ejemplos de comandos para abrir aplicaciones
            if "navegador" in comando or "browser" in comando:
                abrir_aplicacion("navegador")
            elif "editor de texto" in comando or "text editor" in comando:
                abrir_aplicacion("editor de texto")
            elif "explorador de archivos" in comando or "file explorer" in comando:
                abrir_aplicacion("explorador de archivos")
            elif "youtube" in comando:
                abrir_aplicacion("youtube")
            else:
                hablar("No entendí ese comando. ¿Puedes repetirlo?... I don't understand. Can you repeat?")
        elif "cerrar" in comando or "close" in comando:
            # Ejemplos de comandos para cerrar aplicaciones
            if "navegador" in comando or "browser" in comando:
                cerrar_aplicacion("brave.exe")
            elif "editor de texto" in comando or "text editor" in comando:
                cerrar_aplicacion("notepad.exe")
            elif "explorador de archivos" in comando or "file explorer" in comando:
                cerrar_aplicacion("explorer.exe")
            else:
                hablar("No entendí ese comando. ¿Puedes repetirlo?... I don't understand. Can you repeat?")
        else:
            hablar("No entendí ese comando. ¿Puedes repetirlo?... I don't understand. Can you repeat?")

if __name__ == "__main__":
    asistente()
