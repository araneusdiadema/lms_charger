import subprocess
import re
import sys

def get_latest_tag():
    try:
        return subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], 
                                       stderr=subprocess.DEVNULL).decode().strip()
    except subprocess.CalledProcessError:
        return 'v0.0.0'  # Default if no tag exists

def increment_version(version, increment='patch'):
    match = re.match(r'v?(\d+)\.(\d+)\.(\d+)(-[\w\.]+)?(\+[\w\.]+)?', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    
    major, minor, patch, prerelease, buildmetadata = match.groups()
    major, minor, patch = map(int, (major, minor, patch))
    
    if increment == 'major':
        major += 1
        minor = patch = 0
    elif increment == 'minor':
        minor += 1
        patch = 0
    elif increment == 'patch':
        patch += 1
    elif increment == 'none':
        return None
    else:
        raise ValueError(f"Invalid increment: {increment}")
    
    new_version = f'v{major}.{minor}.{patch}'

    if prerelease:
        new_version += prerelease
    if buildmetadata:
        new_version += buildmetadata
    
    return new_version

def get_commit_messages(since_tag):
    return subprocess.check_output(['git', 'log', f'{since_tag}..HEAD', '--pretty=format:%s']).decode().split('\n')

def determine_version_increment(commit_messages):
    for msg in commit_messages:
        if re.search(r'\bBREAKING[ -]CHANGE\b', msg, re.IGNORECASE):
            return 'major'
        if msg.startswith('feat'):
            return 'minor'
        if msg.startswith('fix'):
            return 'patch'
    return 'none'

def create_tag(tag):
    if tag is None:
        return
    else:
        # Get the current commit message
        commit_message = subprocess.check_output(['git', 'log', '-1', '--pretty=%B', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()

        # Create a new annotated tag with the commit message
        subprocess.run(['git', 'tag', '-a', tag, '-m', commit_message, 'HEAD'], check=True)
        
        print(f"Created new tag: {tag}")

if __name__ == "__main__":
    latest_tag = get_latest_tag()
    commit_messages = get_commit_messages(latest_tag)
    increment = determine_version_increment(commit_messages)
    new_tag = increment_version(latest_tag, increment)
    create_tag(new_tag)