# Github check

import sys
import subprocess

lang = sys.argv[1]


dummy_main = """class Main {
    main() {
        return 0;
    }
}

module.exports = Main;
"""

dummy_test = """const Main = require("./index.js")
describe("Dummy stuff", () => {
    it("should work", () => {
        const main = new Main();
        expect(main.main()).toBe(0);
    });
});
"""

husky_commit_message= """#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no-install commitlint --edit "$1"
"""

def check_for_github_login():
    print("🤔 Checking github login...")
    login = subprocess.run("git config user.name",
                           capture_output=True, text=True)
    isLoggedIn = False
    if login.stdout:
        print("🐼 You are logged into Github")
        isLoggedIn = True
    else:
        print("🙀 You are NOT logged into Github.")
        sys.exit(1)
    return isLoggedIn


def check_for_github_client():
    print("🤔 Checking github...")
    isGithubInstalled = False
    try:
        gh = subprocess.run(["git"], capture_output=True)
        print("🐼 Github Client is installed")
        isGithubInstalled = True
    except:
        print("🙀 Github is not found on your computer")
        sys.exit(1)
    return isGithubInstalled


def make_cli_call(command_list):
    call = subprocess.run(command_list,shell=True, cwd="test",capture_output=True)


def create_file_with_content(file_name, content=""):
    with open("test/"+file_name, "w+") as f:
        f.write(content)


def create_node_project():
    print("🤔 Creating node project...")
    try:
        make_cli_call(["npm", "init", "--yes"])
        make_cli_call(["npm", "install", "husky"])
        make_cli_call(["npm", "install", "jest"])
        create_file_with_content("index.js", dummy_main)
        create_file_with_content("test.js", dummy_test)
        create_file_with_content("README.md")
        make_cli_call(["npx","husky","init"])
        make_cli_call(["mkdir","husky"])
        create_file_with_content("husky/commit-msg",husky_commit_message)
        make_cli_call(["npm", "install"])
        make_cli_call(["npx", "jest", "--coverage"])
        print("🐼 Node project successfully created!")
    except:
        print("🙀 Node project could not be created!")
        sys.exit(1)


def push_to_git():
    try:
        print("🤔 Pushing to git...")
        repository = input("Please enter the git repository:")
        make_cli_call(["git","init"])
        make_cli_call(["git","fetch"])
        make_cli_call(["git","add","."])
        make_cli_call(["git","commit","-m","initialise"])
        make_cli_call(["git","remote","add","origin",repository])
        make_cli_call(["git","fetch"])
        make_cli_call(["git","push","-u","origin","master"])
    except:
        print("🙀 Git push was not successful")
        sys.exit(1)

if __name__ == "__main__":
    print(f"👋 Welcome to the {lang.upper()} kata repository jumpstart...")
    print("--------------------------------------")
    check_for_github_client()
    check_for_github_login()
    if lang.upper() == "NODE":
        create_node_project()
    push_to_git()
