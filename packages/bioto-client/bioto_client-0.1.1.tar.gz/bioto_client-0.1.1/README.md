# PyClient

Python Client for retrieving Bioto sensor data

## Goals

### Auth0 login

- [x] As a user I can login via auth0 to get a valid access token

Both of these steps can be accomplished by enabling device authentication.

### Retrieving sensor data

- [x] As a user I can find a garden
- [ ] As a user I can subscribe to that garden
- [ ] As a user I can see my subscribtion state for that garden
  (pending/approved/declined)
- [ ] As a iser I can get an overview of "my gardens"
- [ ] As a user I can retrieve sensor data from my gardens
  - current
  - raw data up to 7 days ago
  - downsampled data when more than 7 days ago

## Getting started

Software is installed via make (see below), this will setup a [virtual python
environments][3] managed via [`poetry`][4]

```bash
% pip install --user bioto-client
```

## How to use

When not installed as a python package but via `make install` run `poetry shell`
from the root of the project first. Otherwise the first step can be skipped.

```bash

# Call the client with the `user` command to assert a valid session
% bioto-client user

Loading session

Not logged in, please take the following steps:

1. On your computer or mobile device navigate to: https://biotoco.eu.auth0.com/activate?user_code=NEWT-OKEN
2. Enter the following code:  NEWT-OKEN

Succesfully logged in.

Bioto CLI client
Session token ***5OFd09w
```

## Improve the client

If you want to improve the client or add something which you think is missing to
the project you can either [open an issue][1] or develop the feature yourself
and open [a pull request with your changes][2].

To get started clone this project and create a branch. Now fix the bug or create
the feature you want and write some tests for it to prove it works. This can be
done by executing:

```bash
% make check
```

> **Note** This will run both tests and linters, use `make test` when you're in
`red - green - refactor` mode

When the checks are all passing and you've committed your changes, you can push
these by running:

```bash
% make dist
```

[1]: https://github.com/wearebioto/PyClient/issues
[2]: https://github.com/wearebioto/PyClient/pulls
[3]: https://docs.python.org/3/library/venv.html
[4]: https://python-poetry.org/docs/
