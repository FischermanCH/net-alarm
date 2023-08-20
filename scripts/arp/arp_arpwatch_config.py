def save_config_to_file(form_data, config_file_path):
    with open(config_file_path, 'w') as f:
        f.write("[Debug]\n")
        f.write(f"Mode = {form_data['debug']}\n\n")

        f.write("[File]\n")
        f.write(f"DataFile = {form_data['file']}\n\n")

        f.write("[Interface]\n")
        f.write(f"Name = {form_data['interface']}\n\n")

        f.write("[Network]\n")
        f.write(f"AdditionalLocalNetworks = {form_data['network']}\n\n")

        f.write("[Bogon]\n")
        f.write(f"DisableReporting = {form_data['disableBogon']}\n\n")

        f.write("[Packet]\n")
        f.write(f"ReadFromFile = {form_data['readFile']}\n\n")

        f.write("[Privileges]\n")
        f.write(f"DropRootAndChangeToUser = {form_data['dropPrivileges']}\n\n")

        f.write("[Email]\n")
        f.write(f"Recipient = {form_data['emailRecipient']}\n")
        f.write(f"Sender = {form_data['emailSender']}\n")
