#!/usr/bin/env python3
"""switchmap.classes that manage various configurations."""

import os.path
import os

# Import project libraries
from switchmap.utils import general
from switchmap.utils import log


class Config(object):
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        hosts:
        snmp_auth:
    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Update the configuration directory
        # 'SWITCHMAP_CONFIGDIR' is used for unittesting
        if 'SWITCHMAP_CONFIGDIR' in os.environ:
            config_directory = os.environ['SWITCHMAP_CONFIGDIR']
        else:
            config_directory = ('%s/etc') % (general.root_directory())
        directories = [config_directory]

        # Return
        self.config_dict = general.read_yaml_files(directories)

    def cache_directory(self):
        """Determine the cache_directory.

        Args:
            None

        Returns:
            value: configured cache_directory

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'cache_directory'

        # Process configuration
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'cache_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1030, log_message)

        # Return
        return value

    def topology_device_file(self, host):
        """Determine the topology_device_file.

        Args:
            host: Hostname

        Returns:
            value: configured topology_device_file

        """
        # Get parameter
        value = ('%s/%s.yaml') % (self.cache_directory(), host)

        # Return
        return value

    def listen_address(self):
        """Get listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'listen_address'
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 0.0.0.0
        if result is None:
            result = '0.0.0.0'
        return result

    def bind_port(self):
        """Get bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'bind_port'
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 6000
        if result is None:
            result = 7000
        return result

    def agent_threads(self):
        """Get agent_threads.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'agent_threads'
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 20
        if result is None:
            result = 20
        return result

    def hostnames(self):
        """Get hostnames.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        result = []

        # Get config
        key = 'main'
        sub_key = 'hostnames'
        agent_config = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Get result
        if isinstance(agent_config, list) is True:
            result = sorted(agent_config)

        # Return
        return result

    def log_directory(self):
        """Determine the log_directory.

        Args:
            None

        Returns:
            value: configured log_directory

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'log_directory'

        # Process configuration
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'log_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1030, log_message)

        # Return
        return value

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = ('%s/switchmap-ng.log') % (self.log_directory())

        # Return
        return result

    def log_level(self):
        """Get log_level.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'log_level'
        result = None
        key = 'main'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Return
        return result


class ConfigSNMP(object):
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        hosts:
        snmp_auth:
    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.none = None

        # Update the configuration directory
        # 'SWITCHMAP_CONFIGDIR' is used for unittesting
        if 'SWITCHMAP_CONFIGDIR' in os.environ:
            config_directory = os.environ['SWITCHMAP_CONFIGDIR']
        else:
            config_directory = ('%s/etc') % (general.root_directory())
        directories = [config_directory]

        # Return
        self.config_dict = general.read_yaml_files(directories)

    def snmp_auth(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            group: Group name to filter results by

        Returns:
            snmp_data: List of SNMP data dicts found in configuration file.

        """
        # Initialize key variables
        seed_dict = {}
        seed_dict['snmp_version'] = 2
        seed_dict['snmp_secname'] = None
        seed_dict['snmp_community'] = None
        seed_dict['snmp_authprotocol'] = None
        seed_dict['snmp_authpassword'] = None
        seed_dict['snmp_privprotocol'] = None
        seed_dict['snmp_privpassword'] = None
        seed_dict['snmp_port'] = 161
        seed_dict['group_name'] = None

        # Read configuration's SNMP information. Return 'None' if none found
        if 'snmp_groups' in self.config_dict:
            if isinstance(self.config_dict['snmp_groups'], list) is True:
                if len(self.config_dict['snmp_groups']) < 1:
                    return None
            else:
                return None

        # Start populating information
        snmp_data = []
        for read_dict in self.config_dict['snmp_groups']:
            # Next entry if this is not a dict
            if isinstance(read_dict, dict) is False:
                continue

            # Assign good data
            new_dict = {}
            for key in seed_dict.keys():
                if key in read_dict:
                    new_dict[key] = read_dict[key]
                else:
                    new_dict[key] = seed_dict[key]

            # Convert relevant strings to integers
            new_dict['snmp_version'] = int(new_dict['snmp_version'])
            new_dict['snmp_port'] = int(new_dict['snmp_port'])

            # Append data to list
            snmp_data.append(new_dict)

        # Return
        return snmp_data

    def dont_use(self):
        """Dummy method to pass linter.

        Args:
            None

        Returns:
            none: Nothing

        """
        # Initialize key variables
        none = self.none
        return none


def _agent_config(agent_name, config_dict):
    """Get agent config parameter from YAML.

    Args:
        agent_name: Agent Name
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    key = 'agents'
    result = None

    # Get new result
    if key in config_dict:
        configurations = config_dict[key]
        for configuration in configurations:
            if 'agent_name' in configuration:
                if configuration['agent_name'] == agent_name:
                    result = configuration
                    break

    # Error if not configured
    if result is None:
        log_message = (
            'Agent %s not defined in configuration in '
            'agents:%s section') % (key, key)
        log.log2die(1094, log_message)

    # Return
    return result


def _key_sub_key(key, sub_key, config_dict, die=True):
    """Get config parameter from YAML.

    Args:
        key: Primary key
        sub_key: Secondary key
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    result = None

    # Verify config_dict is indeed a dict.
    # Die safely as log_directory is not defined
    if isinstance(config_dict, dict) is False:
        log.log2die_safe(1021, 'Invalid configuration file. YAML not found')

    # Get new result
    if key in config_dict:
        # Make sure we don't have a None value
        if config_dict[key] is None:
            log_message = ('%s: value in configuration is blank. Please fix')
            log.log2die_safe(1022, log_message)

        # Get value we need
        if sub_key in config_dict[key]:
            result = config_dict[key][sub_key]

    # Error if not configured
    if result is None and die is True:
        log_message = (
            '%s:%s not defined in configuration') % (key, sub_key)
        log.log2die_safe(1016, log_message)

    # Return
    return result
