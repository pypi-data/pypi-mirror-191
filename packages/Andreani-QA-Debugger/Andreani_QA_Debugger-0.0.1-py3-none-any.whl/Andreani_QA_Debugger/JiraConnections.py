import os
import pprint
import sys
import tkinter

import requests
from requests.auth import HTTPBasicAuth
import json

import Andreani_QA_Functions.Functions as Functions

basedir = os.path.abspath(os.path.join(__file__, "../"))
sys.path.append(basedir)


class JiraConnections:
    def __init__(self, instancia, user_description, error_code, id_project, report_file, data_cache, data_resource,
                 exception_handling, label_id, token_jira, case_severity, true_custom_fields):
        self.instancia = instancia
        self.user_description = user_description
        self.error_code = error_code
        self.id_project = id_project
        self.report_file_img = report_file
        self.data_cache = data_cache
        self.data_resource = data_resource
        self.exception_handling = exception_handling
        self.label_id = label_id
        self.token_jira = token_jira
        self.case_severity = case_severity
        self.true_custom_fields = true_custom_fields

    def main(self):
        return_report_defect = self.report_defect
        return return_report_defect

    @property
    def report_defect(self):
        # Ordenar las keys y values del data resource
        resource_ordenado = ''
        for key in self.data_resource:
            resource_ordenado += ("\n           * {}: {}".format(key, self.data_resource[key]))
        # Ordenar las keys y values del data cache
        cache_ordenado = ''
        for key in self.data_cache:
            cache_ordenado += ("\n           * {}: {}".format(key, self.data_cache[key]))

        # Se modifica el resultado esperado de ingles a castellano
        exception_handling = None
        if self.exception_handling == "NoSuchElementException":
            exception_handling = "No se encuentra el elemento"
        if self.exception_handling == "TimeoutException":
            exception_handling = "Se agota el tiempo de espera y no se puede cargar el elemento"

        # variables para generar la descripción del caso
        ####################################################****************************
        description_header = f"Informer ID: {self.label_id}"
        description_body = f"\n \n " \
                           f"Información Extra suministrada por el usuario: " \
                           f"\n -{self.user_description}" \
                           f"\n" \
                           f"\n -Resultado Esperado: {self.instancia.message_container}" \
                           f"\n" \
                           f"\n -Resultado Obtenido: {exception_handling}" \
                           f"\n" \
                           f"\n -Resource info: {resource_ordenado}" \
                           f"\n" \
                           f"\n -Cache info: {cache_ordenado}" \
                           f"\n" \
                           f"\n -Lista de pasos: \n {self.instancia.steps_case}" \
            ####################################################****************************
        summary_text = f"AUTOMATION || No se puede {self.instancia.message_container} en el elemento: {self.error_code}"
        # validacion de bug dentro de jira
        is_already_reported = self.buscar_defectos_proyecto(summary_text)
        if is_already_reported is None:
            return "Servicio de Jira No Disponible"
        if is_already_reported == True:
            return "defecto existente"
        else:
            print("Iniciando Reporte!")
            endpoint = f"https://andreani.atlassian.net//rest/api/2/issue/"
            headers = \
                {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            payload = {
                "fields":
                    {
                        "project":
                            {
                                "key": f"{self.id_project}"
                            },
                        "summary": f"{summary_text}",
                        "description": description_header + description_body,
                        "issuetype":
                            {
                                "name": "Bug"
                            },

                        # Severidad - 10100 Bloqueante, 10101 Alta, 10102 Media, 10103 Baja.
                        "customfield_10202":
                            {
                                "id": f"{self.case_severity}"
                            }
                    }
            }
            payload['fields'].update(self.true_custom_fields)
            payload = json.dumps(payload)
            response = requests.post(endpoint, headers=headers, data=payload, auth=(self.label_id, self.token_jira))
            # print(response.text)
            # Separo la key del nuevo defecto creado
            # print(response.json())
            new_id_issue = response.json()['key']
            # print(new_id_issue)
            # Luego de crear el defecto se le adjunta la imagen
            dominio_defecto = 'https://andreani.atlassian.net//rest/api/2/issue/' + new_id_issue + "/attachments"
            auth = HTTPBasicAuth(self.label_id, self.token_jira)
            # creo directorio y archivo de imagen
            try:
                with open(os.path.join(self.instancia.path_output, "jira_report.png"), "wb") as create_image:
                    create_image.write(self.report_file_img)
                    create_image.close()
            except FileNotFoundError:
                print("Error al intentar escribir la imagen que debe ser adjuntada")
            try:
                with open(os.path.join(self.instancia.path_output, "jira_report.png"), "rb") as f_image:
                    upload_file = f_image.read()
            except FileNotFoundError:
                print("Error al intentar encontrar la imagen que debe ser adjuntada")
            headers_defecto = {
                "X-Atlassian-Token": "no-check",
            }
            files = {
                'file': (
                    "evidencia.png", upload_file)
            }
            requests.post(dominio_defecto, headers=headers_defecto, files=files, auth=auth)
            os.remove(os.path.join(self.instancia.path_output, "jira_report.png"))
            f_image.close()
            return "defecto reportado correctamente"

    def buscar_defectos_proyecto(self, summary):
        """

        Args:
            summary: Se require el título del la tarjeta para revisar si la misma ya existe.

        Returns:
            False: Si la tarjeta no existe para el proyecto activo.
            True: Si la tarjeta existe para el proyecto activo.

        """
        endpoint = f"https://andreani.atlassian.net/rest/api/2/search"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"jql": f"project =  {self.id_project} AND issuetype in ('Bug (subtarea)','Bug')", "startAt": 0,
                   "maxResults": 100,
                   "fields": ["id", "key", "summary", "issuetype", "status", "reporter", "project"]}
        response = requests.post(endpoint, headers=headers, json=payload,
                                 auth=(self.label_id, self.token_jira))
        if response.status_code != 400:
            issues = response.json()["issues"]
            # key = None
            # se recorre la lista de issues actuales para el proyecto activo
            for issue in issues:
                # Si el nombre de la incidencia existe existe dentro de las tarjetas obtenidas
                if summary == issue["fields"]["summary"]:
                    # se revisa que el estado de la misma no sea finalizada o cancelada para darla como ya reportado
                    if not issue["fields"]["status"]["name"] in ("Finalizado", "Cancelado"):
                        return True
                    else:
                        # si el estado actual corresponde a alguno de estos
                        # entonces esta tarjeta no existe y el usuario puede crearla
                        return False
                else:
                    # si el título no existe, se retorna falso dando lugar a la creación de la misma
                    return False
        else:
            print(f"El servicio de Jira arrojó el status {response.status_code}")
            return None

    ####################################################################################################################
    #                                       IMPORTANTE                                                                 #
    # Para que la validación sea correcta el usuario debe cumplir las siguientes condiciones:                          #
    # * El proyecto debe estar registrado dentro de la DB de Jira_Reports.                                             #
    # * El proyecto debe estar activo dentro de la DB de Jira_Reports.                                                 #
    # * Debe existir vinculación entre proyecto y usuario buscado.                                                     #
    # * El usuario debe tenér un token válido de Jira, ingresado previamente al XML.                                   #
    ####################################################################################################################
    def obtain_activated_projects(self, active_project):
        """
                Return: Retorna una lista de diccionarios con los proyectos activos.

        """
        self.db_server_py = Functions.Functions.get_data_from_xml_encrypted(Functions, "CLAVES", "id", "Base de PresentacionPybot", "IP")
        self.db_name_py = Functions.Functions.get_data_from_xml_encrypted(Functions, "CLAVES", "id", "Base de PresentacionPybot", "BASE")
        self.db_user_py = Functions.Functions.get_data_from_xml_encrypted(Functions, "CLAVES", "id", "Base de PresentacionPybot", "USER")
        query = "SELECT [project_name] FROM [PresentacionPybot].[dbo].[dim_projects]  WHERE activated = 1"
        # primero obtengo los proyectos activos desde PresentacionPybot
        activated_projects = Functions.Functions.get_recordset_sqlserver(self, self.db_server_py, self.db_name_py,
                                                               self.db_user_py, None, query)
        # print(f"proyec: {activated_projects}")
        mail_list = []
        user_name_list = []
        user_token_list = []
        final_user_list = []
        projects_list = []
        list_validated_projects = []
        for elemento in activated_projects:
            list_validated_projects.append(elemento['project_name'])
        # si el proyecto activo no existe en la db, freno la ejecución y devuelvo False, None (diccionario)
        if active_project not in list_validated_projects:
            return False, None
        # en base a los proyectos activos, obtengo los usuarios asignados a los mismos
        query_mails = "SELECT DP.project_name, DU.user_email, DU.user_name FROM [PresentacionPybot].[dbo].[rel_projects_users] as PU " \
                      "INNER JOIN dim_users AS DU on PU.user_id = DU.user_id INNER JOIN dim_projects AS " \
                      f"DP ON DP.project_id = PU.project_id where DP.project_name = '{active_project}' AND " \
                      "PU.users_project_activate = 1"
        user_mails = Functions.Functions.get_recordset_sqlserver(self, self.db_server_py, self.db_name_py,
                                                       self.db_user_py, None, query_mails)
        for mails in user_mails:
            mail_list.append(mails)
            projects_list.append(active_project)
        for nombres in mail_list:
            if nombres['user_name'] is not None:
                user_name_list.append(nombres['user_name'])
        # una vez obtenidos todos los nombres de usuario
        # ahora necesito comprarlos con los existentes dentro del yml para poder obtener los token
        for users in user_name_list:
            user_token = Functions.Functions.get_data_from_xml_encrypted(self, "TOKEN", "id", users, "USER_TOKEN")
            if user_token is not None:
                user_token_list.append(user_token)
                final_user_list.append(users)
        # finalmente preparo un diccionario de usuario:token para su posterior trabajo
        dict_user_token = dict(zip(final_user_list, user_token_list))
        exist_project = JiraConnections.validate_user_in_project(self, os.getlogin(), projects_list)
        # se retorna un diccionario compuesto por usuarios actuales del proyecto
        return exist_project, dict_user_token

    # validacion si el usuario existe dentro del proyecto
    def validate_user_in_project(self, user, in_project):
        is_in_project = bool(False)
        for project_name in in_project:
            validate_user_query = "SELECT DP.project_name, DU.user_email, DU.user_name " \
                                  "FROM [PresentacionPybot].[dbo].[rel_projects_users] as PU " \
                                  "INNER JOIN dim_users AS DU on PU.user_id = DU.user_id INNER JOIN dim_projects AS " \
                                  f"DP ON DP.project_id = PU.project_id where DP.project_name = '{project_name}' AND " \
                                  f"PU.users_project_activate = 1 and DU.user_name = '{user}'"
            validate_user_query = Functions.Functions.get_recordset_sqlserver(self, self.db_server_py, self.db_name_py,
                                                                    self.db_user_py, None, validate_user_query)
            if len(validate_user_query) != 0:
                is_in_project = True

        return is_in_project

# if __name__ == '__main__':
# JiraConnections(sys.argv[1], sys.argv[2], sys.argv[3]).main()
# JiraConnections.obtain_activated_projects(Functions)
