# droplet-cloudflare-updatefw
This is a tool to retrieve a list of origin network IP CIDR blocks (netblocks) from Cloudflare and then use DigitalOcean's API to update the firewall for one or more droplets.

## How It Works
This script pulls down a list of netblocks from Cloudflare, checks it against the last list that was downloaded (if one exists yet), and if there have been changes it will create or replace a firewall that is associated with any droplets that it can find using the API access key.

The trick here to preserving your other firewall access settings is to have another firewall associated with the droplet(s) that has your more permanent access rules in it.

When this script is functioning properly for you, remove your HTTP/HTTPS access rules from your permanent firewall and let this script update access so that only Cloudflare's IPs can reach your webserver directly.

## Installing
This could run in any user account. First, clone the repository:
```
git clone https://github.com/erickmetz/droplet-cloudflare-updatefw.git
```

Next install the requirements:
```
cd droplet-cloudflare-updatefw
pip install -r requirements.txt
```

Make the script executable, make a home for the script, and copy it over:
```
chmod +x droplet-cloudflare-updatefw.py
mkdir ~/scripts
cp droplet-cloudflare-updatefw.py ~/scripts
```

Edit the code with your favorite editor similar to this:
```
vim ~/scripts/droplet-cloudflare-updatefw.py
```

And replace this constant's string value with your DigitalOcean API token, replacing *DIGITALOCEAN_API_TOKEN_GOES_HERE*:
```
DIGO_TOKEN = 'DIGITALOCEAN_API_TOKEN_GOES_HERE'

```

Take it for a spin:
```
~/scripts/droplet-cloudflare-updatefw.py
```

You should notice a new firewall set up on the DigitalOcean web management console under the Networking -> Firewalls page, called "cloudflare", that is associated with your droplet(s)

## Automating
You could make a cronjob to run this at a regular interval.

To do this you would run:
```
crontab -e

```

Add this to the file, staying mindful of what your actual path to the script is and changing the entry, accordingly. This example checks for netblock changes daily at 1-2am pacific time, or 9am UTC:
```
0 9 * * * /home/user/scripts/droplet-cloudflare-updatefw.py > /dev/null 2>&1

```

### Requirements
* DigitalOcean API token - [Here's how to Create a Token](https://docs.digitalocean.com/reference/api/create-personal-access-token/)
* Python 3
* The python3-pip package

### Caution
As it's presently written, this will associate *every single droplet* that it can discover through API requests with the firewall that it generates. Utilizing droplet tags and some minor changes in the future will allow more granular targetting of droplets.

### The Future
* The ability to get droplets only with a specific tag
* This same functionality could be reproduced for AWS, GCP, Azure, and other APIs. Perhaps this will evolve into a multicloud tool for this at some point.
