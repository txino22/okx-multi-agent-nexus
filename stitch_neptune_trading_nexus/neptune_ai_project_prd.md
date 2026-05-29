# Neptune AI: Project Brief & PRD

## 1. Product Vision
**Neptune AI** is an advanced, AI-driven command center for high-frequency trading and portfolio orchestration on OKX. It replaces traditional, static dashboards with a conversational "Nexus" that deploys autonomous sub-agents and visualizes market volatility through fluid, predictive analytics.

### Core Value Proposition
- **Conversational Intelligence:** A primary AI agent that provides real-time insights and handles complex command execution.
- **Autonomous Fleet:** Deployment of specialized trading bots (Grid, Momentum, Arbitrage) that operate independently.
- **Predictive Visualization:** "Pulse" charts that map historical data against AI-forecasted trajectories.
- **Frictionless Orchestration:** A unified mobile interface designed for "abyssal" focus and data fluidity.

---

## 2. Design System: Abyssal Bioluminescence
The visual identity is defined by a futuristic "underwater data stream" aesthetic, prioritizing high-precision data and premium dark-mode execution.

### Color Palette
- **Primary (Bioluminescent Cyan):** `#00F0FF` — Core actions, active statuses, and historical trend lines.
- **Background (Abyssal Navy):** `#040814` — The absolute foundation.
- **Surface (Translucent Deep Blue):** `rgba(10, 17, 40, 0.8)` — Glassmorphic cards with `backdrop-filter: blur(12px)`.
- **Accent (Neon Purple):** `#7000FF` — Predictive AI trajectories and anomaly detection.
- **Text:** `#F8FAFC` (Primary White), `#64748B` (Muted Slate).

### Typography
- **Headings & Data:** `Space Grotesk` (700 weight for titles/numbers) — Technical, geometric, and high-contrast.
- **Body & Chat:** `Outfit` (400 weight) — Clean, modern, and highly legible.

---

## 3. Screen Specifications

### A. The Nexus (The Command Center)
The primary entry point. A conversational interface where the AI proactively flags market anomalies.
- **Key Features:** Pulsing gradient avatar, staggered chat bubble animations, and dynamic quick-action chips (e.g., "Analyze BTC").
- **Insight Flow:** When a "Critical Insight" (like an ETH volume spike) is detected, it triggers a glowing card with a direct "Deploy Agent" CTA.

### B. Deploy Agent (Configuration Flow)
A high-fidelity bottom sheet that slides up from The Nexus to configure new nodes.
- **Simplified Parameters:** Users select from a Strategy Matrix (Grid, Momentum, Arbitrage) and define Capital Allocation.
- **Interaction:** A tactile "Activate Sub-Agent" button with a heavy glow effect.

### C. Pulse (Predictive Engine)
A dedicated analysis screen for asset-specific forecasting.
- **Predictive Trajectory:** A custom SVG chart displaying historical price (solid cyan) vs. AI prediction (dotted purple).
- **Metric Cards:** Real-time Volatility Index, AI Sentiment (Bullish/Bearish), and Whale Accumulation alerts.

### D. Fleet (Agent Monitoring)
A hub for managing active autonomous sub-agents.
- **Live Feed:** Individual bot cards showing performance sparklines, current pair/position, and "breathing" status indicators.
- **Fleet PnL:** A prominent header display featuring the aggregate 24h performance with high-precision shimmers.

### E. Vault (Portfolio Visualization)
Real-time asset allocation and performance tracking.
- **Fluid Donut Chart:** Layered SVG rings with gradient shimmers representing holdings.
- **Asset Hierarchy:** Precision-styled rows for Bitcoin, Ethereum, and Solana with live volatility delta.

---

## 4. Technical Constraints & Interactivity
- **Device:** Mobile-First (Optimized for one-handed operation and high data density).
- **Transitions:** Fluid "liquid" transitions using `ease-in-out` curves and spring-physics for UI elements.
- **Animations:** 
  - Particle systems for "data dust" in the background.
  - SVG path animations for sparklines.
  - Backdrop-blur transitions for overlays.

---

## 5. Success Metrics
- **Deployment Velocity:** Time taken from AI insight to sub-agent activation.
- **Predictive Accuracy:** Delta between AI trajectory and actual market performance.
- **Cognitive Load:** Reduction in manual trade execution vs. agent-led orchestration.