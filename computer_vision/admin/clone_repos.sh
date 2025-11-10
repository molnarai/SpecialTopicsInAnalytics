#!/bin/bash

while IFS=',' read -r orgid username displayname gitrepo; do
    # Skip header line
    [[ "$username" == "Username" ]] && continue
    
    # Remove # from username
    clean_username=${username#\#}
    
    # Create folder
    mkdir -p "$clean_username"
    
    # Clone repo if not exists
    if [ ! -d "$clean_username/.git" ]; then
        git clone "$gitrepo" "$clean_username"
    fi
done