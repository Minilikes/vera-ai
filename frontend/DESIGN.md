---
name: Deep Space System
colors:
  surface: '#0d1515'
  surface-dim: '#0d1515'
  surface-bright: '#333b3b'
  surface-container-lowest: '#080f10'
  surface-container-low: '#151d1e'
  surface-container: '#192122'
  surface-container-high: '#232b2c'
  surface-container-highest: '#2e3637'
  on-surface: '#dce4e4'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dce4e4'
  inverse-on-surface: '#2a3232'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dbe7'
  primary: '#e1fdff'
  on-primary: '#00363a'
  primary-container: '#00f2ff'
  on-primary-container: '#006a71'
  inverse-primary: '#00696f'
  secondary: '#ffb1c3'
  on-secondary: '#66002c'
  secondary-container: '#ff4b89'
  on-secondary-container: '#590026'
  tertiary: '#fff5f2'
  on-tertiary: '#561f00'
  tertiary-container: '#ffd1bd'
  on-tertiary-container: '#a24100'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#74f5ff'
  primary-fixed-dim: '#00dbe7'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#ffd9e0'
  secondary-fixed-dim: '#ffb1c3'
  on-secondary-fixed: '#3f0019'
  on-secondary-fixed-variant: '#8f0041'
  tertiary-fixed: '#ffdbcc'
  tertiary-fixed-dim: '#ffb693'
  on-tertiary-fixed: '#351000'
  on-tertiary-fixed-variant: '#7a3000'
  background: '#0d1515'
  on-background: '#dce4e4'
  surface-variant: '#2e3637'
typography:
  display-lg:
    fontFamily: Space Grotesk
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-sm:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: 0em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  body-lg:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  body-md:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  container-max: 1440px
  gutter: 24px
---

## Brand & Style

The design system is engineered to evoke the vastness and technical precision of deep-space exploration. It targets a high-tech audience, blending scientific rigor with the awe-inspiring aesthetics of a nebula. The personality is "Futuristic Explorer"—mysterious yet highly functional, utilizing light as a primary navigator through the darkness.

The visual language is defined by a sophisticated mix of **Glassmorphism** and **Neon-Retro** influences. High-transparency layers sit atop complex, dark voids, creating a sense of three-dimensional depth. Glowing accents simulate pulsars and distant stars, providing high-contrast focal points that guide user interaction.

## Colors

The palette is built upon a foundation of infinite darkness. **Deep Obsidian** serves as the primary canvas, while **Dark Nebula Purple** provides structural depth for surfaces and containers. 

Interactive elements utilize three high-energy accents:
- **Starlight Teal** acts as the primary action color, representing clarity and navigation.
- **Pulsar Pink** is the secondary accent, used for highlights and energetic feedback.
- **Supernova Orange** is reserved for critical alerts, warnings, and system status changes.

Gradients should transition from Dark Nebula Purple to the accent colors to simulate the "glow" effect of celestial bodies.

## Typography

This design system exclusively employs **Space Grotesk** to maintain a cohesive, technical aesthetic. The typeface's geometric construction and unique apertures provide the futuristic edge necessary for a space-themed interface.

For information hierarchy, utilize wide letter spacing and uppercase styling for labels to mimic telemetry readouts. Headlines should remain tight and bold. When layering text over glass surfaces, ensure a slight text shadow or high contrast ratio is maintained to counter background blur interference.

## Layout & Spacing

The layout philosophy emphasizes the "Void." Use generous margins and white space (or "dark space") to prevent the UI from feeling claustrophobic. A **12-column fluid grid** is used for desktop layouts, while a 4-column grid is standard for mobile.

Spacing follows a strict 4px/8px baseline rhythm. Elements should feel intentionally placed within the vacuum, often floating or centered to draw the eye toward critical data points. Gutters are kept wide to accommodate glowing border overflows without visual crowding.

## Elevation & Depth

Depth in this design system is conveyed through **Glassmorphism** and light emission rather than traditional shadows. 

1.  **Backdrop Blur:** All elevated surfaces must use a backdrop blur (minimum 12px, maximum 40px) to simulate frosted cockpit glass.
2.  **Translucency:** Surfaces use a 60% opacity of Dark Nebula Purple.
3.  **Neon Borders:** Instead of drop shadows, use a 1px inner or outer border with a subtle "bloom" effect (box-shadow with high spread and low opacity) using the accent colors.
4.  **Z-Axis:** Higher elevation levels are indicated by increased border brightness and higher backdrop blur intensity, making the element appear "closer" to the viewer.

## Shapes

The shape language is "Soft-Technical." Elements use a base roundedness of 0.25rem (`rounded-sm`) to 0.5rem (`rounded-md`) to maintain a structural, engineered feel while avoiding the harshness of sharp corners. 

Buttons and input fields should utilize the `rounded-lg` (0.5rem) setting for a modern, ergonomic touch. Avoid full pill shapes except for specific notification badges or tags, as they can detract from the technical, grid-aligned aesthetic of the system.

## Components

### Buttons
Primary buttons feature a Starlight Teal gradient fill with a white 1px inner border. Secondary buttons are glassmorphic with a Pulsar Pink glowing stroke. On hover, buttons should "ignite," increasing the glow spread and intensity.

### Cards & Containers
Cards must use a `rgba(13, 11, 31, 0.6)` background with a `backdrop-filter: blur(20px)`. The border is a 1px solid line using a 20% opacity version of the primary accent.

### Inputs & Form Elements
Input fields are "Ghost" style: transparent backgrounds with a Pulsar Pink bottom border that glows when focused. Labels should always sit above the field in uppercase `label-sm` typography.

### Star-Field Backgrounds
The base level of the application should contain a subtle, non-moving "star-field" background consisting of 1px and 2px white dots at varying opacities (10%-40%). This provides texture to the Deep Obsidian base without distracting from the content.

### Feedback Elements
- **Success:** Pulsar Pink (Softened).
- **Error:** Supernova Orange (Vibrant glow).
- **Processing:** Starlight Teal (Pulsing animation).