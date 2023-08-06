import bloodyAD.patch.winacl_patch
from bloodyAD.formatters import (
    accesscontrol,
    common,
    cryptography,
    dns,
    ldaptypes,
    helpers,
)
from bloodyAD import formatters
import base64
from winacl.dtyp.security_descriptor import SECURITY_DESCRIPTOR

RESOLVING = False

def formatAccountControl(userAccountControl):
    userAccountControl = int(userAccountControl.decode())
    return [
        key
        for key, val in accesscontrol.ACCOUNT_FLAGS.items()
        if userAccountControl & val == val
    ]


def formatSD(sd_bytes):
    if not RESOLVING:
        return SECURITY_DESCRIPTOR.from_bytes(sd_bytes).to_sddl()

    sd = ldaptypes.SR_SECURITY_DESCRIPTOR(data=sd_bytes)
    pretty_sd = {}
    if sd["OffsetOwner"] != 0:
        pretty_sd["Owner"] = helpers.resolveSid(sd["OwnerSid"].formatCanonical())
    if sd["OffsetGroup"] != 0:
        pretty_sd["Group"] = helpers.resolveSid(sd["GroupSid"].formatCanonical())
    if sd["OffsetSacl"] != 0:
        pretty_sd["Sacl"] = base64.b64encode(sd["Sacl"].getData())
    if sd["OffsetDacl"] != 0:
        pretty_aces = []
        for ace in sd["Dacl"].aces:
            pretty_aces.append(accesscontrol.decodeAce(ace))
        pretty_sd["Dacl"] = pretty_aces
    return pretty_sd


def formatFunctionalLevel(behavior_version):
    behavior_version = behavior_version.decode()
    return (
        common.FUNCTIONAL_LEVEL[behavior_version]
        if behavior_version in common.FUNCTIONAL_LEVEL
        else behavior_version
    )


def formatSchemaVersion(objectVersion):
    objectVersion = objectVersion.decode()
    return (
        common.SCHEMA_VERSION[objectVersion]
        if objectVersion in common.SCHEMA_VERSION
        else objectVersion
    )


def formatGMSApass(managedPassword):
    gmsa_blob = cryptography.MSDS_MANAGEDPASSWORD_BLOB(managedPassword)
    ntlm_hash = "aad3b435b51404eeaad3b435b51404ee:" + gmsa_blob.toNtHash()
    return  f"NTLM {ntlm_hash} B64ENCODED {base64.b64encode(gmsa_blob['CurrentPassword'])}"


def formatDnsRecord(dns_record):
    return dns.Record(dns_record).toDict()


def formatKeyCredentialLink(key_dnbinary):
    return cryptography.KEYCREDENTIALLINK_BLOB(
        common.DNBinary(key_dnbinary).value
    ).toString()
