
# dummy

Documentation for app: `dummy`

## Documentation

### Dummy

This is a dumb plugin



## Variables

``` yaml title="vars.yml"
app_description: Dummy app for docker compose with networks only

```

## Docker compose files





### main


``` yaml title="docker-compose.yml"
# Blank app that does nothing

services:
  default:
    image: ${app_image:-alpine}
    restart: "no"

```


