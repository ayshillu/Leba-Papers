# Project Setup & Integration Instructions

The current codebase is a static HTML/CSS/JavaScript project. To integrate the `Glow Menu` component (which uses React, Framer Motion, and Tailwind CSS) and support `shadcn/ui`, the project needs to be migrated to a modern React framework like Next.js.

## 1. Setup Next.js with Tailwind CSS & TypeScript

To initialize a new project with all requirements:

```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint
# When prompted, choose 'Yes' for "Use `src/` directory?" and "Use App Router?"
```

## 2. Initialize Shadcn UI

Navigate to your project directory and run:

```bash
cd my-app
npx shadcn-ui@latest init
```

**Configuration Choices:**
- **Style:** Default
- **Base Color:** Slate
- **CSS:** `app/globals.css`
- **Components:** `components/ui` (Important Standard)

### Why `components/ui`?
Shadcn/ui uses a "copy-paste" architecture where UI primitives (like buttons, inputs, menus) live in your codebase rather than a node_module. The `components/ui` folder is the standard convention for these base primitives, keeping them efficient and separate from your feature-specific components.

## 3. Install Dependencies for Glow Menu

The requested component requires these specific libraries:

```bash
npm install framer-motion lucide-react next-themes clsx tailwind-merge
```

## 4. Integration Steps

### A. Utility Class Helper
Ensure you have `lib/utils.ts` (created by shadcn init):
```ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### B. Add the Component
Create `components/ui/glow-menu.tsx` and paste the provided Glow Menu code.

### C. Use the Component
In `app/page.tsx` (or your layout), import and use `MenuBarDemo`.

---

## Alternative: Using Existing Stack (Static HTML + GSAP)

If you prefer **NOT** to migrate to React/Next.js, we can replicate the "Glow Menu" look and feel using your existing **GSAP** setup. This involves:
1.  Writing semantic HTML for the menu.
2.  Using CSS for the glassmorphism and gradients.
3.  Using GSAP for the hover animations (scale, opacity, 3D rotation).

**Recommendation:**
- If you need a scalable web app: **Migrate to Next.js** (Follow steps 1-4).
- If you just want the menu in this landing page: **Port to GSAP/HTML** (Ask me to do this!).
