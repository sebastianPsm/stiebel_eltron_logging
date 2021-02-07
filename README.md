# stiebel_eltron_logging
Stiebel-Eltron heat pumps monitoring with ModBus TCP and Prometheus/Grafana.

This project provides an modbus.yaml file for the fabulous [modbus_exporter](https://github.com/RichiH/modbus_exporter) for [Prometheus](https://prometheus.io/)/[Grafana](https://grafana.com/).

If you have a Stiebel-Eltron heat pump with WMPsystem controller, then you can just download the [modbus.yaml](https://github.com/sebastianPsm/stiebel_eltron_logging/blob/main/modbus.yaml) file and use it with the [modbus_exporter](https://github.com/RichiH/modbus_exporter). If you have another heat pump exporter (WPM 3 or WPM3i), then you can use the build_modbus_exporter_config.py to build a suitable modbus.yaml.

```
py .\build_modbus_exporter_config.py --modbus .\modbus_registers.csv --controller "WPMsystem" --out modbus.yaml --prefix se_
```

