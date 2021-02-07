# stiebel_eltron_logging
Stiebel-Eltron heat pumps monitoring with ModBus TCP and Prometheus/Grafana.

This project provides a modbus.yaml file for the fabulous [modbus_exporter](https://github.com/RichiH/modbus_exporter) for [Prometheus](https://prometheus.io/)/[Grafana](https://grafana.com/).

If you have a Stiebel-Eltron heat pump with WMPsystem controller, then you can just download the [modbus.yaml](https://github.com/sebastianPsm/stiebel_eltron_logging/blob/main/modbus.yaml) file and use it with the [modbus_exporter](https://github.com/RichiH/modbus_exporter). If you have another heat pump exporter (WPM 3 or WPM3i), then you can use the build_modbus_exporter_config.py to build a suitable modbus.yaml.

```
py .\build_modbus_exporter_config.py --modbus .\modbus_registers.csv --controller "WPMsystem" --out modbus.yaml --prefix se_
```

## Requirements
- Running Prometheus/Grafana instance
- ISG (web?) with Modbus (afaik. all newer devices have an enabled Modbus TCP/IP server)
- Some Linux system to run the modbus_exporter
-- Why do I need the modbus_exporter: It is the missing link between the Modbus TCP/IP server running on the Stiebel-Eltron ISG and Prometheus

## Howto
- See the official Prometheus/Grafana documentation to get this up & running
- Download, build and run the modbus_exporter as a service on a Linux system. See the provided documentation in the repo
- Edit or overwrite the modbus_exporter example [modbus.yaml](https://github.com/RichiH/modbus_exporter/blob/master/modbus.yml) with the modbus.yaml from this project (if you habe a WPM 3 or WPM 3i, then build your own modbus.yaml with the build_modbus_exporter_config.py script)
- Register the modbus_exporter in Prometheus (prometheus.yaml). For example add the following:
- 
  ```
  ... other jobs from the prometheus.yaml
  
  
  - job_name: 'modbus'
    metrics_path: /modbus
    static_configs:
      - targets:
        - 192.168.178.45:502  # Modbus device. (IP of the Stiebel-Eltron ISG)
    params:
      module: ["ISGweb"]
      sub_target: ["1"] # Modbus unit identifier, e.g. when using Modbus TCP as a gateway.
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9602  # The modbus exporter's real hostname:port. (I run prometheus and the modbus_exporter on the same system)
  ```
- If not already done, then register Prometheus in Grafana
- Build your own dashboard or import [my](https://github.com/sebastianPsm/stiebel_eltron_logging/blob/main/grafana_dashboard.json) Grafana dashboard

## Result
![Grafana Dashboard 1](https://github.com/sebastianPsm/stiebel_eltron_logging/blob/main/Capture1.PNG)
![Grafana Dashboard 2](https://github.com/sebastianPsm/stiebel_eltron_logging/blob/main/Capture2.PNG)

## Resources
- [Stiebel-Eltron ISG Modbus documentation](https://www.stiebel-eltron.de/content/dam/ste/cdbassets/historic/bedienungs-_u_installationsanleitungen/ISG_Modbus__b89c1c53-6d34-4243-a630-b42cf0633361.pdf)
