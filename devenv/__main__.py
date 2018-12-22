import devenv.cli
import devenv.conf
import yaml
import sys


def main():
    # Parse the command line separating the options:
    # - args: dockit options
    # - extras: optional docker-compose options
    (args, extras) = devenv.cli.parse_commandline()

    # print("Passed options")
    # print(args)
    # print(extras)
    # print()

    # Load and parse the yaml file
    config = devenv.conf.loadfile(args.file)
    # print(config)
    # print()

    # Split the regular docker-compose section with the devenv section
    (devenv_yaml, compose_yaml) = devenv.conf.split(config)

    # For all the services check if a devenv configuration exists
    for service in compose_yaml["services"].keys():
        if service in devenv_yaml:
            # Process the devenv section and fill the service
            devenv.conf.process(
                compose_yaml["services"][service], devenv_yaml[service])
        else:
            print("Skipping", service, ", not handled by dockit")

    # Create the file for docker-compose
    yaml.safe_dump(compose_yaml, args.output, default_flow_style=False)

    if not args.generate:
        from compose.cli.main import main as compose_main
        sys.argv[:] = ['docker-compose', '-f', args.output.name] + extras
        print("Executing docker-compose")
        compose_main()
