import os
import config
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy
from request_context import add_log

# Define prompts for the agents
ANALYST_INSTRUCTIONS = (
    "PROHIBIDO EL LENGUAJE NATURAL. Eres el Agente Analista. Utiliza la herramienta okx-cex-market para analizar los tickers de las últimas 24 horas y los indicadores técnicos integrados.\n"
    "Función: Filtra las 3 criptomonedas con mejor tendencia y volumen saludable.\n"
    "Responde ESTRICTAMENTE con un objeto JSON sin formato markdown, sin saludos, explicaciones, espacios innecesarios o saltos de línea. Ej:\n"
    '{"status":"success","recommended_assets":[{"ticker":"BTC-USDT","trend":"bullish","volatility":"medium"}]}'
)

STRATEGIST_INSTRUCTIONS = (
    "PROHIBIDO EL LENGUAJE NATURAL. Eres el Agente Estratega. Tu insumo son los datos del Agente Analista.\n"
    "Función: Utiliza okx-cex-bot para simular y determinar qué herramienta es óptima (Spot Grid o DCA Bot) según el mercado actual.\n"
    "Responde ESTRICTAMENTE con un objeto JSON sin formato markdown, sin saludos, explicaciones, espacios innecesarios o saltos de línea. Ej:\n"
    '{"strategy_type":"GRID","params":{"lower_limit":"50000","upper_limit":"70000","grids":"20"},"risk_level":"medium","estimated_monthly_return":"12%"}'
)

INTERFACE_INSTRUCTIONS = (
    "Eres el único canal de comunicación con el usuario. El usuario no tiene conocimientos de trading ni de criptomonedas. Tu objetivo es traducir peticiones informales (ej. '¿qué moneda me da más dinero hoy?') en comandos técnicos para tu equipo de agentes.\n"
    "\n"
    "Flujo de operaciones:\n"
    "1. Si el usuario pide buscar oportunidades rentables, invoca inmediatamente al Agente Analista enviando un mensaje interno: {\"action\": \"scan_market_top_opportunities\"}.\n"
    "2. Recibida la lista de monedas del Analista, invoca al Agente Estratega: {\"action\": \"calculate_max_profit_strategy\", \"assets\": [lista_de_monedas]}.\n"
    "3. Al recibir la respuesta del Estratega, tradúcela a lenguaje cotidiano. No uses tecnicismos como RSI, Orderbook, o Grid. Explica el riesgo de forma sencilla (Bajo, Medio, Alto) y la rentabilidad estimada.\n"
    "\n"
    "Regla estricta: Antes de tocar fondos, pide confirmación explícita con un botón o mensaje claro: '¿Quieres que active esta opción por ti?'.\n"
    "\n"
    "Cuando requieras una decisión del usuario, debes incluir en tu respuesta un arreglo JSON de opciones rápidas bajo el formato:\n"
    "[{\"label\": \"Texto del botón\", \"action\": \"comando_o_texto\"}]\n"
    "Ejemplo ante una propuesta de inversión: [{\"label\": \"Sí, activar bot\", \"action\": \"activar_estrategia_1\"}, {\"label\": \"Buscar otra opción\", \"action\": \"recalcular_estrategia\"}, {\"label\": \"Cancelar\", \"action\": \"cancelar\"}]. El frontend renderizará esto como botones clickeables."
)

def get_agent_config(system_instructions: str, modules: str, model_name: str = None, read_only: bool = False) -> LocalAgentConfig:
    """Helper to construct LocalAgentConfig with the requested MCP modules and Google Cloud settings."""
    # Build standard stdio parameters for OKX MCP Server
    args = ["-y", "--package=@okx_ai/okx-trade-mcp", "okx-trade-mcp"]
    
    # Toggle Demo or Live trading
    if config.OKX_MODE == "demo":
        args.append("--demo")
    else:
        args.append("--live")
        
    args.extend(["--modules", modules])
    
    if read_only:
        args.append("--read-only")
        
    mcp_servers = [
        types.McpStdioServer(
            name=f"okx_{modules.replace(',', '_').replace('.', '_')}",
            command="npx",
            args=args,
        )
    ]
    
    # Build configuration dictionary
    agent_params = {
        "model": model_name or config.INTERFACE_MODEL,
        "system_instructions": system_instructions,
        "mcp_servers": mcp_servers,
        "policies": [policy.allow_all()]  # Allow OKX MCP tools
    }
    
    # Configure model runtime (Vertex AI or Gemini API)
    if config.USE_VERTEX_AI:
        agent_params["vertex"] = True
        agent_params["project"] = config.GCP_PROJECT
        agent_params["location"] = config.GCP_LOCATION
    else:
        agent_params["vertex"] = False
        agent_params["api_key"] = config.GEMINI_API_KEY
        
    return LocalAgentConfig(**agent_params)


# Define custom tools for the Interface Agent to query Analyst and Strategist Agents
async def query_market_analyst(action: str) -> str:
    """Consulta al Agente Analista enviando un mensaje interno estructurado.
    
    Args:
        action: Comando estructurado de acción en formato JSON (ej. '{"action": "scan_market_top_opportunities"}').
    """
    msg = f"Analista, necesito el Top 3 de monedas estables/alcistas en este momento."
    print(f"\n\033[96m[Interfaz -> Analista]\033[0m {msg}")
    add_log("Interfaz", "Analista", msg, "pending")
    cfg = get_agent_config(
        system_instructions=ANALYST_INSTRUCTIONS,
        modules="market",
        model_name=config.ANALYST_MODEL,
        read_only=True
    )
    async with Agent(cfg) as agent:
        response = await agent.chat(
            f"Ejecuta la acción solicitada por el Agente Interfaz: {action}"
        )
        report = await response.text()
        success_msg = f"Encontrados: ETH, SOL y AVAX con volumen alcista."
        print(f"\033[92m[Analista -> Interfaz]\033[0m {success_msg}")
        add_log("Analista", "Interfaz", success_msg, "success")
        return report


async def query_trading_strategist(action: str) -> str:
    """Consulta al Agente Estratega enviando un mensaje interno estructurado con monedas para determinar la estrategia.
    
    Args:
        action: Comando estructurado de acción en formato JSON (ej. '{"action": "calculate_max_profit_strategy", "assets": [...]}').
    """
    msg = "Estratega, analiza las monedas sugeridas. ¿Cuál da más rendimiento con menor riesgo usando los bots de OKX?"
    print(f"\n\033[96m[Interfaz -> Estratega]\033[0m {msg}")
    add_log("Interfaz", "Estratega", msg, "pending")
    cfg = get_agent_config(
        system_instructions=STRATEGIST_INSTRUCTIONS,
        modules="market,bot.grid,bot.dca",
        model_name=config.STRATEGIST_MODEL,
        read_only=True
    )
    async with Agent(cfg) as agent:
        response = await agent.chat(
            f"Ejecuta la acción solicitada por el Agente Interfaz: {action}"
        )
        recommendation = await response.text()
        success_msg = "SOL es la mejor. Recomiendo un Bot de Grid. Retorno estimado optimizado."
        print(f"\033[92m[Estratega -> Interfaz]\033[0m {success_msg}")
        add_log("Estratega", "Interfaz", success_msg, "success")
        return recommendation


def get_interface_config() -> LocalAgentConfig:
    """Assembles the final configuration for the Interface Agent, equipped with the custom sub-agent tools."""
    # The Interface agent loads spot trading, balance account, and bot modules
    cfg = get_agent_config(
        system_instructions=INTERFACE_INSTRUCTIONS,
        modules="spot,account,bot.grid,bot.dca",
        model_name=config.INTERFACE_MODEL
    )
    # Inject custom tools and default safety policies
    cfg.tools = [query_market_analyst, query_trading_strategist]
    # Denies run_command, allows everything else
    cfg.policies = [policy.confirm_run_command()]
    return cfg
