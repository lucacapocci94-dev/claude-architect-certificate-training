# Sample Angular + Node project

A small, **realistic-shape** Angular front-end + Express back-end used by the training program as a hands-on sandbox. Use it any time a lesson asks for "a real project to point Claude at" and you don't have one ready.

## What's in here

```
sample-angular-project/
├── src/app/products/
│   ├── product.model.ts             ← shared interface
│   ├── products.service.ts          ← HTTP client to the backend
│   ├── products.service.spec.ts     ← Jasmine tests for the service
│   ├── products-list.component.ts   ← standalone Angular component
│   └── products-list.component.spec.ts
└── server/
    ├── index.js                     ← Express server
    ├── products.controller.js       ← GET /api/products + GET /api/products/:id
    └── products.controller.spec.js  ← Jest tests for the controller
```

This is **not** a fully bootstrapped Angular workspace (no `angular.json`, no `tsconfig.json`, no `node_modules`). The point is to give you canonical-shape files to read, refactor, test, and ask Claude about — **not** to be a starter you `npm start`. If you want to run it, drop these files into a fresh `ng new` workspace + `npm init` backend.

## How the training uses it

| Lesson | What you'll do here |
|---|---|
| `first-session` | Run `claude` here, ask "what does this repo do?" — watch the agentic loop in action |
| `init-walkthrough` | Run `/init` here, look at the generated `CLAUDE.md`, edit it |
| `rules-and-memory` | Add a `.claude/rules/` file with glob frontmatter for `src/app/**` (Angular rules) vs `server/**` (Node rules) |
| `slash-commands-intro` | Write `/ng-component` that scaffolds a new standalone Angular component |
| `plan-mode` | Ask Claude to plan adding a "search by name" feature across frontend + backend |
| `tdd-with-claude` | Add a `getById` method to `products.service.ts` test-first |
| `iterative-refinement` | Get Claude to fix the products-list component to handle the loading + error states properly |

Use it freely — there is nothing precious here. Break it, refactor it, ask Claude to rewrite it. That **is** the lesson.
