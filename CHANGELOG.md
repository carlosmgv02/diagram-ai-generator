# Changelog

All notable changes to this project will be documented in this file.

## [1.0.6] - 2025-10-02

### ✨ Added
- Refactor MCP tools and diagram service architecture  [`c47325f`](https://github.com/carlosmgv02/diagram-ai-generator/commit/c47325f) ([#6)(#6](https://github.com/carlosmgv02/diagram-ai-generator/pull/6)
- remove unnecessary files  [`0114ca4`](https://github.com/carlosmgv02/diagram-ai-generator/commit/0114ca4) ([#5)(#5](https://github.com/carlosmgv02/diagram-ai-generator/pull/5)

### 🔧 Changed
- update CHANGELOG for v1.0.5 [`814aa59`](https://github.com/carlosmgv02/diagram-ai-generator/commit/814aa59)

### 📝 Other
- Change image link to GitHub hosted version [`afb409d`](https://github.com/carlosmgv02/diagram-ai-generator/commit/afb409d)


## [1.0.5] - 2025-10-02

### ⚠️ BREAKING CHANGES
- Minimum Python version is now 3.10 (was 3.9) due to MCP dependencies

### ✨ Added
- Professional badges in README (PyPI version, downloads, workflow status)
- GitHub Actions CI/CD pipeline with automated releases
- Intelligent release detection (skips docs-only changes)
- Automatic CHANGELOG generation from commits and PRs

### 🔧 Changed
- Updated Python requirement to >=3.10 for better MCP compatibility
- Improved workflow efficiency with expanded paths-ignore
- Synced PR check and release workflow ignore patterns

### 🗑️ Removed
- Unnecessary config files (.DS_Store, .pypirc.example, Makefile, etc.)
- Legacy files from old repository structure

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2025-10-02

### 🐛 Fixed
- Fixed default output directory using `Path.home()` instead of `Path.cwd()`
- Diagrams now save to `~/generated_diagrams` by default instead of package directory
- `DIAGRAM_OUTPUT_DIR` environment variable working correctly

## [1.0.3] - 2025-10-02

### ✨ Added
- Hexagonal architecture with Port/Adapter pattern for storage
- `DiagramStoragePort` interface for future extensibility
- `FilesystemDiagramStorage` adapter implementation
- Configurable output directory via `DIAGRAM_OUTPUT_DIR` environment variable

### 🔧 Changed
- Simplified README - removed Docker complexity
- `DiagramService` now uses dependency injection for storage

### 🗑️ Removed
- Docker configuration and deployment files
- Unnecessary build and run scripts

## [1.0.2] - 2025-10-02

### 🔧 Changed
- Updated author information to Carlos Martínez García-Villarrubia
- Corrected repository URLs to `carlosmgv02/diagram-ai-generator`
- Improved Claude Desktop configuration documentation

## [1.0.1] - 2025-09-30

### ✨ Added
- Initial release with MCP server support
- Multi-cloud diagram generation
- Support for AWS, Azure, GCP, Kubernetes and more
- Professional architecture diagram generation
- Claude Desktop integration

---

**Note**: Versions follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backwards compatible manner
- PATCH version for backwards compatible bug fixes

