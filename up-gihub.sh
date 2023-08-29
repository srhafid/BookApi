#!/bin/bash

# Check if the required arguments are provided
if [ $# -ne 3 ]; then
    echo "Usage: $0 <user_email> <user_name> <repository_url>"
    exit 1
fi

# Assign the arguments to variables
user_email=$1
user_name=$2
repository_url=$3

# Configure user information for Git
git config user.email "$user_email"
git config user.name "$user_name"

# Create a README.md file and add content
echo "# BookApi" > README.md

# Initialize a Git repository
git init

# Add the README.md file to the staging area
git add README.md

# Make the first commit
git commit -m "first commit"

# Switch to the "main" branch (adjust based on your configuration)
git branch -M main

# Add a remote repository named "origin" with the provided GitHub repository URL
git remote add origin "$repository_url"

# Push the changes to the remote repository on the "main" branch and set tracking
git push -u origin main