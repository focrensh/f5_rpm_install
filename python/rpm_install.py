import requests,os,time
requests.packages.urllib3.disable_warnings()

def rest_upload(rpm_name):
    upload_url = "https://%s/mgmt/shared/file-transfer/uploads/%s" % (bigip, rpm_name)
    fp = "../rpms/%s" % (rpm_name)
    chunk_size = 512 * 1024
    headers = {'Content-Type': 'application/octet-stream','X-F5-Auth-Token': tkn}
    fileobj = open(fp, 'rb')
    filename = os.path.basename(fp)
    size = os.path.getsize(fp)

    start = 0

    while True:
        file_slice = fileobj.read(chunk_size)
        if not file_slice:
            break

        current_bytes = len(file_slice)
        if current_bytes < chunk_size:
            end = size
        else:
            end = start + current_bytes

        content_range = "%s-%s/%s" % (start, end - 1, size)
        headers['Content-Range'] = content_range
        requests.post(upload_url, data=file_slice, headers=headers, verify=False)
        start += current_bytes


def rpm_install(rpm_name):
    install_url = "https://%s/mgmt/shared/iapp/package-management-tasks" % (bigip)
    headers = {'Content-Type': 'application/json','X-F5-Auth-Token': tkn}
    install_body = {"operation":"INSTALL", "packageFilePath":"/var/config/rest/downloads/" + rpm_name}
    r = requests.post(install_url, headers=headers, json=install_body, verify=False)
    install_id = r.json()['id']
    sts = "running"
    while True:
        time.sleep(3)
        check_url = "https://%s/mgmt/shared/iapp/package-management-tasks/%s" % (bigip, install_id)
        r = requests.get(check_url, headers=headers, verify=False) 
        sts = r.json()['status']
        if sts == "FAILED":
            stsmessage = r.json()['errorMessage']
            out = "%s: %s" % (sts,stsmessage)
            break
        if sts == "FINISHED":
            out = sts
            break

    return out
    
#VARS
rpm_name = "f5-appsvcs-3.8.0-3.noarch.rpm"
bigips = ["10.192.75.89:8443","testfail.local"]
un = "admin"
pw = "admin"

for bigip in bigips:
    print "%s STARTING" % (bigip)
    try:   
        #AUTH
        authurl = "https://%s/mgmt/shared/authn/login" % (bigip)
        headers = {'Content-Type': 'application/json'}
        body = { "username":un, "password":pw, "loginProviderName":"tmos"}
        r = requests.post(authurl, headers=headers, json=body, verify=False)
        tkn = r.json()['token']['token']

        #UPLOAD RPM
        rest_upload(rpm_name)

        #INSTALL RPM
        install_state = rpm_install(rpm_name)
        print "%s install status: %s" % (bigip,install_state)
    except Exception as e:
        print "%s FAILED | %s" % (bigip, e)