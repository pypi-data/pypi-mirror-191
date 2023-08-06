import subprocess

def KAURG():
    # Get the list of all installed packages
    installed_packages = subprocess.check_output("pip list", shell=True).decode().split("\r\n")

    # Get the list of all outdated packages
    outdated_packages = subprocess.check_output("pip list --outdated", shell=True).decode().split("\r\n")

    # Initialize the list of updated packages
    updated_packages = []

    # Initialize the list of non-updated packages
    not_updated_packages = []

    # Iterate over the list of outdated packages
    for package in outdated_packages:
        if package:
            package_name = package.split(" ")[0]
            # Skip the package if it is already updated
            if package_name not in installed_packages:
                continue
            # Update the package
            subprocess.call(f"pip install --upgrade {package_name}", shell=True)
            # Add the package to the list of updated packages
            updated_packages.append(package_name)
        else:
            not_updated_packages.append(package_name)

    # Print the lists of updated and non-updated packages
    print("Updated packages:")
    for package in updated_packages:
        print(package)

    print("\nNot updated packages:")
    for package in not_updated_packages:
        print(package)

    return

exit()