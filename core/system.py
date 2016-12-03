from subprocess import check_output

def power_off():
    result = str(check_output(["poweroff"]))

    return result

    
