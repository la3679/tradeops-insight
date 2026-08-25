.PHONY: bootstrap format format-check lint typecheck build verify

bootstrap:
	npm ci

format:
	npm run format

format-check:
	npm run format:check

lint:
	npm run lint

typecheck:
	npm run typecheck

build:
	npm run build

verify: format-check lint typecheck build
