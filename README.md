# droplet-cloudflare-updatefw
Tool to retrieve a list of origin network IP CIDR blocks (netblocks) from Cloudflare and then use DigitalOcean's API to update the firewall for one or more droplets.

## How It Works
This python script pulls down a list of netblocks from Cloudflare, checks it against the last list that was downloaded (if one exists yet), and if there have been changes it will create or replace a firewall that is associated with any droplets that it can find using the API access key.

The trick here to preserving your other firewall access settings is to have another firewall associated with the droplet(s) that has your more permanent access rules in it.

When this script is functioning properly for you, remove your HTTP/HTTPS access rules from your permanent firewall and let this script update access so that only Cloudflare's IPs can reach your webserver.

## Installing
This could run in any user account. In this case we'll say there's a generic "user" account. In this example we'll use /home/user/scripts/.

First, clone the repository:
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

And replace this constant's string value with your DigitalOcean API token
```
DIGO_TOKEN = '___your digitalocean token goes here___'

```

Take it for a spin:
```
~/scripts/droplet-cloudflare-updatefw.py
```

You should notice a new firewall set up on DigitalOcean called "cloudflare" that is associated with your droplets

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

### The Future
This same functionality could be reproduced for AWS, GCP, Azure, and other APIs. Perhaps there will a multicloud tool for this at some point.
