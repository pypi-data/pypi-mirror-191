
# dns

Documentation for app: `dns`

## Documentation

No readme


## Variables

``` yaml title="vars.yml"
No var file
```

## Docker compose files





### main


``` yaml title="docker-compose.yml"
version: "3.8"
services:
  dns:
    image: phensley/docker-dns
      #command: --domain $app_domain
    command: --domain docker
    volumes:
      - $app_docker_socket:/docker.sock:ro
    networks:
      default:
        aliases:
          - dns
          - dns.dns

```


