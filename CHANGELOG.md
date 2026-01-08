# Changelog

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
