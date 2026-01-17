---
name: frontend-ui-builder
description: Build responsive frontend pages and reusable UI components with clean layouts and modern styling.
---

# Frontend UI Builder Skill

## Instructions

1. **Page Structure**
   - Semantic HTML (`header`, `main`, `section`, `footer`)
   - Clear content hierarchy
   - Accessible markup

2. **Layout & Styling**
   - Flexbox and CSS Grid for layouts
   - Responsive design (mobile-first)
   - Consistent spacing and typography
   - Use design tokens (colors, fonts, spacing)

3. **Components**
   - Reusable UI components (buttons, cards, navbars)
   - Component-based structure
   - State-based styling (hover, focus, active)

4. **Responsiveness**
   - Media queries
   - Fluid layouts
   - Scalable units (`rem`, `%`, `vh`, `vw`)

## Best Practices
- Keep components small and reusable
- Follow mobile-first design
- Maintain consistent naming conventions
- Avoid inline styles
- Optimize for accessibility (ARIA, contrast, keyboard navigation)

## Example Structure

```html
<main class="page-container">
  <header class="navbar">
    <h1 class="logo">Brand</h1>
    <nav class="nav-links">
      <a href="#">Home</a>
      <a href="#">About</a>
      <a href="#">Contact</a>
    </nav>
  </header>

  <section class="content">
    <div class="card">
      <h2>Component Title</h2>
      <p>Reusable component content goes here.</p>
      <button class="primary-btn">Action</button>
    </div>
  </section>

  <footer class="footer">
    <p>© 2026 All rights reserved</p>
  </footer>
</main>
