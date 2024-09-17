import subprocess

first_new_line = True

server_files = [
    "/home/root/screenly/temp-update/templates/index.html=/usr/src/app/templates/index.html",
    "/home/root/screenly/temp-update/templates/base.html=/usr/src/app/templates/base.html",
    "/home/root/screenly/temp-update/templates/head.html=/usr/src/app/templates/head.html",
    "/home/root/screenly/temp-update/templates/header.html=/usr/src/app/templates/header.html",
    "/home/root/screenly/temp-update/templates/footer.html=/usr/src/app/templates/footer.html",
    "/home/root/screenly/temp-update/static/css/anthias.css=/usr/src/app/static/css/anthias.css",
    "/home/root/screenly/temp-update/static/img/logo-full-kinderland.png=/usr/src/app/static/img/logo-full-kinderland.png"
]

# viewer_files = [
#     "/home/root/screenly/viewer.py=/usr/src/app/viewer.py"
# ]


# Zeilen in der Config die für die fehlerfreie Nutzung benötigt werden

# "hdmi_group=1",
# "hdmi_mode=32",
# "hdmi_ignore_cec=1"
new_lines = [
    "hdmi_force_hotplug=1",
]



print("Update.py erfolgrecih gestartet....")
print("")
print("Boot config wird bearbeitet...")
print("")
print("")

# boot config einlesen um fehlende einstellungen zu finden
with open('/boot/config.txt', 'r') as config:
    lines = config.read().splitlines()


# boot config mit "write" öffnen um fehlende einstellungen hinzuzufügen / ändern
with open('/boot/config.txt', 'w') as config:
    for line in lines:
        try:
            var, val = line.split('=')

            # wenn fkms an dann zu kms ändern
            if "fkms" in val:
                val = val.replace("fkms", "kms")
                print(var, val, "fkms wurde erfolgreich durch kms ausgetauscht.")


            # wenn hdmi mode da aber falsch dann auf 32 setzen
            # if "hdmi_mode" in var and "32" not in val:
            #     val = "32"
            #     print(f"ersetze {val} mit 32")


            #ver#nderte werte in die Zeile (line) schreiben
            config.write(f"{var}={val}\n")
        except:
            # wenn fehler auftausch line so lassen
            config.write(line + "\n")

    # durch alle new_lines gehen
    for new_line in new_lines:
        #wenn benötigte zeile nicht vorhanden
        if new_line not in lines:
            #wenn das erste mal geändert [all] erst hinzufügen
            if first_new_line:
                config.write("[all]" + "\n")
                first_new_line = False


            #neue zeile hinzufügen
            config.write(new_line + "\n")
            print(f"{new_line} fehlte und wurde erfolgreich hinzugefügt.")


print("Boot config erfolgreich bearbeitet, docker werden gescannt...")
print("")

output = subprocess.check_output(["docker", "ps", "-a"]).decode("utf-8")
lines = output.split("\n")

for line in lines:
    if "anthias-server" in line:
        columns = line.split()
        container_id = columns[0]
        print(f"Container ID of anthias-server: {container_id}")
        for file in server_files:
            src, goal = file.split('=')

            command = ["docker", "cp", f"{src}", f"{container_id}:{goal}"]
            try:
                subprocess.check_output(command)
                print("Datei erfolgreich in anthias-server kopiert")
            except subprocess.CalledProcessError as e:
                print(f"Datei konnte nicht in anthias-server kopiert werden {e}")

    # if "anthias-viewer" in line:
    #     columns = line.split()
    #     container_id = columns[0]
    #     print(f"Container ID of anthias-viewer: {container_id}")
    #     for file in viewer_files:
    #         src, goal = file.split('=')

    #         command = ["docker", "cp", f"{src}", f"{container_id}:{goal}"]
    #         try:
    #             subprocess.check_output(command)
    #             print("Datei erfolgreich in anthias-viewer kopiert")
    #         except subprocess.CalledProcessError as e:
    #             print(f"Datei konnte nicht in anthias-viewer kopiert werden {e}")


            
print("Update.py ist zuende!")




