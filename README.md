### Build podman image
```sh
podman build . --tag stress_analyzer
```

### Run image
```sh
podman run --env-file .env --rm -p 8000:8000 stress_analyzer
```
