import meraki   # handles Meraki specific API calls in python
import credentials
import csv
import time
from csv import DictReader

# Call Meraki API
dashboard = meraki.DashboardAPI(credentials.api_key)

# Type the tag or tags you need in order to filter networks
arr = input(f"\nType the tags to filter the networks that you want to change organization, separate them by a space: " )
l = list(arr.split(" "))

#Set your source organization id

organization_id = XXXXXXXXXXXXXXXX

networks = dashboard.organizations.getOrganizationNetworks(
    organization_id, total_pages='all', tags=[l], tagsFilterType='withAnyTags')

# Record number of networks
num_networks = len(networks)

# header of the CSV File, this could be changed based on your needs, in my project I need all this values
header = ['Free', 'NetworkID', 'Name', 'Tag1', 'Tag2', 'Tag3', 'Tag4', 'Tag5', Direccion', 'Serial1', 'Serial2', 'Serial3', 'Nombre', 'VLAN10', 'SVI10', 'VLAN20', 'SVI20', 'VLAN30', 'SVI30', 'VLAN40', 'SVI40']

# write header into CSV named inventario.csv
with open ('inventario.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

# Iterate over the networks to fill the CSV file
count = 0
while count < num_networks:

    # For each network, extract the relevant values

    network = networks[count]
    network_id = network['id']
    network_name = network['name']
    tags = network['tags']
    tag1 = network['tags'][0]
    tag2 = network['tags'][1]
    tag3 = network['tags'][2]
    tag4 = network['tags'][3]
    tag5 = network['tags'][4]

    # Get the VLANS data for the network, override on vlan 10, 20, 30 and 40, 
    #if you dont need to override the vlan values you can comment this section of the code

    vlans = dashboard.appliance.getNetworkApplianceVlans(network_id)
    subnet10 = vlans[0]['subnet']
    svi10 = vlans[0]['applianceIp']
    subnet20 = vlans[1]['subnet']
    svi20 = vlans[1]['applianceIp']
    subnet30 = vlans[2]['subnet']
    svi30 = vlans[2]['applianceIp']
    subnet40 = vlans[3]['subnet']
    svi40 = vlans[3]['applianceIp']

    # Get the devices on the network
    devices = dashboard.networks.getNetworkDevices(network_id)

    # How many devices have the network?
    num_devices = len(devices)

    # Fill the CSV file in the righ format with the right info,
    # For this specific project, the max number of devices in a network is 3 (1MR, 1MS, 1MX)
    if num_devices == 3:
        serial1 = devices[0]['serial']
        serial2 = devices[1]['serial']
        serial3 = devices[2]['serial']
        address = devices[0]['address']
        name = tag1 + '-' + tag2
        data = ['', network_id, network_name, tag1, tag2, tag3, tag4, tag5, address, serial1, serial2, serial3, name, subnet10, svi10, subnet20, svi20, subnet30, svi30, subnet40, svi40]
        with open ('inventario.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    elif num_devices == 2:
        serial1 = devices[0]['serial']
        serial2 = devices[1]['serial']
        serial3 = ''
        address = devices[0]['address']
        name = tag1 + '-' + tag2
        data = ['', network_id, network_name, tag1, tag2, tag3, tag4, tag5, address, serial1, serial2, serial3, name, subnet10, svi10, subnet20, svi20, subnet30, svi30, subnet40, svi40]
        with open ('inventario.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    elif num_devices == 1:
        serial1 = devices[0]['serial']
        serial2 = ''
        name2 = ''
        serial3 = ''
        name3 = ''
        address = devices[0]['address']
        name = tag1 + '-' + tag2
        data = ['', network_id, network_name, tag1, tag2, tag3, tag4, tag5, address, serial1, serial2, serial3, name, subnet10, svi10, subnet20, svi20, subnet30, svi30, subnet40, svi40]
        with open ('inventory.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    count = count+1
    time.sleep(5)

# Import the CSV created in the first part of the script, (yes, inventory.csv)

with open('inventory.csv', 'r') as read_obj:
    dict_reader = DictReader(read_obj)
    list_tiendas = list(dict_reader)

# Get the number of stores within the CSV
num_tiendas = len(list_tiendas)

# Set Source organization ID and destination Org id
org_orig = 'XXXXXXXXXXXX'
org_dest = 'ZZZZZZZZZZZZ'

# repeating routine to move all networks entered in the CSV to the destination org

count = 0
while count < num_tiendas:
    try:

        s1 = list_tiendas[count]['Serial1']
        print(s1)
        s2 = list_tiendas[count]['Serial2']
        print(s2)
        s3 = list_tiendas[count]['Serial3']
        print(s3)

        netid = list_tiendas[count]['NetworkID']
        print (netid)

        # remove devices from the origin network
        removes1 = dashboard.networks.removeNetworkDevices(netid, s1)
        time.sleep(2)
        licenses1 = dashboard.organizations.getOrganizationLicenses(org_orig, deviceSerial=s1)
        s1_lic = (licenses1[0]['id'])
        nid1 = (licenses1[0]['networkId'])
        print(s1_lic)
        print(nid1)
        if s2 == '':
            print ('Only MX on the network')
        else:
            removes2 = dashboard.networks.removeNetworkDevices(netid, s2)
            time.sleep(2)
            licenses2 = dashboard.organizations.getOrganizationLicenses(org_orig, deviceSerial=s2)
            s2_lic = (licenses2[0]['id'])
            nid2 = (licenses2[0]['networkId'])
            print(s2_lic)
            print(nid2)
        if s3 == '':
            print ('no MR on the network')
        else:
            removes3 = dashboard.networks.removeNetworkDevices(netid, s3)
            time.sleep(2)
            licenses3 = dashboard.organizations.getOrganizationLicenses(org_orig, deviceSerial=s3)
            s3_lic = (licenses3[0]['id'])
            nid3 = (licenses3[0]['networkId'])
            print(s3_lic)
            print(nid3)

        if s2 == '' and s3 == '':
            license_ids = [s1_lic]
        elif s2 != '' and s3 == '':
            license_ids = [s1_lic, s2_lic]
        elif s2 != '' and s3 != '':
            license_ids = [s1_lic, s2_lic, s3_lic]

        # move licence and devices to the target organization
        claim_license = dashboard.organizations.moveOrganizationLicenses(
            org_orig, org_dest, license_ids)

        # Create network in the target organization
        product_types = ['appliance', 'switch', 'wireless']
        name = list_tiendas[count]['Name']
        tag1 = list_tiendas[count]['Tag1']
        tag2 = list_tiendas[count]['Tag2']
        tag3 = list_tiendas[count]['Tag3']
        tag4 = list_tiendas[count]['Tag4']
        create_network = dashboard.organizations.createOrganizationNetwork(org_dest, name, product_types,
                                                                       tags= [tag1.replace(" ", ""), tag2.replace(" ", ""), tag3.replace(" ", ""), tag4.replace(" ", "")],
                                                                       timeZone='America/Mexico_City',
                                                                       notes='')
        # Add devices to the created network
        network_new = create_network['id']

        if s2 == '' and s3 == '':
            serials = [s1]
        elif s2 != '' and s3 == '':
            serials = [s1, s2]
        elif s2 != '' and s3 != '':
            serials = [s1, s2, s3]

        claim = dashboard.networks.claimNetworkDevices(network_new, serials)
          
        # Bind the new network to a template
        # If you want, you can only set the template id manually, instead of asking the user which is the destination template for every network.
        # template = 'XXXXXXXXXXXXXXXXXXXX'
        

        available_templates = dashboard.organizations.getOrganizationConfigTemplates(org_dest)

        # Show the templates available in the organization, you must select the target template.
        print("Available Templates\n---------------------------")
        for i in range(len(available_templates)):
            option = f"{i}: {available_templates[i]['name']}"
            print(option)

        # Prompt user to select a template
        user_selection = input(f"\nSelect a template [0-{len(available_templates)-1}]: ")

        # Get the template
        template = available_templates[int(user_selection)]

        bind = dashboard.networks.bindNetwork(network_new, template['id'],autoBind=True)
        
        # Override the addressing in 4 vlans, if you dont need to override the subnets of the vlans, comment this section.
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        VLAN10 = list_tiendas[count]['VLAN10']
        SVI10 = list_tiendas[count]['SVI10']
        VLAN20 = list_tiendas[count]['VLAN20']
        SVI20 = list_tiendas[count]['SVI20']
        VLAN30 = list_tiendas[count]['VLAN30']
        SVI30 = list_tiendas[count]['SVI30']
        VLAN40 = list_tiendas[count]['VLAN40']
        SVI40 = list_tiendas[count]['SVI40']
        mod_vlan10 = dashboard.appliance.updateNetworkApplianceVlan(
            network_new, vlan_id1,
            subnet=VLAN10,
            applianceIp=SVI10,
        )
        mod_vlan20 = dashboard.appliance.updateNetworkApplianceVlan(
            network_new, vlan_id2,
            subnet=VLAN20,
            applianceIp=SVI20,
        )
        mod_vlan30 = dashboard.appliance.updateNetworkApplianceVlan(
            network_new, vlan_id3,
            subnet=VLAN30,
            applianceIp=SVI30,
        )
        mod_vlan40 = dashboard.appliance.updateNetworkApplianceVlan(
            network_new, vlan_id4,
            subnet=VLAN40,
            applianceIp=SVI40,
        )

        # Set a name and address of the devices in the network.
        address = list_tiendas[count]['Direccion']
        print (address)
        nombre = list_tiendas[count]['Nombre']
        print (nombre)

        update_device_s1 = dashboard.devices.updateDevice(s1, name=nombre , address=address, moveMapMarker='true', 
                                                          tags=[tag1.replace(" ", ""),
                                                                tag2.replace(" ", ""),
                                                                tag3.replace(" ", ""),
                                                                tag4.replace(" ", "")
                                                                ])
                                                                              
        if s2 != '':
            update_device_s2 = dashboard.devices.updateDevice(s2, name=nombre, address=address, moveMapMarker='true', 
                                                          tags=[tag1.replace(" ", ""),
                                                                tag2.replace(" ", ""),
                                                                tag3.replace(" ", ""),
                                                                tag4.replace(" ", "")
                                                                ])
        else:
            print ('Network with MX only')
        if s3 != '':
            update_device_s3 = dashboard.devices.updateDevice(s3, name=nombre, address=address, moveMapMarker='true', 
                                                          tags=[tag1.replace(" ", ""),
                                                                tag2.replace(" ", ""),
                                                                tag3.replace(" ", ""),
                                                                tag4.replace(" ", "")
                                                                ])
        else:
            print ('Network without MR')

        
        # the counter is incremented to run the routine in the next network defined in the CSV.
        count = count+1
          
    except TypeError as e:
        print(e)
    except meraki.APIError as e:
        print(e)
        print('--failure trying to move the network, check logs--')
        count = count+1
