# droplet-cloudflare-updatefw
This is a tool to retrieve a list of origin network IP CIDR blocks (netblocks) from Cloudflare and then use DigitalOcean's API to update the firewall for one or more droplets.

## How It Works
This script pulls down a list of netblocks from Cloudflare, checks it against the last list that was downloaded (if one exists yet), and if there have been changes it will create or replace a firewall that is associated with droplets, tagged as 'webserver', that it can find using the API access key.

The trick here to preserving your other firewall access settings is to have another firewall associated with the droplet(s) that has your more permanent access rules in it.

When this script is functioning properly for you, remove your HTTP/HTTPS access rules from your permanent firewall and let this script update access so that only Cloudflare's IPs can reach your webserver directly.

## Installing
This could run in any user account. First, clone the repository:
```console
git clone https://github.com/erickmetz/droplet-cloudflare-updatefw.git
```

Next install the requirements:
```console
cd droplet-cloudflare-updatefw
pip install -r requirements.txt
```

Make the script executable, make a home for the script, and copy it over:
```console
chmod +x droplet-cloudflare-updatefw.py
mkdir ~/scripts
cp droplet-cloudflare-updatefw.py ~/scripts
```

Edit the code with your favorite editor similar to this:
```console
vim ~/scripts/droplet-cloudflare-updatefw.py
```

And replace this constant's string value with your DigitalOcean API token, replacing *DIGITALOCEAN_API_TOKEN_GOES_HERE*:
```python
DIGO_TOKEN = 'DIGITALOCEAN_API_TOKEN_GOES_HERE'

```

Take it for a spin:
```console
~/scripts/droplet-cloudflare-updatefw.py
```

You should notice a new firewall set up on the DigitalOcean web management console under the Networking -> Firewalls page, called "cloudflare", that is associated with your droplet(s)

## Automating
You could make a cronjob to run this at a regular interval.

To do this you would run:
```console
crontab -e
```

Add this to the file, staying mindful of what your actual path to the script is and changing the entry and the timezone configuration of the server that will be running this script. This example checks for netblock changes daily at 1-2am pacific time, or 9am UTC:
```
0 9 * * * /home/user/scripts/droplet-cloudflare-updatefw.py > /dev/null 2>&1

```

### Requirements
* DigitalOcean API token - [Here's how to Create a Token](https://docs.digitalocean.com/reference/api/create-personal-access-token/)
* Python 3
* The python3-pip package

### Note
This is now set up to only find droplets that have are tagged as the string constance DIGO_TAG, which defaults to 'webserver'. In order to include your droplet in this processing, you must enter your droplet in the web console and hit Tags -> Manage Tags and add a string that is consistent with the DIGO_TAG constant for your droplet to be associated with the firewall changes.

### The Future
* This same functionality could be reproduced for AWS, GCP, Azure, and other APIs. Perhaps this will evolve into a multicloud tool for this at some point.
