from discord import Member

def create_response(added_911_role_list: list[Member], added_scene_role_list: list[Member], removed_911_role_list: list[Member], removed_scene_role_list: list[Member]) -> str:
    response = ""
    if added_911_role_list or removed_911_role_list:
        response += "911 роль:\n"

        if added_911_role_list:
            response += "\tДодано роль для:\n"
            for member in added_911_role_list:
                response += f"\t\t{member.mention}\n"

        if removed_911_role_list:
            response += "\tЗабрано роль в:\n"
            for member in removed_911_role_list:
                response += f"\t\t{member.mention}\n"

    if added_scene_role_list or removed_scene_role_list:
        response += "\nScene роль:\n"

        if added_scene_role_list:
            response += "\tДодано роль для:\n"
            for member in added_scene_role_list:
                response += f"\t\t{member.mention}\n"

        if removed_scene_role_list:
            response += "\tЗабрано роль в:\n"
            for member in removed_scene_role_list:
                response += f"\t\t{member.mention}\n"

    if not response:
        return "Здається всіх було синхронізовано"
    return response