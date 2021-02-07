# stiebel_eltron_logging
Stiebel-Eltron heat pumps monitoring with ModBus TCP and Prometheus/Grafana.

This project provides an modbus.yaml file for the fabulous [modbus_exporter](https://github.com/RichiH/modbus_exporter) for [Prometheus](https://prometheus.io/)/[Grafana](https://grafana.com/).

If you have a Stiebel-Eltron heat pump with WMPsystem controller, then you can just download the [modbus.yaml](https://github.com/sebastianPsm/stiebel_eltron_logging/blob/main/modbus.yaml) file and use it with the [modbus_exporter](https://github.com/RichiH/modbus_exporter). If you have another heat pump exporter (WPM 3 or WPM3i), then you can use the build_modbus_exporter_config.py to build a suitable modbus.yaml.

```
py .\build_modbus_exporter_config.py --modbus .\modbus_registers.csv --controller "WPMsystem" --out modbus.yaml --prefix se_
```

## Requirements
- Running Prometheus/Grafana instance
- ISG (web?) with Modbus (afaik. all newer devices have an enabled Modbus TCP/IP server)
- Some Linux system to run the modbus_exporter

## Howto
- See the official Prometheus/Grafana documentation to get this up & running
- Download and install the modbus_exporter. See the provided documentation in the repo
- Edit or overwrite the modbus_exporter example [modbus.yaml](https://github.com/RichiH/modbus_exporter/blob/master/modbus.yml) with the modbus.yaml from this project (if you habe a WPM 3 or WPM 3i, then build your own modbus.yaml with the build_modbus_exporter_config.py script)
- Register the modbus_exporter in Prometheus (prometheus.yaml)
- If not already done, then register Prometheus in Grafana
- Build your own dashboard or import my Grafana dashboard

## Resources
- [Stiebel-Eltron ISG Modbus documentation](https://www.stiebel-eltron.de/content/dam/ste/cdbassets/historic/bedienungs-_u_installationsanleitungen/ISG_Modbus__b89c1c53-6d34-4243-a630-b42cf0633361.pdf)
