import re
p = "/etc/nginx/sites-enabled/agent"
s = open(p).read()
loc = ("\n    location /asistente {\n"
       "        proxy_pass http://127.0.0.1:8790;\n"
       "        proxy_http_version 1.1;\n"
       "        proxy_set_header Host $host;\n"
       "        proxy_set_header X-Real-IP $remote_addr;\n"
       "        proxy_read_timeout 120;\n"
       "        add_header Access-Control-Allow-Origin * always;\n"
       "    }\n")
anchor = "ssl_ciphers HIGH:!aNULL:!MD5;"
i = s.find(anchor)
if i == -1:
    print("ANCHOR NOT FOUND"); raise SystemExit(1)
if "/asistente" in s:
    print("YA PARCHEADO"); raise SystemExit(0)
s = s[:i+len(anchor)] + "\n" + loc + s[i+len(anchor):]
open(p, "w").write(s)
print("PATCHED")
