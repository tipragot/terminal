#!/usr/bin/env python3

from c_formatter_42.run import run_all
from datetime import datetime
from os import environ
import sys

def generate_header(filename: str, content: str, update_time: bool = True) -> str:
    content = content.strip()
    user_login = environ.get("LOGIN", "tcezard")
    user_mail = f"{user_login} <{user_login}@student.42nice.fr>"
    final_login = user_login + " " * (13 - len(user_login))
    today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    if content.startswith("/* "):
        if filename == "unknown":
            try: filename = content[248:293].strip()
            except: filename = "unknown"
        try:
            created_at = datetime.strptime(content[581:600], "%Y/%m/%d %H:%M:%S")
            created_at = created_at.strftime("%Y/%m/%d %H:%M:%S")
        except: created_at = today
        if not update_time:
            try:
                today = datetime.strptime(content[662:681], "%Y/%m/%d %H:%M:%S")
                today = today.strftime("%Y/%m/%d %H:%M:%S")
            except: pass
    else: created_at = today
    return f"""/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   {filename + " " * (45 - len(filename))      }      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: {user_mail + " " * (41 - len(user_mail))}  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: {created_at       } by {final_login}     #+#    #+#             */
/*   Updated: {today            } by {final_login}    ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */"""

def format_file(filename: str, content: str) -> str:
    content = content.strip()
    header = generate_header(filename, content)
    lines = content.split('\n')
    while lines and lines[0].startswith("/* "): lines.pop(0)
    content = header + '\n\n' + '\n'.join(lines).strip()
    return content + '\n'

if __name__ == "__main__":
    print(run_all(format_file("unknown", sys.stdin.read())).strip())