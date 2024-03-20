#!/bin/bash

# if auth.yaml exists, warn user and exit
if [ -f auth.yaml ]; then
  echo "auth.yaml already exists. Please remove it before running this script."
  exit 1
fi

# ask for a username
echo "Enter your username:"
read username

# ask for a password
echo "Enter your password:"
read -s password

# python3.11 -c "import streamlit_authenticator as stauth; print(stauth.Hasher(['$password']).generate()[0])"
# import streamlit_authenticator as stauth
# print(stauth.Hasher([input("Enter password: ")]).generate()[0])
hashed_psk=$(python3.11 -c "import streamlit_authenticator as stauth; print(stauth.Hasher(['$password']).generate()[0])")

cat << EOF > auth.yaml
credentials:
  usernames:
    $username:
      email: $username@plebby.me
      name: $username
      password: $hashed_psk
cookie:
  expiry_days: 7
  key: nos4a2_auth_widget_key
  name: nos4a2_auth
preauthorized:
  emails:
    - $username@plebby.me
EOF