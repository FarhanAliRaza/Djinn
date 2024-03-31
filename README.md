# Djinn - Django ultimate starter template for building apis with DRF

## With Code Generation built in

## Project Setup

```
mkdir -p local
cp djinn/project/settings/templates/settings.dev.py ./local/settings.dev.py
cp djinn/project/settings/templates/settings.unittests.py ./local/settings.unittests.py
```

If you some locales related error

```
sudo apt-get clean && sudo apt-get update
sudo apt-get install locales
locale-gen en_US.UTF-8
```

## Todos (WIP)

- [x] Serializer generation
- [x] View generation
- [x] Url generation
- [x] Model generation
- [x] App generation
- [x] Add CLI for code generation
- [x] Add CLI for model generation
- [x] Add CLI for app generation
- [x] Google Oauth
- [x] Add docker support
- [x] Github Actions
- [ ] Openapi for client generation
- [ ] Setup guide???
- [ ] Add Environment variable file support
- [ ] Add Docs for setting up and using the project
- [ ] Add Cookie cutter
- [ ] Resolve error (if file exists but the code class does not exist it does not generate new code)
- [ ] Spin a separate package for code generator
