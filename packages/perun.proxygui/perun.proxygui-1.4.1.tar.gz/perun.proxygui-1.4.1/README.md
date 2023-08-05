# perun.proxygui

Pages used by microservices in [satosacontrib.perun](https://gitlab.ics.muni.cz/perun-proxy-aai/python/satosacontrib-perun).

Place your config at `/etc/perun.proxygui.yaml`.

## Run

To run this Flask app with uWSGI, use the callable `perun.proxygui.app:get_app`, e.g.

```
mount = /proxygui=perun.proxygui.app:get_app
```
