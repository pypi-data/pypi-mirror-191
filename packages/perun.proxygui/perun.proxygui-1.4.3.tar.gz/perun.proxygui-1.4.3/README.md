# perun.proxygui

Pages used by microservices in [satosacontrib.perun](https://gitlab.ics.muni.cz/perun-proxy-aai/python/satosacontrib-perun).

## Configuration

Copy `perun.proxygui.yaml` from config_templates to `/etc/` (it needs to reside at `/etc/perun.proxygui.yaml`) and adjust to your needs.

The `global_cfg_filepath` option needs to point to the location of the global microservice config from the [satosacontrib.perun](https://gitlab.ics.muni.cz/perun-proxy-aai/python/satosacontrib-perun) module.

## Run

To run this Flask app with uWSGI, use the callable `perun.proxygui.app:get_app`, e.g.

```
mount = /proxygui=perun.proxygui.app:get_app
```
