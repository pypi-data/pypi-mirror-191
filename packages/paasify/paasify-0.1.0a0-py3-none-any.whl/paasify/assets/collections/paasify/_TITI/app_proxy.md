
# proxy

Documentation for app: `proxy`

## Documentation

### Traefik

This stack will deploy a simple Traefik server. It will listen for http and https.

#### Quickstart

With paasify:
```
paasify install mrjk/docker-compose
paasify create mrjk/docker-compose/traefik traefik
paasify build traefik
```


#### See also

https://github.com/thomseddon/traefik-forward-auth#operation-modes



## Variables

``` yaml title="vars.yml"
app_product: traefik
app_image_name: traefik
app_image_version: v2.9
app_port: '8080'

traefik_net_name: $app_network_name

  #traefik_net_external: false
  # Simple version: traefik_docker_constraint: "Label(`traefik.group`,`$app_network_name`)"
traefik_docker_constraint: "LabelRegex(`traefik.group`, `(^|,)${traefik_net_name}(,|$$)`)"


  # traefik_svc_tls: true

  # # Take over network_proxy !
  # app_network_name: ${net_proxy}
  #
  # traefik_docker_constraint: Label(`traefik.group`,`$app_network_name`)
  #
  # # Let's encrypt support
  # traefik_svc_certresolver: default
  # traefik_svc_certresolver_provider: null
  # traefik_svc_certresolver_resolvers:

  #
  # # OVH support for Let's encrypt
  # traefik_svc_certresolver_ovh_endpoint: ovh-eu
  # traefik_svc_certresolver_ovh_app_key:
  # traefik_svc_certresolver_ovh_app_secret:
  # traefik_svc_certresolver_ovh_consumer_key:

```

## Docker compose files





### main


``` yaml title="docker-compose.yml"
---
version: "3.7"

# Notes:
#  Only entrypoints with chars and number are accepted, because:
#  - bash does not allow hyphen in their name
#  - Traefik does not allow underscore when shell configuration is used


  # x-paasify:
  #   app:
  #     service: traefik
  #     port: 8080
  #     image: traefik
  #     version: v1.6
  #     cmd: my command
  #     cmd_help:
  #     cmd_shell:
  #     cmd_status:
  #   conf:
  #     traefik_svc_tls: false
  #     traefik_svc_entrypoints: default-http

networks:
  default:
    #external: true
    name: ${traefik_net_name}


services:
  traefik:
    image: ${app_image_name}:${app_image_version}
    restart: always
    networks:
      default:
        aliases:
          - traefik
          - traefik.proxy

    environment:

      # Core config
      - TRAEFIK_API=true
      - TRAEFIK_API_DEBUG=false
      - TRAEFIK_API_DASHBOARD=true
      - TRAEFIK_API_INSECURE=true
      # Logging
      - TRAEFIK_LOG_LEVEL=$app_log_level
      - TRAEFIK_ACCESSLOG=$app_log_access
      - TRAEFIK_ACCESSLOG_FILEPATH=/logs/access.log

      # Docker configuration
      - TRAEFIK_PROVIDERS_DOCKER=true
      - TRAEFIK_PROVIDERS_DOCKER_WATCH=true
      - TRAEFIK_PROVIDERS_DOCKER_EXPOSEDBYDEFAULT=false
      - TRAEFIK_PROVIDERS_DOCKER_NETWORK=${traefik_net_name-}
      - TRAEFIK_PROVIDERS_DOCKER_ENDPOINT=unix:///var/run/docker.sock
      - TRAEFIK_PROVIDERS_DOCKER_SWARMMODE=false
      - TRAEFIK_PROVIDERS_FILE_DIRECTORY=/etc/traefik

      # This will restrict traefik to conatiners having label `proxy.group`
      - TRAEFIK_PROVIDERS_DOCKER_CONSTRAINTS=${traefik_docker_constraint}
      # traefik_docker_constraint: "LabelRegex(`traefik.group`, `(^|,)${traefik_net_name}(,|$$)`)"
      #- TRAEFIK_PROVIDERS_DOCKER_DEFAULTRULE=Host(`{{ .Name }}.{{ index .Labels \"proxy.name\"}}`)

      # Entrypoints, always listen both http and https
      - TRAEFIK_ENTRYPOINTS_web=True
      - TRAEFIK_ENTRYPOINTS_web_ADDRESS=:80
      - TRAEFIK_ENTRYPOINTS_websecure_ADDRESS=:443

      # Deprecated
      # - TRAEFIK_PILOT_DASHBOARD=false

    labels:
      - traefik.group=${traefik_net_name}

    volumes:
      - $app_dir_conf:/etc/traefik
      - $app_dir_data:/data
      - $app_dir_logs:/logs
      - /var/run/docker.sock:/var/run/docker.sock:ro

```





### expose_http


``` yaml title="docker-compose.expose_http.yml"
---

services:
  traefik:
    ports:
      - "$app_expose_ip:80:80"

```





### le-dns


``` yaml title="docker-compose.le-dns.yml"
---

services:

  traefik:
    environment:
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}=true
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_EMAIL=${app_admin_email}
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_STORAGE=/data/acme-${traefik_svc_certresolver}.json
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_DNSCHALLENGE=true

      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_DNSCHALLENGE_PROVIDER=${traefik_cert_provider}
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_DNSCHALLENGE_RESOLVERS=${traefik_cert_provider_resolvers}
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_DNSCHALLENGE_DELAYBEFORECHECK=${traefik_cert_provider_delay:-10}

      # ACME support for ovh
      - OVH_ENDPOINT=${traefik_cert_provider_endpoint}
      - OVH_APPLICATION_KEY=${traefik_cert_provider_app_key}
      - OVH_APPLICATION_SECRET=${traefik_cert_provider_app_secret}
      - OVH_CONSUMER_KEY=${traefik_cert_provider_consumer_key}

```





### redirect_http


``` yaml title="docker-compose.redirect_http.yml"
---
# Force http redirect to https (web -> websecure)


services:
  traefik:
    environment:
      TRAEFIK_ENTRYPOINTS_web_HTTP_REDIRECTIONS_ENTRYPOINT_PERMANENT: true
      TRAEFIK_ENTRYPOINTS_web_HTTP_REDIRECTIONS_ENTRYPOINT_SCHEME: https
      TRAEFIK_ENTRYPOINTS_web_HTTP_REDIRECTIONS_ENTRYPOINT_TO: websecure

```





### debug


``` yaml title="docker-compose.debug.yml"
---
services:
  traefik:
    environment:
      - TRAEFIK_LOG_LEVEL=debug
      - TRAEFIK_ACCESSLOG=true
      - TRAEFIK_API_DEBUG=true
        #- TRAEFIK_ACCESSLOG_FILEPATH=

```





### auth


``` yaml title="docker-compose.auth.yml"

services:
  traefik:
    labels:
      # To declare
      - "traefik.http.middlewares.${traefik_svc_auth:-default}.basicauth.usersfile=/etc/traefik/users.auth"
      # To apply
      #- "traefik.http.routers.whoami.middlewares=${traefik_svc_auth:-default}"

```





### expose_dns


``` yaml title="docker-compose.expose_dns.yml"
---
version: "3.7"

services:
  traefik:
    ports:
      - "$app_expose_ip:53:53/tcp"
      - "$app_expose_ip:53:53/udp"

    environment:

      # Entrypoints
      - TRAEFIK_ENTRYPOINTS_dnsudp_ADDRESS=:53/udp
      - TRAEFIK_ENTRYPOINTS_dnsctp_ADDRESS=:53/tcp

```





### le-tls


``` yaml title="docker-compose.le-tls.yml"
---

services:

  traefik:
    environment:
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}=true
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_TLSCHALLENGE=true
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_EMAIL=${app_admin_email}
      - TRAEFIK_CERTIFICATESRESOLVERS_${traefik_svc_certresolver}_ACME_STORAGE=/data/acme-${traefik_svc_certresolver}.json

```





### expose_admin


``` yaml title="docker-compose.expose_admin.yml"
---

services:
  traefik:
    ports:
      - "$app_expose_ip:8080:8080"

```





### expose_https


``` yaml title="docker-compose.expose_https.yml"
---

services:
  traefik:
    ports:
      - "$app_expose_ip:443:443"
        #labels:
        #  - "traefik.http.routers.dashboard.tls=true"
    environment:

      # Entrypoints
      - TRAEFIK_ENTRYPOINTS_websecure_ADDRESS=:443 # <== Defining an entrypoint for port :80 named default

        # # Forced Http redirect to https
        # - TRAEFIK_ENTRYPOINTS_web_HTTP_REDIRECTIONS_ENTRYPOINT_PERMANENT=true
        # - TRAEFIK_ENTRYPOINTS_web_HTTP_REDIRECTIONS_ENTRYPOINT_SCHEME=https
        # - TRAEFIK_ENTRYPOINTS_web_HTTP_REDIRECTIONS_ENTRYPOINT_TO=websecure

```


