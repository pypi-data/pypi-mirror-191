import requests
import logging
import urllib
import json
import dateutil.parser

from datetime import datetime, timedelta
from RW import platform
from RW.Utils import utils
from RW.K8s import K8s

logger = logging.getLogger(__name__)


FAILING_PDBS = "failing_pdbs"


class CHES:
    """
    Keyword integration for users of CHES.
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    _k8s: K8s()

    def __init__(self):
        self._k8s = K8s()

    def results_by_namespace(self, results: list) -> dict:
        """Helper method that takes the results of a promql fan-out style query result and organizes it into
        a dict of namespaces with their associated list of failing PDBs.

        Args:
            results (list): the fan-out query result returned from the Prometheus endpoint.

        Returns:
            dict: a mapping of namespaces to their list of failing PDBs.
        """
        results_by_namespace = {}
        for result in results:
            ns = result["metric"]["namespace"]
            if ns not in results_by_namespace:
                results_by_namespace[ns] = {}
            if FAILING_PDBS not in results_by_namespace[ns]:
                results_by_namespace[ns][FAILING_PDBS] = []
            results_by_namespace[ns][FAILING_PDBS].append(result["metric"]["poddisruptionbudget"])
            results_by_namespace[ns]["contacts"] = None
        return results_by_namespace

    def add_emails_to_results(
        self,
        results,
        kubeconfig: platform.Secret,
        target_service: platform.Service,
        context: str,
        binary_name: str = "kubectl",
    ) -> dict:
        for ns in results.keys():
            try:
                ns_rsp = self._k8s.shell(
                    cmd=f"{binary_name} get ns {ns} --context={context} -o json",
                    target_service=target_service,
                    kubeconfig=kubeconfig,
                )
                if not utils.is_json(ns_rsp):
                    break
                ns_rsp = utils.from_json(ns_rsp)
                ns_contacts = utils.search_json(ns_rsp, "metadata.annotations.contacts")
                if not ns_contacts:
                    break
                results[ns]["contacts"] = ns_contacts
            except err:
                logger.warning(
                    f"The command: '{binary_name} get ns {ns} --context={context} -o json' caused an exception but we're continuing on:\n{err}"
                )
        return results

    def pdb_mass_email(self, email_template: str, email_data: any) -> dict:
        email_results = {"emails_sent": {}, "errors": []}
        for namespace in email_data.keys():
            contacts = utils.from_json(email_data[namespace]["contacts"])
            contacts_list = [f"Email: {contact['email']} Role: {contact['role']}" for contact in contacts]
            contacts_list = "\n".join(contacts_list)
            pdb_list = "\n".join(email_data[namespace][FAILING_PDBS])
            email_content = email_template.format(contacts_list=contacts_list, pdb_list=pdb_list, namespace=namespace)
            # do email
            email_results["emails_sent"][namespace] = email_content
        return email_results
