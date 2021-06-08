# CTF config

!!! note
    Config files can be either YAML (`ctf.yml`) or JSON (`ctf.json`).

A CTF config file **must** follow the shown syntax:

```yaml
kind: ctf
name: fake-ctf
teams_file: null
challenges: []
deployments:
    internal_domain: fake.ctf
    environment: testing
    provider: gcp
    gcp:
        node_count: 1
        region: europe-west1
        machine_type: e1-standard-2
        project: change-this-123
        zone: europe-west1-b
    azure: null
```

## `kind`

The type of the config, either `ctf` or `challenge`.

## `name`

The name of the CTF.

## `teams_file`

The path of the [teams file](/configuration-files/teams-file/) for the CTF.

## `challenges`

A list of the paths of the challenges to be deployed with the CTF:

```yaml
challenges:
    - ./challenges/my-challenge
    - ./challenges/other-challenge
```

## `deployments`

The main part of a CTF config.

### `internal_domain`

The root domain name to deploy the challenges on.

### `environment`

The CTF environment, one of:

* `testing`
* `production`

### `provider`

The provider to use, must be one of:

* `gcp`
* `azure` (not implemented yet)
* `local` (not implemented yet)

!!! note
    If you are using one provider, you **must** mark as `null` the others following attributes, of course CTFKit will do it automatically.

### `gcp` (optionnal)

The configuration of GCP.


#### `node_count`

The number of nodes to deploy.

#### `region`

The region of the CTF, ex. `europe-west1`.

#### `machine_type`

The type of the machine, ex. `e1-standard-2`.

#### `project`

The GCP project's ID.

#### `zone`

The zone of the node(s), ex. `europe-west1-b`.

### `azure` (optionnal) (not implemented yet)

The configuration of Azure.

