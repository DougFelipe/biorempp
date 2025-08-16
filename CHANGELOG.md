# Changelog

All notable changes to this project will be documented in this file. See [Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [0.6.1](https://github.com/DougFelipe/biorempp/compare/v0.6.0...v0.6.1) (2025-08-16)


* Merge pull request #40 from DougFelipe/development ([37ba8b9](https://github.com/DougFelipe/biorempp/commit/37ba8b946396543670117832cde53baaa38b874f)), closes [#40](https://github.com/DougFelipe/biorempp/issues/40)


### chore

* Add documentation warnings summary and priority list ([cd3a13f](https://github.com/DougFelipe/biorempp/commit/cd3a13f6cfd195fc8908955a9ff1ac39af49e649))


### revert

* volta a configuração original com documentação dando certo ([6162c42](https://github.com/DougFelipe/biorempp/commit/6162c42e0777362dca4d0d8f95db4decb051e2f9))


### refactor

* and enhance documentation across multiple modules automatizando os ajustes por scripts python ([05abad1](https://github.com/DougFelipe/biorempp/commit/05abad10085025524c6a721c96bcde8030fdfdfe))


### docs

* Add comprehensive API reference documentation and contributor guidelines ([c3e8331](https://github.com/DougFelipe/biorempp/commit/c3e8331590e1c75a3e2dee2ce00ceeba128f4c43))
* Add comprehensive documentation and build script for BioRemPP ([c504b94](https://github.com/DougFelipe/biorempp/commit/c504b9406f6bb52ede71af6ab09d7ebfd0ca19ab))
* Add comprehensive test suite documentation outlining testing architecture, methodologies, and metrics ([282ef0e](https://github.com/DougFelipe/biorempp/commit/282ef0e6a25fa39903994c436eb2a9c35b95ee01))

## [0.6.0](https://github.com/DougFelipe/biorempp/compare/v0.5.0...v0.6.0) (2025-08-15)


* Merge pull request #39 from DougFelipe/v0.5.0/simplified-architecture ([770d06b](https://github.com/DougFelipe/biorempp/commit/770d06b5b9d7230dde164f7e7d6e55a8c01c2e04)), closes [#39](https://github.com/DougFelipe/biorempp/issues/39)


### feat

* add .pypirc template and configuration script for PyPI setup ([42ed60d](https://github.com/DougFelipe/biorempp/commit/42ed60ddf1551fea47065ee7fd5c2f341a720ec8))

## [0.5.0](https://github.com/DougFelipe/biorempp/compare/v0.4.0...v0.5.0) (2025-08-14)


* Merge pull request #37 from DougFelipe/v0.5.0/simplified-architecture ([3cbd75e](https://github.com/DougFelipe/biorempp/commit/3cbd75e3db8db87e1002d4cd8adc0ff5e05aa927)), closes [#37](https://github.com/DougFelipe/biorempp/issues/37)
* Fix user experience: remove confusing fallback warning message ([240cbc5](https://github.com/DougFelipe/biorempp/commit/240cbc5c8d619ac455e899c6afea5973b5daf23c))
* Final TestPyPI configuration: fix license format, add upload script and validation checklist ([4c4a7d5](https://github.com/DougFelipe/biorempp/commit/4c4a7d52c3bc75fe7f1ca85d6e1ac648ffd12514))
* Fix TestPyPI compatibility: update build config and setuptools_scm ([6fd1931](https://github.com/DougFelipe/biorempp/commit/6fd19316f7137c36c1b9da6f027bce3d4005fd0d))


### fix

* remove unnecessary blank lines in io_utils.py for cleaner code ([bbcb032](https://github.com/DougFelipe/biorempp/commit/bbcb0321a4c7c93b7905127454984ea60c049589))
* update license field format in pyproject.toml and add pypirc_example template for PyPI credentials ([c348d2b](https://github.com/DougFelipe/biorempp/commit/c348d2bc6d5a54115a8a2365f72d12f3aa687448))


### feat

* inclide deepwiki badge link in README for improved documentation ([c37bb69](https://github.com/DougFelipe/biorempp/commit/c37bb69525f1463c4f42ede1ba9954af46efb6f3))

## [0.4.0](https://github.com/DougFelipe/biorempp/compare/v0.3.1...v0.4.0) (2025-08-13)


* Merge pull request #36 from DougFelipe/v0.5.0/simplified-architecture ([8968f13](https://github.com/DougFelipe/biorempp/commit/8968f13c2e4bb52c7d5966381101f0dedc59ecd3)), closes [#36](https://github.com/DougFelipe/biorempp/issues/36)
* Merge pull request #35 from DougFelipe/v0.5.0/simplified-architecture ([1fd9779](https://github.com/DougFelipe/biorempp/commit/1fd977913023a04797353226693cb0eb416ee5e9)), closes [#35](https://github.com/DougFelipe/biorempp/issues/35)


### feat

* add missing import and set PYTHONPATH in test for running module as script ([7d8ca80](https://github.com/DougFelipe/biorempp/commit/7d8ca80391c1cfff3479fe27cd976f262d0328a7))


### docs

* enhance semantic release configuration comments for clarity and detail ([beeef4e](https://github.com/DougFelipe/biorempp/commit/beeef4eb1b5b1823143bc5767a894ee56c02a421))
* improve docstring formatting and clarity in multiple modules ([fb72e8f](https://github.com/DougFelipe/biorempp/commit/fb72e8f145d151ee28048458f15220364c8fe843))
* update docstring example in merge_input_with_biorempp function to include output shape ([849443f](https://github.com/DougFelipe/biorempp/commit/849443f7601beab689b29cb4642d218b8f4bac05))


### ci

* update flake8 linting to only check src/ directory ([d6b9c72](https://github.com/DougFelipe/biorempp/commit/d6b9c72679bb47132958e178c098557767a153b8))


### test

* remove empty __init__.py file from tests directory ([56bc8dc](https://github.com/DougFelipe/biorempp/commit/56bc8dca2ce5526a0dd3e6173b566ba2430d1c5d))

## [0.3.1](https://github.com/DougFelipe/biorempp/compare/v0.3.0...v0.3.1) (2025-08-13)


* Merge pull request #34 from DougFelipe/v0.5.0/simplified-architecture ([bc19fa9](https://github.com/DougFelipe/biorempp/commit/bc19fa9307c8a1411455d895ea928b95c8469a4b)), closes [#34](https://github.com/DougFelipe/biorempp/issues/34)


### test

* Add comprehensive tests for enhanced logging, user feedback, error handling, and progress indicators ([5ce8fc4](https://github.com/DougFelipe/biorempp/commit/5ce8fc4a7b92c2432a1d23bcabf19eb778dbaa26))


### docs

* enhance documentation clarity and conciseness across multiple modules ([585e72b](https://github.com/DougFelipe/biorempp/commit/585e72b895f159b5e5759bca01e00905d93c9ad6))
* enhance documentation clarity and conciseness in __init__.py and enhanced_errors.py ([7757f06](https://github.com/DougFelipe/biorempp/commit/7757f067669ef8b3efd79e71c2c09296d651a93f))
* enhance module docstrings for clarity and conciseness in __init__.py and main.py ([1d4af54](https://github.com/DougFelipe/biorempp/commit/1d4af540753771aa50b7dc1fa39f651c7530fcad))
* update input_processing.py  database description and enhance pipeline documentation clarity ([fe603f1](https://github.com/DougFelipe/biorempp/commit/fe603f1f260bb438b2a60d1c20b7715adfe492da))


### refactor

* enhance clarity and conciseness in logging and user feedback documentation ([7e6d0b8](https://github.com/DougFelipe/biorempp/commit/7e6d0b81df198b264a7d6db093afa4ca6376a723))
* improve documentation clarity and user experience in CLI modules ([ec19806](https://github.com/DougFelipe/biorempp/commit/ec198068c7b29ab72e98a9926d54454562b290ae))
* improve documentation clarity by simplifying language and removing unnecessary details ([ab96ae0](https://github.com/DougFelipe/biorempp/commit/ab96ae0b9481d25499ca67a47933a42db682061f))
* remove author attribution from command module docstrings ([9d26df3](https://github.com/DougFelipe/biorempp/commit/9d26df3e7f7034a84ff3bb685a832c0772051d6e))
* remove author attribution from module docstrings ([c4c58ce](https://github.com/DougFelipe/biorempp/commit/c4c58ce3010170fd350009bed6aa2ec0df61abd6))
* simplify language and remove example usage in documentation ([2f946e3](https://github.com/DougFelipe/biorempp/commit/2f946e3343e6478101ca269aec2d34a3544259ad))
* update database file paths and improve documentation clarity across multiple modules ([584faa5](https://github.com/DougFelipe/biorempp/commit/584faa5aca932ac8182c6976ffd3d104f4de9e66))

## [0.3.0](https://github.com/DougFelipe/biorempp/compare/v0.2.0...v0.3.0) (2025-08-11)


* Merge pull request #33 from DougFelipe/v0.5.0/simplified-architecture ([17f7130](https://github.com/DougFelipe/biorempp/commit/17f71303c96b3154a0acc4cc840a3bd21bedd29f)), closes [#33](https://github.com/DougFelipe/biorempp/issues/33)
* Merge pull request #32 from DougFelipe/v0.5.0/simplified-architecture ([f0011c5](https://github.com/DougFelipe/biorempp/commit/f0011c5ac0526ec7beeaf428385eb7e02ad604b7)), closes [#32](https://github.com/DougFelipe/biorempp/issues/32)
* Merge pull request #31 from DougFelipe/v0.5.0/simplified-architecture ([65a215b](https://github.com/DougFelipe/biorempp/commit/65a215b9cbeb974049902458eaae9dfb52294b3a)), closes [#31](https://github.com/DougFelipe/biorempp/issues/31)
* Merge pull request #30 from DougFelipe/v0.5.0/simplified-architecture ([bbd66e5](https://github.com/DougFelipe/biorempp/commit/bbd66e58205ddc778a8899162453ebf1356f2677)), closes [#30](https://github.com/DougFelipe/biorempp/issues/30)


### test

* add comprehensive test suite for BioRemPP processing pipelines ([82764e5](https://github.com/DougFelipe/biorempp/commit/82764e58a6e686688722b6c34b5558b137d438d4))
* add comprehensive test suites for application and command factory modules ([b7dc9e3](https://github.com/DougFelipe/biorempp/commit/b7dc9e3ab35681f91f8f102d5c401944cfe42636))
* add comprehensive test suites for command classes ([53ce667](https://github.com/DougFelipe/biorempp/commit/53ce667c7f0c8d2b6f97176a00e9d887337ca203))


### feat

* enhance argument parsing and logging path resolution ([d652aa0](https://github.com/DougFelipe/biorempp/commit/d652aa00d39ae88b4b49ec9d8b67963902fcb7a7))


### chore

* enhance GitHub Actions workflow with improved steps and clarity for release process ([b92d98b](https://github.com/DougFelipe/biorempp/commit/b92d98bb72d1338eb438c7801b915dc221a5ab40))
* update changelog with new features and bug fixes for development version ([aba8ca0](https://github.com/DougFelipe/biorempp/commit/aba8ca08d8286b1ed348b2ac0fff56786887f3eb))
* update semantic release configuration for improved clarity and functionality ([1c4eacf](https://github.com/DougFelipe/biorempp/commit/1c4eacf6dcdf3c80df61726e57773f3016641634))

## [0.2.0](https://github.com/DougFelipe/biorempp/compare/v0.1.0...v0.2.0) (2025-08-10)


* Merge pull request #29 from DougFelipe/v0.5.0/simplified-architecture ([66d2624](https://github.com/DougFelipe/biorempp/commit/66d2624a5a0a13d834a7ea2cfff81f1e06a38780)), closes [#29](https://github.com/DougFelipe/biorempp/issues/29)
* Merge pull request #28 from DougFelipe/v0.5.0/simplified-architecture ([fc496fd](https://github.com/DougFelipe/biorempp/commit/fc496fdfbea58f98112b33a36142fd589c6d1b5b)), closes [#28](https://github.com/DougFelipe/biorempp/issues/28)
* Merge pull request #26 from DougFelipe/v0.5.0/simplified-architecture ([a659461](https://github.com/DougFelipe/biorempp/commit/a6594611083ef9a16aa26d3852a69a48e55c9f79)), closes [#26](https://github.com/DougFelipe/biorempp/issues/26)
* Merge pull request #25 from DougFelipe/v0.5.0/simplified-architecture ([3210e68](https://github.com/DougFelipe/biorempp/commit/3210e682cc2428c8a69ee29b7941cf8eaeb7a5a5)), closes [#25](https://github.com/DougFelipe/biorempp/issues/25)
* Merge pull request #24 from DougFelipe/v0.5.0/simplified-architecture ([62c6b21](https://github.com/DougFelipe/biorempp/commit/62c6b21f1dd2c8d03b86939e9e095959b5a7f122)), closes [#24](https://github.com/DougFelipe/biorempp/issues/24)
* Merge pull request #23 from DougFelipe/v0.5.0/simplified-architecture ([fa3ed2e](https://github.com/DougFelipe/biorempp/commit/fa3ed2ecf7857ae07baa941fea5b0ecf2a964403)), closes [#23](https://github.com/DougFelipe/biorempp/issues/23)
* Merge pull request #22 from DougFelipe/v0.5.0/simplified-architecture ([a52134f](https://github.com/DougFelipe/biorempp/commit/a52134f9f2a14c3311f8aefe42c9ff1d5b988982)), closes [#22](https://github.com/DougFelipe/biorempp/issues/22)
* Implement enhanced error handling, logging, and user feedback system for BioRemPP CLI ([d4bd74a](https://github.com/DougFelipe/biorempp/commit/d4bd74a472a88bf78129cffb8855951b37aa9c56))
* Merge pull request #21 from DougFelipe/v0.4.0/entities-interactions ([169795f](https://github.com/DougFelipe/biorempp/commit/169795f1cad4357daa30fe8263e91e4726969f87)), closes [#21](https://github.com/DougFelipe/biorempp/issues/21)
* Merge pull request #18 from DougFelipe/implement-gene-pathway-plotting-class ([3f029a9](https://github.com/DougFelipe/biorempp/commit/3f029a90c0f926c1e74811248fc4e88af8cfa94f)), closes [#18](https://github.com/DougFelipe/biorempp/issues/18)
* Merge pull request #16 from DougFelipe/io-processed-merged-input ([45a4db0](https://github.com/DougFelipe/biorempp/commit/45a4db0a20d75fdd64efb837735c4477852e2f9d)), closes [#16](https://github.com/DougFelipe/biorempp/issues/16)
* Merge pull request #15 from DougFelipe/io-processed-merged-input ([bbf479b](https://github.com/DougFelipe/biorempp/commit/bbf479bc10caf0ff665249a5e6953314931dcf73)), closes [#15](https://github.com/DougFelipe/biorempp/issues/15)
* Merge pull request #14 from DougFelipe/io-processed-merged-input ([c67fc15](https://github.com/DougFelipe/biorempp/commit/c67fc15c3110d42cacdadd8ab0d178ef40a9cae1)), closes [#14](https://github.com/DougFelipe/biorempp/issues/14)
* Merge pull request #11 from DougFelipe/v0.2.0/refactor-input-toxcsm-merge ([b4c4277](https://github.com/DougFelipe/biorempp/commit/b4c4277f1c63b76b1f9928add2eb6eb4aff00bdd)), closes [#11](https://github.com/DougFelipe/biorempp/issues/11)
* Merge pull request #9 from DougFelipe/v0.2.0/refactor-input-toxcsm-merge ([caf5cdc](https://github.com/DougFelipe/biorempp/commit/caf5cdce93d51a886f92c9cbf2c86469b34287a6)), closes [#9](https://github.com/DougFelipe/biorempp/issues/9)
* Merge pull request #8 from DougFelipe/6-refactor-hadeg-merge-functions-into-package-structure ([af09534](https://github.com/DougFelipe/biorempp/commit/af09534b6b00f5b743b4d8b83187485a03777c5d)), closes [#8](https://github.com/DougFelipe/biorempp/issues/8)
* Merge pull request #7 from DougFelipe/6-refactor-hadeg-merge-functions-into-package-structure ([713ccd8](https://github.com/DougFelipe/biorempp/commit/713ccd86528966ae3c471ae990441b9aa17fb21c)), closes [#7](https://github.com/DougFelipe/biorempp/issues/7)


### chore

* improve GitHub Actions release workflow for clarity and consistency ([8cf0355](https://github.com/DougFelipe/biorempp/commit/8cf0355065d58fcdbd2ade3222bf230f2746fe32))
* refactor GitHub Actions workflow and remove .releaserc.json for streamlined release process ([d225462](https://github.com/DougFelipe/biorempp/commit/d2254621e8f0dcdfa5afbdbbca362e7c1b779ef4))
* remove unused devDependencies from package.json for cleaner configuration ([0533706](https://github.com/DougFelipe/biorempp/commit/05337061c5e13da8b0ae7e54616a8554fc5e47d5))
* update .gitignore to include .pypirc and dist/ directory ([4a4f7e4](https://github.com/DougFelipe/biorempp/commit/4a4f7e47b6877cc12c0ffbc7e51611f051f05422))
* update configuration in .releaserc.json and package.json for improved semantic release setup ([234805c](https://github.com/DougFelipe/biorempp/commit/234805ce2312c109c21b3b81505a77db26519b3d))
* update GitHub Actions workflow and documentation configurations for improved clarity and stability ([772a4f5](https://github.com/DougFelipe/biorempp/commit/772a4f50eff991006c6c6663d6892407a6139d8e))


### feat

* add gene pathway plotting functionality and update dependencies ([2271bc4](https://github.com/DougFelipe/biorempp/commit/2271bc4900095cbc3b13178b4c83f51afcc0208b))
* add GenePathwayAnalyzer class for KO analysis post-merge ([1950714](https://github.com/DougFelipe/biorempp/commit/1950714ec83c794158181aa599f2778c5a527b36))
* add HADEG database pipeline with CLI support ([76a52be](https://github.com/DougFelipe/biorempp/commit/76a52bef1947cbf6ca9a9816ddef152d966b5ded))
* add KEGG-specific analysis methods and update documentation for post-merge processing ([041a631](https://github.com/DougFelipe/biorempp/commit/041a6318eb70f124806d2e89e47371a1d219b8a0))
* Add release preparation script for BioRemPP ([ee2a566](https://github.com/DougFelipe/biorempp/commit/ee2a56670f9bb0f16727f6b512d9459c12836f18))
* add SampleCompoundInteraction processor and corresponding tests for extracting sample-compound interactions ([f7f916d](https://github.com/DougFelipe/biorempp/commit/f7f916d4e739d514bcb19e832acab9e78a8622fd))
* Complete BioRemPP simplified architecture - Phases 3 & 4 ([5b85ab9](https://github.com/DougFelipe/biorempp/commit/5b85ab92c598b8cda88d90097cab141cc0b31ba3))
* Enhance InfoCommand with detailed database descriptions and add database analysis script ([bb7e58e](https://github.com/DougFelipe/biorempp/commit/bb7e58ec668ad549470fb32e3081c4d31a542b11))
* enhance user feedback and error handling messages for clarity and consistency ([8c19f55](https://github.com/DougFelipe/biorempp/commit/8c19f550f99087bff36ca32ed39bc165ed3f23ab))
* Implement BioRemPP CLI and command architecture ([31d0aa6](https://github.com/DougFelipe/biorempp/commit/31d0aa62b2e3e8794c4acee8f398ef66c0cc109f))
* Implement BioRemPP simplified architecture - Phases 1 & 2 complete ([5fdd733](https://github.com/DougFelipe/biorempp/commit/5fdd733057d25243dce0c07bc069a750a2ffae4e))
* implements PostMergeDataReader class for downstream analysis ([e60f42d](https://github.com/DougFelipe/biorempp/commit/e60f42d63627f44bfe6d2df0aa7fbb15671c68b2))
* Initialize global logger and feedback manager instances if not already set ([039608f](https://github.com/DougFelipe/biorempp/commit/039608f3ef5151c84547b9a81f62ac6e4dd4c5b8))
* Phase 1 - Surgical cleanup of modular components ([82b22e2](https://github.com/DougFelipe/biorempp/commit/82b22e2784b12848e491662c426486fbf79651bc))
* **pipeline:** integrate ToxCSM processing pipeline into BioRemPP ([a8a066c](https://github.com/DougFelipe/biorempp/commit/a8a066c347a82ca76baa2d849c8301b3a78fcb7a))
* Refactor SampleCompoundInteraction processor and update tests for new module structure ([e9a0c79](https://github.com/DougFelipe/biorempp/commit/e9a0c79c6fc1cfde3e51f285b4b230de5606c51a))
* update README and documentation structure, add new data files to MANIFEST.in ([c61560d](https://github.com/DougFelipe/biorempp/commit/c61560d2bd95ab62ac56085c7248f9187ecba4df))


### docs

* Add BioRemPP simplified architecture design document ([9afa0c7](https://github.com/DougFelipe/biorempp/commit/9afa0c7476e402e530b816c13c3fce282e8e4e7b))
* ajustes na documentação ([691cf55](https://github.com/DougFelipe/biorempp/commit/691cf551a07cb7380fe1f640fe077b5752304d5a))
* ajustes na documentação do package commands, pipelines e input_processing ([fc1bc20](https://github.com/DougFelipe/biorempp/commit/fc1bc20abe1c7979afecba531d99df2a33ee38af))
* enhance documentation across application, CLI, and command factory modules for clarity and usability ([5212cae](https://github.com/DougFelipe/biorempp/commit/5212caeb8d0f9f1dc8e461d8e0e07a1ef62d3585))
* enhance documentation across utility modules for clarity and usability ([6450072](https://github.com/DougFelipe/biorempp/commit/6450072966d2986685ebd48f2481c153257c7828))
* enhance documentation for command modules with detailed descriptions and usage examples ([b9dc35a](https://github.com/DougFelipe/biorempp/commit/b9dc35ac443a8779fa95af3e0af600d61d072cf9))
* update index and create overview documentation for BioRemPP package ([43acfe5](https://github.com/DougFelipe/biorempp/commit/43acfe5e49b6f7e852053b04058e9df5023114d8))


### refactor

* BioRemPP pipeline by removing post-merge analysis functionality and mantain modular processing ([e76e2bb](https://github.com/DougFelipe/biorempp/commit/e76e2bb4533588d3bb4ede74eab3742bc0787f74))
* BioRemPP to implement modular data processing architecture ([a30511b](https://github.com/DougFelipe/biorempp/commit/a30511b756bab8287c94d5d29d601058bb9f0b6e))
* enhance gene pathway analysis to support HADEG data source and improve logging ([cc42c38](https://github.com/DougFelipe/biorempp/commit/cc42c38f86f9602a1684c3f2112b7cf472e11a94))
* Remove all processing pipelines and update merger command documentation depracated ([daa81cc](https://github.com/DougFelipe/biorempp/commit/daa81ccb9a397d1247ae281fb14ebd9e2add3aab))
* remove deprecated process_ko_data function and update imports ([690b618](https://github.com/DougFelipe/biorempp/commit/690b618d2f00b138c509fdd10e0154cfe8d21ab0))
* update command-line arguments for post-merge and gene pathway plotting, enhance data handling in pipelines ([02bd738](https://github.com/DougFelipe/biorempp/commit/02bd7382560d396a24174c5b1a1203859ffb636b))
* update GenePathwayAnalyzer import and remove obsolete modules ([531d0f7](https://github.com/DougFelipe/biorempp/commit/531d0f7b07cc6a913812dd1bdd75710a7b3be972))
* update main function documentation and prevent CLI output pollution ([1d19faf](https://github.com/DougFelipe/biorempp/commit/1d19fafe627643036e8ed2793b4627f99ebdcc2f))


### fix

* correct import statements in analysis modules for clarity ([17431e3](https://github.com/DougFelipe/biorempp/commit/17431e383881d8c8d2362751cf9193ae0128fb19))
* update upload-artifact action to v4 in release workflow ([39f0240](https://github.com/DougFelipe/biorempp/commit/39f024082e6c26bf8489bcefcf690b7f97a91d91))


### test

* **toxcsm:** add comprehensive tests for ToxCSM fixtures with edge cases, missing values, and duplicates ([7e5c016](https://github.com/DougFelipe/biorempp/commit/7e5c01609e01525a525782ab289f80a848159331))

# Changelog

## Version 0.1 (development)

- Feature A added
- FIX: nasty bug #1729 fixed
- add your changes here!
