# COMMON
CLI_UNEXPECTED_ERROR = "Unexpected error while executing command. details: {0}"
OUTPUT_DIR_LOCATION = "the location of the output directory"

# LOGIN
LOGIN_PROMPT_DOMAIN = "Please enter your cnvrg domain"
LOGIN_PROMPT_EMAIL = "Please enter your email"
LOGIN_PROMPT_PASSWORD = "Please enter your password"
LOGIN_HELP_AUTH_TOKEN = "Enter authentication token instead of password"
LOGIN_ORGANIZATION_HELP = "Organization to log in to"
LOGIN_ALREADY_LOGGED_IN = "Seems you\'re already logged in"
LOGIN_SUCCESS = "Successfully logged in as {0}"
LOGIN_INVALID_CREDENTIALS = "Invalid credentials"

# LOGOUT
LOGOUT_SUCCESS = "Logged out successfully"
LOGOUT_CONFIG_MISSING = "Cannot logout. Config file is missing. Try logging in first"

# ME
ME_SUCCESS_API = "API: {0}/api/v2"
ME_SUCCESS_LOGS = "Logs file located at: {0}"
ME_SUCCESS = "Logged in as: {0}"
ME_LOGGER_SUCCESS = "Successfully printed user's details (cnvrgv2 me)"

# DATA OWNER
DATA_UPLOAD_SUCCESS = "Successfully uploaded updated files"
DATA_DOWNLOAD_SUCCESS = "Successfully downloaded updated files"
DATA_COMMIT_MESSAGE = "Commit message"
DATA_UPLOAD_HELP_GIT_DIFF = "From the list of files, upload those who returned from git diff command."
DATA_UPLOAD_HELP_FORCE = "Enable to create an empty commit without files from parent commit."
DATA_UPLOAD_HELP_OVERRIDE = "Enable to re-upload even if the file already exists."
DATA_PROMPT_COMMIT = "Please enter sha1 to clone"
DATA_PROMPT_CACHE = "Please enter sha1 to cache"
DATA_DOWNLOAD_ERROR = "Unexpected error while executing command"
SYNC_OUTPUT_DIR = "The directory that will be synced inside the project"
CLONE_NUMBER_OF_THREADS = "Number of threads that will be used to preform the clone"
QUERY_SLUG = "Query slug"

# DATASET
DATASET_PROMPT_CLONE = "Please enter dataset name to clone"
DATASET_HELP_CLONE = "Name of the dataset to clone"
DATASET_HELP_CACHE = "Name of the dataset to cache"
DATASET_HELP_UNCACHE = "Name of the dataset to uncache"
DATASET_HELP_CLONE_OVERRIDE = "Whether or not re-clone in case the dataset already cloned"
DATASET_HELP_CLONE_COMMIT = "The commit sha1 to clone"
DATASET_CLONE_SKIP = "Dataset {0} is already cloned, therefore skip clone." \
                     " If you want to override, run again using -o flag."
DATASET_PROMPT_NAME = "Please enter dataset name"
DATASET_PROMPT_DISK_NAME = "Please enter disk name"
DATASET_HELP_NAME = "Name of the dataset"
DATASET_CLONE_SUCCESS = "Successfully cloned dataset: {0}"
DATASET_PUT_PROMPT_FILES = "Please enter a comma separated list of file paths to upload. use . " \
                           "to upload the whole directory"
DATASET_PUT_HELP_FILES = "A comma separated list of file paths to upload. use . " \
                         "to upload the whole directory"
DATASET_REMOVE_PROMPT_FILES = "Please enter a comma separated list of file paths to remove. Wildcards allowed"
DATASET_REMOVE_HELP_FILES = "A comma separated list of file paths to remove. use Wildcards allowed"
DATASET_REMOVE_SUCCESS = "Files removed successfully"
DATASET_PROMPT_DELETE = "Please enter dataset name to delete"
DATASET_HELP_DELETE = "Name of the dataset to delete"
DATASET_DELETE_CONFIRM = "Are you sure you want to delete dataset: {0}?"
DATASET_DELETE_SUCCESS = "Successfully deleted dataset: {0}"
DATASET_SYNC_SUCCESS = "Successfully synced dataset {0}"
DATASET_PROMPT_CREATE = "Please enter dateset name to create"
DATASET_HELP_CREATE = "Name for the new dataset"
DATASET_CREATE_FOLDER_NOT_EMPTY = "Warning! You're about to associate a non empty folder with the new dataset." \
                                  "\r\nContinue?"
DATASET_CREATING_MESSAGE = "Creating new dataset {0}"
DATASET_CONFIGURING_FOLDER = "Configuring dataset folder"
DATASET_CREATE_SUCCESS = "Successfully created dataset {0}"
DATASET_SCAN_START = "Scanning datasets"
DATASET_SCAN_NO_RESULTS = "No datasets found in working dir"
DATASET_VERIFY_STATUS = "Success: {0}"
DATASET_UNCACHE_SUCCESS = "Dataset successfully uncached"
DATASET_CACHE_SUCCESS = "Dataset successfully cached"
DATASET_NAMES = "Dataset names"
DATASET_NAMES_HELP = "Dataset names to verify"
DATASET_VERIFY_TIMEOUT = "Timeout"

# PROJECT
PROJECT_PROMPT_CLONE = "Please enter project name to clone"
PROJECT_HELP_CLONE = "Name of the project to clone"
PROJECT_PROMPT_DELETE = "Please enter project name to delete"
PROJECT_HELP_DELETE = "Name of the project to delete"
PROJECT_HELP_CLONE_OVERRIDE = "Whether or not re-clone in case the project already cloned"
PROJECT_HELP_CLONE_COMMIT = "The commit sha1 to clone"
PROJECT_CLONE_SKIP = "Project {0} is already cloned, therefore skip clone." \
                     " If you want to override, run again using -o flag."
PROJECT_CLONE_SUCCESS = "Successfully cloned project: {0}"
PROJECT_DELETE_SUCCESS = "Successfully deleted project: {0}"
PROJECT_DELETE_CONFIRM = "Are you sure you want to delete project: {0}?"
PROJECT_DOWNLOAD_SUCCESS = "Successfully downloaded updated files"
PROJECT_LINK_PROMPT_NAME = "Please enter a name for the new project"
PROJECT_LINK_HELP_NAME = "Name for the new project"
PROJECT_PROMPT_NAME = "Please enter project name"
PROJECT_HELP_NAME = "Name of the project"
PROJECT_LINK_GIT_PROMPT_NAME = "Please enter the name of the git project"
PROJECT_LINK_GIT_HELP_NAME = "Name of the git project"
SOFT_LINK_GIT_PROJECT = "Link the git project, if it hasn't done before"
PROJECT_GIT_LINK_SKIP = "Project {0} is already linked, therefore skip linking"
PROJECT_JOB_SLUG_HELP_NAME = "Slug of the job"
PROJECT_LINK_SUCCESS = "Finished linking project {0} successfully."
PROJECT_CREATE_NEW = "Creating new project {0}"
PROJECT_CONFIGURING_FOLDER = "Configuring project folder"
PROJECT_UPLOAD = "Uploading project files"
PROJECT_PROMPT_CREATE = "Please enter project name to create"
PROJECT_HELP_CREATE = "Name for the new project"
PROJECT_CREATE_FOLDER_NOT_EMPTY = "Warning! You're about to associate a non empty folder with the new project." \
                                  "\r\nContinue?"
PROJECT_CREATING_PROJECT = "Creating new project {0}"
PROJECT_CREATE_SUCCESS = "Successfully created project {0}"
PROJECT_SYNC_SUCCESS = "Successfully synced project {0}"

# FILES
FILES_UPLOAD_SUCCESS = "Successfully uploaded files"
COMMIT_SHA1_MESSAGE = "Commit sha1: {0}"

# LIBRARIES
LIBRARY_PROMPT_CLONE = "Please enter library name to clone"
LIBRARY_VERSION_PROMPT_CLONE = "Please enter library version name to clone (default = \"latest\")"
LIBRARY_CLONE_SKIP = "Library {0} is already cloned, skipping action"
LIBRARY_CLONE_SUCCESS = "Successfully cloned library: {0}"

# MEMBERS
MEMBER_ADDED_SUCCESS = "{0} was added successfully with role {1}"
MEMBER_UPDATED_SUCCESS = "{0} was updated successfully to role {1}"
MEMBER_ENTER_EMAIL = "Please enter a valid user email"
MEMBER_HELP_EMAIL = "A valid email of exists user"
MEMBER_ENTER_ROLE = "Please enter a valid role [admin, manager, member, reviewer]"
MEMBER_HELP_ROLE = "A role for the user, must be one of the following: admin, manager, member, reviewer"
MEMBER_REMOVED_SUCCESS = "{0} was removed successfully"

# EXPERIMENT
EXPERIMENT_PROMPT_TITLE = "Please enter a title for the experiment"
EXPERIMENT_PROMPT_COMMIT = "Please enter commit to merge"
EXPERIMENT_ARTIFACTS_PROMPT_COMMIT = "Please enter commit"
EXPERIMENT_HELP_COMMIT = "Commit sha1 to merge"
EXPERIMENT_ARTIFACTS_HELP_COMMIT = "Commit sha1 of artifacts"
EXPERIMENT_HELP_TITLE = "Name of the experiment"
EXPERIMENT_HELP_TEMPLATES = "Comma separated list of template names"
EXPERIMENT_HELP_LOCAL = "Boolean. Run the experiment locally"
EXPERIMENT_PROMPT_COMMAND = "Please enter a command to run as experiment"
EXPERIMENT_HELP_COMMAND = "The command to run"
EXPERIMENT_HELP_DATASETS = "list of comma separated datasets names to use in the experiment"
EXPERIMENT_HELP_VOLUME = "A volume name to attach to this experiment"
EXPERIMENT_HELP_SYNC_BEFORE = "Boolean. Sync environment before running the experiment"
EXPERIMENT_HELP_SYNC_AFTER = "Boolean. sync environment after the experiment finished"
EXPERIMENT_HELP_IMAGE = "Image name and tag to create experiment with. format - image_name:tag"
EXPERIMENT_HELP_GIT_BRANCH = "The branch to pull files from for the experiment, in case project is git project"
EXPERIMENT_HELP_GIT_COMMIT = "The commit to pull files from for the experiment, in case project is git project"
EXPERIMENT_CREATE_SUCCESS = "Experiment {0} created successfully. \r\nExperiment is available at: {1}"
EXPERIMENT_MERGE_SUCCESS = "Commit successfully merged to master"
EXPERIMENT_GIT_ERROR_MESSAGE = "Cannot merge commits for git projects"
EXPERIMENT_DOES_NOT_EXIST = "Couldn't find experiment. Try with env variables or passing --slug"
EXPERIMENT_LOG_ARTIFACTS_SUCCESS = "Successfully logged artifacts"
EXPERIMENT_LOG_IMAGES_SUCCESS = "Successfully logged images"
EXPERIMENT_PULL_ARTIFACTS_SUCCESS = "Successfully pulled artifacts"
EXPERIMENT_HELP_WORK_DIR = "Working Dir to upload files to"

# LOGS
LOG_START_COMMAND = "Starting command {0}. Options: {1}"
LOG_CLONING_PROJECT = "Cloning project: {0}"
LOG_CLONING_LIBRARY = "Cloning library: {0}=={1}"
LOG_CLONING_DATASET = "Cloning dataset: {0}"

# SSH
SSH_HELP_PORT = "Port to bind on host"
SSH_HELP_USERNAME = "Username to login in container, default will be image default user"
SSH_HELP_PASSWORD = "Password for login"
SSH_HELP_KUBECTL = "Full path to kubeconfig file, otherwise default will be used"
SSH_STARTING_SESSION = "Starting a new ssh session"
SSH_WAITING_FOR_READY = "Waiting for ssh session to be ready..."
SSH_READY = "\r\nSsh session is ready to receive connections.\r\n" \
            "\r\nIn order to connect to your job, define your ssh connection with the following params:\r\n" \
            "host: 127.0.0.1\r\n" \
            "port: {0}\r\n" \
            "username: {1}\r\n" \
            "password: {2}"

# WORKSPACE
WORKSPACE_DOES_NOT_EXIST = "Workspace was not found, check env or pass slug"
WORKSPACE_SLUG = "Slug of the workspace"

# ENDPOINT
Endpoint_DOES_NOT_EXIST = "Endpoint was not found, check env or pass slug"
ENDPOINT_SLUG = "Slug of the endpoint"
ENDPOINT_PROMPT_METRIC_NAME = "Please enter the metric name"
ENDPOINT_PROMPT_METRIC_X = "Please enter the metric x value"
ENDPOINT_PROMPT_METRIC_Y = "Please enter the metric y value"
ENDPOINT_METRIC_NAME = "The metric name"
ENDPOINT_METRIC_X = "The metric x value"
ENDPOINT_METRIC_Y = "The metric y value"

# FLOWS
FLOW_YAML_PATH = "Path to yaml file, describing the new flow"
FLOW_CREATE_SUCCESS = "Flow {0} created successfully."

# CONFIG
CONFIG_HELP_CHECK_CERTIFICATE = "{0} ssl validation on https requests"
CONFIG_UPDATE_SUCCESS = "Config updated successfully"
CONFIG_HELP_ORGANIZTION = "Name of organization to switch to"
CONFIG_NO_ARGS_LOG = "No arguments sent. Showing help message instead"

# IMAGE
IMAGE_HELP_TAG = "Image tag"
IMAGE_HELP_SLUG = "Image slug"
IMAGE_HELP_NAME = "Image repository name"
IMAGE_HELP_LOGO = "Image logo"
IMAGE_HELP_CUSTOM = "Is custom image (requires dockerfile)"
IMAGE_HELP_README = "Readme path for the image"
IMAGE_HELP_REGISTRY = "Image registry"
IMAGE_HELP_DOCKERFILE = "Dockerfile path to build a custom image"

IMAGE_PROMPT_TAG = "Please enter image tag"
IMAGE_PROMPT_SLUG = "Please enter image slug"
IMAGE_PROMPT_NAME = "Please enter image name (repository)"
IMAGE_PROMPT_LOGO = "Please enter image logo"
IMAGE_PROMPT_REGISTRY = "Please enter image registry"

IMAGE_INVALID_README = "Readme path is invalid"
IMAGE_INVALID_DOCKERFILE = "Dockerfile path is invalid"

IMAGE_CREATE_SUCCESS = "Successfully created image {0}"

# REGISTRY
REGISTRY_HELP_URL = "Registry url"
REGISTRY_HELP_TYPE = "Registry type (cnvrg, dockerhub, gcr, acr, ecr, ...)"
REGISTRY_HELP_SLUG = "Registry slug"
REGISTRY_HELP_TITLE = "Registry title"
REGISTRY_HELP_USERNAME = "Registry username for private registries"
REGISTRY_HELP_PASSWORD = "Registry password for private registries"

REGISTRY_PROMPT_URL = "Please enter registry url"
REGISTRY_PROMPT_TITLE = "Please enter registry tag"

REGISTRY_CREATE_SUCCESS = "Successfully created registry {0}"

# ORGANIZATION SETTINGS
ORGANIZATION_SETTINGS_HELP_DEFAULT_COMPUTES = "Default computes"
ORGANIZATION_SETTINGS_HELP_INSTALL_DEPENDENCIES = "Install dependencies"
ORGANIZATION_SETTINGS_HELP_SLACK_WEBHOOK_URL = "Slack webhook URL"
ORGANIZATION_SETTINGS_HELP_DEBUG_TIME = "Debug time"
ORGANIZATION_SETTINGS_HELP_EMAIL_ON_ERROR = "Send email on error"
ORGANIZATION_SETTINGS_HELP_EMAIL_ON_SUCCESS = "Send email on success"
ORGANIZATION_SETTINGS_HELP_QUEUED_COMPUTE_WAIT_TIME = "Queued compute wait time"
ORGANIZATION_SETTINGS_HELP_IDLE_ENABLED = "Enable or Disable idle time"
ORGANIZATION_SETTINGS_HELP_IDLE_TIME = "Idle time"
ORGANIZATION_SETTINGS_HELP_MAX_DURATION_WORKSPACES = "Max duration for workspaces"
ORGANIZATION_SETTINGS_HELP_MAX_DURATION_EXPERIMENTS = "Max duration for experiments"
ORGANIZATION_SETTINGS_HELP_MAX_DURATION_ENDPOINTS = "Max duration for endpoints"
ORGANIZATION_SETTINGS_HELP_MAX_DURATION_WEBAPPS = "Max duration for webapps"
ORGANIZATION_SETTINGS_HELP_AUTOMATICALLY_CLEAR_CACHED_COMMITS = "Number of cached commits to be cleared" \
                                                                " automatically"
ORGANIZATION_SETTINGS_HELP_CUSTOM_PYPI_ENABLED = "Enable custom PYPI"
ORGANIZATION_SETTINGS_HELP_CUSTOM_PYPI_URL = "Custom PYPI URL"
