#! /bin/bash
####################################################################################
# Script to automate persistent volumes creation for applog collection
# Using this script we can creat a pv and pvc with specific name to collect applogs
#####################################################################################

red="[ERROR] :"
green="[INFO] :"
yellow="[WARNING] :"
GLOBAL_LOG_DIR="/var/log/Ose_Custom/Log"
LOG_DIR=${GLOBAL_LOG_DIR}/`basename $0 | cut -d "." -f1`
LOG_FILE="${LOG_DIR}/log_file.log"
DEFAULT_PV_SIZE="1"
GLOBAL_NAS_PATH="/NFS"
GLOBAL_NAS_PATH_PV="${GLOBAL_NAS_PATH}/logs"
TEMPLATE_FOR_LOG="${GLOBAL_NAS_PATH_PV}/log-template"
PV_PVC_CONF_DIR="${GLOBAL_NAS_PATH}/conf"


function usage {
        echo "Usage : `basename $0`  -n <project_name> [-s size ]
                                option n is mandatory, which expects projectname to be passed to the script.
                                PV would be created with applogs_<project_name>
                                PVC would be created with applogs in the project <project_name>
                                -s is optional , if no size is specified then default size is 1Gi"
        exit 700
}

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

while getopts n:s: o
do
    case "$o" in
        n) project="$OPTARG";;
        s) size="$OPTARG";;
        [?] | h | help )  usage ;
                                           exit 1;;
    esac
done


function Check_Input_perameters {
if [ -z $project ]
then
        LOG "${red} No Project Name is provided, exiting the script"
        usage
        exit 400
else
        LOG "${green} Project name is $project "
fi

if [ -z $size ]
then
        LOG "${green} PV Size is not defined, creating with default size ${DEFAULT_PV_SIZE}Gi .. "
        size=${DEFAULT_PV_SIZE}
fi
        LOG "${green} PV Size is $size "
}

function Check_For_Pre_Requs {

if [ ! -d ${GLOBAL_NAS_PATH} ]
then
        LOG "${red} Directory ${GLOBAL_NAS_PATH} doesn't exist, exiting ... "
        exit 300
else
        if [ ! -d ${TEMPLATE_FOR_LOG}/RT && -d ${TEMPLATE_FOR_LOG}/BT ]
        then
                LOG "${red} One of the directory  ${TEMPLATE_FOR_LOG}/RT or ${TEMPLATE_FOR_LOG}/BT are missing, existing .."
                exit 300
        else
                if [ ! -f ${PV_PVC_CONF_DIR}/pv-template.yaml && -f ${PV_PVC_CONF_DIR}/pvc-template.yaml ]
                then
                        LOG "${red} One of the templates for PV or PVC are missing, exiting .. "
                        exit 300
                fi
        fi
fi
}

function Complete_Prereq_For_PV_LOG {
        PROJECT=$1
        LOG "${green} Creating logs Directory ${GLOBAL_NAS_PATH_PV}/${PROJECT} "
        mkdir -m 777 ${GLOBAL_NAS_PATH_PV}/${PROJECT}
        if [ $? -ne 0 ]
        then
                LOG "${red} Directory ${GLOBAL_NAS_PATH_PV}/${PROJECT} creating failed, exiting "
                exit 500
        else
                LOG "${green} Directory sucessfully ${GLOBAL_NAS_PATH_PV}/${PROJECT} created"
        fi

        LOG "${green} copying files required for Project logs"
        cp -R ${TEMPLATE_FOR_LOG}/* ${GLOBAL_NAS_PATH_PV}/${PROJECT}/
        if [ $? -ne 0 ]
        then
                LOG "${red} copying files from ${TEMPLATE_FOR_LOG} to ${GLOBAL_NAS_PATH_PV}/${PROJECT} failed , exiting "
                exit 500
        else
                LOG "${green} sucessfully copied files from ${TEMPLATE_FOR_LOG} to ${GLOBAL_NAS_PATH_PV}/${PROJECT} "
        fi
}

function Check_For_Project {
        PROJECT=$1
        Project_Count=`oc get project | grep -w ${PROJECT}|wc -l`
        if [ ${Project_Count} -eq 0 ]
        then
                LOG "${red} No projects found with the name ${PROJECT}, exiting"
                exit 700
        elif [ ${Project_Count} -gt 1 ]
        then
                LOG "${red} Found more than 1 project with match ${PROJECT}, exiting"
                exit 700
        else
                LOG "${green} Found project ${PROJECT}, procceding further"
        fi
}

function Check_PV {
        PV_NAME=$1
        pv_count=`oc get pv | grep ${PV_NAME} | wc -l`
        echo ${pv_count}
        return ${pv_count}
}

function Check_PVC {
        PVC_NAME=$1
        PROJECT=$2
        pvc_count=`oc get pvc -n ${PROJECT} | grep ${PVC_NAME}|wc -l`
        echo ${pvc_count}
        return ${pvc_count}
}

function Create_Pv_Pvc {
        PROJECT=$1
        cp ${PV_PVC_CONF_DIR}/pv-template.yaml  ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml || ERROR "${red} PV Config file creation Failed !!!"
        cp ${PV_PVC_CONF_DIR}/pvc-template.yaml ${PV_PVC_CONF_DIR}/${PROJECT}-PVC.yaml || ERROR "${red} PVC Config file creation Failed !!!"
        #oc create -f ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml
        sed -i "s#PV_NAME#applogs-${PROJECT}#g"  ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml || ERROR "${red} Failed to update of PV_NAME in ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml"
        sed -i "s#SIZE#${size}#g"  ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml || ERROR "${red} Failed to update of SIZE in ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml"
        sed -i "s#PATH_NAME#${GLOBAL_NAS_PATH_PV}/${PROJECT}#g"  ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml || ERROR "${red} Failed to update of PATH_NAME in ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml"
        LOG  "${green} Updated PV Configuration file"
        sed -i "s#SIZE#${size}#g"  ${PV_PVC_CONF_DIR}/${PROJECT}-PVC.yaml || ERROR "${red} Failed to update of SIZE in ${PV_PVC_CONF_DIR}/${PROJECT}-PVC.yaml"
        sed -i "s#PV_NAME#applogs-${PROJECT}#g"  ${PV_PVC_CONF_DIR}/${PROJECT}-PVC.yaml || ERROR "${red} Failed to update of PATH_NAME in ${PV_PVC_CONF_DIR}/${PROJECT}-PVC.yaml"
        LOG  "${green} Updated PVC Configuration file"

        if [ "`Check_PV applogs-${PROJECT}`" -eq "0" ]
        then
                oc create -f ${PV_PVC_CONF_DIR}/${PROJECT}-PV.yaml
                if [ "`Check_PV applogs-${PROJECT}`" -eq "1" ]
                then
                        LOG "${green} Sunccessfully created PV applogs-${PROJECT}"
                else
                        ERROR "${red} Failed to create PV applogs-${PROJECT} "
                fi
        else
                        ERROR "${red} PV with name applogs-${PROJECT}, already exist. Not creating one, exiting .."
        fi

        if [ "`Check_PVC applogs ${PROJECT}`" -eq "0" ]
        then
                oc create -f ${PV_PVC_CONF_DIR}/${PROJECT}-PVC.yaml -n ${PROJECT}
                if [ "`Check_PVC applogs ${PROJECT}`" -eq "1" ]
                then
                        LOG "${green} Sunccessfully created PVC applogs"
                else
                        ERROR "${red} Failed to create PVC applogs"
                fi
        else
                        ERROR "${red} PVC with name applogs, already exist. Not creating one, exiting .."
        fi
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

# Validate Script Inputs
Check_Input_perameters

LOG " "
LOG "------------------------------------------------------------------------------------------------------------"
LOG "`date`"
LOG "------------------------------------------------------------------------------------------------------------"
LOG " "

# Check for existanse of project
Check_For_Project $project
echo test-0
#Validate PV
#Check_For_Pre_Requs
echo test-1
# Complete Pre-Requists for PV
Complete_Prereq_For_PV_LOG $project
echo test-2
# Create PV & PVC
Create_Pv_Pvc $project
