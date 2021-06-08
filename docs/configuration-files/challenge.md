# Challenge config

!!! note
    Config files can be either YAML (`challenge.yml`) or JSON (`challenge.json`).

A challenge config file **must** follow the shown syntax:

```yaml
name: my-challenge
description: <<-EOF
This is my super description
EOF
points: 10
category: pwn
author: Me!
files:
  - chall.jpg
containers:
  - image: nginx:latest
    ports:
      - proto: TCP
        port: 80
      - proto: UDP
        port: 31337
```

## `name`

The name of the challenge.

## `description`

The description of the challenge, can be multiline.


## `points`

The points awarded once the challenge has been solved.

## `category`

The category of the challenge.

## `author`

The challenge's author.

## `files` (optionnal)

A list of the paths of the attached files for the challenge.

## `containers`

The containers' configuration for the challenge.

### `image`

The Docker image to use for the challenge. Must be accessible from your provider.

### `ports`

A list of the ports to expose for the challenge.

#### `proto`

The protocol to serve of that port, must be one of:

* `TCP`
* `UDP`

#### `port`

The number of the port to open on the container.
