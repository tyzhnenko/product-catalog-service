# Changelog

## [0.5.0](https://github.com/tyzhnenko/product-catalog-service/compare/v0.4.4...v0.5.0) (2026-08-15)


### Features

* add variant-level filtering to product listing ([20ddb10](https://github.com/tyzhnenko/product-catalog-service/commit/20ddb10d0a8ebbb737718e3afc7af9a1a7c3b0d5))
* collapse price/location/region query params into a single price search string ([#48](https://github.com/tyzhnenko/product-catalog-service/issues/48)) ([1009ea5](https://github.com/tyzhnenko/product-catalog-service/commit/1009ea503ca6b674b481d7b0fd371dc7943b81ea))


### Bug Fixes

* update location model index to enforce unique store_id and name combination ([d02fd48](https://github.com/tyzhnenko/product-catalog-service/commit/d02fd48ab6eb4a7444892b882e326559e6e3ca64))


### Documentation

* add CLAUDE.md ([e95a944](https://github.com/tyzhnenko/product-catalog-service/commit/e95a9444dd9e12fd0fb4b2e56671aece9ef778f9))
* add new features in readme ([a1cfa39](https://github.com/tyzhnenko/product-catalog-service/commit/a1cfa396a6ceba60058c24c14ea3a23651247503))


### Continuous Integration

* bump workflow action versions ([#46](https://github.com/tyzhnenko/product-catalog-service/issues/46)) ([935047c](https://github.com/tyzhnenko/product-catalog-service/commit/935047cf338000f74fd2ef567298cce765e0a5f1))

## [0.4.4](https://github.com/tyzhnenko/product-catalog-service/compare/v0.4.3...v0.4.4) (2026-07-31)


### Continuous Integration

* add building arm64 images natively ([#44](https://github.com/tyzhnenko/product-catalog-service/issues/44)) ([05866f4](https://github.com/tyzhnenko/product-catalog-service/commit/05866f454c690d642bf9e9c2e6cf08ddacb56418))

## [0.4.3](https://github.com/tyzhnenko/product-catalog-service/compare/v0.4.2...v0.4.3) (2026-06-24)


### Chores

* **deps:** bump pydantic-settings from 2.14.1 to 2.14.2 ([#41](https://github.com/tyzhnenko/product-catalog-service/issues/41)) ([add2d53](https://github.com/tyzhnenko/product-catalog-service/commit/add2d5373293053b2352643d0d86a913d3570015))
* **deps:** bump starlette from 1.3.0 to 1.3.1 ([#40](https://github.com/tyzhnenko/product-catalog-service/issues/40)) ([ed89464](https://github.com/tyzhnenko/product-catalog-service/commit/ed89464cade2a9fe840031149015ef2e6d44527d))
* update python client ([#42](https://github.com/tyzhnenko/product-catalog-service/issues/42)) ([a21c4e0](https://github.com/tyzhnenko/product-catalog-service/commit/a21c4e0506e2972c9e34dafcb5ecec9be682ce7f))

## [0.4.2](https://github.com/tyzhnenko/product-catalog-service/compare/v0.4.1...v0.4.2) (2026-06-11)


### Chores

* add python client ([#38](https://github.com/tyzhnenko/product-catalog-service/issues/38)) ([724ccc9](https://github.com/tyzhnenko/product-catalog-service/commit/724ccc958ba744e60867a5fd543b855cd7a93756))

## [0.4.1](https://github.com/tyzhnenko/product-catalog-service/compare/v0.4.0...v0.4.1) (2026-06-07)


### Chores

* **deps:** bump starlette from 0.50.0 to 1.0.1 ([#36](https://github.com/tyzhnenko/product-catalog-service/issues/36)) ([b40b626](https://github.com/tyzhnenko/product-catalog-service/commit/b40b6262f78f3dfe4e715e6ad0b70cb8126da999))

## [0.4.0](https://github.com/tyzhnenko/product-catalog-service/compare/v0.3.2...v0.4.0) (2026-06-01)


### Features

* add pagination for bundles, categories, locations, products, stores and variants ([#34](https://github.com/tyzhnenko/product-catalog-service/issues/34)) ([45dba6b](https://github.com/tyzhnenko/product-catalog-service/commit/45dba6b4175b80b5e6eeeb251189c066aa752333))
* implement attribute and price filtering for bundles, categories, products, and variants ([#35](https://github.com/tyzhnenko/product-catalog-service/issues/35)) ([a732211](https://github.com/tyzhnenko/product-catalog-service/commit/a732211d9e58c72bc2a9f511937fb24f4d3b70ce))


### Chores

* **deps-dev:** bump pytest from 9.0.2 to 9.0.3 ([#29](https://github.com/tyzhnenko/product-catalog-service/issues/29)) ([3efd6d2](https://github.com/tyzhnenko/product-catalog-service/commit/3efd6d298dbec98879058efab3b5fbb7505cbf89))
* **deps:** bump idna from 3.11 to 3.15 ([#31](https://github.com/tyzhnenko/product-catalog-service/issues/31)) ([3c8c51d](https://github.com/tyzhnenko/product-catalog-service/commit/3c8c51d364b599d5c1d94a712d4fcedff33b63d9))
* **deps:** bump pygments from 2.19.2 to 2.20.0 ([#28](https://github.com/tyzhnenko/product-catalog-service/issues/28)) ([84ad25c](https://github.com/tyzhnenko/product-catalog-service/commit/84ad25c2195ddbd76d3d6659641fa0ce51942f64))
* **deps:** bump python-dotenv from 1.2.1 to 1.2.2 ([#30](https://github.com/tyzhnenko/product-catalog-service/issues/30)) ([aceeb43](https://github.com/tyzhnenko/product-catalog-service/commit/aceeb438fdf0f5d421ac913de37b51bb48e33a4a))


### Documentation

* add batch create/update and paginated listing features to various management sections in README ([#33](https://github.com/tyzhnenko/product-catalog-service/issues/33)) ([adedd85](https://github.com/tyzhnenko/product-catalog-service/commit/adedd85c777466d148c70d94d315d71e2adaedfe))

## [0.3.2](https://github.com/tyzhnenko/product-catalog-service/compare/v0.3.1...v0.3.2) (2026-03-21)


### Bug Fixes

* add transformation of Decimal128 to Decimal in DecimalAttributeValue and tests for attribute type conversions ([5d497be](https://github.com/tyzhnenko/product-catalog-service/commit/5d497be404427d3e63f768b361d74313bb0af3f0))

## [0.3.1](https://github.com/tyzhnenko/product-catalog-service/compare/v0.3.0...v0.3.1) (2026-03-21)


### Chores

* add titles to ID fields for better clarity in bundles, categories, locations, products, stores, and variants ([7725236](https://github.com/tyzhnenko/product-catalog-service/commit/77252364732c29cf63bb868497449df71fca2083))

## [0.3.0](https://github.com/tyzhnenko/product-catalog-service/compare/v0.2.1...v0.3.0) (2026-02-09)


### Features

* add map and data list attribute types ([ab81155](https://github.com/tyzhnenko/product-catalog-service/commit/ab81155d5af3ba34adbab010dc54b40601de64b8))


### Chores

* add pre-commit hooks and update CI configuration ([3f68c7a](https://github.com/tyzhnenko/product-catalog-service/commit/3f68c7a1909f231cb3cd3f526fa58dc72b2339a9))


### Continuous Integration

* add uv.lock to release-please config ([2fc9e62](https://github.com/tyzhnenko/product-catalog-service/commit/2fc9e62c3bfcab1c828abff6f33c4dd15d2e9839))

## [0.2.1](https://github.com/tyzhnenko/product-catalog-service/compare/v0.2.0...v0.2.1) (2026-02-02)


### Chores

* remove unused UUID7 import from domain types and test files ([70e92db](https://github.com/tyzhnenko/product-catalog-service/commit/70e92dbe1b45c95877455e31a8537d5415044f53))
* update type annotations for attributes, bundles, categories, common, locations, media, prices, products, stores, and variants ([b9c056b](https://github.com/tyzhnenko/product-catalog-service/commit/b9c056b4006a86e1c43594ad6764b19fce988d56))


### Refactors

* Refactor ID types to use PydanticObjectId ([e72c01e](https://github.com/tyzhnenko/product-catalog-service/commit/e72c01e791274cadc08c8016c4f48c4a924111fa))

## [0.2.0](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.10...v0.2.0) (2026-01-22)


### Features

* implement soft delete cascading for stores and products ([69b24fa](https://github.com/tyzhnenko/product-catalog-service/commit/69b24fa0d4ed1108d0570ae11454984c8dc5d2a6))


### Tests

* enhance recursive delete tests to verify resource removal ([195dcaf](https://github.com/tyzhnenko/product-catalog-service/commit/195dcaf9a84ae796e9632f9003571bceaf53076d))

## [0.1.10](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.9...v0.1.10) (2026-01-21)


### Bug Fixes

* make SEO fields optional in CategorySEO model ([ec0744d](https://github.com/tyzhnenko/product-catalog-service/commit/ec0744dae8a1a4cf09d31c4963e9f44484902573))


### Documentation

* enhance API endpoints with detailed descriptions and operation IDs ([a6009c4](https://github.com/tyzhnenko/product-catalog-service/commit/a6009c44d46cbf074ba187d04e94e067b21b0e75))

## [0.1.9](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.8...v0.1.9) (2026-01-13)


### Bug Fixes

* add missed attributes and brand fields in product models ([3eb8a23](https://github.com/tyzhnenko/product-catalog-service/commit/3eb8a2385910a6ccbf86a33b3c0ce8f086b32765))
* disable separate input/output schemas generation ([c6cc87e](https://github.com/tyzhnenko/product-catalog-service/commit/c6cc87ebbfb3d2146cc0d8558e693e509febecc6))


### Chores

* add OpenAPI client generator config file ([742fd94](https://github.com/tyzhnenko/product-catalog-service/commit/742fd94d237d058ca810258acbc70e71feb2f626))
* add openapi-python-client and dev dependencies ([8a938dd](https://github.com/tyzhnenko/product-catalog-service/commit/8a938dddd0c1acd6e6b65f76f63a10f832e3a8cd))
* clean up imports and improve docstring punctuation in tests ([62a993e](https://github.com/tyzhnenko/product-catalog-service/commit/62a993ee5c489711498d9764aafe0b900f489617))
* update settings to ignore extra parameters ([c55c6e7](https://github.com/tyzhnenko/product-catalog-service/commit/c55c6e7a5622089a5221df6c5c6b94c0a27646ef))


### Continuous Integration

* correct linter command syntax in CI workflow ([1424dd7](https://github.com/tyzhnenko/product-catalog-service/commit/1424dd724cd673f105700c2c465eda95cd0ffdda))
* update CI workflow to include linting steps and add Justfile for task management ([a82ce5a](https://github.com/tyzhnenko/product-catalog-service/commit/a82ce5a33e9b14f7b99c8afe4f9cfccdd654d537))

## [0.1.8](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.7...v0.1.8) (2026-01-09)


### Chores

* add APP_SETTINGS_FILE environment variable in Dockerfile ([b84a220](https://github.com/tyzhnenko/product-catalog-service/commit/b84a220a3e6705f90b2ef2f07bf942019d4b4a6c))

## [0.1.7](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.6...v0.1.7) (2026-01-09)


### Continuous Integration

* remove branch prefix from SHA metadata tag in Docker publish workflow ([b085e14](https://github.com/tyzhnenko/product-catalog-service/commit/b085e14134b09c5b9c10dd0488a25612d574d2fb))

## [0.1.6](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.5...v0.1.6) (2026-01-09)


### Continuous Integration

* update Docker metadata tags to include event ([72d26be](https://github.com/tyzhnenko/product-catalog-service/commit/72d26be64c0a737ffdc6ded3640886736eb0aed2))

## [0.1.5](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.4...v0.1.5) (2026-01-09)


### Continuous Integration

* add master branch in push triggers for image build action ([4ed8ca2](https://github.com/tyzhnenko/product-catalog-service/commit/4ed8ca27b292101fbbb69fb656aff609460b8fda))

## [0.1.4](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.3...v0.1.4) (2026-01-09)


### Continuous Integration

* remove release trigger from Docker image build workflow ([62c988f](https://github.com/tyzhnenko/product-catalog-service/commit/62c988f3619b4a016b4f58929285e8db24fd23a2))

## [0.1.3](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.2...v0.1.3) (2026-01-09)


### Continuous Integration

* update release-please token to use RELEASE_PLEASE_TOKEN ([5fa3940](https://github.com/tyzhnenko/product-catalog-service/commit/5fa39407b84a2d647cb07d66cec28ff81c93b3ef))

## [0.1.2](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.1...v0.1.2) (2026-01-09)


### Continuous Integration

* add release trigger for Docker image build and push workflow ([90803b5](https://github.com/tyzhnenko/product-catalog-service/commit/90803b5adef842cc79b116566d577da795ff71b8))

## [0.1.1](https://github.com/tyzhnenko/product-catalog-service/compare/v0.1.0...v0.1.1) (2026-01-09)


### Continuous Integration

* update docker-publish workflow to remove release trigger and add debug step for metadata tags ([b9825e2](https://github.com/tyzhnenko/product-catalog-service/commit/b9825e2afd8e5229ac6b19e4bc9d50683833ee50))

## 0.1.0 (2026-01-08)


### Features

* add bundle management functionality with models, types, and tests ([fbe36ac](https://github.com/tyzhnenko/product-catalog-service/commit/fbe36ac69c6367eb03fdb9db8ab7760a5a7e32a8))
* add categories API endpoints and service. Add tests for split_path function. ([7a1d7c7](https://github.com/tyzhnenko/product-catalog-service/commit/7a1d7c7ffc21baf92e816dd7fa9ef42ec182c047))
* add category handling to products ([bffafb0](https://github.com/tyzhnenko/product-catalog-service/commit/bffafb064293bf67857432cb9fb73eeadb0ba2a8))
* add Docker support with Dockerfile and docker-compose configuration ([a4193ab](https://github.com/tyzhnenko/product-catalog-service/commit/a4193ab18faa481fdb2cb49e122d3d7aa7b82853))
* add duplicate options validation for variant creation and updates ([1516e9b](https://github.com/tyzhnenko/product-catalog-service/commit/1516e9b5d1f28cc7184615a4d00da87878ac397e))
* add GitHub Actions workflow for building and pushing Docker images ([#2](https://github.com/tyzhnenko/product-catalog-service/issues/2)) ([5f57e11](https://github.com/tyzhnenko/product-catalog-service/commit/5f57e11cb165b8bafc997b09d540d53b5473b0fe))
* add GitHub Actions workflow for testing with MongoDB and coverege reporting ([#1](https://github.com/tyzhnenko/product-catalog-service/issues/1)) ([49c9e90](https://github.com/tyzhnenko/product-catalog-service/commit/49c9e907c9efc0b8dffbcede4443b7da72f34dde))
* add images support for bundles, categories, and variants ([225b726](https://github.com/tyzhnenko/product-catalog-service/commit/225b7262056781f338e2f2ff578d976c422c41ea))
* add location and region price handling to variants, including sanitization and validation ([fc7adee](https://github.com/tyzhnenko/product-catalog-service/commit/fc7adee23240b501bd9d2c54159ff415a90cc5bd))
* add PriceMap support to variants and implement price handling in CRUD operations ([8a565e9](https://github.com/tyzhnenko/product-catalog-service/commit/8a565e913070576a59c1d8c60b71b7fbc439cef9))
* add Product and Variant models with CRUD endpoints ([aed290d](https://github.com/tyzhnenko/product-catalog-service/commit/aed290da2674259c226888e1497000de069a3a5f))
* add release-please configuration for automated release management ([#4](https://github.com/tyzhnenko/product-catalog-service/issues/4)) ([21c21e8](https://github.com/tyzhnenko/product-catalog-service/commit/21c21e8970c79ffdf73e1e886387be7783dd6d2a))
* add stores endpoints tests ([2cf4fa2](https://github.com/tyzhnenko/product-catalog-service/commit/2cf4fa272fe327522652ff4e8e8df5a07c25051e))
* enhance location model and service to support attributes management ([7a6c9a1](https://github.com/tyzhnenko/product-catalog-service/commit/7a6c9a16e44fc8f561fdc15ab595b8e430374343))
* implement initial server setup and core configurations ([37766ce](https://github.com/tyzhnenko/product-catalog-service/commit/37766ceea200c4d4dd664136355d5d3208091a12))
* implement locations management CRUD API ([5177b49](https://github.com/tyzhnenko/product-catalog-service/commit/5177b4991814e1f36859cb0ce4951042397bed2e))
* implement ro/rw security access controls for bundles, categories, locations, products, stores, and variants ([573df07](https://github.com/tyzhnenko/product-catalog-service/commit/573df076f0047943aa57eb8c590a823c385a861f))
* implement store management API with CRUD operations and integrate GZip middleware ([53f8ae8](https://github.com/tyzhnenko/product-catalog-service/commit/53f8ae84075f6f0268e17f7d508dab6a70904287))
* refactor code structure for improved readability and maintainability ([ab9da3a](https://github.com/tyzhnenko/product-catalog-service/commit/ab9da3a58b167b20d81ffa3e58572d415c7915b7))
* update attributes handling in products and variants to use AttributesMap ([7b4acec](https://github.com/tyzhnenko/product-catalog-service/commit/7b4acec8dc78b04faddb794eba170b6a0a9c8105))
* update Docker configuration and add entrypoint script for environment variable checks ([#3](https://github.com/tyzhnenko/product-catalog-service/issues/3)) ([3fc5920](https://github.com/tyzhnenko/product-catalog-service/commit/3fc5920ff098f9845e42c59aa62feb62206a2192))
* update README with detailed features and contributing guidelines ([65719a0](https://github.com/tyzhnenko/product-catalog-service/commit/65719a0b9d8a51d08f985131fbda809a06611904))


### Bug Fixes

* reorganize test dependencies in pyproject.toml for better clarity ([3f06da0](https://github.com/tyzhnenko/product-catalog-service/commit/3f06da09a524435665e9483a61e7f709214460f7))


### Chores

* fix package path in release-please configuration ([f58e136](https://github.com/tyzhnenko/product-catalog-service/commit/f58e1366dc70dd2c7b7bbca318fa1fd290c9df2f))
* release 0.1.1 ([#5](https://github.com/tyzhnenko/product-catalog-service/issues/5)) ([6daebb8](https://github.com/tyzhnenko/product-catalog-service/commit/6daebb869943f7f8f5465c10d6a8c0c4cdf1dd4a))
* release 0.1.2 ([#7](https://github.com/tyzhnenko/product-catalog-service/issues/7)) ([7a6043a](https://github.com/tyzhnenko/product-catalog-service/commit/7a6043aa472bc8ba0dfa1e060fc95cca27b26404))
* remove changelog configuration from release-please setup ([#6](https://github.com/tyzhnenko/product-catalog-service/issues/6)) ([17089a8](https://github.com/tyzhnenko/product-catalog-service/commit/17089a8c717d78cbde5efd458e441c97c90290b6))
* reset release-please manifest to an empty state ([ce1389e](https://github.com/tyzhnenko/product-catalog-service/commit/ce1389e7e2e67192a7bc33affacade9e526d939d))
* restructure release-please configuration to include packages section ([c104f7c](https://github.com/tyzhnenko/product-catalog-service/commit/c104f7c60fe2526d116ffffb8927cf04fd7afa85))
* set initial version to 0.1.0 in project configuration ([#9](https://github.com/tyzhnenko/product-catalog-service/issues/9)) ([f55d8a2](https://github.com/tyzhnenko/product-catalog-service/commit/f55d8a235d0079a8f5c0345785a6d2ea7cfa57ff))
* simplify release-please configuration by removing unnecessary packages wrapper ([81eda67](https://github.com/tyzhnenko/product-catalog-service/commit/81eda678d64fe5b5f3438d6035bae13b954c208e))
* update release-please configuration and permissions ([#8](https://github.com/tyzhnenko/product-catalog-service/issues/8)) ([edc1898](https://github.com/tyzhnenko/product-catalog-service/commit/edc1898082153967ae1a62c2c55e99bb45a13198))
