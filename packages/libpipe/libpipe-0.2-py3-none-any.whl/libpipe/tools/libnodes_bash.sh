# No argument
init_run_all() {
    cmd_list_file=$(mktemp "${TMPDIR:-/tmp/}$(basename $0).XXXXXXXXXXXX")
}

# add_cmd CMD 
add_cmd() {
    echo ${@} >> ${cmd_list_file}
}

# run_all LOG_FILE
run_all() {
    if [ ! -z "${max_concurrent}" ]
    then
        max_concurrent="-m ${max_concurrent}"
    fi
    if [ ! -z "${env_source_file}" ]
    then
        env_source_file="-e ${env_source_file}"
    fi
    if [ ! -z "${nodes}" ]
    then
        nodes="-n ${nodes}"
    fi

    if [ -z ${1} ]
    then
        nodetool run_all ${nodes} ${max_concurrent} ${env_source_file} ${cmd_list_file}
    else
        nodetool run_all --log_file ${1} ${nodes} ${max_concurrent} ${env_source_file} ${cmd_list_file}
    fi

    rm ${cmd_list_file}
}
