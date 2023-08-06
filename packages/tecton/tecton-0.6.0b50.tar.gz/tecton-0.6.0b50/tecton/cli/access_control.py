import sys
from enum import Enum

import click

from tecton._internals import metadata_service
from tecton._internals.display import Displayable
from tecton.cli import printer
from tecton.cli.command import TectonGroup
from tecton_proto.auth.authorization_service_pb2 import Assignment
from tecton_proto.auth.authorization_service_pb2 import AssignRolesRequest
from tecton_proto.auth.authorization_service_pb2 import GetAssignedRolesRequest
from tecton_proto.auth.authorization_service_pb2 import UnassignRolesRequest
from tecton_proto.auth.principal_pb2 import PrincipalType
from tecton_proto.auth.resource_pb2 import ResourceType
from tecton_proto.metadataservice.metadata_service_pb2 import GetUserRequest


class Roles(Enum):
    VIEWER = "view_role"
    CONSUMER = "read_data_role"
    EDITOR = "apply_role"
    OWNER = "manage_role"
    ADMIN = "admin_role"

    @classmethod
    def from_generic_name(cls, name):
        return ROLE_NAMES[name]

    def get_generic_name(self):
        return TECTON_ROLE_TO_USER_ROLES[self]


ROLE_NAMES = {
    "viewer": Roles.VIEWER,
    "consumer": Roles.CONSUMER,
    "editor": Roles.EDITOR,
    "owner": Roles.OWNER,
    "admin": Roles.ADMIN,
}
TECTON_ROLE_TO_USER_ROLES = {v: k for k, v in ROLE_NAMES.items()}

RESOURCE_TYPES = {
    "WORKSPACE": ResourceType.RESOURCE_TYPE_WORKSPACE,
    "ORGANIZATION": ResourceType.RESOURCE_TYPE_ORGANIZATION,
}


@click.command("access-control", cls=TectonGroup)
def access_control():
    """Manage Access Controls"""


@access_control.command("assign-role")
@click.option("-w", "--workspace", required=False)
@click.option("-r", "--role", required=True, type=click.Choice([role.get_generic_name() for role in Roles]))
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
def assign_role_command(workspace, role, user, service_account):
    """Assign a role to a principal."""
    update_role(workspace, role, user, service_account)


@access_control.command()
@click.option("-w", "--workspace", required=False)
@click.option("-r", "--role", required=True, type=click.Choice([role.get_generic_name() for role in Roles]))
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
def unassign_role(workspace, role, user, service_account):
    """Unassign a role from a principal."""
    update_role(workspace, role, user, service_account, unassign=True)


def update_role(workspace, role, user, service_account, unassign=False):
    assignment = Assignment()
    principal_type, principal_id = get_principal_details(user, service_account)

    if role == "admin":
        if workspace:
            raise click.ClickException("'Admin' is a cluster-wide role. Please remove the --workspace argument.")
        resource_type = ResourceType.RESOURCE_TYPE_ORGANIZATION
    elif workspace:
        resource_type = ResourceType.RESOURCE_TYPE_WORKSPACE
        assignment.resource_id = workspace
    else:
        raise click.ClickException("Please mention a workspace name using --workspace")

    assignment.resource_type = resource_type
    assignment.principal_type = principal_type
    assignment.principal_id = principal_id
    assignment.role = Roles.from_generic_name(role).value

    try:
        if unassign:
            request = UnassignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().UnassignRoles(request)
        else:
            request = AssignRolesRequest()
            request.assignments.append(assignment)
            metadata_service.instance().AssignRoles(request)
        printer.safe_print("Successfully updated role.")
    except Exception as e:
        printer.safe_print(f"Failed to update role: {e}", file=sys.stderr)
        sys.exit(1)


def get_roles(principal_type, principal_id, resource_type):
    request = GetAssignedRolesRequest()
    request.principal_type = principal_type
    request.principal_id = principal_id
    request.resource_type = resource_type
    response = metadata_service.instance().GetAssignedRoles(request)
    return response


def display_table(headings, ws_roles):
    table = Displayable.from_table(headings=headings, rows=ws_roles, max_width=0)
    # Align columns in the middle horizontally
    table._text_table.set_cols_align(["c" for _ in range(len(headings))])
    printer.safe_print(table)


@access_control.command("get-roles")
@click.option("-u", "--user", default=None, help="User Email")
@click.option("-s", "--service-account", default=None, help="Service Account ID")
@click.option(
    "-r",
    "--resource_type",
    default=None,
    type=click.Choice(RESOURCE_TYPES.keys()),
    help="Optional Resource Type to which the Principal has roles assigned.",
)
def get_assigned_roles(user, service_account, resource_type):
    """Get the roles assigned to a principal."""
    if resource_type is not None:
        resource_type = RESOURCE_TYPES[resource_type]
    principal_type, principal_id = get_principal_details(user, service_account)

    try:
        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_WORKSPACE:
            ws_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_WORKSPACE)
            ws_roles = []
            for assignment in ws_response.assignments:
                if len(assignment.roles) > 0:
                    roles = ",".join([Roles(role).get_generic_name() for role in assignment.roles])
                    ws_roles.append([assignment.resource_id, roles])
            headings = ["Workspace", "Role"]
            display_table(headings, ws_roles)

        print()

        if resource_type is None or resource_type == ResourceType.RESOURCE_TYPE_ORGANIZATION:
            org_response = get_roles(principal_type, principal_id, ResourceType.RESOURCE_TYPE_ORGANIZATION)
            org_roles = []
            for assignment in org_response.assignments:
                if len(assignment.roles) > 0:
                    org_roles.append([Roles(assignment.roles[0]).get_generic_name()])
            headings = ["Organization Roles"]
            display_table(headings, org_roles)
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles: {e}", file=sys.stderr)
        sys.exit(1)


def get_user_id(email):
    try:
        request = GetUserRequest()
        request.email = email
        response = metadata_service.instance().GetUser(request)
        return response.user.okta_id
    except Exception as e:
        printer.safe_print(f"Failed to Get Roles: {e}", file=sys.stderr)
        sys.exit(1)


def get_principal_details(user, service_account):
    if user and service_account:
        raise click.ClickException("Please mention a single Principal Type using one of --user or --service-account")
    if user:
        return PrincipalType.PRINCIPAL_TYPE_USER, get_user_id(user)
    elif service_account:
        return PrincipalType.PRINCIPAL_TYPE_SERVICE_ACCOUNT, service_account
    else:
        raise click.ClickException("Please mention a Principal Type using --user or --service-account")
