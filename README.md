# awscli-helper

Show AWS CLI usage and examples on the terminal. This does not eliminate the need to lookup aws cli documentation on the web but might minimize the number of times you need to leave the terminal and navigate web links before finding an example or synopsis you are looking for. This context switch is expensive and hopefully this tool minimizes it.

## Quickstart

Clone the repo
```
git clone https://github.com/ranjitiyer/awscli-helper
```
Print help
```
./awscli-usage.sh help
```
List S3 commands
```
./awscli-usage.sh s3 commands
```
Show S3 `rm` usage
```
./awscli-usage.sh s3 rm usage
```
Show S3 `rm` examples
```
./awscli-usage.sh s3 rm examples
```
![awscli-usage](https://user-images.githubusercontent.com/529036/53047970-78c55a00-3448-11e9-980d-c2d5ea873dc5.gif)

# How does it work

A Python program scrapes all the AWS CLI html pages, reads off description, synopsis and examples text and copies them to the local file system. The bash script acts as the front end. 

# Generate the usage database locally

Delete the local usage database 
```
rm -rf db
```
Setup dev environment
```
virtualenv --no-setuptools --no-wheel --python=python3 .
source bin/activate
pip install -r requirements.txt
python src/download.py
```

If there are transient failures like connection issues, re-run the download script. It keeps a history file so it won't process commands already completed. If you do actually want a full recreation of the database, delete the `.history` file in the parent folder.

# Improvements
* Colored printing of code snippets
* Create a command to list AWS services
