import boto3
from datetime import datetime, timezone

# Configurations
region_name = "<your region name>"
domain_id = "<your domain id here>"
days_threshold = <how many days>  # Change to the desired number of days , ex days_threshold = 2

# Initialize the boto3 client
sagemaker = boto3.client('sagemaker', region_name=region_name)

# Gets the current date
current_time = datetime.now(timezone.utc)

# List all user profiles
user_profiles = sagemaker.list_user_profiles(DomainIdEquals=domain_id)

# Iterates over each user profile
for user_profile in user_profiles['UserProfiles']:
    user_profile_name = user_profile['UserProfileName']
    
    # List all apps in the user profile
    app_list = sagemaker.list_apps(DomainIdEquals=domain_id, UserProfileNameEquals=user_profile_name)
    
    for app in app_list['Apps']:
        if app['AppType'] == 'KernelGateway':
            app_name = app['AppName']
            creation_time = app['CreationTime']
            
            # Calculates the difference in days
            diff_days = (current_time - creation_time).days
            
            # Checks if the Kernel Gateway was created more than X days ago
            if diff_days > days_threshold:
                print(f"User Profile: {user_profile_name}, Kernel Gateway: {app_name} - Created {diff_days} days ago. Will be deleted.")
                
                # Delete the Kernel Gateway
                print(f"Deleting Kernel Gateway: {app_name} from User Profile: {user_profile_name}")
                sagemaker.delete_app(DomainId=domain_id, UserProfileName=user_profile_name, AppType='KernelGateway', AppName=app_name)