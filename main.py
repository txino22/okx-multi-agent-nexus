import asyncio
import sys
import config
from agents import get_interface_config
from google.antigravity import Agent

def print_header():
    # Abyssal Bioluminescence Aesthetics (Futuristic terminal header)
    print("\033[96m" + "=" * 65 + "\033[0m")
    print("\033[96m       _   _             _                      _     ___ \033[0m")
    print("\033[96m      | \\ | |___ _ __  _| |_ _   _ _ __   ___  / \\   |_ _|\033[0m")
    print("\033[96m      |  \\| / _ \\ '_ \\|_   _| | | | '_ \\ / _ \\/ _ \\   | | \033[0m")
    print("\033[96m      | |\\  |  __/ |_) || | | |_| | | | |  __/ ___ \\  | | \033[0m")
    print("\033[96m      |_| \\_|\\___| .__/ |_|  \\__,_|_| |_|\\___/_/   \\_\\|___|\033[0m")
    print("\033[96m                 |_|                                      \033[0m")
    print("\033[96m" + "=" * 65 + "\033[0m")
    print("\033[95m                NEPTUNE AI: OKX MULTI-AGENT NEXUS\033[0m")
    print(f"\033[90m          Runtime: Google Cloud Vertex AI  |  Trading: {config.OKX_MODE.upper()}\033[0m")
    print("\033[96m" + "=" * 65 + "\033[0m\n")

async def chat_loop():
    print_header()
    config.validate_config()
    
    interface_cfg = get_interface_config()
    
    print("\033[94m[System]\033[0m Inicializando Agente Interfaz y conectando a OKX MCP...")
    try:
        async with Agent(interface_cfg) as agent:
            print("\033[92m[System] Conexión establecida. Escribe 'exit' o 'quit' para salir.\033[0m\n")
            
            while True:
                try:
                    user_input = input("\033[97mUsuario >\033[0m ")
                    if not user_input.strip():
                        continue
                    if user_input.strip().lower() in ("exit", "quit"):
                        print("\033[94m[System] Apagando el nexo de agentes. Hasta luego.\033[0m")
                        break
                    
                    print("\033[90m[Pensando...] El Agente Interfaz está procesando tu solicitud...\033[0m", end="\r", flush=True)
                    response = await agent.chat(user_input)
                    
                    # Clear the Thinking... prompt
                    sys.stdout.write("\033[K")
                    
                    print("\033[96mInterfaz >\033[0m ", end="", flush=True)
                    async for chunk in response:
                        print(chunk, end="", flush=True)
                    print("\n")
                except KeyboardInterrupt:
                    print("\n\033[94m[System] Interrupción detectada. Cerrando sesión...\033[0m")
                    break
                except Exception as e:
                    print(f"\n\033[91m[Error de ejecución] {e}\033[0m\n")
    except Exception as e:
        print(f"\033[91m[Fatal] Error al iniciar la sesión del Agente: {e}\033[0m")
        print("\nVerifica que tus credenciales de Google Cloud o el API key de Gemini estén correctamente configurados en tu archivo .env.")

def main():
    try:
        asyncio.run(chat_loop())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
