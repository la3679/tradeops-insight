# TradeOps Insight

Create a new project named "TradeOps Copilot". This first change is only the reviewed frontend foundation, not the complete application.

Product: an independent educational portfolio operations console for investigating synthetic fixed-income trade exceptions. It is not affiliated with any financial institution, does not execute trades, and uses only synthetic/public data.

Build only:
- React + TypeScript strict-mode foundation using the project’s supported Vite, Tailwind, and shadcn/ui stack
- accessible application shell with left navigation, top status bar, responsive layout, keyboard-visible focus states, and semantic landmarks
- deep navy/slate neutral palette, restrained teal verified state, amber pending state, red only for genuine high severity
- compact professional typography and 8-point spacing; no crypto/neon aesthetic, glassmorphism, giant marketing cards, gradients, or fake market drama
- route structure/placeholders for Overview, Exception Queue, Knowledge, Evaluations, Observability, Audit, Settings, and About
- a polished Overview screen with clearly labeled deterministic mock data only
- a persistent visible portfolio disclaimer in About and a concise footer
- reusable design tokens and small focused components
- loading, empty, and permission-denied state primitives
- no backend, database, authentication implementation, API secrets, financial rules, or model calls in this change
- no casual any, no production console.log, and no invented performance/accuracy claims

Include a concise root AGENTS.md stating that security, authorization, financial rules, and backend logic are owned outside Lovable; all Lovable output requires review and tests. Keep the change coherent and componentized.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/d5b87042-8fcf-41cf-aa66-075bf21f45ba).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
