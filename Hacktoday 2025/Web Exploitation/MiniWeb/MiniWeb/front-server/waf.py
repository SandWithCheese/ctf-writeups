 
import re


def sanitize_input(input_string):

    input_string = re.sub(r"<script.*?>.*?</script>", "", input_string, flags=re.IGNORECASE)

    sql_patterns = [
        r"(--|#|;|\b(select|drop|insert|delete|update|union|or)\b)", 
        r"(\b(0x[a-fA-F0-9]{2,8})\b)",  
    ]
    
    for pattern in sql_patterns:
        input_string = re.sub(pattern, "BLOCKED", input_string)

    dangerous_chars = r"[+<>$%&\";]"
    for dc in dangerous_chars:
        input_string = input_string.replace(dc, "BLOCKED")

    dangerous_patterns = [
        r"(\b[a-zA-Z]'\s*'[a-zA-Z]\b)"
    ]
    
    for pattern in dangerous_patterns:
        input_string = re.sub(pattern, "BLOCKED", input_string)

    command_injections = ['subprocess', 'os', 'command', 'system', '\\','pty','eval','exec','sys', 'lower','upper', 'from', 'Popen','popen','read','run','check_output','execv','call','execvp','execle']
    for cmd in command_injections:
        input_string = input_string.replace(cmd, "BLOCKED")

    if "BLOCKED" in input_string :
        return "Blocked By WAF"
    else :
        return input_string