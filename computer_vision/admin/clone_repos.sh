#!/bin/bash

while IFS=',' read -r orgid username displayname gitrepo; do
    # Skip header line
    [[ "$username" == "Username" ]] && continue
    
    # Clean fields - remove whitespace, line breaks, carriage returns
    clean_username=$(echo "${username#\#}" | tr -d '\n\r\t ' )
    clean_gitrepo=$(echo "$gitrepo" | tr -d '\n\r\t ' )
    
    # Create folder
    mkdir -p "$clean_username"
    
    # Clone repo if not exists
    if [ ! -d "$clean_username/.git" ]; then
        echo "Cloning $clean_gitrepo into $clean_username"
        if ! git clone "$clean_gitrepo" "$clean_username" 2>/dev/null; then
            echo "ERROR: Failed to clone $clean_gitrepo for $clean_username"
            rmdir "$clean_username" 2>/dev/null
        fi
    else
        echo "Repository already exists for $clean_username"
    fi
done