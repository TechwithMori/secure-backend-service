import pkg_resources

# Function to check if a package is installed
def check_package(package, version):
    try:
        dist = pkg_resources.get_distribution(package)
        installed_version = dist.version
        if installed_version == version:
            return f"{package}=={version} is installed."
        else:
            return f"{package}=={version} is not installed. Installed version: {installed_version}"
    except pkg_resources.DistributionNotFound:
        return f"{package}=={version} is not installed."

# Read the requirements.txt file
with open('requirements.txt') as f:
    dependencies = f.readlines()

# Check each dependency
results = [check_package(*dep.strip().split('==')) for dep in dependencies]

# Print the results
for result in results:
    print(result)
