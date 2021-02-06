import argparse
import csv
import yaml

unit_converter = {"°C"    : "_celsius",
                  "bar"   : "_bar",
                  "l/min" : "_liter_per_minute",
                  "K"     : "_kelvin",
                  "h"     : "_hour",
                  "%"     : "_percent",
                  "kWh"   : "_kilo_watt_hour",
                  "MWh"   : "_mega_watt_hour",
                 }

factor_converter = { "2"    : 0.1, 
                     "6"    : 1, 
                     "7"    : 0.01, 
                     "8"    : 1
                   }

datatype_converter = { "2"    : "int16", 
                       "6"    : "uint16", 
                       "7"    : "int16", 
                       "8"    : "uint16"
                     }

def create_argparser():
    my_parser = argparse.ArgumentParser(description='Build a config file for modbus_exporter')
    my_parser.add_argument('--out', action='store',
                       type=str,
                       help='Path of the generated modbus.yaml file for the modbus_exporter',
                       required=True)
    my_parser.add_argument('--prefix', action='store',
                       type=str,
                       help='Prefix for each matric',
                       required=True)
    my_parser.add_argument('--modbus', action='store',
                       type=str,
                       help='The path to the modbus_registers csv-file. This file is a csv representation of the original Stiebel-Eltron PDF: (Software-Erweiterung für Internet Service Gateway, Modbus TCP/IP)',
                       required=True)
    my_parser.add_argument('--controller', action='store',
                       type=str,
                       help='Controller type (either: "WPMsystem", "WPM 3" or "WPM 3i"). See the original Stiebel-Eltron PDF for details: (ISG Kompatibilitätsübersicht). E.g. a "WPL 13 ACS classic" uses a "WPM System" controller',
                       required=True)
    return my_parser

if __name__ == "__main__":
    parser = create_argparser()
    args = parser.parse_args()

    if not (args.controller == "WPMsystem" or args.controller == "WPM 3" or args.controller == "WPM 3i"):
        raise ValueError(f'Unknown controller type. This script only handles "WPMsystem", "WPM 3" or "WPM 3i". You\'ve selected "{args.controller}"')

    print(f'- Selected controller: "{args.controller}"')
    print(f'- csv-file with modbus register information: "{args.modbus}"')
    
    metrics = []
    with open(args.modbus, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='|')
        for row in reader:
            if not row[args.controller]: continue

            unit_str = ""
            if row["Unit"]:
                unit_str = unit_converter[row["Unit"]]
            
            address = 0
            if row["Function Code"] == "0x04":
                address = 400000
            elif row["Function Code"] == "0x03":
                address = 300000
            else:
                raise ValueError(f"Unknown function code for row: {row}")

            address += int(row["Modbus address"])-1
            name = row["Object designation"].lower().replace(" ", "_").replace("-", "_").replace(",", "_").replace("/", "_")

            metrics.append({
                "name": args.prefix + name + unit_str,
                "endianness": "big",
                "factor": factor_converter[row["Data type"]],
                "dataType": datatype_converter[row["Data type"]],
                "address": address,
                "metricType": "gauge",
                "help": row["Comments"]
            })

    yaml_dict = {
        "modules": [
            {
                "name": "ISGweb",
                "protocol": "tcp/ip",
                "metrics": metrics
            }
        ]
    }

    with open(args.out, 'w') as file:
        documents = yaml.dump(yaml_dict, file, sort_keys=False)