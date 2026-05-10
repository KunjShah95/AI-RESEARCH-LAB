# Autonomous Paper Analyzer - Frontend

React frontend for the Autonomous Paper Analyzer application.

## Features

- **Premium Design**: "Academic Noir" aesthetic with distinctive typography and rich visual effects
- **24+ Pages**: Full-featured SPA with landing, auth, dashboard, search, and more
- **API Integration**: Connected to backend with graceful fallback to mock data
- **Responsive**: Works on desktop and tablet devices
- **Animations**: Smooth transitions powered by Framer Motion

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## Design System

The app uses a custom "Academic Noir" design system defined in `App.css`:

- **Fonts**: Cormorant Garamond, Outfit, Instrument Serif
- **Colors**: Deep charcoal (#1a1a1a, #2d2d2d), warm gold (#d4a853)
- **Components**: Cards, buttons, inputs, modals, toasts
- **Effects**: Noise texture, glassmorphism, subtle animations

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server at localhost:5173 |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx       # Main app with all pages
│   ├── App.css      # All styles and design system
│   ├── main.jsx     # Entry point
│   ├── services/
│   │   └── api.js   # API service layer
│   └── index.css    # Global styles and fonts
├── package.json
└── vite.config.js
```

## API Connection

The frontend connects to the backend at `VITE_API_URL` (default: http://localhost:8000). All pages have:
- Try/catch error handling
- Fallback to mock data when API unavailable
- Loading states with spinners
- Error messages for failed requests