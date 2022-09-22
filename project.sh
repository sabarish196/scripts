#! /bin/bash
####################################################################
# Script is used for automating the project creation process 
# Using this script we can create a project with quotas assigned 
# Author: Sabarish reddy       Email: sabarish.reddy@gmail.com
####################################################################

red="[ERROR] :"
green="[INFO] :"
yellow="[WARNING] :"
GLOBAL_LOG_DIR="/var/log/Ose_Custom/Log"
LOG_DIR=${GLOBAL_LOG_DIR}/`basename $0 | cut -d "." -f1`
LOG_FILE="${LOG_DIR}/log_file.log"
TIMESTAMP=`date +"%Y%m%d_%H%M%S"`
QUOTAS_CONF_DIR="/root/quotas/conf"
project_tokens_dir="/root/tokens"
projects_dir="/root/projects"
cc_list=""
cc1_list=""

function LOG {
        message=${*}
        echo "${message}" >> ${LOG_FILE}
        echo "${message}"
}

function ERROR {
        message=${*}
        echo "${message}" >> ${LOG_FILE}
        echo "${message}"
		exit
}

if [ ! -d ${LOG_DIR} ]
then
        LOG "${yellow} Directory ${LOG_DIR} doesn't exist, creating one "
        mkdir -p ${LOG_DIR}
        if [ $? -ne 0 ]
        then
                ERROR "${red} Directory ${LOG_DIR} creation failed, existing the script"

        else
                LOG "${green} Directory ${LOG_DIR} created sucessfully"
        fi
fi


function usage {
        echo "Usage : `basename $0`  -n <project_name>   -s <small,medium,large> -e <email> 
                                option n is mandatory, which expects projectname to be passed to the script.
				-d is to pass project Display_Name, this is optional. If no value is passed then project name is cosidered.
				-D is to pass project Description, this is optional , if no value is passed then project name is considerd.
                                option s is mandatory , which expects size of quota to immplement."
        exit 700
}


### This function checks for number of projects found with "Project Name"
function Check_For_Project {
	PROJECT="$1"
	Project_Count=`oc get project $PROJECT --no-headers| wc -l`
	echo ${Project_Count}
}



function switch_to_project {
  PROJECT=$1
  current_project=`oc project | grep -x "${PROJECT}" | wc -l`
  if [ "${current_project}"  -eq 0 ]
  then
    LOG "${red}  current projects is not ${PROJECT}, switching "
    /usr/bin/oc project ${PROJECT}
  else
    LOG "${green}  current project is  ${PROJECT}, procceding further"
fi
}


function MAIL {
        echo "`hostname` : `date +"%Y%m%d_%H%M%S"`: ${1}. ${2}" | mailx -r "From Address" -s "$1" -S smtp="SMTPserver:25" ${MAIL_ID}
}


function create_quota {
        PROJECT=$1
        SIZE=$2

        cp ${QUOTAS_CONF_DIR}/${SIZE}-quota-template.yaml  ${QUOTAS_CONF_DIR}/created_templates/${PROJECT}-quota.yaml || ERROR "${red} QUOTA Config file creation Failed !!!"
        cp ${QUOTAS_CONF_DIR}/${SIZE}-limits-template.yaml ${QUOTAS_CONF_DIR}/created_templates/${PROJECT}-limits.yaml || ERROR "${red} Limits Config file creation Failed !!!"



        if [ "`oc get quota -n ${PROJECT} |wc -l`" -eq "0" ]
        then
           oc create -f ${QUOTAS_CONF_DIR}/created_templates/${PROJECT}-quota.yaml
           if [ "`oc get quota -n ${PROJECT} | wc -l`" -eq "2" ]
           then
                   LOG "${green} Sunccessfully created quota for project ${PROJECT}"
           else
                   ERROR "${red} Failed to create quota for project ${PROJECT} "
           fi
        else
                   ERROR "${red} ${PROJECT} already has existing quotas and limits. exiting the script."
        fi



        if [ "`oc get limits -n ${PROJECT} | wc -l`" -eq "0" ]
        then
                oc create -f ${QUOTAS_CONF_DIR}/created_templates/${PROJECT}-limits.yaml
                if [ "`oc get limits -n ${PROJECT} |wc -l`" -eq "2" ]
                then
                        LOG "${green} Sunccessfully created limits for project ${PROJECT}"
                else
                        ERROR "${red} Failed to create limits for project ${PROJECT}"
                fi
        else
                        ERROR "${red} limits for project ${PROJECT}, already exist in project"
        fi

}


### This Function checkes the current user, if current user is not System Admin then
### Swithc the Id to System:admin
function Swich_to_Admin {
	current_user=`/usr/bin/oc whoami`

	if [ "${current_user}" != "system:admin" ]
	then
		LOG "${yellow} Current user is not a systemadmin, switching to System Admin"
		/usr/bin/oc login -u system:admin > /dev/null 2> /dev/null

		if [ $? -eq 0 ]
		then
			if [ "`/usr/bin/oc whoami`" == "system:admin" ]
			then
				LOG "${green} Current User is System Admin"
			else
				ERROR "${red} Failed to Switch to System Admin"
			fi
		else
			ERROR "${red} Failed to Switch to System Admin"
		fi
	else
		LOG "${green} Current User is System Admin"
	fi
}

function secret {
  PROJECT="$1"
  LOG "${green} creating a secret to pull from nexus"
  oc secrets new nexus-secret-pull .dockerconfigjson=/<path to config file>/nexusconfig.json -n $PROJECT
  if [ ! $? -eq 0 ]
   then 
   LOG " ${red} secret creation failed "
 else 
   LOG " ${green} sucessfully created a secret "
 fi
LOG "${green} Adding secret to builder service account nexus"
  oc secrets add serviceaccount/builder secrets/nexus-pull --for=pull -n $PROJECT
  if [ ! $? -eq 0 ]
   then 
   LOG " ${red} Adding secret to builder service account nexus failed  "
  else 
   LOG " ${green} sucessfully Added the secret to builder service account  "  
 fi
}

function satokenjenkins {
  PROJECT="$1"
  LOG "${green} creating a project directory to save token"
  mkdir -p ${project_tokens_dir}/$PROJECT
  if [ ! $? -eq 0 ]
  then 
  LOG "${red} directory creation failed, exiting the script"
  else
  LOG "${green} directory creation successfuly created"
  fi
  LOG "${green} token saving directory is created "
  LOG "${green} creatin a non expiry token for jenkins deployment for project "
  oc create sa jenkins-svc-account -n $PROJECT
  if [ $? -eq 0 ]
  then
    LOG " ${green} serviceacoount creation is succesfull"
    LOG "${green} generating the non-expiry token for jemkins deployments"
    oc policy add-role-to-user edit system:serviceaccount:$PROJECT:jenkins-svc-account
    if [ $? -eq 0 ]
    then
      LOG " ${green} serviceacoount has asigned the rolebindings to deploy in project $PROJECT "
      LOG " Saving the token to a file and will be emailed to project admin through a email"
      sleep 4
      oc describe secret -n $PROJECT $(oc get sa jenkins-svc-account -o yaml | grep -A2 secrets: | grep token | awk '{print $3}') | grep token: | awk '{print $2}'  > ${project_tokens_dir}/$PROJECT/${PROJECT}-jenkins-token.txt 
      if [ $? -eq 0 ] 
      then 
      LOG " ${green} token is saved to file "
    else
      LOG " ${red} token saving failed"
    fi
  else
    LOG " ${red} adding the rolebinding to sa failed"
  fi 
else
  LOG " ${red} serviceacoount creation is failed"
fi
}

function emailuser {
  PROJECT="$1"
  EMAIL="$2"
  #copy content of the file and token to a file 
  cp ${projects_dir}/data.txt ${projects_dir}/${PROJECT}-details.txt || ERROR "${red} Project-details file creation Failed !!!"
  sed -i "s#PROJECT#${PROJECT}#g"  ${projects_dir}/${PROJECT}-details.txt || ERROR "${red} Failed to update file ${projects_dir}/${PROJECT}-details.txt"
  #cat ${project_tokens_dir}/$PROJECT/jenkins-token.txt >> ${projects_dir}/$PROJECT/project-info.txt
  echo "$(cat ${projects_dir}/${PROJECT}-details.txt)" | mailx -r "OCP-Project-Ceation@alerts.amexgbt.com" -s "New Project $PROJECT is created in EPaaS2.0 PROD" -c "$cc_list" -S smtp="psmtp.gbt.gbtad.com:25" ${EMAIL}
 # echo "Token for jenkins deployments " | mailx -r "Epaas-jenkins-token@alerts.amexgbt.com" -s "Non-Expiry jenkins token for $PROJECT in EPaaS2.0 DEV " -a "${project_tokens_dir}/$PROJECT/${PROJECT}-jenkins-token.txt" -c "$cc1_list" -S smtp="psmtp.gbt.gbtad.com:25" ${EMAIL}
 LOG " ${green} all the information is emailed to the user" 
}


while getopts u:n:d:D:s:e: o
do
    case "$o" in
        n) project="$OPTARG";;
        d) display_name="$OPTARG";;
	D) description="$OPTARG" ;;
        e) email="$OPTARG" ;;
        s) size="$OPTARG" ;;
	[?] | h | help )  usage ;
                			   exit 1;;
    esac
done

LOG " "
LOG "------------------------------------------------------------------------------------------------------------"
LOG "`date`"
LOG "------------------------------------------------------------------------------------------------------------"
LOG " "


### Validating Input values passed to the script & Set the default values for optionl arguments

if [ -z $project ]
then
        LOG "${red} No Project Name is provided, exiting the script"
        usage
        exit 400
elif [ -z $size ]
then
                LOG "${red} No size is  provided, exiting the script"
                usage
                exit 400
elif [ -z $email ]
then
                LOG "${red} NO email is provided, exiting the script"
                usage
                exit 400

else
	LOG "${green} Project name is ${project}"
        LOG "${green} email of teh user is ${email}"
        LOG "${green} quota size is ${size}"
	if [ -z "$display_name" ]
	then
		LOG "${yellow} Display name for the project is not specified, ${project} would be considered .. "
		display_name="${project}"
	else
		LOG "${green} Display Name of the project is -> ${display_name}"
	fi

	if [ -z "$description" ]
	then
		LOG "${yellow} Description for the project is not specified, ${project} would be considered .. "
		description="${project}"
	else
		LOG "${green} Description of project is -> ${description}"
	fi
fi

# Swith to System Admin
#Swich_to_Admin
#
if [ "`Check_For_Project ${project}`" -eq 0 ]
then
	LOG "${green} Project ${project} doesn't exist in the Cluster, creating one "
	/usr/bin/oc adm new-project ${project}   --display-name="${display_name}" --description="${description}"

	if [ $? -eq 0 ]
	then
		sleep 2
		if [ "`Check_For_Project ${project}`" -eq 1 ]
		then
			LOG "${green} Project ${project} sucessfull created "
		else
			ERROR "${red} Project ${project} creation failed"
		fi
	else
		ERROR "${red} Project ${project} creation failed"
	fi
else
	ERROR "${red} Project ${project} already exist in the system, exiting"
fi

#switch to project
switch_to_project $project
# Validate Script Inputs
LOG "${green} Validating the input parameters"
if [ -z $project ]
then
        LOG "${red} No project name is provided, exiting the script"
        usage
        exit 600
elif [ -z $email ]
then
                LOG "${red} No email is  provided, exiting the script"
                usage
                exit 400
else
        if [[ "$size" == "small" ]]
        then
                 create_quota $project small

        elif [[ "$size" == "medium" ]]
        then
                create_quota $project medium

        elif [[ "$size" == "large" ]]
        then
                create_quota $project large
        else

                LOG "${red} To execute the script -s size is mandatory. Please run the script by passing -s value"
                exit
        fi
fi
LOG "${green} successfuly implemented quotas and limits for project $project"

LOG "${green} adding image pull secret to project"
secret $project 

#LOG "${green} Generating the jenkins token"
#satokenjenkins $project 

emailuser $project $email
