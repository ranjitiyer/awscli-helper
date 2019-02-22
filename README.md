# awscli-helper

Show AWS CLI usage and examples on the terminal. This does not eliminate the need to lookup aws cli documentation on the web but might minimize the number of times you need to leave the terminal and navigate web links in order to find an example or synopsis for a command you want to construct. This context switch has a huge cost and hopefully this tool minimizes it.

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
Show S3 `cp` usage
```
./awscli-usage.sh s3 cp usage
```
Show S3 `cp` examples
```
./awscli-usage.sh s3 cp examples
```
![awscli-usage](https://user-images.githubusercontent.com/529036/53047970-78c55a00-3448-11e9-980d-c2d5ea873dc5.gif)

# How does it work

A Python script scrapes AWS CLI html pages, reads off description, synopsis and examples and copies them to files under a folder structure that looks like this 
```
./db/<service>/commands                       # supported commands
./db/<service>/<command>/<command>.desc       # command description
./db/<service>/<command>/<command>.syn        # command synopsis
./db/<service>/<command>/<command>.examples   # command examples
```

The bash script acts as the front end to the tool.

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

If there are transient failures like connection issues, re-run the download script. It keeps a history file so it won't process commands already completed. If you do actually want a full recreation of the database, delete the `.history` file in the parent folder before running the script.

# Limitations
* Script and db must be in the same folder because an installer doesn't exist yet.

# Improvements
* Installer
* Colored printing of code snippets
* Command to list AWS services
