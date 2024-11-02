#function to load a testbed
from genie.testbed import load

#aetest for the creation of automated tests
from pyats import aetest

#interact with command-line arguments
import sys

#ConnectionError exception for handling connection issues
from unicon.core.errors import ConnectionError

#logging information, warnings, and errors
import logging

#banner utility for better visual separation of log outputs
from pyats.log.utils import banner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of VLANs you intended to create (can also be passed as command-line arguments)
if len(sys.argv) > 1:
    EXPECTED_VLANS = [int(vlan) for vlan in sys.argv[1:]]
else:
    EXPECTED_VLANS = [11, 12, 13]

"""
-> Common Setup Class:
Connects to all devices defined in the testbed YAML file.
Stores the connected devices in self.parent.parameters['devices'].
Logs a message upon a successful connection.
Fails the script if it cannot connect to a device.
"""
class CommonSetup(aetest.CommonSetup):
    """ Common Setup Section """

    @aetest.subsection
    def connect_to_devices(self, testbed):
        """Connect to all devices in the testbed."""
        self.parent.parameters['devices'] = {}
        for device_name, device in testbed.devices.items():
            try:
                device.connect()
                self.parent.parameters['devices'][device_name] = device
                logger.info(banner(f"Connected to {device_name}"))
            except ConnectionError as e:
                self.failed(f"Failed to connect to device {device_name}: {e}")

"""
-> main test case for verifying VLAN configurations:

-> setup Method:
Attempts to get a specific device (sic_leaf1) from the testbed.
If the device is not found, it fails the setup.
Runs the show vlan command to get VLAN data and parses the output.
If parsing fails, the setup is marked as failed.

-> verify_vlans Test Method:
Verifies that all expected VLANs (EXPECTED_VLANS) are present in the device's VLAN configuration.
Converts VLAN IDs from the parsed output to integers and stores them in vlan_list.
If any expected VLAN is missing, it adds it to missing_vlans.
Uses an assert statement to raise an error if there are any missing VLANs.

-> cleanup Method:
Disconnects from sic_leaf1.
Logs a message to confirm disconnection.
Logs a warning if disconnection fails.
"""
class VLANVerificationTestcase(aetest.Testcase):
    """ VLAN Verification Test Case """

    @aetest.setup
    def setup(self, testbed):
        """ Connect to the device and load VLAN information """
        self.device = testbed.devices.get('sic_leaf1')
        if not self.device:
            self.failed("Device 'sic_leaf1' not found in the testbed.")
        try:
            # Use the generic 'show vlan' command instead of 'show vlan brief'
            self.vlan_data = self.device.parse('show vlan')
        except Exception as e:
            self.failed(f"Failed to parse VLAN information: {e}")

    @aetest.test
    def verify_vlans(self):
        """ Verify that all the expected VLANs are present """
        missing_vlans = []
        vlan_list = [int(vlan['vlan_id']) for vlan in self.vlan_data['vlans'].values()]
        for vlan in EXPECTED_VLANS:
            if vlan not in vlan_list:
                missing_vlans.append(vlan)

        assert len(missing_vlans) == 0, f"Missing VLANs: {missing_vlans}"

    @aetest.cleanup
    def cleanup(self):
        """ Cleanup Section """
        try:
            self.device.disconnect()
            logger.info(banner(f"Disconnected from {self.device.name}"))
        except Exception as e:
            logger.warning(f"Failed to disconnect device: {e}")

"""
-> Common Cleanup Class:
Disconnects from all devices connected during CommonSetup.
Logs a message to indicate that each device has been disconnected.
Logs a warning if it cannot disconnect from a device.
"""
class CommonCleanup(aetest.CommonCleanup):
    """ Common Cleanup Section """

    @aetest.subsection
    def disconnect_from_devices(self):
        """Disconnect from all devices."""
        devices = self.parent.parameters.get('devices', {})
        if devices:
            for device in devices.values():
                try:
                    device.disconnect()
                    logger.info(banner(f"Disconnected from {device.name}"))
                except Exception as e:
                    logger.warning(f"Failed to disconnect device {device.name}: {e}")

if __name__ == '__main__':
    # Load the testbed file (YAML) to connect to the devices
    testbed = load('testbed.yaml')
    aetest.main(testbed=testbed)



"""
                            +--------------+
                            |  TestScript  |
                            +-------+------+
                                    |
       +----------------------------+---------------------------+
       |                            |                           |
+------+------+            +--------+-------+           +-------+-------+
| CommonSetup |            |   Testcases    |           | CommonCleanup |
+------+------+            +--------+-------+           +-------+-------+
       |                            |                           |
+------+------+                     |                    +------+------+
| subsections |          +----------+-----------+        | subsections |
+-------------+          |          |           |        +-------------+
                     +---+---+  +---+---+  +----+----+
                     | setup |  | tests |  | cleanup |
                     +-------+  +-------+  +---------+
"""