### Build podman image
```sh
podman build . --tag otp-verification
```

### Run image
```sh
podman run --rm -p 8000:8000 otp-verification
```
