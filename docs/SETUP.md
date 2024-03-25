# How to deploy this for yourself

I recommend a dedicated Debian vitrual machine.

# first, change the prompt
```sh
echo 'export PS1="\n\[\e[1;35m\](\[\e[1;31m\]\u\[\e[1;35m\]@\[\e[1;34m\]\h\[\e[1;35m\]) [\w]\n\[\e[1;36m\]\$ \[\e[0m\]"' >> ~/.bashrc
source .bashrc
```

## `apt-update` and install prerequesties
```sh
apt-get update
apt-get upgrade -y

apt-get install -y git curl python3-venv python3-pip
```

## update time zone
```sh
dpkg-reconfigure tzdata
```

## install MongoDB
```sh
# https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-debian/
apt-get install gnupg curl

curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/debian bookworm/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

apt-get update

apt-get install -y mongodb-org

echo "mongodb-org hold" | dpkg --set-selections
echo "mongodb-org-database hold" | dpkg --set-selections
echo "mongodb-org-server hold" | dpkg --set-selections
echo "mongodb-mongosh hold" | dpkg --set-selections
echo "mongodb-org-mongos hold" | dpkg --set-selections
echo "mongodb-org-tools hold" | dpkg --set-selections


systemctl start mongod
systemctl status mongod

systemctl enable mongod

# test it out
mongosh
```





## Create a non-`root` user

```sh
adduser satoshi
usermod -aG sudo satoshi
```

Then, log out of `root` and log in as this user

```sh
# signal that we are non-root
echo 'export PS1="\n\[\e[1;35m\](\[\e[1;31m\]\u\[\e[1;35m\]@\[\e[1;34m\]\h\[\e[1;35m\]) [\w] \[\e[33;3m\]\A\[\e[0m\] \[\e[1;36m\]\$ \[\e[0m\]\n"' >> ~/.bashrc
source .bashrc
```

## clone the repo

```sh
git clone https://github.com/PlebeiusGaragicus/NOS4A2.git
cd NOS4A2
```

## configure the Python virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## create user accounts for the application

... the easy way!!! ;)
```sh
sh generate_auth_yaml.sh
```

## create the `.env` file with API keys

```sh
cat << EOF > .env
NWC="_node_wallet_connect_uri_goes_here_"
EOF

nano .env
```

## setup a `systemd` service to launch the application

Note: This will need `root` access.  Log in as `root` for these next steps.


```sh
cat << EOF > /etc/systemd/system/NOS4A2.service
[Unit]
Description=nos4a2 Service
After=network.target

[Service]
User=satoshi
WorkingDirectory=/home/satoshi/NOS4A2
ExecStart=/bin/bash -c "/home/satoshi/NOS4A2/production"
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

nano /etc/systemd/system/NOS4A2.service
```

Also, replace `satoshi` with the non-root Linux username that you created earlier.

## start the service and monitor for errors

```sh
systemctl start NOS4A2
systemctl status NOS4A2

# works..?  If so:
systemctl enable NOS4A2

# watch it run via:
journalctl -u NOS4A2 -f # hitting 'q' will exit
```

## Visit the application

Open a browser and go to the IP address of the server at port 8501. To determine the ip address, run the `ip addr` command.

For example, if your ip address is `192.169.10.200`, then put `192.169.10.200:8501` in your browser and it should work.

If you're running this locally instead of on a dedicated server then visit [localhost:8501](http://localhost:8501)
