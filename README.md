# Product Catalog Service (PCS)

## Terms of usage

By using this project or its source code, for any purpose and in any shape or form, you grant your implicit agreement to all the following statements:

    You condemn Russia and its military aggression against Ukraine
    You recognize that Russia is an occupant that unlawfully invaded a sovereign state
    You support Ukraine's territorial integrity, including its claims over temporarily occupied territories of Crimea and Donbas
    You reject false narratives perpetuated by Russian state propaganda

## Features

- [x] Store management
- [x] Product management
    - [x] Dynamic attributes
    - [x] Categories assignment
    - [x] Paginated listing
    - [ ] Search by attributes (coming soon)
    - [ ] Batch create/update (coming soon)
- [x] Variant management with option combinations
    - [x] Dynamic attributes
    - [x] Default price management
    - [x] Location specific price management
    - [x] Region specific price management
    - [x] Paginated listing
    - [ ] Search by attributes (coming soon)
    - [ ] Search by prices (coming soon)
    - [ ] Batch create/update (coming soon)
- [x] Categories management
    - [x] Attributes management
    - [x] Paginated listing
    - [ ] Search by attributes (coming soon)
    - [ ] Batch create/update (coming soon)
- [x] Locations management
    - [x] Attributes management
    - [x] Paginated listing
    - [ ] Search by attributes (coming soon)
    - [ ] Batch create/update (coming soon)
- [x] Bundles management
    - [x] Dynamic attributes
    - [x] Default price management
    - [x] Location specific price management
    - [x] Region specific price management
    - [x] Paginated listing
    - [ ] Search by attributes (coming soon)
    - [ ] Search by prices (coming soon)
    - [ ] Batch create/update (coming soon)

## Start with Docker

1. Ensure Docker and Docker Compose are installed on your machine.
2. Clone the repository:
   ```bash
   git clone https://github.com/tyzhnenko/product-catalog-service.git
   cd product-catalog-service
   ```
3. Edit `docker/docker-compose.yaml` to set your desired API keys and other configurations.
4. Start the services:
   ```bash
   docker compose -p catalog -f docker/docker-compose.yaml up --build
   ```
5. Access the API at `http://localhost:8000` and Mongo Express at `http://localhost:8081`.


## Contributing

### Development Workflow
- Create a feature branch from `master`.
- Follow Conventional Commits for messages (e.g., `feat: add ledger summary endpoint`).
    - `feat:` for new features
    - `fix:` for bug fixes
    - `chore:` for maintenance tasks
    - `docs:` for documentation changes
    - `refactor:` for code changes that neither fix a bug nor add a feature
    - `perf:` for performance improvements
    - `test:` for adding or updating tests
    - `build:` for build system changes
    - `ci:` for CI/CD changes
    - `style:` for formatting changes
    - `revert:` for reverting changes
    - `deps:` for dependency updates
    - `security:` for security fixes
    - `contributors:` for acknowledging contributors
    - use an `!` after the type (e.g., `feat!:`) or add a `BREAKING CHANGE:` footer for changes that break backward compatibility
- Keep PRs focused and small; include tests for new behavior.
- Ensure CI basics pass locally: lint, format, type-check, and tests. Run these commands before pushing:
```bash
just format
just lint
just test
```
- Use pre-commit hooks for consistent code quality. Install them with:
```bash
uv run prek install
```

### Pull Request Checklist
- [ ] Tests added/updated for changes
- [ ] `ruff check` and `ruff format` pass
- [ ] `mypy` passes
- [ ] Brief description of changes and rationale

### Reporting Issues
- Include steps to reproduce, expected vs actual behavior, and environment details.
- Propose a minimal fix or a direction when possible.

Thank you for helping improve Product Catalog Service!
