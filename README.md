# MoveNetworks_Orgs
Move Networks between organizations.

In case you are growing in your Meraki organization and need to do a split to move networks to a second organization, 
this script can help you make the move simpler.


Considerations

- Networks to be moved to a second organization are filtered using tags.
- Templates are used in networks that move between organizations.
- Both organizations use per device license
- All networks have a Meraki MX
- An override of 4 vlans is made, to preserve the addressing the network had in the original organization.
- For this project, a maximum of 3 devices per network is considered (1 MS, 1MR, 1MX), this can be modified if necessary.
- For my project this combinations of devices are allowed
  - 1 MX
  - 1 MX + 1 MS
  - 1 MX + 1 MS + 1 MR

How it works.

The script will ask you to type the tag or tags (separated by a space) that will be used to filter the networks you want 
to move to a second organization.
The script generate a CSV file (inventory.csv), In the CSV is stored all the information needed to move the network 
to the target organization.
The script load the inventory.CSV file to get the information of the source networks and start the move.
The script will ask you which is the destination template, to which the created network must be added.
You are all set, the network and devices are now in the target organization :)

Enjoy! 
