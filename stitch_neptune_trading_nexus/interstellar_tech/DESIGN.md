---
name: Interstellar Tech
colors:
  surface: '#10131a'
  surface-dim: '#10131a'
  surface-bright: '#363940'
  surface-container-lowest: '#0b0e14'
  surface-container-low: '#181c22'
  surface-container: '#1c2026'
  surface-container-high: '#272a31'
  surface-container-highest: '#31353c'
  on-surface: '#e0e2eb'
  on-surface-variant: '#c1c6d5'
  inverse-surface: '#e0e2eb'
  inverse-on-surface: '#2d3037'
  outline: '#8b919f'
  outline-variant: '#414753'
  surface-tint: '#aac7ff'
  primary: '#aac7ff'
  on-primary: '#002f64'
  primary-container: '#1275e2'
  on-primary-container: '#000512'
  inverse-primary: '#005db8'
  secondary: '#aec7f7'
  on-secondary: '#143057'
  secondary-container: '#2d476f'
  on-secondary-container: '#9db6e4'
  tertiary: '#ffb68c'
  on-tertiary: '#532200'
  tertiary-container: '#c05900'
  on-tertiary-container: '#0d0300'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d6e3ff'
  primary-fixed-dim: '#aac7ff'
  on-primary-fixed: '#001b3e'
  on-primary-fixed-variant: '#00458d'
  secondary-fixed: '#d6e3ff'
  secondary-fixed-dim: '#aec7f7'
  on-secondary-fixed: '#001b3d'
  on-secondary-fixed-variant: '#2d476f'
  tertiary-fixed: '#ffdbc9'
  tertiary-fixed-dim: '#ffb68c'
  on-tertiary-fixed: '#321200'
  on-tertiary-fixed-variant: '#763400'
  background: '#10131a'
  on-background: '#e0e2eb'
  surface-variant: '#31353c'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.5px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin: 24px
---

# Interstellar Tech Design System

## Brand & Style
The brand personality is professional, modern, and high-tech, shifting from a warm, utilitarian energy to a sleek, digital-first aesthetic. It targets tech-savvy users and enterprise environments where reliability and clarity are paramount. The style is **Corporate / Modern**, emphasizing a clean interface that feels both expansive and focused. By using a dark mode foundation with vibrant blue accents, the UI evokes a sense of innovation and precision, providing a comfortable, low-strain experience for long-term usage.

## Colors
The color palette is optimized for a dark-mode environment, focusing on depth and legibility.

- **Primary (#1275e2):** A vibrant, digital blue used for key actions, active states, and brand highlights.
- **Secondary (#5f78a3):** A muted, slate blue used for supporting UI elements and less prominent actions.
- **Tertiary (#c55b00):** A warm amber used sparingly for highlights, warnings, or contrasting interactive elements to draw the eye.
- **Neutral (#74777f):** A cool grey used for surfaces, borders, and secondary text, ensuring the interface feels cohesive and structured.

## Typography
The system uses **Inter** across all levels to ensure maximum readability and a clean, geometric feel. The type scale is optimized for screen performance, with generous line heights to prevent text crowding in dark environments. Headlines utilize a heavier weight (600-700) to establish a clear hierarchy, while body text remains at weight 400 for clarity. Labels use a medium weight with slight letter spacing to remain legible at small sizes.

## Layout & Spacing
The system utilizes a 12-column fluid grid for desktop and a single-column layout for mobile. A standard 8px base unit governs all spacing decisions (increments of 4px/8px/16px/24px/32px). This creates a consistent rhythm and ensures that elements are aligned predictably. Margins are set to 24px on mobile to ensure content doesn't hit the edge of the screen, while gutters remain at 16px to maintain a compact but breathable information density.

## Elevation & Depth
In this dark-themed system, elevation is conveyed primarily through **Tonal Layers**. Higher elevation levels are represented by lighter surface colors rather than heavy shadows. Interactive elements like cards or menus use subtle low-opacity outlines and soft ambient shadows with a cool tint to separate them from the background. This approach prevents visual clutter while clearly defining the stack order of the interface.

## Shapes
The UI moves away from sharp edges to a **Rounded** aesthetic. Standard components like buttons and input fields use a 0.5rem (8px) corner radius. Larger containers like cards or modals use 1rem (16px), and oversized elements use 1.5rem (24px). This rounding softens the technical feel of the dark mode, making the interface more approachable and modern.

## Components
- **Buttons:** Feature 8px rounded corners. Primary buttons use a solid blue background (#1275e2) with white text. Secondary buttons use an outlined style with the slate blue (#5f78a3).
- **Input Fields:** Semi-transparent neutral backgrounds with a subtle border that glows primary blue on focus.
- **Cards:** Use a slightly lighter dark grey than the background to indicate elevation, with 16px rounded corners.
- **Chips:** Highly rounded (pill-shaped) with tertiary amber (#c55b00) used for status highlights or specific categories.
- **Lists:** Clean, separated by subtle low-contrast dividers, ensuring high readability against the dark background.