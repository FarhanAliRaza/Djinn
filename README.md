# Project setup

Clone the repository

mkdir -p local
cp djinn/project/settings/templates/settings.dev.py ./local/settings.dev.py

## Todos

- [x] Serializer generation
- [x] View generation
- [x] Url generation

- [ ] Resolve error (if file exists but the code class does not exist it does not generate new code)
- [x] Add CLI for code generation
- [ ] Add CLI for model generation
- [x] Add CLI for app generation

- [ ] Add Environment variable support
- [ ] Add docker support
- [ ] Add Docs for setting up and using the project
- [ ] Add Cookie cutter
- [ ] Allow user to change project name
