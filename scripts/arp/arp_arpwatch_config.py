def save_config_to_file(form_data, config_file_path):
    with open(config_file_path, 'w') as f:
        f.write("[Debug]\n")
        f.write(f"Mode = {form_data['Debug']['Mode']}\n\n")

        f.write("[File]\n")
        f.write(f"DataFile = {form_data['File']['DataFile']}\n\n")

        f.write("[Interface]\n")
        f.write(f"Name = {form_data['Interface']['Name']}\n\n")

        f.write("[Network]\n")
        f.write(f"AdditionalLocalNetworks = {form_data['Network']['AdditionalLocalNetworks']}\n\n")

        f.write("[Bogon]\n")
        f.write(f"DisableReporting = {form_data['Bogon']['DisableReporting']}\n\n")

        f.write("[Packet]\n")
        f.write(f"ReadFromFile = {form_data['Packet']['ReadFromFile']}\n\n")

        f.write("[Privileges]\n")
        f.write(f"DropRootAndChangeToUser = {form_data['Privileges']['DropRootAndChangeToUser']}\n\n")

        f.write("[Email]\n")
        f.write(f"Recipient = {form_data['Email']['Recipient']}\n")
        f.write(f"Sender = {form_data['Email']['Sender']}\n")
